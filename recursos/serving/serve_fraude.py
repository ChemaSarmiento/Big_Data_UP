"""API docente: medir latencia; Spark local no implica un SLA de producción."""
import os
import secrets
import threading
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession, types as T
from model_store import local_model

MODEL_URI = os.environ.get("MODELO", "")
MODEL_ROOT = os.environ.get("MODELO_ROOT", "")
RELOAD_TOKEN = os.environ.get("RELOAD_TOKEN", "")
lock = threading.RLock()
state = {}


def load(uri):
    local, staging = local_model(uri)
    try:
        return PipelineModel.load(local), staging
    except Exception:
        if staging: staging.cleanup()
        raise


@asynccontextmanager
async def lifespan(app):
    if not MODEL_URI or not RELOAD_TOKEN or not MODEL_ROOT:
        raise RuntimeError("Configura MODELO, MODELO_ROOT y RELOAD_TOKEN")
    spark = SparkSession.builder.appName("serve_fraude").master("local[2]").getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    spark.sparkContext.setLogLevel("ERROR")
    try:
        model, staging = load(MODEL_URI)
        state.update(spark=spark, model=model, staging=staging, uri=MODEL_URI)
        yield
    finally:
        if state.get("staging"): state["staging"].cleanup()
        state.clear(); spark.stop()


app = FastAPI(title="Serving docente de transacciones", lifespan=lifespan)


class Transaccion(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False)
    transaction_id: str = Field(min_length=1)
    timestamp: datetime
    amount: float
    currency: str = Field(min_length=1)


class Reload(BaseModel):
    model_uri: str


@app.post("/score")
def score(transaction: Transaccion):
    schema = T.StructType([
        T.StructField("transaction_id", T.StringType()), T.StructField("timestamp", T.TimestampType()),
        T.StructField("amount", T.DoubleType()), T.StructField("currency", T.StringType()),
    ])
    with lock:
        row = state["spark"].createDataFrame([transaction.model_dump()], schema=schema)
        result = state["model"].transform(row).select("prediction", "probability").first()
        return {"transaction_id": transaction.transaction_id, "es_sospechosa_pred": bool(result["prediction"]),
                "prob_sospechosa": float(result["probability"][1]), "modelo_uri": state["uri"]}


@app.post("/reload")
def reload_model(request: Reload, x_reload_token: str = Header(default="")):
    if not secrets.compare_digest(x_reload_token, RELOAD_TOKEN):
        raise HTTPException(status_code=403, detail="Token de recarga inválido")
    if not request.model_uri.startswith(MODEL_ROOT.rstrip('/') + '/') or '/..' in request.model_uri:
        raise HTTPException(status_code=400, detail="Modelo fuera del directorio autorizado")
    with lock:
        model, staging = load(request.model_uri)
        old_staging = state["staging"]
        state.update(model=model, staging=staging, uri=request.model_uri)
        if old_staging: old_staging.cleanup()
    return {"status": "modelo recargado", "modelo_uri": request.model_uri}


@app.get("/health")
def health():
    return {"status": "ok", "modelo_uri": state.get("uri")}
