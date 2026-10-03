"""S9: ventanas sobre eventos JSON depositados por pubsub_to_gcs.py."""
import argparse
from pyspark.sql import SparkSession, functions as F
from stream_common import events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--seconds", type=int, default=180)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("seconds debe ser positivo")
    spark = SparkSession.builder.appName("07a_streaming_conteo").getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    counts = events(spark, args.input).groupBy(F.window("timestamp", "1 minute"), "currency").count()
    query = counts.writeStream.format("console").outputMode("append").option("checkpointLocation", args.checkpoint).trigger(processingTime="10 seconds").start()
    try:
        query.awaitTermination(args.seconds)
    finally:
        query.stop(); spark.stop()


if __name__ == "__main__":
    main()
