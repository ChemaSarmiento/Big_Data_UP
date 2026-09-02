"""
02_dataframes.py
Objetivo: pasar de RDDs a la DataFrame API, leer datos reales (CSV/Parquet),
y aprender a leer el plan de ejecución con .explain() -- la herramienta de
diagnóstico más usada en el resto del curso.

Correr local:   spark-submit --master local[*] 02_dataframes.py --input ../datasets/transacciones.csv
"""

import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="Ruta al CSV o Parquet de entrada")
args = parser.parse_args()

spark = SparkSession.builder.appName("02_dataframes").getOrCreate()

# --- 1. Lectura ---
df = spark.read.csv(args.input, header=True, inferSchema=True)
df.printSchema()

# --- 2. Transformaciones con la DataFrame API ---
resumen = (
    df.filter(F.col("monto") > 0)
    .groupBy("sucursal", "tipo_transaccion")
    .agg(
        F.count("*").alias("num_transacciones"),
        F.sum("monto").alias("monto_total"),
        F.avg("monto").alias("monto_promedio"),
    )
    .orderBy(F.desc("monto_total"))
)

# --- 3. Leer el plan físico ANTES de ejecutar (clave para optimizar en sesiones futuras) ---
print("=== Plan físico (Catalyst) ===")
resumen.explain(mode="formatted")

# --- 4. Acción: aquí sí se ejecuta todo el plan de arriba ---
resumen.show(20, truncate=False)

# --- 5. Guardar en formato columnar particionado (preparación para la sesión de Data Lakes) ---
resumen.write.mode("overwrite").partitionBy("sucursal").parquet("/tmp/resumen_transacciones")

spark.stop()
