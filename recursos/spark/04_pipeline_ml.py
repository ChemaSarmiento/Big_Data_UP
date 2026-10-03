"""Entrenamiento reproducible, contrato bancario y artefactos versionados.
Ver README.md; enviar ml_common.py con spark-submit --py-files.
"""
import argparse
import json
from datetime import datetime, timezone
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.sql import SparkSession
from ml_common import read_transactions, temporal_split, feature_stages


def write_json(spark, path, payload):
    jvm = spark.sparkContext._jvm
    target = jvm.org.apache.hadoop.fs.Path(path)
    stream = target.getFileSystem(spark.sparkContext._jsc.hadoopConfiguration()).create(target, True)
    try:
        stream.write(bytearray(json.dumps(payload).encode("utf-8")))
    finally:
        stream.close()


def train(spark, input_uri, output, cutoff):
    df = read_transactions(spark, input_uri)
    train_df, test_df = temporal_split(df, cutoff)
    train_df, test_df = train_df.cache(), test_df.cache()
    try:
        lr = LogisticRegression(featuresCol="features", labelCol="is_suspicious", maxIter=30, regParam=0.1)
        model = Pipeline(stages=feature_stages() + [lr]).fit(train_df)
        prediction = model.transform(test_df)
        evaluator = BinaryClassificationEvaluator(labelCol="is_suspicious")
        metrics = {
            "auc": evaluator.setMetricName("areaUnderROC").evaluate(prediction),
            "pr_auc": evaluator.setMetricName("areaUnderPR").evaluate(prediction),
            "train_rows": train_df.count(), "test_rows": test_df.count(),
            "train_null_amounts": train_df.filter("amount IS NULL").count(),
            "test_null_amounts": test_df.filter("amount IS NULL").count(),
            "cutoff": cutoff, "input": input_uri, "model_uri": f"{output}/pipeline",
            "trained_at": datetime.now(timezone.utc).isoformat(), "spark_version": spark.version,
            "validation": "temporal_holdout", "schema_version": 1,
        }
        # Each run has its own output: retries reuse that run, not another run's metrics.
        model.write().overwrite().save(metrics["model_uri"])
        train_df.select("amount").filter("amount IS NOT NULL").sample(False, min(1.0, 100_000 / metrics["train_rows"]), seed=42).limit(100_000).write.mode("overwrite").parquet(f"{output}/referencia.parquet")
        write_json(spark, f"{output}/metrics.json", metrics)
        print(json.dumps(metrics, indent=2))
        return metrics
    finally:
        train_df.unpersist(); test_df.unpersist()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True, help="Directorio exclusivo del run: gs://bucket/modelos/runs/<run-id>")
    parser.add_argument("--cutoff", required=True, help="Fecha ISO, fijada antes de evaluar")
    args = parser.parse_args()
    spark = SparkSession.builder.appName("04_pipeline_ml").getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    try:
        train(spark, args.input, args.output.rstrip("/"), args.cutoff)
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
