# Streaming e inferencia en tiempo real (Pub/Sub Lite + Structured Streaming)

Material técnico de Maestría Sesión 7: streaming real sobre Google Cloud, con el
mismo modelo entrenado en la Sesión 4/5. `recursos/etl-cripto/` (Sesión 1)
introduce la idea en batch como puente conceptual, pero un pipeline en batch, sin
importar qué tan rápido corra, no tiene windowing, watermarks ni estado — por eso
esta sesión necesita un motor de streaming real y no solo "correr el batch más
seguido".

## Por qué Pub/Sub Lite y no Pub/Sub estándar

Apache Spark no trae un conector nativo de Structured Streaming para Pub/Sub
estándar. **Pub/Sub Lite sí tiene un conector oficial de Google**
(`pubsublite-spark-sql-streaming`), mantenido por el mismo equipo de Dataproc —
es la opción real y soportada para conectar Spark a un stream de eventos en GCP,
no un rodeo. (`environment/gcp-setup.md` menciona Pub/Sub estándar en la tabla de
Always Free — Pub/Sub Lite se cobra distinto, por capacidad reservada, revisar
cuota antes del lab.)

## Los dos scripts

| Archivo | Qué hace | Dónde corre |
|---|---|---|
| `producer_transacciones_stream.py` | Lee `bank_transactions.csv` fila por fila y publica cada una como evento JSON, a una tasa controlada | Tu máquina o Cloud Shell — no necesita el cluster |
| `07_streaming_scoring.py` | Consume el stream, aplica el `PipelineModel` de la Sesión 4/5 y genera un score por transacción + un conteo de alertas por ventana de 1 minuto | Cluster de Spark (`spark-submit --master yarn`) |

## Lo que enseña que el lab de esta sesión pide explícitamente

- **Windowing + watermark:** `groupBy(F.window(...))` con `withWatermark("timestamp", "2 minutes")` — ver los comentarios del script para la distinción entre "exactly-once en el conteo" y "sin duplicados en el broker" (son garantías distintas, se confunden fácil).
- **Scoring en el stream (no vía endpoint externo):** el `PipelineModel` se carga una vez y se aplica directo sobre el DataFrame en streaming — el patrón contrario a la Sesión 8, donde el modelo se sirve como endpoint HTTP. Buen punto de comparación explícito en clase.
- **Feature freshness:** `hora_del_dia` se deriva del mismo `timestamp` del evento, no de la hora de procesamiento — si el stream se atrasa, la feature sigue siendo correcta (a diferencia de usar `current_timestamp()`).

## Correr

```bash
# Una sola vez
gcloud pubsub lite-topics create transacciones-stream --location=us-central1-a --partitions=1 --per-partition-bytes=30GiB
gcloud pubsub lite-subscriptions create transacciones-stream-sub --location=us-central1-a --topic=transacciones-stream

# Terminal 1 (productor)
python producer_transacciones_stream.py --project <PROJECT_ID> --tasa 20

# Terminal 2 / cluster (consumidor)
spark-submit --master yarn 07_streaming_scoring.py \
    --project <PROJECT_ID> --subscription transacciones-stream-sub \
    --modelo gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
    --salida gs://<TU-BUCKET>/streaming/scores
```

## Ver también

- [`recursos/spark/04_pipeline_ml.ipynb`](../spark/04_pipeline_ml.ipynb) — de donde sale el `PipelineModel` que este job carga.
- [`recursos/etl-cripto/`](../etl-cripto/) — mantiene su rol de puente conceptual (batch con dos rondas de Extract) antes de pasar a este lab.
