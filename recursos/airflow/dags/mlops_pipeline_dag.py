"""
mlops_pipeline_dag.py
DAG de Airflow que conecta ingesta -> features -> entrenamiento -> evaluación ->
(condicional) despliegue, sobre bank_transactions.csv y el mismo Pipeline de
MLlib de la Sesión 4/5 de Maestría. Corre en Airflow standalone en la VM
e2-micro Always Free (ver environment/gcp-setup.md) o en Cloud Composer si el
crédito de $300 alcanza -- Composer es el servicio más caro del curso, por eso
gcp-setup.md recomienda standalone por default.

pip install apache-airflow apache-airflow-providers-google

Variables de Airflow requeridas (Admin > Variables):
  gcp_project_id, gcp_bucket (gs://...), serving_host (host:puerto del endpoint
  de recursos/serving/serve_fraude.py)
"""
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

PROJECT_ID = "{{ var.value.gcp_project_id }}"
REGION = "us-central1"
CLUSTER_NAME = "curso-cluster"
BUCKET = "{{ var.value.gcp_bucket }}"
AUC_MINIMO = 0.75

default_args = {
    "owner": "curso-bigdata",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="mlops_fraude_bank_transactions",
    description="Ingesta -> features -> entrenamiento -> evaluación -> despliegue (bank_transactions.csv)",
    schedule="@weekly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["maestria", "sesion-08"],
) as dag:

    # --- Ingesta + features + entrenamiento en un solo job de Dataproc ---
    # Reusa recursos/spark/04_pipeline_ml.py tal cual (subido antes a
    # gs://<TU-BUCKET>/scripts/), el mismo Pipeline de MLlib de la Sesión 4/5.
    features_job = {
        "reference": {"project_id": PROJECT_ID},
        "placement": {"cluster_name": CLUSTER_NAME},
        "pyspark_job": {
            "main_python_file_uri": f"{BUCKET}/scripts/04_pipeline_ml.py",
            "args": ["--input", f"{BUCKET}/raw/bank_transactions/bank_transactions.csv"],
        },
    }

    entrenamiento_y_features = DataprocSubmitJobOperator(
        task_id="entrenamiento_y_features",
        job=features_job,
        region=REGION,
        project_id=PROJECT_ID,
    )

    def leer_auc_del_job(**contexto):
        # El notebook de la Sesión 4/5 (recursos/spark/04_pipeline_ml.ipynb, celda
        # final) escribe metrics.json explícitamente para este paso -- no se parsea
        # el log del job de Dataproc, es frágil y cambia de formato entre versiones.
        import json

        from google.cloud import storage

        bucket_nombre = BUCKET.replace("gs://", "")
        cliente = storage.Client()
        blob = cliente.bucket(bucket_nombre).blob("modelos/metrics.json")
        metricas = json.loads(blob.download_as_text())
        contexto["ti"].xcom_push(key="auc", value=metricas["auc"])
        return metricas["auc"]

    evaluar_metricas = PythonOperator(
        task_id="evaluar_metricas",
        python_callable=leer_auc_del_job,
    )

    def decidir_despliegue(**contexto):
        auc = contexto["ti"].xcom_pull(task_ids="evaluar_metricas", key="auc")
        return "desplegar_modelo" if auc >= AUC_MINIMO else "no_desplegar"

    puerta_calidad = BranchPythonOperator(
        task_id="puerta_calidad",
        python_callable=decidir_despliegue,
    )

    def desplegar(**contexto):
        # recursos/serving/serve_fraude.py expone POST /reload para recargar el
        # PipelineModel más reciente sin reiniciar el proceso. Con Vertex AI
        # Endpoints en vez de serving propio, este paso sería
        # `gcloud ai endpoints deploy-model ...` -- se deja como comentario porque
        # el curso usa Vertex AI solo como panorama (ver PROGRAMA.md, Sesión 5).
        import requests

        requests.post("http://{{ var.value.serving_host }}/reload", timeout=30)

    desplegar_modelo = PythonOperator(task_id="desplegar_modelo", python_callable=desplegar)
    no_desplegar = EmptyOperator(task_id="no_desplegar")

    entrenamiento_y_features >> evaluar_metricas >> puerta_calidad >> [desplegar_modelo, no_desplegar]
