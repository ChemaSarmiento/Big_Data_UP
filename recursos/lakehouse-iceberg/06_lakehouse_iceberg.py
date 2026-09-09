"""
06_lakehouse_iceberg.py
Objetivo: mostrar por qué Parquet plano en carpetas (bronze/silver/gold de
recursos/etl-tipo-cambio/) no es lo mismo que un lakehouse transaccional real.
Migra la tabla de features de bank_transactions.csv (Sesión 5/6 de Maestría) a
Apache Iceberg y demuestra las tres cosas que Parquet plano en una carpeta NO
puede hacer sin reescribir todo: MERGE INTO (upsert), time travel (consultar un
snapshot anterior) y evolución de esquema sin romper lecturas viejas.

Requiere un cluster con el runtime de Iceberg. Crearlo con (además de las flags
de recursos/managed-spark-cluster/README.md):

  --properties="^#^spark:spark.jars.packages=org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1#\
spark:spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions#\
spark:spark.sql.catalog.local=org.apache.iceberg.spark.SparkCatalog#\
spark:spark.sql.catalog.local.type=hadoop#\
spark:spark.sql.catalog.local.warehouse=gs://$BUCKET_NAME/curso-bigdata/lakehouse"

(el prefijo "^#^" cambia el separador de propiedades de "," a "#", necesario
porque la lista de paquetes de Maven ya usa comas)

Correr en el cluster:
  spark-submit --master yarn 06_lakehouse_iceberg.py --bucket gs://<TU-BUCKET>
"""
import argparse

from pyspark.sql import SparkSession, functions as F

parser = argparse.ArgumentParser()
parser.add_argument("--bucket", required=True, help="gs://<TU-BUCKET> (sin slash final)")
args = parser.parse_args()

spark = SparkSession.builder.appName("06_lakehouse_iceberg").getOrCreate()

RAW = f"{args.bucket}/raw/bank_transactions/bank_transactions.csv"
TABLA_SILVER = "local.curso_bigdata.transacciones_silver"
TABLA_GOLD = "local.curso_bigdata.transacciones_gold"

# --- BRONZE: leer el CSV crudo, igual que en la Sesión 5 ---
bronze = spark.read.csv(RAW, header=True, inferSchema=True)
bronze = bronze.withColumn("is_suspicious", F.col("is_suspicious").cast("int"))
bronze = bronze.withColumn("hora_del_dia", F.hour("timestamp"))

# --- SILVER: crear la tabla Iceberg (primera carga) ---
spark.sql("CREATE NAMESPACE IF NOT EXISTS local.curso_bigdata")
(
    bronze.select("transaction_id", "timestamp", "amount", "currency", "hora_del_dia", "is_suspicious")
    .writeTo(TABLA_SILVER)
    .using("iceberg")
    .partitionedBy("currency")
    .createOrReplace()
)
print(f"=== Snapshot inicial creado. Filas: {spark.table(TABLA_SILVER).count()} ===")

# --- (1) MERGE INTO: por qué Parquet plano no alcanza ---
# Simula una corrección tardía: un pipeline de reglas de negocio detecta que un
# lote de transacciones llegó con `currency` mal etiquetado y las corrige después
# del hecho. Con Parquet en carpetas esto obliga a reescribir el archivo/partición
# completa; con Iceberg es un MERGE INTO transaccional sobre solo esas filas.
correcciones = (
    spark.table(TABLA_SILVER)
    .filter(F.col("currency") == "USD")
    .limit(1000)
    .withColumn("currency", F.lit("MXN"))
)
correcciones.createOrReplaceTempView("correcciones")
spark.sql(f"""
    MERGE INTO {TABLA_SILVER} t
    USING correcciones c
    ON t.transaction_id = c.transaction_id
    WHEN MATCHED THEN UPDATE SET t.currency = c.currency
""")
print("=== MERGE INTO aplicado sin reescribir la tabla completa ===")

# --- (2) Time travel: consultar un snapshot anterior al MERGE ---
snapshots = spark.sql(f"SELECT snapshot_id, committed_at, operation FROM {TABLA_SILVER}.snapshots ORDER BY committed_at")
snapshots.show(truncate=False)
primer_snapshot_id = snapshots.first()["snapshot_id"]
antes_del_merge = spark.read.format("iceberg").option("snapshot-id", primer_snapshot_id).load(TABLA_SILVER)
print(f"=== USD ANTES del MERGE (snapshot {primer_snapshot_id}): "
      f"{antes_del_merge.filter(F.col('currency') == 'USD').count()} ===")
print(f"=== USD DESPUÉS del MERGE (tabla actual): "
      f"{spark.table(TABLA_SILVER).filter(F.col('currency') == 'USD').count()} ===")

# --- (3) Evolución de esquema sin romper lecturas viejas ---
# Con Parquet plano, agregar una columna nueva obliga a versionar la carpeta entera
# o a que todo lector maneje esquemas distintos según qué archivo le tocó leer.
spark.sql(f"ALTER TABLE {TABLA_SILVER} ADD COLUMN es_horario_nocturno BOOLEAN")
spark.sql(f"UPDATE {TABLA_SILVER} SET es_horario_nocturno = (hora_del_dia < 6 OR hora_del_dia > 22)")
spark.table(TABLA_SILVER).show(5)

# --- GOLD: agregación de negocio sobre la tabla Iceberg ya versionada ---
gold = (
    spark.table(TABLA_SILVER)
    .groupBy("currency", "es_horario_nocturno")
    .agg(F.count("*").alias("num_transacciones"), F.avg("amount").alias("monto_promedio"))
)
gold.writeTo(TABLA_GOLD).using("iceberg").createOrReplace()
gold.show()

spark.stop()
