# Teoría — Sesión 10: Streaming II — inferencia en tiempo real

> Segunda de dos sesiones de streaming. La Sesión 9 dejó windowing/watermarks
> funcionando sobre un conteo simple; hoy se agrega el modelo entrenado en la
> Sesión 6, sin reentrenar nada — el mismo `PipelineModel`, aplicado a datos que
> llegan continuamente.

## 1. Dos patrones de scoring en tiempo real

| Patrón | Cómo funciona | Trade-off |
|---|---|---|
| **Modelo cargado en el stream** | El `PipelineModel` se carga una vez, en memoria del job de streaming, y se aplica directo sobre cada microlote (`recursos/streaming/07_streaming_scoring.py`) | Baja latencia (no hay llamada de red por evento), pero el modelo solo se actualiza si se reinicia el job |
| **Llamada a un endpoint externo** | El job de streaming hace una petición HTTP a un servicio de serving (Sesión 11) por cada evento o microlote | El modelo se puede actualizar sin tocar el job de streaming (solo el endpoint), a cambio de latencia de red y un punto de falla adicional |

Este curso usa el primer patrón en streaming (hoy) y el segundo en serving batch
(Sesión 11) — la comparación directa entre ambos, con el mismo modelo, es justo el
ejercicio que conecta las dos sesiones.

**Por qué `PipelineModel.transform()` funciona igual en streaming que en batch:**
todas las etapas del pipeline (`Imputer`, `StringIndexer`, `OneHotEncoder`,
`VectorAssembler`, `StandardScaler`, `LogisticRegression` ya *fit*) son row-wise —
ninguna mantiene estado nuevo entre filas. Por eso el mismo objeto guardado en la
Sesión 6 se aplica sin modificar una sola línea sobre un DataFrame en streaming.

## 2. Feature freshness

Una feature "fresca" es una que refleja el estado real del mundo en el momento de la
predicción, no un valor calculado hace horas. En streaming esto tiene un matiz sutil:

```python
# BIEN: derivado del timestamp del EVENTO
.withColumn("hora_del_dia", F.hour("timestamp"))

# MAL: derivado del momento de PROCESAMIENTO
.withColumn("hora_del_dia", F.hour(F.current_timestamp()))
```

Si el stream se atrasa por cualquier razón (una ráfaga de eventos, un reinicio del
job), la versión "MAL" queda sistemáticamente equivocada, mientras que la versión
"BIEN" sigue siendo correcta sin importar cuándo se procesó realmente el evento.

## 3. Lo que cambia hoy respecto al lab de la Sesión 9

`07_streaming_scoring.py` retoma exactamente el mismo esqueleto de
`07a_streaming_conteo.py` (lectura de Pub/Sub Lite, parseo del JSON, windowing con
watermark) y agrega dos cosas: la carga del `PipelineModel` de la Sesión 6, y un
segundo sink que escribe cada transacción scoreada a Parquet — para auditoría o
reentrenamiento futuro, el mismo principio de versionado de datos de la Sesión 8
aplicado a datos que llegan en tiempo real.

---

## Referencias

- [Apache Spark — Structured Streaming Programming Guide](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Apache Spark MLlib — ML Pipelines (docs oficiales)](https://spark.apache.org/docs/latest/ml-pipeline.html)
- [Google Cloud — Pub/Sub Lite overview](https://cloud.google.com/pubsub/lite/docs/overview)
