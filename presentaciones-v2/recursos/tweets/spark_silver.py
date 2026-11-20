# Silver con PySpark: mismas columnas que 20_silver_tweets.sql, leyendo el Parquet de Bronze.
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("silver_tweets").getOrCreate()
raw = spark.read.parquet("gs://big-data-lunes-20260223/tweets_parquet/")
j = lambda ruta: F.get_json_object("value", ruta)

silver = raw.select(
    j("$.id").cast("long").alias("tweet_id"),
    j("$.date").cast("timestamp").alias("fecha_hora"),
    j("$.date").cast("timestamp").cast("date").alias("fecha"),
    j("$.lang").alias("idioma"),
    j("$.content").alias("texto"),
    j("$.url").alias("url"),
    j("$.user.username").alias("usuario"),
    j("$.user.verified").cast("boolean").alias("usuario_verificado"),
    j("$.user.followersCount").cast("long").alias("seguidores"),
    j("$.user.location").alias("ubicacion_usuario"),
    j("$.likeCount").cast("long").alias("likes"),
    j("$.retweetCount").cast("long").alias("retuits"),
    j("$.replyCount").cast("long").alias("respuestas"),
    j("$.quoteCount").cast("long").alias("citas"),
    j("$.inReplyToTweetId").isNotNull().alias("es_respuesta"),
    j("$.quotedTweet.id").isNotNull().alias("es_cita"),
    F.from_json(j("$.hashtags"), "array<string>").alias("hashtags"),
    j("$.sourceLabel").alias("aplicacion"),
)

silver.write.mode("overwrite").partitionBy("fecha").parquet("gs://big-data-lunes-20260223/tweets_silver_spark/")

resultado = spark.read.parquet("gs://big-data-lunes-20260223/tweets_silver_spark/")
print("FILAS_SILVER_SPARK", resultado.count())
print("IDS_DISTINTOS", resultado.select("tweet_id").distinct().count())
print("DIAS", sorted(r["fecha"].isoformat() for r in resultado.select("fecha").distinct().collect()))
