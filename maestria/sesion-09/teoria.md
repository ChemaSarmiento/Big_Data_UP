# Teoría — Sesión 09: Streaming I — fundamentos y setup

> Primera de dos sesiones de streaming. Todo lo construido en las Sesiones 5-6
> (features, modelo) se reutiliza sin cambios en la Sesión 10 — hoy el foco es el
> contexto de ejecución nuevo: datos que nunca "terminan" de llegar.

## 1. Windowing y watermarks

Un stream, por definición, no tiene fin — "agrupa todos los eventos" no tiene sentido
sin acotar de alguna forma el tiempo. **Windowing** resuelve esto: agrupa eventos en
ventanas de tiempo fijas (ej. "cuenta las transacciones cada minuto") en vez de
intentar agregar un stream infinito de una sola vez.

El problema que windowing por sí solo no resuelve: los eventos no siempre llegan en
orden — la red puede retrasar un mensaje, y llega "tarde" a una ventana que
lógicamente ya debería estar cerrada. Un **watermark** es la respuesta a "¿cuánto
tiempo espero antes de dar por cerrada una ventana?" — declara explícitamente cuánta
tardanza estás dispuesto a tolerar antes de calcular el resultado final de esa ventana.

```python
# recursos/streaming/07a_streaming_conteo.py
transacciones
    .withWatermark("timestamp", "2 minutes")  # tolera hasta 2 min de retraso
    .groupBy(F.window("timestamp", "1 minute"), "currency")  # ventanas de 1 minuto
    .count()
```

Con esta configuración: si un evento llega con más de 2 minutos de retraso respecto al
cierre de su ventana, se descarta — es la contraparte necesaria de la promesa de
"resultados en tiempo real": nunca vas a esperar indefinidamente a un evento rezagado.

## 2. Exactly-once vs. at-least-once

Dos garantías distintas sobre qué tan seguro es que un evento se procesó exactamente
una vez:

- **At-least-once:** un evento puede llegar a procesarse más de una vez (por ejemplo,
  si el sistema falla justo después de procesar pero antes de confirmar que lo hizo, y
  reintenta) — nunca se pierde un evento, pero puede duplicarse.
- **Exactly-once:** cada evento se procesa exactamente una vez, sin pérdidas ni
  duplicados — la garantía más fuerte, y la más cara de implementar correctamente.

Un `checkpointLocation` con watermark da exactly-once en el **cálculo de la
agregación** (cada ventana se calcula una sola vez, de forma determinística), pero
eso es una garantía distinta de "no duplicados en el broker" — esa segunda garantía
la da Pub/Sub Lite del lado del envío de mensajes. Confundir ambas lleva a asumir
garantías más fuertes de las que realmente se tienen.

## 3. Setup de Pub/Sub Lite

A diferencia de Pub/Sub estándar (mencionado en `environment/gcp-setup.md` como
Always Free), **Pub/Sub Lite** se cobra por capacidad reservada, no por mensaje — y
es el único conector de Structured Streaming que Google mantiene oficialmente para
Spark. El setup de hoy, una sola vez por proyecto:

```bash
gcloud pubsub lite-topics create transacciones-stream \
    --location=us-central1-a --partitions=1 --per-partition-bytes=30GiB
gcloud pubsub lite-subscriptions create transacciones-stream-sub \
    --location=us-central1-a --topic=transacciones-stream
```

Con el topic y la suscripción listos, `producer_transacciones_stream.py` publica
`bank_transactions.csv` fila por fila a una tasa controlada, simulando llegada en
tiempo real sin depender de que ocurra un evento real — y `07a_streaming_conteo.py`
es el primer consumidor, deliberadamente simple (solo cuenta, no aplica ningún
modelo) para que el grupo vea windowing/watermarks funcionar de forma aislada antes
de agregar la complejidad del scoring en la Sesión 10.

---

## Referencias

- [Apache Spark — Structured Streaming Programming Guide (windowing, watermarks)](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Google Cloud — Pub/Sub Lite overview](https://cloud.google.com/pubsub/lite/docs/overview)
- [Akidau et al. — The Dataflow Model (el paper que formalizó windowing/watermarks, Google, VLDB 2015)](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/)
