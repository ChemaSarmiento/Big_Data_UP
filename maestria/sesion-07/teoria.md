# Teoría — Sesión 07: Streaming e inferencia en tiempo real

> Todo lo construido en las Sesiones 4-5 (features, modelo) se reutiliza hoy sin
> cambios — lo que cambia es el contexto de ejecución: datos que nunca "terminan" de
> llegar, y garantías distintas sobre tiempo y duplicados.

## 1. Windowing y watermarks

Un stream, por definición, no tiene fin — "agrupa todos los eventos" no tiene sentido
sin acotar de alguna forma el tiempo. **Windowing** resuelve esto: agrupa eventos en
ventanas de tiempo fijas (ej. "cuenta las alertas cada minuto") en vez de intentar
agregar un stream infinito de una sola vez.

El problema que windowing por sí solo no resuelve: los eventos no siempre llegan en
orden — la red puede retrasar un mensaje, y llega "tarde" a una ventana que
lógicamente ya debería estar cerrada. Un **watermark** es la respuesta a "¿cuánto
tiempo espero antes de dar por cerrada una ventana?" — declara explícitamente cuánta
tardanza estás dispuesto a tolerar antes de calcular el resultado final de esa ventana.

```python
# recursos/streaming/07_streaming_scoring.py
scoreadas
    .withWatermark("timestamp", "2 minutes")  # tolera hasta 2 min de retraso
    .groupBy(F.window("timestamp", "1 minute"))  # ventanas de 1 minuto
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

El detalle que suele confundirse (marcado explícitamente en
`recursos/streaming/07_streaming_scoring.py`): un `checkpointLocation` con watermark
da exactly-once en el **cálculo de la agregación** (cada ventana se calcula una sola
vez, de forma determinística), pero eso es una garantía distinta de "no duplicados en
el broker" — esa segunda garantía la da Pub/Sub Lite del lado del envío de mensajes.
Confundir ambas lleva a asumir garantías más fuertes de las que realmente se tienen.

## 3. Patrones de scoring en tiempo real

Dos formas de aplicar un modelo entrenado a datos que llegan en streaming:

| Patrón | Cómo funciona | Trade-off |
|---|---|---|
| **Modelo cargado en el stream** | El `PipelineModel` se carga una vez, en memoria del job de streaming, y se aplica directo sobre cada microlote (`recursos/streaming/07_streaming_scoring.py`) | Baja latencia (no hay llamada de red por evento), pero el modelo solo se actualiza si se reinicia el job |
| **Llamada a un endpoint externo** | El job de streaming hace una petición HTTP a un servicio de serving (`recursos/serving/serve_fraude.py`) por cada evento o microlote | El modelo se puede actualizar sin tocar el job de streaming (solo el endpoint), a cambio de latencia de red y un punto de falla adicional |

Este curso usa el primer patrón en streaming (Sesión 7) y el segundo en serving batch
(Sesión 8) — la comparación directa entre ambos, con el mismo modelo, es justo el
ejercicio que conecta las dos sesiones.

## 4. Feature freshness

Una feature "fresca" es una que refleja el estado real del mundo en el momento de la
predicción, no un valor calculado hace horas. En streaming esto tiene un matiz sutil:
`hora_del_dia` debe derivarse del **timestamp del evento** (`F.hour("timestamp")`),
no del momento en que el job lo procesa (`current_timestamp()`) — si el stream se
atrasa por cualquier razón (una ráfaga de eventos, un reinicio del job), una feature
basada en tiempo de procesamiento estaría sistemáticamente equivocada, mientras que
una basada en tiempo del evento sigue siendo correcta sin importar cuándo se procesó
realmente.

---

## Referencias

- [Apache Spark — Structured Streaming Programming Guide (windowing, watermarks)](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Google Cloud — Pub/Sub Lite overview](https://cloud.google.com/pubsub/lite/docs/overview)
- [Akidau et al. — The Dataflow Model (el paper que formalizó windowing/watermarks, Google, VLDB 2015)](https://research.google/pubs/the-dataflow-model-a-practical-approach-to-balancing-correctness-latency-and-cost-in-massive-scale-unbounded-out-of-order-data-processing/)
