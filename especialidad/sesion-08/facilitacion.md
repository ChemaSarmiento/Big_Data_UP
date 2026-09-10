# Facilitación — Sesión 08: Costos, gobernanza y cómo evaluar un proyecto de datos

> Guion de 3 horas: taller práctico con framework de decisión. Esta es la sesión
> más directamente aplicable al rol del grupo — el taller final debe sentirse
> como algo que van a usar la próxima semana en su trabajo, no como un ejercicio
> académico.

## Antes de empezar (facilitador)

Prepara un caso ficticio de propuesta técnica (puede ser inventado, con
suficiente detalle de arquitectura/costo/riesgo para que el framework tenga
algo real que evaluar).

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Hoy no construyen nada — construyen la capacidad de hacer las preguntas
> correctas cuando su equipo técnico les presente una propuesta. Es, quizás, la
> habilidad más directamente útil de todo el curso para su rol."

**Pregunta de apertura:**

> "¿Alguna vez han aprobado (o visto aprobar) un proyecto de tecnología sin
> entender bien cómo se iba a cobrar? ¿Qué pasó después?"

---

## Bloque 2 — Cómo se cobra la nube (0:15–0:50, 35 min)

Recorre los tres modelos (por uso, por hora, por almacenamiento) con ejemplos
concretos de lo que ya vivieron en el curso: "el cluster que crearon en
Maestría cobra por hora mientras está prendido — por eso insistimos tanto en
apagarlo".

**Pregunta:** "¿cuál de los tres modelos les parece más fácil de que se salga
de control sin que nadie lo note?" (por hora — algo prendido "por si acaso" es
el error #1).

---

## Bloque 3 — Break (0:50–1:00, 10 min)

---

## Bloque 4 — Las cinco preguntas (1:00–1:40, 40 min)

Recorre cada una de las 5 preguntas de `teoria.md` con un ejemplo real
(idealmente del caso ficticio que vas a usar en el taller). Pide que, en
parejas, formulen una sexta pregunta propia antes de seguir — que no se queden
solo con la lista dada.

---

## Bloque 5 — El framework de 4 dimensiones (1:40–2:10, 30 min)

Arquitectura, Costo, Riesgo, Tiempo — recorre cada una con el caso de
`recursos/mariadb/README.md` (antes/después de seguridad) como ejemplo
concreto de una propuesta que fallaba en la dimensión de riesgo aunque fuera
"barata y rápida".

**Talking point central de la sesión:**

> "'Barato y rápido' y 'bien gobernado' no siempre son lo mismo — y ninguna de
> las cuatro preguntas del framework se salta la de riesgo solo porque el
> costo se ve bien."

---

## Bloque 6 — Taller: aplicar el framework (2:10–2:50, 40 min)

En equipos, aplicar las 4 dimensiones al caso ficticio preparado. Cada equipo
debe producir una recomendación clara: ¿aprobarían la propuesta tal cual, con
condiciones, o la rechazarían?

**Talking point mientras circulas:** "No busco que todos lleguen a la misma
conclusión — busco que cada equipo pueda defender la suya con las 4
dimensiones, no con una opinión general."

---

## Bloque 7 — Cierre (2:50–3:00, 10 min)

**Entregable de hoy:** framework aplicado al caso ficticio.

**Puente a la Sesión 9:**

> "La próxima sesión es la última — presentan su propio proyecto final. Todo
> lo que vieron desde la Sesión 1 (cuándo se justifica Big Data, cómo se ve un
> pipeline real, cómo evaluar costo y riesgo) es exactamente lo que van a
> aplicar ahí."

---

## Notas de costo GCP

- Buen cierre práctico: pide que cada quien revise su propio consumo de
  crédito hasta ahora (`Billing → Reports`) — conecta directo con el contenido
  de hoy, no como tarea aparte.
