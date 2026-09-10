# Facilitación — Sesión 10: Streaming II — inferencia en tiempo real

> Guion de 3 horas: talking points + lab guiado. Retoma exactamente el pipeline de
> la Sesión 9 — hoy se agrega el modelo, sin tocar el mecanismo de windowing que
> ya quedó claro la sesión pasada.

## Antes de empezar (facilitador)

Confirma que el topic/suscripción de Pub/Sub Lite de la Sesión 9 sigue activo.
Ten a la mano la ruta del `PipelineModel` guardado en la Sesión 6.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "La sesión pasada contaron transacciones por ventana. Hoy van a scorear cada
> una con el modelo que entrenaron en la Sesión 6 — sin reentrenar nada, sin
> reescribir el pipeline de features. El mismo objeto, aplicado a datos que
> llegan en vivo."

**Pregunta de apertura:**

> "¿Creen que `PipelineModel.transform()` va a funcionar diferente sobre un
> DataFrame en streaming comparado con uno estático? ¿Por qué sí o por qué no?"

(Gancho hacia el punto técnico de la teoría: todas las etapas son row-wise, por
eso funciona igual.)

**Ejemplo de actualidad:**

> "Esto es literalmente el patrón de un sistema de detección de fraude en
> producción: el modelo no se reentrena por cada transacción — se aplica, ya
> entrenado, sobre el stream. El reentrenamiento pasa aparte, con su propio
> ciclo — lo vamos a ver en la Sesión 12."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Dos patrones de scoring (20 min)

Tabla comparativa en el pizarrón: modelo en el stream vs. endpoint externo.
Pregunta: **"¿cuál eligirían si el modelo cambia cada semana? ¿Y si necesitan
la latencia más baja posible?"** — no hay respuesta única, es un trade-off que
la Sesión 11 profundiza del otro lado (endpoint).

### Por qué `PipelineModel.transform()` funciona igual en streaming (15 min)

Punto técnico central: ninguna etapa (`Imputer`, `StringIndexer`,
`OneHotEncoder`, `VectorAssembler`, `StandardScaler`, `LogisticRegression`, ya
*fit*) mantiene estado nuevo entre filas — son todas transformaciones row-wise.
Por eso el mismo objeto se aplica sin modificar una línea.

### Feature freshness (10 min)

Muestra las dos versiones de código lado a lado (`timestamp` del evento vs.
`current_timestamp()`) y pregunta qué pasa si el stream se atrasa 5 minutos con
cada una.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Correr el productor (5 min)

```bash
python producer_transacciones_stream.py --project <PROJECT_ID> --tasa 20
```

### Paso 2 — Correr el consumidor con scoring (50 min)

```bash
spark-submit --master yarn 07_streaming_scoring.py \
    --project <PROJECT_ID> --subscription transacciones-stream-sub \
    --modelo gs://<TU-BUCKET>/modelos/fraude_bank_transactions_pipeline \
    --salida gs://<TU-BUCKET>/streaming/scores
```

**Deberías ver:** dos salidas simultáneas — el Parquet de scores escribiéndose
(confirmar con `gsutil ls gs://<TU-BUCKET>/streaming/scores/` en otra terminal)
y las ventanas de alertas (solo transacciones marcadas como sospechosas) en
consola cada 30 segundos.

**Si no aparecen alertas:** normal si `producer_transacciones_stream.py`
publica pocas transacciones sospechosas en la ventana de tiempo de la demo —
confirmar que el pipeline sí está scoreando revisando el Parquet de salida
directamente, no solo la consola.

### Paso 3 — Inspeccionar el Parquet de scores (20 min)

```python
scores = spark.read.parquet("gs://<TU-BUCKET>/streaming/scores")
scores.select("transaction_id", "prob_sospechosa", "es_sospechosa_pred").show(10)
```

**Pregunta de verificación:** "¿este Parquet tiene algo que ver con lo que
vimos en la Sesión 7-8 sobre versionado de datos?" (sí — es exactamente el tipo
de dato que valdría la pena migrar a una tabla Iceberg si se necesitara
corregirlo o auditarlo después).

### Paso 4 — Documentar el entregable (15 min)

Capturas de: el productor corriendo, las ventanas de alertas en consola, y una
muestra del Parquet de scores.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Detener ambos procesos.** Esta vez sí, si nadie más va a usar el topic
pronto, bórralo:

```bash
gcloud pubsub lite-subscriptions delete transacciones-stream-sub --location=us-central1-a
gcloud pubsub lite-topics delete transacciones-stream --location=us-central1-a
```

**Entregable de hoy:** pipeline de streaming con inferencia funcionando
end-to-end.

**Puente a la Sesión 11:**

> "Hoy sirvieron el modelo dentro del stream mismo. La próxima sesión lo sirven
> de la otra forma — como un endpoint HTTP al que cualquier sistema externo le
> puede preguntar. Van a comparar ambos patrones con el mismo modelo."

---

## Notas de costo GCP

- Si nadie más en el curso va a usar Pub/Sub Lite pronto, borrar el
  topic/suscripción al final de esta sesión — es el último lab que lo necesita
  hasta el capstone (si alguien lo reusa ahí).
