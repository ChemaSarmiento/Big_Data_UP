# Facilitación — Sesión 00: Prerequisito obligatorio

> Guion de 3 horas: repaso guiado + checkpoint de admisión. A diferencia de las demás
> sesiones, aquí no hay lab de código nuevo — el objetivo es confirmar que el grupo
> puede seguir el ritmo desde la Sesión 1, y nivelar a quien no pueda antes de que
> el curso avance.

## Antes de empezar (facilitador)

Ten listo el quiz + mini-ejercicio de admisión (SQL + Python) desde el inicio —
la sesión termina con el checkpoint, no lo improvises al final.

---

## Bloque 1 — Apertura (0:00–0:15)

**Talking point de apertura:**

> "A diferencia de Especialidad, aquí este módulo sí se evalúa. No es para
> filtrarlos — es porque desde la Sesión 1 no va a haber tiempo de clase para
> depurar un error de sintaxis básico de Python o un JOIN mal escrito. Hoy
> repasamos juntos, y al final hay un checkpoint corto."

**Pregunta de diagnóstico rápido (levanten la mano):**

> "¿Quién ha usado `ssh` para entrar a una máquina remota? ¿Quién ha escrito una
> window function en SQL? ¿Quién ha usado `gcloud` desde la terminal?"

No corrijas a nadie aquí — solo úsalo para calibrar cuánto tiempo dedicar a cada
bloque de teoría.

---

## Bloque 2 — Repaso guiado (0:15–1:00, 45 min)

Sigue `teoria.md` como contenido. Reparte el tiempo según lo que viste en el
diagnóstico de apertura — no des los 4 bloques por igual si el grupo ya domina uno.

### Linux (10 min)
Demo en vivo: `gcloud compute ssh <instancia>`, y desde ahí `ps aux | grep java`
sobre un cluster ya prendido — que vean un proceso real de Spark corriendo, no
una explicación abstracta de "qué es un proceso".

### Python (10 min)
Escribe en vivo una list comprehension y su equivalente en un loop tradicional,
lado a lado. Pregunta: **"¿por qué este patrón se va a repetir constantemente en
Spark?"** (respuesta: `df.select(F.col("x")**2)` es el mismo patrón mental,
distribuido).

### SQL (15 min)
Proyecta una window function ya armada y pide que la lean en voz alta antes de
explicarla tú. El objetivo es diagnosticar quién necesita más práctica antes del
checkpoint, no enseñarla desde cero — para eso está `recursos/sql-practica/`.

### GCP (10 min)
Demo en vivo: `gcloud config set project`, `gcloud compute ssh`. Pregunta:
**"¿qué pasa si alguien crea un cluster sin haber corrido el primer comando?"**
(respuesta: se crea en el proyecto equivocado — el error #1 de esta parte del
curso).

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Práctica dirigida (1:10–2:30, 80 min)

### SQL sobre `test_db` (50 min)

Corre `recursos/sql-practica/employee_db_queries.sql` completo (no solo las
primeras secciones, a diferencia de Especialidad) — en parejas, alternando quién
escribe y quién interpreta el resultado.

**Deberías ver:** todas las secciones corriendo sin error contra la base
`employees` ya cargada. Si alguien no tiene la base cargada, es más rápido que
la clonen ahora (`git clone https://github.com/datacharmer/test_db.git`) que
resolverlo después con el grupo esperando.

### Simulacro de checkpoint (30 min)

Da 2-3 preguntas del mismo estilo del checkpoint real (una de SQL con window
function, una de Python con manejo de excepciones) para que las resuelvan en
parejas — no es el checkpoint en sí, es para que nadie llegue al checkpoint real
sin haber visto el formato antes.

---

## Bloque 5 — Checkpoint de admisión (2:30–3:00, 30 min)

Individual, sin ayuda de compañeros. Quiz corto + mini-ejercicio de SQL y Python.

**Talking point antes de empezar:**

> "Quien no pase esto hoy no se queda fuera del curso — recibe material de
> refuerzo y practica antes de la Sesión 1. Lo que no puede pasar es que alguien
> llegue a la Sesión 3 sin poder leer un `.explain()` porque nunca vio Python con
> soltura."

**Entregable:** checkpoint aprobado + proyecto de GCP configurado (checklist de
`environment/gcp-setup.md`, Sección 5).

---

## Notas de costo GCP

- Esta sesión no requiere cluster propio del estudiante — usa el que tenga el
  facilitador para las demos en vivo. Bórralo o déjalo en pausa según el
  `--max-idle` configurado.
- Buen momento para que cada estudiante configure su alerta de presupuesto
  (`environment/gcp-setup.md`, Sección 1) si no lo ha hecho — antes de que
  empiecen a crear sus propios clusters en la Sesión 1.
