"""
01_rdd_basico.py
Objetivo: entender RDDs, la diferencia entre transformaciones (lazy) y acciones,
y comparar el paradigma MapReduce clásico con su equivalente en Spark.

Correr local:   spark-submit --master local[*] 01_rdd_basico.py
Correr Dataproc: gcloud dataproc jobs submit pyspark 01_rdd_basico.py --cluster=<CLUSTER> --region=<REGION>
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("01_rdd_basico").getOrCreate()
sc = spark.sparkContext

# --- 1. Crear un RDD a partir de una lista (para practicar sin necesitar un archivo) ---
transacciones = [
    "sucursal_norte,retiro,1500",
    "sucursal_sur,deposito,3200",
    "sucursal_norte,deposito,800",
    "sucursal_centro,retiro,500",
    "sucursal_sur,retiro,1200",
]
rdd = sc.parallelize(transacciones)

# --- 2. Transformaciones (lazy: no se ejecutan hasta que hay una acción) ---
pares = rdd.map(lambda linea: linea.split(","))
solo_montos_por_sucursal = pares.map(lambda campos: (campos[0], float(campos[2])))

# --- 3. Acción: reduceByKey SÍ dispara la ejecución (aquí es donde ocurre el shuffle) ---
total_por_sucursal = solo_montos_por_sucursal.reduceByKey(lambda a, b: a + b)

print("=== Total de movimientos por sucursal (Spark, estilo MapReduce) ===")
for sucursal, total in total_por_sucursal.collect():
    print(f"{sucursal}: {total}")

# --- 4. Comparación conceptual con MapReduce clásico ---
# En Hadoop MapReduce, este mismo cálculo requeriría:
#   - Un Mapper que emite (sucursal, monto) por cada línea
#   - Un shuffle/sort que agrupa por llave (lo gestiona el framework)
#   - Un Reducer que suma los valores por llave
# La diferencia clave: Spark mantiene los datos en memoria entre pasos (aquí no hay
# escritura a disco entre "map" y "reduce"), por eso es más rápido en pipelines
# iterativos o con múltiples transformaciones encadenadas.

spark.stop()
