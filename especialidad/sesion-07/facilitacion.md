# Facilitación — Sesión 07: Datos en tiempo real

> Guion de 3 horas: demo guiada + discusión, sin código de código para el grupo.
> El objetivo es que reconozcan, en su propio negocio, cuándo tiempo real se
> justifica y cuándo no.

## Antes de empezar (facilitador)

Prepara un flujo de eventos simple para demo (puede ser tan básico como una
serie de datos llegando cada pocos segundos en una hoja de cálculo simulada, o
si tienes acceso, una demo real de streaming ya armada).

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "La pregunta de hoy no es técnica — es de negocio: ¿alguien va a actuar
> distinto si la respuesta llega en segundos en vez de en horas? Si la
> respuesta es no, tiempo real es pagar complejidad de más sin ganar nada."

**Pregunta de apertura:**

> "¿Cuál creen que es más caro de construir: un reporte que se genera cada
> noche, o un sistema que detecta algo en el momento en que ocurre? ¿Por qué?"

---

## Bloque 2 — Batch vs. tiempo real (0:15–1:00, 45 min)

### La distinción central (15 min)
Reporte mensual vs. detección de fraude en el momento — el contraste de
`teoria.md`. Pide ejemplos propios del grupo para cada categoría.

### Los trade-offs, con la tabla (20 min)
Recorre costo de infraestructura, complejidad de desarrollo, y cuándo se
justifica cada uno. Pregunta después de cada fila: **"¿un ejemplo de su
industria que caiga en esta columna?"**

### El error común (10 min)

> "Construir un sistema de tiempo real para un reporte que de todas formas
> nadie mira hasta la mañana siguiente — eso paga toda la complejidad de la
> tabla de la derecha sin ganar nada de valor real. Es el mismo error de
> sobre-ingeniería de la Sesión 1, con otro disfraz."

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Demo guiada (1:10–2:20, 70 min)

### Correr el flujo de eventos (30 min)

Demo en vivo (facilitador corre, grupo observa) de un flujo simple. Narra cada
evento conforme llega: "esto está pasando ahora mismo, no es un archivo que ya
estaba esperando".

### Discusión guiada: ¿dónde aplicaría en su negocio? (40 min)

En equipos, cada quien identifica un proceso de su propia área que hoy es
batch y evalúa: ¿tiene sentido volverlo tiempo real? Usar explícitamente la
pregunta de apertura como criterio de decisión.

**Talking point mientras circulas:** "No busquen 'sí, esto sería genial en
tiempo real' — busquen honestamente si el costo se justifica. La respuesta
correcta muchas veces es 'no, batch está bien'."

Cada equipo comparte su conclusión en 1-2 minutos.

---

## Bloque 5 — Cierre (2:20–3:00, 40 min)

**Sin entregable formal hoy** — pero dale tiempo real a la puesta en común de
equipos, es donde más valor se genera en esta sesión.

**Puente a la Sesión 8:**

> "Ya vieron casi todo el panorama técnico del curso. La próxima sesión es
> sobre algo distinto: cómo evaluar el costo real de cualquier propuesta que
> les lleve su equipo — la última pieza antes de armar su propio proyecto
> final."

---

## Notas de costo GCP

- No aplica de forma directa — buen momento para mencionar que streaming real
  (lo que Maestría hace con Pub/Sub Lite) tiene un modelo de costo distinto al
  resto del curso, por si alguien pregunta.
