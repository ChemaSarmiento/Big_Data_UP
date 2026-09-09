# Teoría — Sesión 03: Spark Core avanzado

> Hasta ahora Spark ha sido "la herramienta que procesa rápido". Hoy se abre la caja:
> por qué es rápido, qué puede salir mal a escala, y cómo diagnosticarlo con evidencia
> en vez de a prueba y error.

## 1. Catalyst optimizer y Tungsten

Cuando escribes una transformación en Spark (`.filter()`, `.groupBy()`, una consulta
`spark.sql(...)`), no se ejecuta tal cual la escribiste — pasa por un optimizador antes.

- **Catalyst** es el optimizador de consultas de Spark SQL. Toma tu código (DataFrame
  API o SQL, es indistinto — ambos generan el mismo plan lógico) y aplica reglas de
  reescritura: elimina columnas que nunca se usan (*column pruning*), empuja filtros
  lo más temprano posible en el plan (*predicate pushdown*, para leer menos datos desde
  el origen), y reordena joins si eso reduce el trabajo total. El resultado es un plan
  físico optimizado, no una traducción literal de tu código.
- **Tungsten** es el motor de ejecución de bajo nivel: gestiona memoria fuera del heap
  de la JVM (evitando el costo del garbage collector de Java en datos masivos) y genera
  bytecode Java especializado para cada consulta en tiempo de ejecución (*whole-stage
  code generation*), en vez de interpretar operaciones genéricas una por una.

Juntos explican por qué el mismo cálculo escrito con la DataFrame API o con SQL puro
produce planes de ejecución equivalentes — ambos pasan por Catalyst. Verificarlo es
justo el ejercicio de `recursos/spark/03_spark_sql.ipynb`: compara el plan de
`02_dataframes.ipynb` (API) contra su versión en SQL.

## 2. Tipos de shuffle

Un shuffle ocurre cuando Spark necesita mover datos entre particiones a través de la
red — típicamente porque una operación (`groupBy`, `join`, `distinct`) necesita juntar
filas que originalmente estaban en máquinas distintas. Es la operación más cara de
Spark, y distinguir cuándo ocurre es la base del diagnóstico de performance:

- **Shuffle por agregación** (`groupBy`, `reduceByKey`): los datos se redistribuyen
  para que todas las filas con la misma clave terminen en la misma partición.
- **Shuffle por join** (`join` sin broadcast): ambas tablas se redistribuyen por la
  clave de join — el más costoso, porque mueve datos de *ambos* lados.
- **Shuffle por repartición explícita** (`.repartition()`, `.coalesce()` con
  `shuffle=True`): cuando tú mismo pides cambiar el número de particiones.

## 3. Skew: causas y mitigación

**Skew** (desbalance) ocurre cuando una clave concentra muchas más filas que las
demás — el trabajador que procesa esa clave se convierte en cuello de botella mientras
el resto del cluster espera ocioso. Es la causa #1 de "mi job tarda 10x más de lo que
debería" en producción.

| Estrategia | Cómo funciona | Cuándo usarla |
|---|---|---|
| **Salting** | Se agrega un sufijo aleatorio a la clave sesgada antes del shuffle (ej. `"MXN"` → `"MXN_0"`, `"MXN_1"`, ...), repartiendo artificialmente esa clave entre más particiones, y se agrega en dos etapas | Cuando una sola clave (ej. una moneda dominante) concentra la mayoría de las filas |
| **Broadcast join** | Si una de las dos tablas del join es pequeña (cabe en memoria de cada worker), se envía una copia completa a cada nodo en vez de hacer shuffle de ambas | Join entre una tabla grande y una tabla de catálogo/dimensión pequeña — el patrón más común en la práctica |
| **AQE** (Adaptive Query Execution) | Spark re-optimiza el plan de ejecución *durante* la corrida, con estadísticas reales (no estimadas) — puede convertir un shuffle join en broadcast join sobre la marcha, o repartir automáticamente particiones desbalanceadas | Activado por default desde Spark 3.x (`spark.sql.adaptive.enabled`); reduce la necesidad de salting manual en muchos casos |

## 4. Leer planes físicos con `.explain()`

`.explain(mode="formatted")` imprime el plan de ejecución real que Catalyst decidió —
no lo que tú escribiste, sino cómo se va a ejecutar. Tres cosas a buscar:

- **`Exchange`** en el plan = un shuffle. Si ves más `Exchange` de los que esperabas,
  ahí está el costo oculto.
- **`BroadcastHashJoin` vs. `SortMergeJoin`** — el primero es barato (una tabla pequeña
  enviada completa), el segundo implica shuffle de ambos lados.
- **`PushedFilters`** — confirma si un filtro se empujó hasta el origen de datos
  (leyendo menos) o se aplicó después de leer todo.

`recursos/spark/02_dataframes.ipynb` y `03_spark_sql.ipynb` imprimen exactamente esto
antes de ejecutar — es la herramienta de diagnóstico central del lab de hoy: correr un
job con skew, leer su plan, aplicar salting o broadcast join, y comparar el plan
"antes" contra el "después".

---

## Referencias

- [Apache Spark — SQL, DataFrames and Datasets Guide (Catalyst)](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Databricks — Deep Dive into Spark SQL's Catalyst Optimizer](https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html)
- [Apache Spark — Performance Tuning (shuffle, AQE)](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
- [Databricks — Handling Data Skew in Apache Spark](https://www.databricks.com/blog/2020/12/16/managing-data-skew-in-apache-spark.html)
