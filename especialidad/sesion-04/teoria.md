# Teoría — Sesión 04: Introducción a Spark

> No vas a "aprender Spark" hoy — vas a entender qué problema resuelve que SQL no
> resuelve, y a reconocer 3 palabras (DataFrame, transformación, acción) cuando las
> veas en un notebook. Eso es suficiente para completar el lab guiado.

## 1. Qué problema resuelve Spark que SQL no resuelve

BigQuery (Sesión 3) es excelente para preguntas que se expresan bien en SQL: filtros,
agregaciones, joins. Pero hay tareas que SQL no cubre bien:

- **Lógica de negocio compleja** que no se expresa naturalmente como una consulta —
  por ejemplo, un proceso de limpieza de datos con muchas reglas condicionadas entre sí.
- **Machine learning** — entrenar un modelo sobre datos que no caben en la memoria de
  una sola máquina (esto es justo lo que Maestría hace en sus Sesiones 4-5).
- **Combinar fuentes muy distintas** en un mismo flujo — un archivo CSV, una tabla de
  base de datos, y una llamada a una API, todo en el mismo pipeline.

Spark es un motor de propósito general para procesar datos distribuidos con código
(Python, en este curso) — más flexible que SQL, a cambio de requerir más líneas para
lo mismo que un `SELECT` resuelve en una línea.

## 2. Vocabulario mínimo

Tres palabras cubren todo lo que vas a ver en el notebook de hoy:

- **DataFrame** — una tabla, igual que una tabla de BigQuery o una hoja de cálculo:
  filas y columnas con nombre. La diferencia es que un DataFrame de Spark puede estar
  repartido entre varias máquinas sin que tú tengas que pensar en eso.
- **Transformación** — una operación que describe *qué* quieres hacer con el
  DataFrame (`.filter(...)`, `.groupBy(...)`) pero que **no se ejecuta todavía**. Spark
  solo va anotando "esto es lo que me pediste hacer".
- **Acción** — la operación que sí dispara la ejecución real (`.show()`, `.count()`).
  Hasta que no llamas una acción, Spark no ha tocado ni un solo dato — solo planeó.

Esta separación (transformación planea, acción ejecuta) es la razón por la que a veces
un notebook "no hace nada" durante varias celdas y de repente tarda al llegar a un
`.show()` — no es que esa celda sea lenta, es que ahí se ejecutó todo el plan acumulado.

## 3. Por qué no entramos a shuffle/optimización aquí

Esos temas (qué pasa "por dentro" cuando Spark mueve datos entre máquinas, cómo
diagnosticar cuellos de botella) son el corazón de la Sesión 3 de Maestría — un track
completo de optimización que no tiene sentido cubrir a nivel ejecutivo. Para este
track, con saber que existe la palabra "shuffle" y que es una operación costosa basta
para participar en una conversación técnica sin bloquearte.

---

## Referencias

- [Apache Spark — Quick Start (docs oficiales, versión corta)](https://spark.apache.org/docs/latest/quick-start.html)
- [Databricks — What is a DataFrame?](https://www.databricks.com/glossary/what-are-dataframes)
