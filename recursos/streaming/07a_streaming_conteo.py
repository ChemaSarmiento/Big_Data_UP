"""
07a_streaming_conteo.py
Objetivo: primer contacto con Structured Streaming real -- consumir el stream de
Pub/Sub Lite, parsear el JSON, y calcular un conteo de transacciones por ventana de
tiempo con watermark. Sin scoring todavía -- eso es 07_streaming_scoring.py (Sesión
10), una vez que el grupo ya vio windowing/watermarks funcionando de forma aislada.

Requiere:
  Cluster con --properties="spark:spark.jars.packages=com.google.cloud:pubsublite-spark-sql-streaming:1.0.0"

Antes de correr, arrancar el productor en otra terminal/VM (ver producer_transacciones_stream.py):
  python producer_transacciones_stream.py --project <PROJECT_ID> --tasa 20

Correr este job:
  spark-submit --master yarn 07a_streaming_conteo.py \
      --project <PROJECT_ID> --subscription transacciones-stream-sub
"""
import argparse

from pyspark.sql import SparkSession, functions as F, types as T

parser = argparse.ArgumentParser()
parser.add_argument("--project", required=True)
parser.add_argument("--subscription", required=True, help="nombre de la suscripción de Pub/Sub Lite")
parser.add_argument("--location", default="us-central1-a", help="zona de Pub/Sub Lite")
args = parser.parse_args()

spark = SparkSession.builder.appName("07a_streaming_conteo").getOrCreate()

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

# --- 2. Parsear el JSON del cuerpo del mensaje ---
transacciones = (
    crudo.select(F.col("data").cast("string").alias("json"))
    .select(F.from_json("json", esquema_transaccion).alias("t"))
    .select("t.*")
)

# --- 3. Windowing + watermark: el ejercicio central de hoy ---
# Watermark de 2 minutos: tolera hasta 2 min de retraso en la llegada de un mensaje
# antes de cerrar definitivamente una ventana. Sin esto, Spark tendría que esperar
# indefinidamente a un mensaje que nunca llega, para "estar seguro" de que la ventana
# ya no va a recibir más datos.
conteo_por_ventana = (
    transacciones
    .withWatermark("timestamp", "2 minutes")
    .groupBy(F.window("timestamp", "1 minute"), "currency")
    .count()
)

# --- 4. Sink: consola, para ver las ventanas cerrarse en vivo durante la sesión ---
query = (
    conteo_por_ventana.writeStream
    .format("console")
    .outputMode("update")
    .trigger(processingTime="30 seconds")
    .start()
)

query.awaitTermination()
