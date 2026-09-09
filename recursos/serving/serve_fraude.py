"""
serve_fraude.py
Endpoint HTTP simple para el PipelineModel entrenado en la Sesión 4/5 de Maestría
(recursos/spark/04_pipeline_ml.ipynb) -- la opción "serving simple vía API" que
menciona el PROGRAMA.md de Maestría como alternativa a Vertex AI Endpoints.

Nota de diseño: carga el PipelineModel en una SparkSession local (`local[2]`)
dentro del mismo proceso de la API, no en el cluster de Dataproc. Es el patrón
correcto para *baja latencia por request* (Vertex AI/un cluster completo son para
scoring batch de alto volumen, no para responder una petición HTTP en <1s) --
vale la pena decirlo explícito en clase: "por qué Spark MLlib no es para esto"
es justo lo que la Sesión 5 ya adelanta como límite de Spark MLlib.

pip install fastapi uvicorn pyspark

Correr:
  MODELO=gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
  uvicorn serve_fraude:app --host 0.0.0.0 --port 8080
"""
import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, functions as F

RUTA_MODELO = os.environ.get("MODELO", "gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline")

spark = SparkSession.builder.appName("serve_fraude").master("local[2]").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

modelo = PipelineModel.load(RUTA_MODELO)

app = FastAPI(title="Serving — modelo de fraude (bank_transactions)")


class Transaccion(BaseModel):
    transaction_id: str
    timestamp: datetime
    amount: float
    currency: str


@app.post("/score")
def score(transaccion: Transaccion):
    fila = spark.createDataFrame([transaccion.model_dump()])
    fila = fila.withColumn("hora_del_dia", F.hour("timestamp"))
    resultado = modelo.transform(fila).select("prediction", "probability").first()
    return {
        "transaction_id": transaccion.transaction_id,
        "es_sospechosa_pred": bool(resultado["prediction"]),
        "prob_sospechosa": float(resultado["probability"][1]),
    }


@app.post("/reload")
def reload_modelo():
    # Llamado por recursos/airflow/dags/mlops_pipeline_dag.py después de que un
    # modelo nuevo pasa la puerta de calidad (AUC >= 0.75) -- recarga sin
    # reiniciar el proceso, para no tumbar el endpoint en producción.
    global modelo
    modelo = PipelineModel.load(RUTA_MODELO)
    return {"status": "modelo recargado", "ruta": RUTA_MODELO}


@app.get("/health")
def health():
    return {"status": "ok", "modelo": RUTA_MODELO}
