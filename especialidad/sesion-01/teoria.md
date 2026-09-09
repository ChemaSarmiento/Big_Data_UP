# Teoría — Sesión 01: Big Data para decisiones de negocio

> Objetivo de esta sesión: salir con vocabulario para participar en una conversación
> sobre Big Data sin que te la "vendan" — ni de más (un consultor que quiere venderte
> un cluster para un problema de Excel) ni de menos (un equipo técnico que subestima
> un problema real de escala).

## 1. Las 5 V's

Es el marco más citado para describir cuándo un problema de datos deja de ser "una
base de datos grande" y se vuelve un problema de Big Data de verdad:

| V | Qué significa | Ejemplo de industria |
|---|---|---|
| **Volumen** | Cuántos datos — no en MB, en GB/TB/PB | Un banco genera millones de transacciones al día; una sola tabla puede pesar cientos de GB al mes |
| **Velocidad** | Qué tan rápido llegan y qué tan rápido hay que responder | Detectar fraude *mientras* ocurre la transacción, no al día siguiente en un reporte |
| **Variedad** | Qué tan distintos son los formatos | Texto libre de redes sociales, imágenes de radiografías, logs de sensores — no todo cabe en una tabla con columnas fijas |
| **Veracidad** | Qué tan confiable es el dato | Sensores que fallan, formularios mal llenados, duplicados — el dato "sucio" es la norma, no la excepción, a esta escala |
| **Valor** | Si vale la pena el esfuerzo | La V que más se olvida: procesar 20TB de logs que nadie va a usar para nada es Big Data mal aplicado |

**Ejemplo de salud:** un hospital que analiza expedientes de 500 pacientes en Excel no
tiene un problema de Big Data (Volumen bajo). Una red de hospitales que cruza millones
de expedientes con datos genómicos y de sensores en tiempo real para detectar brotes
tempranos — ahí sí aplican las 5 V's a la vez.

## 2. Cuándo sí y cuándo no

La pregunta correcta nunca es "¿tenemos muchos datos?" — es **"¿el problema que quiero
resolver requiere procesar todo eso junto, rápido, o de formas que una hoja de cálculo
no puede hacer?"**

**No necesita Big Data** (aunque suene impresionante):
- "¿Cuántas ventas tuvo cada sucursal el mes pasado?" — es una suma con filtro. Una
  base de datos tradicional (MySQL, PostgreSQL) o incluso Excel lo resuelve en segundos.
- Un reporte que se genera una vez al mes, sobre datos que caben en la memoria de una
  laptop (unos cuantos GB).

**Sí justifica Big Data:**
- "¿Qué transacciones de las últimas 24 horas, entre millones, tienen un patrón de
  fraude?" — el volumen y la velocidad hacen que ninguna hoja de cálculo, ni siquiera
  una base de datos tradicional sin optimizar, responda esto a tiempo.
- Cruzar datos de fuentes muy distintas (texto, imágenes, series de tiempo) que no
  caben en una sola tabla relacional.

El error más caro no es "usar Big Data quizás de más" — es **sobre-ingeniería**:
montar un cluster de Spark para un problema que un `SELECT` con `GROUP BY` resuelve
en 3 segundos. Ver `recursos/etl-cripto/FLUJO.md` para un ejemplo real de un pipeline
que sí necesita varias etapas — y comparar mentalmente contra "esto podría haber sido
una sola consulta SQL" es un buen ejercicio de esta sesión.

## 3. El ecosistema, a nivel de mapa

No necesitas saber operar cada pieza — sí necesitas reconocer el nombre cuando lo oigas
en una junta:

| Categoría | Qué resuelve | Ejemplos que vas a escuchar en el curso |
|---|---|---|
| **Storage** (almacenamiento) | Dónde viven los datos crudos | Cloud Storage, HDFS |
| **Cómputo distribuido** | Procesar datos repartidos entre varias máquinas a la vez | Spark, (antes) Hadoop MapReduce |
| **Bases analíticas** | Responder preguntas SQL sobre datos masivos | BigQuery |
| **Streaming** | Procesar datos que llegan continuamente, no en lote | Pub/Sub |
| **Orquestación** | Coordinar que cada paso de un pipeline corra en el orden correcto | Airflow |

Piensa en esto como el mapa de una ciudad, no como un manual de manejo: en las
siguientes sesiones vas a visitar cada zona (Sesión 3: bases analíticas, Sesión 4:
cómputo distribuido, Sesión 7: streaming), pero hoy solo necesitas el mapa completo
para no perderte.

---

## Referencias

- [NIST Big Data Interoperability Framework — definición oficial de las V's](https://www.nist.gov/publications/nist-big-data-interoperability-framework-volume-1-definitions)
- [Google Cloud — panorama de servicios de datos](https://cloud.google.com/products/data-analytics)
- `recursos/etl-cripto/FLUJO.md` — ejemplo real de un pipeline de varias etapas, para contrastar contra "esto podría ser una sola consulta"
