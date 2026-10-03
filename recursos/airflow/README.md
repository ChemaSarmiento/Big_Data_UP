# Airflow S12 — candidato versionado y despliegue condicionado

Ruta docente: **Airflow 2.11.0 / Python 3.11**, en un entorno propio en laptop o VM temporal `e2-standard-2` con 8 GB. No usar `e2-micro` como configuración recomendada. Airflow recomienda al menos 4 GB ([fuente](https://airflow.apache.org/docs/apache-airflow/2.11.0/installation/prerequisites.html)). SQLite y standalone son para clase, no una arquitectura de producción. Cloud Composer es panorama opcional, no recurso que deba permanecer encendido.

## Entorno separado

```bash
python3.11 -m venv .venv-airflow
source .venv-airflow/bin/activate
pip install 'apache-airflow==2.11.0' apache-airflow-providers-google \
  --constraint https://raw.githubusercontent.com/apache/airflow/constraints-2.11.0/constraints-3.11.txt
export AIRFLOW_HOME="$PWD/.airflow-lab"
export AIRFLOW__WEBSERVER__WEB_SERVER_PORT=8081
airflow db migrate
```

Usar ADC en local y una cuenta de servicio con permisos limitados en VM. Subir `04_pipeline_ml.py` y `ml_common.py` al bucket. Crear el cluster solo durante el lab; este DAG **no crea ni borra el cluster**. Mantener el DAG pausado fuera del lab: su schedule semanal necesita un cluster existente y la VM/API activa.

Variables (la configuración del bucket es solo su nombre, sin `gs://`):

```bash
airflow variables set gcp_project_id <PROJECT_ID>
airflow variables set gcp_bucket <BUCKET_UNICO>
airflow variables set gcp_cluster curso-cluster
airflow variables set training_cutoff <FECHA_ISO_DEL_DATASET>
airflow variables set auc_min 0.75
airflow variables set pr_auc_min 0.10
airflow variables set serving_host 127.0.0.1:8080
```

`0.75` y `0.10` son umbrales de demostración que el equipo debe justificar usando prevalencia, costo de falsos positivos y un baseline. No son estándares de aceptación. Configurar `reload_token` como secreto (mismo valor que `RELOAD_TOKEN` del API), sin guardarlo en Git. La URL debe ser accesible desde el worker Airflow; en VM usar túnel/red privada, no abrir puertos al mundo.

```bash
mkdir -p "$AIRFLOW_HOME/dags"
cp recursos/airflow/dags/mlops_pipeline_dag.py "$AIRFLOW_HOME/dags/"
airflow standalone
```

## Qué ocurre en cada run

1. Revisar el motivo (schedule/manual o reporte de drift revisado).
2. Ejecutar el mismo script bancario en Dataproc, con corte temporal y output `modelos/runs/<ts_nodash>`.
3. Leer `metrics.json` de **ese run** y comprobar que la URI del candidato coincide.
4. Comparar ROC-AUC y PR-AUC con umbrales configurados; rechazo conserva el modelo servido.
5. Pedir `/reload` con URI y token; un HTTP fallido hace fallar la tarea.

Las plantillas se pasan por `job` y `op_kwargs`, campos renderizados por Airflow. No se incrustan plantillas Jinja dentro de funciones Python. No hay tareas «verdes» por ignorar una respuesta HTTP fallida.

## Trigger por drift

En S11 se genera un reporte sobre muestras. Revisar causas, cambios de datos, calidad y evidencia de performance antes de activar el candidato:

```bash
python recursos/airflow/trigger_drift.py --report drift.json --run-id drift-20261002-001
```

El disparador envía `dag_run.conf` con PSI/umbral; el DAG puede saltar el entrenamiento si está por debajo. Drift **no despliega automáticamente**: el candidato vuelve a pasar la puerta de calidad. La recarga tiene lock en la API docente; producción requeriría evaluación adicional, rollback y control de concurrencia/carga.

Cerrar el lab: pausar DAG, parar Airflow/API, borrar cluster y detener VM. Guardar modelo, métricas, grafo y reporte asociado para el capstone.
