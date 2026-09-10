# Facilitación — Sesión 03: Spark Core avanzado I — Catalyst y shuffle

> Guion de 3 horas: talking points + lab guiado. Primera de dos sesiones sobre el
> motor interno de Spark — hoy es puramente diagnóstico (leer planes), sin resolver
> nada todavía. La Sesión 4 resuelve el caso real con este mismo par de notebooks.

## Antes de empezar (facilitador)

```bash
gcloud dataproc clusters list --region=us-central1
```

Revisa clusters huérfanos antes de que llegue el grupo — van 2 sesiones previas
creando clusters (S1).

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Hasta ahora han tratado a Spark como una caja negra que 'simplemente
> funciona'. Hoy la abrimos. Cuando escriben `.filter()` o una consulta SQL, eso
> no se ejecuta tal cual lo escribieron — pasa por un optimizador que puede
> reescribir su plan completo antes de tocar un solo dato."

**Pregunta de apertura:**

> "Si escriben el mismo cálculo con la DataFrame API y con SQL puro, ¿esperan
> que Spark lo ejecute distinto, o igual? ¿Por qué?"

(No resuelvas todavía — es el gancho para todo el bloque de teoría.)

**Ejemplo de actualidad:**

> "Databricks reporta que gran parte del trabajo de optimización de costos en
> producción no es reescribir código — es entender qué plan generó Catalyst y
> ajustar de ahí. Leer un plan de ejecución es una habilidad que se paga sola en
> cualquier equipo de datos serio."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Catalyst y Tungsten (15 min)

Dibuja el diagrama de 3 pasos (código → Catalyst → Tungsten → resultado).
Pregunta: **"¿cuáles de estas optimizaciones creen que Catalyst hace solo:
eliminar columnas sin usar, reordenar joins, o ambas?"** (respuesta: ambas, más
predicate pushdown).

### Tipos de shuffle (15 min)

Tabla en el pizarrón: agregación, join, repartición explícita. Pregunta:
**"¿cuál de los tres creen que es más caro, y por qué?"** (join — mueve datos
de ambos lados).

### `.explain()`: qué buscar (15 min)

Proyecta un plan real (correr una celda de `02_dataframes.ipynb` en vivo) y
recorre juntos: dónde está el `Exchange`, si hay `BroadcastHashJoin` o
`SortMergeJoin`, si los filtros se empujaron (`PushedFilters`).

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Correr ambos notebooks (30 min)

```python
# 02_dataframes.ipynb
df.filter(...).groupBy(...).explain(mode="formatted")
```

```python
# 03_spark_sql.ipynb — la MISMA pregunta, en SQL
spark.sql("SELECT ... GROUP BY ...").explain(mode="formatted")
```

**Deberías ver:** dos planes con la misma estructura de fondo (mismo número de
`Exchange`, mismo tipo de join). Si se ven muy distintos, revisar que ambas
consultas realmente pregunten lo mismo — es fácil que una tenga un filtro de
más o de menos al copiar/pegar.

### Paso 2 — Contar shuffles en cada plan (30 min)

En parejas: cada quien cuenta los `Exchange` del plan que le tocó y explica en
voz alta qué operación lo generó, antes de comparar con su pareja.

**Pregunta de verificación:** "¿los dos planes tienen el mismo número de
`Exchange`? Si no, ¿por qué creen que difiere?"

### Paso 3 — Capturar evidencia para el entregable (30 min)

Cada pareja arma su entregable: capturas de ambos planes + su lista de shuffles
identificados con la operación que los originó.

---

## Bloque 5 — Cierre (2:40–2:55, 15 min)

**Entregable de hoy:** capturas de los dos planes comparados + lista de shuffles.

**Puente a la Sesión 4, dilo explícito:**

> "Hoy solo diagnosticamos. La próxima sesión les voy a dar un caso donde el
> plan revela un problema real — una clave que concentra el 80% del trabajo — y
> vamos a resolverlo con las herramientas que hoy solo mencionamos: salting,
> broadcast join, AQE."

---

## Notas de costo GCP

- Si el cluster de la Sesión 1 sigue vivo y dentro de su `--max-age`, reutilízalo
  — no hace falta crear uno nuevo solo para leer planes de ejecución sobre
  datasets pequeños/medianos.
