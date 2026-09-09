"""
07_streaming_scoring.py
Objetivo: consumir un stream de transacciones desde Pub/Sub Lite y aplicar el
MISMO PipelineModel entrenado en la Sesión 5/6 (recursos/spark/04_pipeline_ml.ipynb)
para generar un score de fraude en tiempo real -- el mismo pipeline de features,
ahora sobre datos que llegan continuamente en vez de un CSV ya completo.

Material de la Sesión 10 (Maestría). Retoma el esqueleto de lectura/windowing de
07a_streaming_conteo.py (Sesión 9) y agrega el modelo -- correr aquel primero si
windowing/watermarks todavía no quedaron claros.

Requiere:
  Cluster con --properties="spark:spark.jars.packages=com.google.cloud:pubsublite-spark-sql-streaming:1.0.0"
  (además de las flags de recursos/managed-spark-cluster/README.md)

Antes de correr, arrancar el productor en otra terminal/VM (ver producer_transacciones_stream.py):
  python producer_transacciones_stream.py --project <PROJECT_ID> --tasa 20

Correr este job:
  spark-submit --master yarn 07_streaming_scoring.py \
      --project <PROJECT_ID> --subscription transacciones-stream-sub \
      --modelo gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
      --salida gs://<TU-BUCKET>/streaming/scores
"""
import argparse

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, functions as F, types as T

parser = argparse.ArgumentParser()
parser.add_argument("--project", required=True)
parser.add_argument("--subscription", required=True, help="nombre de la suscripción de Pub/Sub Lite")
parser.add_argument("--location", default="us-central1-a", help="zona de Pub/Sub Lite")
parser.add_argument("--modelo", required=True, help="PipelineModel guardado en la Sesión 5/6")
parser.add_argument("--salida", required=True, help="gs://<TU-BUCKET>/streaming/scores")
args = parser.parse_args()

spark = SparkSession.builder.appName("07_streaming_scoring").getOrCreate()

SUBSCRIPTION_PATH = f"projects/{args.project}/locations/{args.location}/subscriptions/{args.subscription}"

# --- 1. Leer el stream crudo de Pub/Sub Lite (llega como bytes en la columna "data") ---
crudo = (
    spark.readStream.format("pubsublite")
    .option("pubsublite.subscription", SUBSCRIPTION_PATH)
    .load()
)

esquema_transaccion = T.StructType([
    T.StructField("transaction_id", T.StringType()),
    T.StructField("timestamp", T.TimestampType()),
    T.StructField("amount", T.DoubleType()),
    T.StructField("currency", T.StringType()),
])

# --- 2. Parsear el JSON del cuerpo del mensaje y derivar la misma feature que en la Sesión 4 ---
transacciones = (
    crudo.select(F.col("data").cast("string").alias("json"))
    .select(F.from_json("json", esquema_transaccion).alias("t"))
    .select("t.*")
    .withColumn("hora_del_dia", F.hour("timestamp"))
)

# --- 3. Aplicar el pipeline ya entrenado (sin reentrenar nada aquí) ---
# PipelineModel.transform() es row-wise para todas las etapas de este pipeline
# (Imputer/StringIndexer/OneHotEncoder/VectorAssembler/StandardScaler/LogisticRegression
# ya están *fit*, ninguna mantiene estado nuevo) -- por eso puede aplicarse
# directo sobre un DataFrame en streaming, igual que sobre uno estático.
modelo = PipelineModel.load(args.modelo)
scoreadas = modelo.transform(transacciones).select(
    "transaction_id", "timestamp", "amount", "currency",
    F.col("probability").alias("prob_sospechosa"),
    F.col("prediction").alias("es_sospechosa_pred"),
)

# --- 4a. Sink 1: cada transacción scoreada, a Parquet (auditoría / reentrenamiento futuro) ---
query_scores = (
    scoreadas.writeStream
    .format("parquet")
    .option("path", args.salida)
    .option("checkpointLocation", f"{args.salida}/_checkpoint")
    .outputMode("append")
    .start()
)

# --- 4b. Sink 2: conteo de transacciones sospechosas por ventana de 1 minuto ---
# Watermark de 2 minutos: tolera hasta 2 min de retraso en la llegada de un mensaje
# antes de cerrar definitivamente una ventana. Esto es exactly-once en el CONTEO
# (cada ventana se calcula una sola vez); la garantía de no procesar el mismo
# mensaje dos veces la da Pub/Sub Lite del lado del broker + el checkpoint de arriba.
alertas_por_ventana = (
    scoreadas
    .withWatermark("timestamp", "2 minutes")
    .filter(F.col("es_sospechosa_pred") == 1.0)
    .groupBy(F.window("timestamp", "1 minute"))
    .count()
)
query_ventanas = (
    alertas_por_ventana.writeStream
    .format("console")
    .outputMode("update")
    .trigger(processingTime="30 seconds")
    .start()
)

spark.streams.awaitAnyTermination()
