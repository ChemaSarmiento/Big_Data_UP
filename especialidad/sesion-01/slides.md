---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
  table { font-size: 0.85em; }
---

# Sesión 01
## Big Data para decisiones de negocio

Especialidad — Big Data

---

## Un banco pregunta dos cosas muy distintas

**"¿Cuántas transacciones tuvo cada sucursal el mes pasado?"**
→ Una consulta SQL de toda la vida. No necesita Big Data.

**"¿Qué transacción, entre millones, es fraude *ahora mismo*?"**
→ <span class="accent">Ahí sí se justifica Big Data</span> — volumen y velocidad juntos, algo que ninguna base tradicional sin optimizar responde a tiempo.

---

## Las 5 V's — el marco para distinguir uno de otro

| V | Pregunta | Ejemplo |
|---|---|---|
| Volumen | ¿GB, TB, o PB? | Millones de transacciones diarias |
| Velocidad | ¿Qué tan rápido hay que responder? | Fraude en el momento vs. reporte mensual |
| Variedad | ¿Un formato, o mezclado? | Texto, imágenes, logs |
| Veracidad | ¿Qué tan sucio es el dato? | Sensores que fallan, duplicados |
| **Valor** | ¿Vale la pena el esfuerzo? | La V que más se olvida |

---

## La V que más se olvida: Valor

Procesar 20TB de logs que nadie va a usar para nada **es** Big Data — mal
aplicado.

<div class="box">
La pregunta nunca es "¿tenemos muchos datos?" — es: <b>¿el problema requiere
procesar todo eso junto, rápido, de formas que una hoja de cálculo no puede?</b>
</div>

---

## El error más caro: sobre-ingeniería

Montar un cluster para un problema que un `SELECT` resuelve en 3 segundos.

El costo no es solo dinero de infraestructura — es tiempo de un equipo técnico
construyendo algo que nadie necesitaba, cuando pudieron resolver un problema
real con ese tiempo.

---

## El mapa del ecosistema

| Categoría | Resuelve | Cuándo lo ves en el curso |
|---|---|---|
| Storage | Dónde viven los datos | Toda sesión con datos |
| Cómputo distribuido | Procesar en paralelo | Sesión 2, 4 |
| Bases analíticas | Responder SQL a escala | Sesión 3 |
| Streaming | Datos que llegan sin parar | Sesión 7 |
| Orquestación | Coordinar pasos de un pipeline | Sesión 5, 6 |

No necesitas memorizar esto — necesitas reconocer el nombre cuando alguien lo
mencione en una junta.

---

# Actividad

## Análisis de casos reales

En equipos: 2-3 casos reales. Cada equipo decide — **¿inversión justificada, o
sobre-ingeniería?** — y defiende su respuesta con una frase.

<div class="box">
No hay una sola respuesta correcta — lo que importa es el razonamiento para
llegar a ella.
</div>

---

## Entregable de hoy

Ficha de **una página**: un caso propio de tu industria — ¿aplica Big Data o
no, y por qué?

No tiene que ser perfecto — es el primer borrador de cómo vas a pensar este
tipo de decisiones el resto del curso.

---

# → Sesión 02

Cómo funciona por dentro (sin código pesado)
