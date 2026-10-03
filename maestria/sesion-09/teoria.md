# Teoría — Streaming: tiempo, estado y garantías

Un stream de archivos procesa objetos nuevos mientras llegan; que cada entrada sea un archivo no lo convierte en un único batch estático. El lab usa Pub/Sub estándar, un puente de persistencia y Spark Structured Streaming. La latencia incluye publicación, escritura del lote, descubrimiento del archivo y trigger de Spark.

## Tiempo de evento y watermark

Las ventanas agrupan timestamp del evento, no hora de recepción. El watermark se deriva del máximo tiempo de evento observado menos la tolerancia; el operador aplica su watermark durante el procesamiento del lote y elimina estado cuando corresponde. No es «esperar dos minutos de reloj». En general `update` puede emitir una ventana varias veces. Este lab encadena deduplicación y agregación, y usa `append`: imprime ventanas finalizadas cuando avanza el watermark.

## Recuperación y duplicados

Pub/Sub estándar entrega al menos una vez por defecto. El puente hace ACK tras escribir un objeto inmutable. Si falla entre escritura y ACK, puede reentregar. Deduplicar por transaction_id dentro del horizonte limita el estado; no sustituye un registro histórico de unicidad. Cada consulta conserva su checkpoint y debe recuperar desde él para mantener continuidad. Watermark no garantiza exactly-once; fuente, sink y protocolo de commit importan.

## Features y scoring

El PipelineModel de S6 incluye derivación de hora, transformaciones ajustadas con train y clasificador. Streaming y API no vuelven a hacer fit. La hora usa UTC y timestamp del evento; el replay omite el label porque en operación se conoce después. Registrar URI de modelo en cada score permite auditar resultados.

## Evidencia y límites

Comparar ID repetido, evento tardío y reinicio con checkpoint. Usar prefijo nuevo si se cambia el contrato o el experimento. La consola es un sink docente no transaccional. Producir máximo 1200 eventos y jobs de 180 segundos mantiene la práctica acotada; el cluster se borra tras guardar evidencia.

Referencias: [Spark 3.5](https://spark.apache.org/docs/3.5.3/structured-streaming-programming-guide.html), [Pub/Sub: duplicados](https://docs.cloud.google.com/pubsub/docs/subscribe-best-practices), [retiro de Lite](https://docs.cloud.google.com/pubsub/lite/docs/release-notes).
