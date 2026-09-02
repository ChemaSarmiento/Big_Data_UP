"""
03_spark_sql.py
Objetivo: mostrar que Spark SQL y la DataFrame API son la misma cosa por debajo
(comparten el mismo optimizador Catalyst), usando window functions -- el puente
directo con lo que ya vieron en la sesión de SQL distribuido / BigQuery.

Correr local: spark-submit --master local[*] 03_spark_sql.py --input ../datasets/transacciones.csv
"""

import argparse
from pyspark.sql import SparkSession

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()

spark = SparkSession.builder.appName("03_spark_sql").getOrCreate()

df = spark.read.csv(args.input, header=True, inferSchema=True)
df.createOrReplaceTempView("transacciones")

# --- Misma pregunta que en 02_dataframes.py, pero en SQL ---
resumen_sql = spark.sql("""
    SELECT sucursal, tipo_transaccion,
           COUNT(*) AS num_transacciones,
           SUM(monto) AS monto_total,
           AVG(monto) AS monto_promedio
    FROM transacciones
    WHERE monto > 0
    GROUP BY sucursal, tipo_transaccion
    ORDER BY monto_total DESC
""")

# --- Window function: ranking de sucursales por monto dentro de cada tipo de transacción ---
ranking_sql = spark.sql("""
    SELECT sucursal, tipo_transaccion, monto,
           RANK() OVER (PARTITION BY tipo_transaccion ORDER BY monto DESC) AS ranking
    FROM transacciones
""")

print("=== Comparar este plan con el de 02_dataframes.py: deberían ser equivalentes ===")
resumen_sql.explain(mode="formatted")
resumen_sql.show(20, truncate=False)

print("=== Ranking por tipo de transacción (window function) ===")
ranking_sql.show(20, truncate=False)

spark.stop()
