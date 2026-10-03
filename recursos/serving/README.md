# Serving y monitoreo S11

La API sirve el mismo pipeline bancario guardado en S6. Es un **prototipo docente** con Spark local: medir latencia fría/caliente y concurrencia; no prometer un SLA inferior a un segundo. Para una solución operable, discutir autenticación, límites, rollback y separación de cómputo.

## API (Python 3.11 / Java 17)

Instalar `environment/requirements-lab.txt`. Un modelo GCS se descarga a una carpeta temporal antes de cargarlo: no se presupone que Spark local tenga conector `gs://`. Usar ADC y una VM/laptop con 4+ GB libres, no una micro compartida para Spark y Airflow.

```bash
export MODELO=gs://<BUCKET>/modelos/runs/<RUN_ID>/pipeline
export MODELO_ROOT=gs://<BUCKET>/modelos/runs
# Configurar RELOAD_TOKEN con un valor secreto, igual al de Airflow; no guardarlo en Git.
uvicorn serve_fraude:app --app-dir recursos/serving --host 127.0.0.1 --port 8080
```

```bash
curl -X POST localhost:8080/score -H 'Content-Type: application/json' \
  -d '{"transaction_id":"t1","timestamp":"2026-03-01T14:00:00Z","amount":12000,"currency":"MXN"}'
```

`/score`: probabilidad, decisión y URI de versión. `/health`: modelo cargado. `/reload`: requiere token y URI bajo `MODELO_ROOT`; carga un candidato completo antes de reemplazarlo. En clase usar loopback/túnel; no exponer `/score` ni `/reload` públicamente. La feature de hora vive dentro del modelo para evitar diferencias entre batch/stream/API.

## PSI con muestras acotadas

El entrenamiento deja `referencia.parquet` de hasta 100,000 montos **del train**. Preparar una muestra reciente desde `scores/datos`, con Spark, sin cargar el stream completo en pandas:

```python
recent = spark.read.parquet("gs://<BUCKET>/streaming/<STREAM_RUN>/scores/datos")
recent.select("amount").limit(100000).write.mode("overwrite").parquet(
    "gs://<BUCKET>/monitoreo/reciente.parquet")
```

```bash
python recursos/serving/monitor_drift.py \
  --referencia gs://<BUCKET>/modelos/runs/<RUN_ID>/referencia.parquet \
  --lote-reciente gs://<BUCKET>/monitoreo/reciente.parquet --salida drift.json
```

Los valores 0.1 y 0.25 son **reglas docentes de investigación**, no umbrales universales ni evidencia de pérdida de performance. PSI mide cambio de distribución, no concept drift. Discutir tamaño, representatividad, nulos y selección de buckets; visualizar distribuciones y contrastar con métricas etiquetadas cuando estén disponibles. Cuantiles repetidos/muestras vacías se tratan explícitamente. No reentrenar ciegamente por estacionalidad.

Tras revisar `drift.json`, [trigger_drift.py](../airflow/trigger_drift.py) puede pedir un candidato nuevo. La puerta ROC/PR-AUC y la revisión del costo siguen siendo necesarias. El proceso de monitoreo no cambia el modelo por su cuenta.
