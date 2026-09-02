"""
04_pipeline_ml.py
Objetivo: cerrar la progresión de Spark con un Pipeline de MLlib completo
(imputacion -> encoding -> escalado -> modelo), el puente directo hacia la
sesion de "Ingenieria de features a escala" del track de Maestria.

Correr local: spark-submit --master local[*] 04_pipeline_ml.py --input ../datasets/transacciones.csv
"""

import argparse
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer, StringIndexer, OneHotEncoder, VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args = parser.parse_args()

spark = SparkSession.builder.appName("04_pipeline_ml").getOrCreate()

df = spark.read.csv(args.input, header=True, inferSchema=True)

# Se asume una columna binaria "es_fraude" como target (ver recursos/datasets/README.md
# para datasets reales que ya traen una columna de este tipo).

# --- 1. Imputacion de nulos en columnas numericas ---
imputer = Imputer(inputCols=["monto"], outputCols=["monto_imputado"])

# --- 2. Encoding de la variable categorica ---
indexer = StringIndexer(inputCol="tipo_transaccion", outputCol="tipo_transaccion_idx", handleInvalid="keep")
encoder = OneHotEncoder(inputCols=["tipo_transaccion_idx"], outputCols=["tipo_transaccion_ohe"])

# --- 3. Ensamblado del vector de features ---
assembler = VectorAssembler(
    inputCols=["monto_imputado", "tipo_transaccion_ohe"],
    outputCol="features_raw",
)

# --- 4. Escalado ---
scaler = StandardScaler(inputCol="features_raw", outputCol="features")

# --- 5. Modelo ---
lr = LogisticRegression(featuresCol="features", labelCol="es_fraude")

pipeline = Pipeline(stages=[imputer, indexer, encoder, assembler, scaler, lr])

# --- 6. Split y entrenamiento ---
train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
modelo = pipeline.fit(train_df)

# --- 7. Evaluacion ---
predicciones = modelo.transform(test_df)
evaluador = BinaryClassificationEvaluator(labelCol="es_fraude", metricName="areaUnderROC")
auc = evaluador.evaluate(predicciones)
print(f"=== AUC en test: {auc:.4f} ===")

# --- 8. Guardar el pipeline entrenado (reproducible, se puede cargar en la sesion de serving) ---
modelo.write().overwrite().save("/tmp/modelo_fraude_pipeline")

spark.stop()
