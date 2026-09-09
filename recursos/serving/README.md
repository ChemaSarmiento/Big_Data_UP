# Model serving y monitoreo de drift

Material técnico de Maestría Sesión 8: un endpoint de modelo real y el monitoreo
de drift que la teoría de la sesión exige como parte de un ciclo de MLOps
completo — un modelo entrenado sin un endpoint que lo sirva, y sin una forma de
detectar cuándo se volvió obsoleto, no cierra el ciclo ingesta→features→
entrenamiento→serving que pide el capstone.

## `serve_fraude.py` — endpoint HTTP

Carga el `PipelineModel` de la Sesión 4/5 en una SparkSession **local** dentro del
mismo proceso (no en el cluster de Dataproc) — es una decisión de diseño
deliberada, no un atajo: un cluster completo no es para responder una sola
petición HTTP en menos de un segundo. Vale la pena discutirlo en clase junto con
"cuándo Spark MLlib no alcanza" de la Sesión 5.

```bash
pip install fastapi uvicorn pyspark
MODELO=gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
  uvicorn serve_fraude:app --host 0.0.0.0 --port 8080

curl -X POST localhost:8080/score -H "Content-Type: application/json" -d '{
  "transaction_id": "t1", "timestamp": "2026-03-01T14:00:00", "amount": 12000, "currency": "MXN"
}'
```

- `POST /score` — un score por transacción.
- `POST /reload` — recarga el modelo sin reiniciar el proceso; lo llama `recursos/airflow/dags/mlops_pipeline_dag.py` al final de un despliegue exitoso.
- `GET /health` — para el liveness check de Cloud Run / Compute Engine si se despliega ahí.

## `monitor_drift.py` — drift de datos

Calcula el **Population Stability Index (PSI)** entre la distribución de `amount`
en el set de entrenamiento y un lote reciente de transacciones scoreadas
(`recursos/streaming/07_streaming_scoring.py` las va guardando en Parquet). Es el
estándar de industria para esto — un solo número interpretable, sin asumir una
distribución particular.

```bash
python monitor_drift.py \
    --referencia gs://<TU-BUCKET>/raw/bank_transactions/bank_transactions.csv \
    --lote_reciente gs://<TU-BUCKET>/streaming/scores \
    --columna amount
```

PSI > 0.25 es la señal para disparar `mlops_pipeline_dag.py` manualmente (fuera de
su corrida semanal) — así se cierra el ciclo completo que pide la teoría de la
Sesión 8: "reentrenamiento programado, triggers por drift".

## Ver también

- [`recursos/spark/04_pipeline_ml.ipynb`](../spark/04_pipeline_ml.ipynb) — el modelo que este endpoint sirve.
- [`recursos/streaming/`](../streaming/) — de donde sale `lote_reciente` para el chequeo de drift.
- [`recursos/airflow/`](../airflow/) — el DAG que llama a `/reload`.
