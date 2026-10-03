"""Lectura, contrato de eventos y deduplicación acotada (Spark 3.5)."""
from pyspark.sql import functions as F, types as T

EVENT_SCHEMA = T.StructType([
    T.StructField("transaction_id", T.StringType()), T.StructField("timestamp", T.TimestampType()),
    T.StructField("amount", T.DoubleType()), T.StructField("currency", T.StringType()),
])


def events(spark, input_uri):
    raw = spark.readStream.schema(EVENT_SCHEMA).option("maxFilesPerTrigger", 10).json(input_uri)
    valid = raw.filter(
        F.col("transaction_id").isNotNull() & (F.length("transaction_id") > 0)
        & F.col("timestamp").isNotNull() & F.col("amount").isNotNull()
        & ~F.isnan("amount") & (F.abs(F.col("amount")) != float("inf")) & F.col("currency").isNotNull()
    )
    return valid.withWatermark("timestamp", "2 minutes").dropDuplicatesWithinWatermark(["transaction_id"])
