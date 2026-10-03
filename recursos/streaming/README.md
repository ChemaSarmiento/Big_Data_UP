# Streaming S9–10 — Pub/Sub estándar, GCS y Spark

Pub/Sub Lite fue retirado el 18 de marzo de 2026 ([Google](https://docs.cloud.google.com/pubsub/lite/docs/release-notes)). El lab usa un productor acotado, un puente de persistencia y el file source nativo de Spark. No requiere Kafka ni un conector comunitario. El puente escribe microlotes mientras Spark procesa nuevos objetos: **medir latencia de segundos/microlotes**, no anunciar tiempo real de milisegundos.

## Contrato y garantías

Evento: `transaction_id`, `timestamp` del evento, `amount`, `currency`. El label no viaja. El replay conserva timestamps históricos: watermark avanza con el máximo tiempo del evento observado, no con el reloj de pared. Repetir un replay requiere un prefijo/checkpoint nuevo para comparar resultados; reutilizar el checkpoint continúa el mismo stream.

Pub/Sub entrega al menos una vez por defecto. El puente confirma mensajes **después** de persistir un objeto inmutable; si falla antes del ACK, puede haber reentrega. IDs de lote repetidos no sobrescriben el objeto. Reagrupaciones pueden crear duplicados: Spark aplica `dropDuplicatesWithinWatermark` por `transaction_id`. Esa deduplicación tiene horizonte acotado; no garantiza unicidad histórica ilimitada. Watermark controla estado/eventos tardíos, no garantiza exactly-once por sí solo. El sink de consola es evidencia docente, no un sink transaccional.

## Preparación (terminal local/VM)

Desde la raíz, Python 3.11 y dependencias de `environment/requirements-lab.txt`:

```bash
gcloud auth application-default login
gcloud pubsub topics create transacciones-stream
gcloud pubsub subscriptions create transacciones-stream-sub --topic=transacciones-stream --ack-deadline=120
export PROJECT_ID=<PROJECT_ID>
export BUCKET_NAME=<BUCKET_UNICO>
export STREAM_RUN=s9-demo-01
```

Iniciar primero el puente y Spark, luego el productor, en terminales distintas. Topic/suscripción requieren permisos de Pub/Sub; puente requiere escritura de objetos en el bucket. El prefijo debe ser exclusivo de la ejecución.

```bash
# Puente (180 segundos; lee hasta 100 mensajes por petición)
python recursos/streaming/pubsub_to_gcs.py --project "$PROJECT_ID" \
  --bucket "$BUCKET_NAME" --prefix "streaming/$STREAM_RUN/entrada" --seconds 180
# Productor: CSV local, lectura secuencial, máximo 1200 eventos (~60 s a 20/s)
python recursos/streaming/producer_transacciones_stream.py --project "$PROJECT_ID" \
  --csv bank_transactions.csv --tasa 20 --max-events 1200
```

El prefijo GCS debe existir antes del job: iniciar el puente, publicar un evento de prueba y verificar que aparece un JSON. Después iniciar Spark y continuar el replay; así no se depende de que un directorio vacío exista en object storage.

## S9: conteo con ventanas

Subir scripts según `recursos/managed-spark-cluster/README.md`:

```bash
gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/07a_streaming_conteo.py \
  --cluster=curso-cluster --region=us-central1 \
  --py-files=gs://$BUCKET_NAME/scripts/stream_common.py -- \
  --input gs://$BUCKET_NAME/streaming/$STREAM_RUN/entrada \
  --checkpoint gs://$BUCKET_NAME/streaming/$STREAM_RUN/checkpoints/conteo --seconds 180
```

Comparar tiempo de evento/procesamiento, ventana de 1 minuto y tolerancia de 2 minutos. Probar un evento repetido y otro fuera del horizonte, explicando el resultado con Spark UI. Guardar captura y condiciones, no solo «corrió».

## S10: scoring con el candidato de S6

```bash
export MODEL_RUN=<RUN_ID_ENTRENAMIENTO>
gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/07_streaming_scoring.py \
  --cluster=curso-cluster --region=us-central1 \
  --py-files=gs://$BUCKET_NAME/scripts/stream_common.py -- \
  --input gs://$BUCKET_NAME/streaming/$STREAM_RUN/entrada \
  --modelo gs://$BUCKET_NAME/modelos/runs/$MODEL_RUN/pipeline \
  --salida gs://$BUCKET_NAME/streaming/$STREAM_RUN/scores --seconds 180
```

El modelo contiene la derivación de hora, transformaciones ajustadas sobre train y clasificador. No se vuelve a ajustar en streaming. Salida: `scores/datos` Parquet con probabilidad escalar, decisión y URI del modelo; checkpoints separados para scores y ventanas. Elegir otro `STREAM_RUN` o realizar un replay explícito para S10.

## Costos y cierre

Limitar eventos, tiempo y objetos. El puente produce archivos pequeños útiles para clase; en producción conviene controlar tamaño/compacción. Detener productor/puente, dejar finalizar Spark, guardar evidencia, borrar cluster y topic/suscripción cuando ya no se usen. Borrar entrada/checkpoints solo después de terminar el consumidor; su eliminación impide continuar ese estado.

Fuentes: [Pub/Sub: reentregas](https://docs.cloud.google.com/pubsub/docs/subscribe-best-practices), [Spark Structured Streaming](https://spark.apache.org/docs/3.5.3/structured-streaming-programming-guide.html).

Las consultas de ventanas usan `append`: emiten resultados cuando avanza el watermark y se finalizan ventanas. Una entrada con timestamps inmóviles puede no emitir ventanas finalizadas; explicar esa diferencia frente a `update`. El scoring por fila también usa append con su propio checkpoint.
