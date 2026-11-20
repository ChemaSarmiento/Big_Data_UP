# json_a_parquet.py · lee el JSON Lines como texto y lo guarda como Parquet (una columna `value`).
from pyspark.sql import SparkSession

BUCKET = "gs://TU_BUCKET"
spark = SparkSession.builder.appName("json_a_parquet").getOrCreate()

crudo = spark.read.text(BUCKET + "/war_tweets.txt")           # transformación: cada línea queda en la columna `value`; aún no lee nada
crudo.write.mode("overwrite").parquet(BUCKET + "/tweets_parquet/")   # acción: aquí empieza el trabajo

resultado = spark.read.parquet(BUCKET + "/tweets_parquet/")
print("FILAS", resultado.count())                             # acción: cuenta las filas escritas
