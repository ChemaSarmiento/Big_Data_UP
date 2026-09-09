# Teoría — Sesión 03: Spark Core avanzado I — Catalyst y shuffle

> Primera de dos sesiones sobre el motor interno de Spark. Hoy: por qué Spark es
> rápido y cómo leer lo que realmente va a ejecutar. La Sesión 4 retoma exactamente
> este mismo par de notebooks para diagnosticar y resolver un caso real de skew.

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
justo el ejercicio de hoy: compara el plan de `02_dataframes.ipynb` (API) contra su
versión en `03_spark_sql.ipynb` (SQL).

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

La Sesión 4 profundiza en qué hacer cuando uno de estos shuffles está desbalanceado
(skew) — hoy el objetivo es solo reconocerlos con certeza en un plan de ejecución.

## 3. Leer planes físicos con `.explain()`

`.explain(mode="formatted")` imprime el plan de ejecución real que Catalyst decidió —
no lo que tú escribiste, sino cómo se va a ejecutar. Tres cosas a buscar:

- **`Exchange`** en el plan = un shuffle. Si ves más `Exchange` de los que esperabas,
  ahí está el costo oculto.
- **`BroadcastHashJoin` vs. `SortMergeJoin`** — el primero es barato (una tabla pequeña
  enviada completa), el segundo implica shuffle de ambos lados.
- **`PushedFilters`** — confirma si un filtro se empujó hasta el origen de datos
  (leyendo menos) o se aplicó después de leer todo.

`recursos/spark/02_dataframes.ipynb` y `03_spark_sql.ipynb` imprimen exactamente esto
antes de ejecutar. El lab de hoy es puramente de lectura y diagnóstico — correr ambos
notebooks, comparar sus planes lado a lado, y contar cuántos `Exchange` aparecen en
cada uno. La Sesión 4 usa esta misma habilidad para resolver un caso donde el plan
revela un problema real.

---

## Referencias

- [Apache Spark — SQL, DataFrames and Datasets Guide (Catalyst)](https://spark.apache.org/docs/latest/sql-programming-guide.html)
- [Databricks — Deep Dive into Spark SQL's Catalyst Optimizer](https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html)
- [Apache Spark — Performance Tuning (shuffle)](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
