# Facilitación — Sesión 09: Streaming I — fundamentos y setup

> Guion de 3 horas: talking points + lab guiado. Esta sesión tiene más setup de
> infraestructura que código nuevo — el topic/suscripción de Pub/Sub Lite no es
> trivial la primera vez. Dale tiempo real a esa parte, no la subestimes en el
> guion.

## Antes de empezar (facilitador)

Crea tú mismo el topic y la suscripción **antes** de la sesión, una vez, para
confirmar que el proyecto tiene los permisos necesarios (Pub/Sub Lite no
siempre viene habilitado por default en un proyecto nuevo). Si falta habilitar
la API, es mejor descubrirlo antes que con 15 personas esperando.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Todo lo que han procesado hasta ahora era un archivo completo, quieto,
> esperando. Hoy trabajamos con datos que nunca 'terminan' de llegar — y eso
> rompe una suposición que llevan usando todo el curso: que pueden leer todo el
> dataset antes de decidir qué hacer con él."

**Pregunta de apertura:**

> "Si les pido 'el promedio de las últimas 24 horas' sobre un stream que nunca
> para, ¿cuándo calculan ese promedio? ¿Cada segundo? ¿Nunca?"

(Es el gancho hacia windowing — déjalo sin resolver.)

**Ejemplo de actualidad:**

> "Cada vez que Uber calcula un precio dinámico, o un banco bloquea una tarjeta
> en el momento de un cargo sospechoso, hay un sistema de streaming con
> windowing resolviendo exactamente esta pregunta en producción, a escala de
> millones de eventos por segundo."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Windowing y watermarks (20 min)

Dibuja una línea de tiempo con ventanas de 1 minuto y un evento que llega
tarde. Pregunta: **"¿qué debería pasar con ese evento tardío — se descarta, se
espera indefinidamente, o algo intermedio?"** Ahí introduces watermark como la
respuesta a "cuánto esperar antes de cerrar definitivamente".

### Exactly-once vs. at-least-once (15 min)

Este es un punto sutil — dale tiempo. La confusión más común: pensar que el
watermark da "exactly-once" de mensajes. Aclara explícito: el watermark da
exactly-once en el **cálculo de la ventana**; que un mensaje no llegue
duplicado es garantía de Pub/Sub Lite, otra capa completamente distinta.

### Por qué Pub/Sub Lite (10 min)

Punto práctico: Spark no tiene conector nativo para Pub/Sub estándar — Pub/Sub
Lite sí, mantenido oficialmente por Google. No es un rodeo, es la única opción
real soportada.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Crear topic y suscripción (20 min)

```bash
gcloud pubsub lite-topics create transacciones-stream \
    --location=us-central1-a --partitions=1 --per-partition-bytes=30GiB
gcloud pubsub lite-subscriptions create transacciones-stream-sub \
    --location=us-central1-a --topic=transacciones-stream
```

**Deberías ver:** ambos comandos confirman creación exitosa.
`gcloud pubsub lite-topics list --location=us-central1-a` debe mostrar el
topic.

**Si falla con permisos:** la API de Pub/Sub Lite puede necesitar habilitarse
explícitamente — `gcloud services enable pubsublite.googleapis.com`.

### Paso 2 — Correr el productor (20 min)

```bash
pip install google-cloud-pubsublite pandas
python producer_transacciones_stream.py --project <PROJECT_ID> --tasa 20
```

**Deberías ver:** el script imprime "Publicando N transacciones..." y sigue
corriendo — déjalo en una terminal visible para todo el bloque.

### Paso 3 — Correr el consumidor de conteo (35 min)

En otra terminal / el cluster:

```bash
spark-submit --master yarn 07a_streaming_conteo.py \
    --project <PROJECT_ID> --subscription transacciones-stream-sub
```

**Deberías ver:** cada 30 segundos, una tabla en consola con `window`,
`currency`, `count` — las ventanas cerrándose en vivo.

**Talking point mientras corre:** "Miren cómo cada ventana aparece una sola vez
en `outputMode('update')` cuando cambia — no está reimprimiendo todo desde el
principio cada vez."

### Paso 4 — Experimentar con el watermark (15 min)

Detén el consumidor, cambia `"2 minutes"` a `"10 seconds"` en el código, y
vuelve a correr. Pregunta: **"¿qué esperan que cambie?"** (más eventos tardíos
se van a descartar — buen momento para verlo en la salida de consola).

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Detener ambos procesos** (Ctrl+C) — no hace falta borrar el topic/suscripción
todavía, la Sesión 10 los reusa.

**Entregable de hoy:** captura de las ventanas de conteo actualizándose en
consola + confirmación de que productor y consumidor corrieron simultáneamente
sin errores.

**Puente a la Sesión 10:**

> "Hoy solo contamos. La próxima sesión le agregamos el modelo entrenado en la
> Sesión 6 — mismo pipeline, ahora con inferencia real sobre cada transacción
> que llega."

---

## Notas de costo GCP

- Pub/Sub Lite **no está en Always Free** — se cobra por capacidad reservada
  (partición + throughput), no por mensaje. No borres el topic/suscripción si
  la Sesión 10 los va a reusar en pocos días, pero sí confirma que nadie deje
  el productor corriendo indefinidamente fuera de horario de clase.
