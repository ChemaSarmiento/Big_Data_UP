"""Verificar DAG real con Airflow instalado, sin submit de jobs GCP."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

path = Path(__file__).resolve().parents[1] / 'recursos/airflow/dags/mlops_pipeline_dag.py'
spec = importlib.util.spec_from_file_location('course_dag', path)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
from airflow.utils.dag_cycle_tester import check_cycle
from airflow.serialization.serialized_objects import SerializedDAG
check_cycle(module.dag)
SerializedDAG.to_dict(module.dag)
config = SimpleNamespace(gcp_project_id='test-project',gcp_bucket='test-bucket',gcp_cluster='test-cluster',
    training_cutoff='2026-01-01',auc_min='0.75',pr_auc_min='0.10',serving_host='127.0.0.1:8080',reload_token='test-token')
context = {'var':SimpleNamespace(value=config), 'ts_nodash':'20261002T010000'}
for task in module.dag.tasks:
    task.render_template_fields(context)
job = module.dag.get_task('entrenamiento_y_features').job
assert job['pyspark_job']['args'][3]=='gs://test-bucket/modelos/runs/20261002T010000'
assert '{{' not in json.dumps(job)
assert module.dag.get_task('evaluar_metricas').op_kwargs['bucket']=='test-bucket'
assert module.dag.get_task('desplegar_modelo').op_kwargs['host']=='127.0.0.1:8080'
assert module.gate_training(dag_run=SimpleNamespace(conf={'reason':'drift','psi':0.01}))=='sin_reentrenamiento'
assert module.gate_training(dag_run=SimpleNamespace(conf={'reason':'drift','psi':0.3}))=='entrenamiento_y_features'
metrics = {'auc':0.8,'pr_auc':0.3,'test_rows':10,'model_uri':'gs://test-bucket/modelos/runs/20261002T010000/pipeline'}
ti = SimpleNamespace(xcom_pull=lambda **kwargs:metrics,xcom_push=lambda **kwargs:None)
assert module.choose_deployment(.75,.1,ti=ti)=='desplegar_modelo'
assert module.choose_deployment(.9,.1,ti=ti)=='no_desplegar'
with patch('google.cloud.storage.Client') as storage:
    storage.return_value.bucket.return_value.blob.return_value.download_as_text.return_value=json.dumps(metrics)
    assert module.read_metrics('test-bucket','20261002T010000',ti=ti)==metrics
    try: module.read_metrics('test-bucket','wrong-run',ti=ti)
    except ValueError: pass
    else: raise AssertionError('Accepted metrics from another run')
with patch('requests.post') as post:
    post.return_value.raise_for_status.side_effect=RuntimeError('HTTP failure')
    try: module.deploy('127.0.0.1:8080','test-token',ti=ti)
    except RuntimeError: pass
    else: raise AssertionError('Deployment swallowed HTTP failure')
print('Airflow: DAG serialized; templates rendered; drift/quality branches, run metrics and failed HTTP checked')
