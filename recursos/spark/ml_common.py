"""Contrato único de features para batch, stream y API (Spark 3.5)."""
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer, StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler, SQLTransformer
from pyspark.sql import functions as F

REQUIRED = {"transaction_id", "timestamp", "amount", "currency", "is_suspicious"}


def read_transactions(spark, uri):
    raw = spark.read.option("header", True).csv(uri)
    missing = REQUIRED - set(raw.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    typed = raw.select(
        F.col("transaction_id").cast("string"), F.to_timestamp("timestamp").alias("timestamp"),
        F.col("amount").cast("double"), F.col("currency").cast("string"),
        F.col("is_suspicious").cast("double"),
    )
    malformed_amount = raw.filter(
        F.col("amount").isNotNull() & ~F.trim(F.col("amount")).isin("", "\\N")
        & F.col("amount").cast("double").isNull()
    ).limit(1).count()
    if malformed_amount:
        raise ValueError("Monto no numérico; separar rechazos antes de entrenar")
    # Null numeric values are allowed: the train-only Imputer learns their fill value.
    invalid = typed.filter(
        F.col("transaction_id").isNull() | (F.length("transaction_id") == 0)
        | F.col("timestamp").isNull() | F.col("currency").isNull()
        | F.isnan("amount") | (F.abs(F.col("amount")) == float("inf"))
        | F.col("is_suspicious").isNull() | ~F.col("is_suspicious").isin(0.0, 1.0)
    ).limit(1).count()
    if invalid:
        raise ValueError("Contrato inválido: revisa identificador, timestamp, monto, moneda y label binario")
    if typed.groupBy("transaction_id").count().filter("count > 1").limit(1).count():
        raise ValueError("transaction_id debe ser único; documenta y resuelve duplicados antes de entrenar")
    return typed


def temporal_split(df, cutoff):
    """La fecha se fija antes de medir; el holdout futuro jamás entra a fit()."""
    train = df.filter(F.col("timestamp") < F.to_timestamp(F.lit(cutoff)))
    test = df.filter(F.col("timestamp") >= F.to_timestamp(F.lit(cutoff)))
    for name, part in [("train", train), ("test", test)]:
        if part.select("is_suspicious").distinct().count() != 2:
            raise ValueError(f"{name} necesita ambas clases; revisa el corte temporal y la muestra")
    return train, test


def feature_stages():
    return [
        SQLTransformer(statement="SELECT *, CAST(hour(timestamp) AS DOUBLE) AS hora_del_dia FROM __THIS__"),
        Imputer(inputCols=["amount", "hora_del_dia"], outputCols=["amount_imp", "hora_imp"]),
        StringIndexer(inputCol="currency", outputCol="currency_idx", handleInvalid="keep"),
        OneHotEncoder(inputCols=["currency_idx"], outputCols=["currency_ohe"]),
        VectorAssembler(inputCols=["amount_imp", "hora_imp", "currency_ohe"], outputCol="features_raw"),
        StandardScaler(inputCol="features_raw", outputCol="features"),
    ]


def feature_pipeline():
    return Pipeline(stages=feature_stages())
