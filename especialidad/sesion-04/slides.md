---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
---

# Sesión 04
## Introducción a Spark

Especialidad — Big Data

---

## ¿Qué hace Spark que SQL no hace?

BigQuery (Sesión 3) es excelente para filtros, agregaciones, joins. Pero hay
tareas que SQL no cubre bien:

- **Lógica de negocio compleja** que no se expresa naturalmente como una consulta
- **Machine learning** — entrenar un modelo sobre datos que no caben en una máquina
- **Combinar fuentes muy distintas** (CSV, base de datos, API) en un mismo flujo

<div class="box">
Spark: más flexible que SQL, a cambio de requerir más líneas para lo mismo que
un <code>SELECT</code> resuelve en una línea.
</div>

---

## Tres palabras cubren todo lo de hoy

- **DataFrame** — una tabla, como en BigQuery o Excel: filas y columnas con nombre
- **Transformación** — describe qué quieres hacer (`.filter()`, `.groupBy()`) —
  **no se ejecuta todavía**
- **Acción** — la que dispara la ejecución real (`.show()`, `.count()`)

<div class="box">
Hasta que no llamas una acción, Spark no ha tocado ni un solo dato — solo
planeó. Por eso un notebook "no hace nada" durante varias celdas y de repente
tarda al llegar a un <code>.show()</code>.
</div>

---

## Por qué no vemos shuffle/optimización hoy

Eso es un track completo en Maestría — un semestre entero de profundidad
técnica sobre cómo Spark mueve datos entre máquinas.

Para este track, con reconocer la palabra "shuffle" como *"mover datos entre
máquinas, y que cuesta"*, ya puedes participar en una conversación técnica sin
bloquearte.

---

# Lab guiado
## Notebook "fill-in-the-blanks" sobre PROFECO

Versión simplificada de `02_dataframes.ipynb` — sin `.explain()` ni el
guardado en Parquet particionado (eso es Maestría). Solo lectura + `filter` +
`groupBy` + `show()`.

---

## Completa el pipeline

```python
df_filtrado = df.filter(F.col("categoria") == ___)
resumen = df_filtrado.groupBy(___).count()
resumen.show()
```

En parejas, completando los espacios en blanco — se leen y se corren, no se
escribe desde cero.

<div class="box">
<b>Error común:</b> <code>.show()</code> no imprime nada → revisa mayúsculas/minúsculas del valor filtrado, no un bug de Spark.
</div>

---

## Entregable de hoy

Notebook completado.

Cada pareja explica a otra pareja, en una frase, qué hace su notebook — es más
valioso que confirmarlo tú mismo.

---

# → Sesión 05

Cómo se ve un pipeline de datos real
