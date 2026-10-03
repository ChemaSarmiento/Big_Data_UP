"""S10: un modelo completo ya ajustado, aplicado a eventos sin labels."""
import argparse
from pyspark.ml import PipelineModel
from pyspark.ml.functions import vector_to_array
from pyspark.sql import SparkSession, functions as F
from stream_common import events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--modelo", required=True)
    parser.add_argument("--salida", required=True)
    parser.add_argument("--seconds", type=int, default=180)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("seconds debe ser positivo")
    spark = SparkSession.builder.appName("07_streaming_scoring").getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    model = PipelineModel.load(args.modelo)
    scored = model.transform(events(spark, args.input)).select(
        "transaction_id", "timestamp", "amount", "currency",
        vector_to_array("probability")[1].alias("prob_sospechosa"),
        F.col("prediction").alias("es_sospechosa_pred"), F.lit(args.modelo).alias("modelo_uri"),
    )
    output = args.salida.rstrip("/")
    scores = scored.writeStream.format("parquet").option("path", f"{output}/datos").option("checkpointLocation", f"{output}/checkpoints/scores").outputMode("append").trigger(processingTime="10 seconds").start()
    alerts = scored.filter("es_sospechosa_pred = 1").groupBy(F.window("timestamp", "1 minute")).count()
    windows = alerts.writeStream.format("console").option("checkpointLocation", f"{output}/checkpoints/ventanas").outputMode("append").trigger(processingTime="10 seconds").start()
    try:
        spark.streams.awaitAnyTermination(args.seconds)
    finally:
        scores.stop(); windows.stop(); spark.stop()


if __name__ == "__main__":
    main()
