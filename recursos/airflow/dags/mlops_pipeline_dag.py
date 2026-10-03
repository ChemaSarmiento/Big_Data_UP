"""Airflow 2.11 / Python 3.11. Entrena un candidato versionado y evalúa antes de recargar.
Cluster efímero existente durante el lab; ver README para límites y limpieza.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

RUN_ROOT = "gs://{{ var.value.gcp_bucket }}/modelos/runs/{{ ts_nodash }}"


def gate_training(dag_run=None, **context):
    # A monitor may trigger this DAG with a reviewed drift report in dag_run.conf.
    # Scheduled/manual runs without a report train normally; drift alone never deploys.
    config = (dag_run.conf or {}) if dag_run else {}
    if config.get("reason") == "drift":
        psi = float(config["psi"])
        if psi < 0 or psi != psi or psi == float("inf"):
            raise ValueError("PSI inválido")
        if psi < float(config.get("threshold", 0.25)): return "sin_reentrenamiento"
    return "entrenamiento_y_features"


def read_metrics(bucket, run_id, **context):
    import json
    from google.cloud import storage
    blob = storage.Client().bucket(bucket).blob(f"modelos/runs/{run_id}/metrics.json")
    metrics = json.loads(blob.download_as_text())
    expected = f"gs://{bucket}/modelos/runs/{run_id}/pipeline"
    if metrics.get("model_uri") != expected or metrics.get("test_rows", 0) <= 0:
        raise ValueError("Las métricas no corresponden al candidato de este run")
    context["ti"].xcom_push(key="metrics", value=metrics)
    return metrics


def choose_deployment(auc_min, pr_auc_min, **context):
    metrics = context["ti"].xcom_pull(task_ids="evaluar_metricas", key="metrics")
    return "desplegar_modelo" if metrics["auc"] >= float(auc_min) and metrics["pr_auc"] >= float(pr_auc_min) else "no_desplegar"


def deploy(host, token, **context):
    import requests
    metrics = context["ti"].xcom_pull(task_ids="evaluar_metricas", key="metrics")
    response = requests.post(f"http://{host}/reload", json={"model_uri": metrics["model_uri"]},
                             headers={"X-Reload-Token": token}, timeout=120)
    response.raise_for_status()
    return response.json()


with DAG(
    dag_id="mlops_fraude_bank_transactions", schedule="@weekly", start_date=datetime(2026, 1, 1),
    catchup=False, max_active_runs=1,
    default_args={"owner": "curso-bigdata", "retries": 1, "retry_delay": timedelta(minutes=1)},
    tags=["maestria", "sesion-12"],
) as dag:
    revisar_trigger = BranchPythonOperator(task_id="revisar_trigger", python_callable=gate_training)
    sin_reentrenamiento = EmptyOperator(task_id="sin_reentrenamiento")
    job = {
        "reference": {"project_id": "{{ var.value.gcp_project_id }}"},
        "placement": {"cluster_name": "{{ var.value.gcp_cluster }}"},
        "pyspark_job": {
            "main_python_file_uri": "gs://{{ var.value.gcp_bucket }}/scripts/04_pipeline_ml.py",
            "python_file_uris": ["gs://{{ var.value.gcp_bucket }}/scripts/ml_common.py"],
            "args": ["--input", "gs://{{ var.value.gcp_bucket }}/raw/bank_transactions/bank_transactions.csv",
                     "--output", RUN_ROOT, "--cutoff", "{{ var.value.training_cutoff }}"],
        },
    }
    entrenamiento_y_features = DataprocSubmitJobOperator(task_id="entrenamiento_y_features", job=job,
        region="us-central1", project_id="{{ var.value.gcp_project_id }}")
    evaluar_metricas = PythonOperator(task_id="evaluar_metricas", python_callable=read_metrics,
        op_kwargs={"bucket": "{{ var.value.gcp_bucket }}", "run_id": "{{ ts_nodash }}"})
    puerta_calidad = BranchPythonOperator(task_id="puerta_calidad", python_callable=choose_deployment,
        op_kwargs={"auc_min": "{{ var.value.auc_min }}", "pr_auc_min": "{{ var.value.pr_auc_min }}"})
    desplegar_modelo = PythonOperator(task_id="desplegar_modelo", python_callable=deploy,
        op_kwargs={"host": "{{ var.value.serving_host }}", "token": "{{ var.value.reload_token }}"})
    no_desplegar = EmptyOperator(task_id="no_desplegar")
    revisar_trigger >> [entrenamiento_y_features, sin_reentrenamiento]
    entrenamiento_y_features >> evaluar_metricas >> puerta_calidad >> [desplegar_modelo, no_desplegar]
