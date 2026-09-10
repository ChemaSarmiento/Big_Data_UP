# Facilitación — Sesión 00: Nivelación

> Guion de 3 horas: repaso introductorio, sin evaluación formal. El objetivo es que
> nadie llegue a la Sesión 1 en blanco — no filtrar acceso. El tono aquí importa
> más que en cualquier otra sesión: es la primera impresión del curso para un
> grupo que puede no haber tocado una terminal en su vida.

## Antes de empezar (facilitador)

Ten a la mano ejemplos de la industria del grupo específico (banca, retail,
salud) — el enganche de este track es la relevancia al negocio desde el primer
minuto, no la elegancia técnica.

---

## Bloque 1 — Apertura (0:00–0:15)

**Talking point de apertura, tono cercano, sin jerga:**

> "Nadie en este salón necesita salir de aquí sabiendo programar. El objetivo
> de hoy es que, cuando en las próximas sesiones vean una terminal o una
> consulta SQL en pantalla, no se sientan perdidos — que reconozcan qué está
> pasando, aunque no lo escriban ustedes."

**Pregunta de apertura, para romper el hielo:**

> "¿Alguien aquí ya ha usado una hoja de cálculo con fórmulas complejas, o
> filtros y tablas dinámicas? Eso que hicieron ahí es, conceptualmente, el 80%
> de lo que va a ver hoy — solo con otro nombre."

---

## Bloque 2 — Repaso guiado (0:15–1:00, 45 min)

Sigue `teoria.md` — el tono es de analogía, nunca de sintaxis memorizada.

### Terminal (10 min)
Muestra la tabla de equivalencias (mouse vs. comando) en pantalla y pide que
alguien la lea en voz alta antes de explicarla — que sientan que ya la
entendían intuitivamente.

### Notebooks (10 min)
Demo en vivo en Colab: corre una celda, cambia el orden, corre otra que
depende de una variable que "borraste" — deja que vean el error real, no lo
describas en abstracto.

### SQL (15 min)
Recorre la consulta de ejemplo (`SELECT / WHERE / GROUP BY`) frase por frase,
traduciéndola a español natural cada vez: "de la tabla empleados, quédate con
los activos...".

### GCP (10 min)
Muestra la consola web en vivo — enfatiza que no instalan nada. Pausa
específica en la alerta de presupuesto: "esto es lo único de configuración que
sí les toca hacer antes de la Sesión 1".

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Práctica guiada (1:10–2:30, 80 min)

### SQL de nivelación (50 min)

`recursos/sql-practica/employee_db_queries.sql`, secciones 1-2 — en parejas,
proyectando el resultado de cada consulta antes de que la corran ellos mismos.

**Talking point antes de empezar:** "No van a escribir SQL nuevo hoy — van a
correr consultas ya hechas y decirme, en una frase, qué responde cada una. Eso
es exactamente lo que van a hacer en la Sesión 3, sobre datos reales."

### Setup de GCP en vivo (30 min)

Que cada quien complete, en su propia cuenta, los 3 pasos de
`environment/gcp-setup.md`: cuenta, proyecto, alerta de presupuesto. Circula
por la sala — es la parte donde más se bloquean por primera vez con algo
técnico.

---

## Bloque 5 — Cierre (2:30–3:00, 30 min)

**Autoevaluación informal** — sin nota, sin presión. Una ronda rápida:
"¿qué fue lo más confuso de hoy?" Úsalo para ajustar el ritmo de la Sesión 1,
no para calificar a nadie.

**Puente a la Sesión 1:**

> "La próxima sesión ya no hablamos de herramientas — hablamos de negocio.
> Vamos a ver casos reales de cuándo Big Data sí se justifica, y cuándo es
> gastar de más en algo que un Excel resuelve."

---

## Notas de costo GCP

- El único costo de hoy es cero — nadie corre nada pesado todavía. Aprovecha
  para insistir en la alerta de presupuesto como hábito, antes de que empiecen
  a correr consultas reales en la Sesión 3.
