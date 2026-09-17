# Temario — Track Maestría en Ciencia de Datos

> Desglose de temas y subtemas por sesión. Para el contenido desarrollado de cada
> tema ver `sesion-XX/teoria.md`; para cómo enseñarlo, `sesion-XX/facilitacion.md`.
> Resumen ejecutivo del programa (objetivos, evaluación): [`PROGRAMA.md`](PROGRAMA.md).

## Módulo 0 — Sesión 00: Prerequisito obligatorio
1. Linux: terminal avanzada, SSH, procesos, permisos
   - SSH como túnel al cluster remoto
   - Gestión de procesos (`ps`, `kill`) para diagnosticar JVMs colgadas
   - Permisos (`chmod`) en scripts de inicialización de cluster
2. Python: estructuras de datos, comprehensions, excepciones
   - List/dict comprehensions como el mismo patrón mental de `df.select()`
   - Manejo de excepciones en pipelines que procesan datos "sucios"
3. SQL: JOINs complejos, window functions, CTEs
   - `LEFT JOIN` y pérdida silenciosa de datos
   - `RANK() OVER (PARTITION BY...)`
   - CTEs recursivas para jerarquías
4. GCP: proyecto, `gcloud` CLI, IAM básico
   - `gcloud config set project`
   - Roles granulares (`dataproc.editor`, `storage.objectViewer`)
- **Checkpoint de admisión** (evaluado, filtro de nivelación antes de Sesión 1)

## Sesión 01: Arquitecturas distribuidas
1. HDFS: NameNode, DataNode, replicación, bloques
   - Por qué 3 réplicas (tolerancia a fallos, no paranoia)
2. Teorema CAP
   - Por qué la tolerancia a Particiones no es opcional
   - La decisión real: Consistencia vs. Disponibilidad
3. MapReduce: map, shuffle, reduce
   - Las tres etapas, con ejemplo de word count
4. Por qué Spark reemplazó a MapReduce puro
   - In-memory (RDDs) vs. disco en cada etapa
   - DAG scheduler vs. secuencia rígida de pasos

## Sesión 02: SQL distribuido avanzado
1. Motor de ejecución de BigQuery
   - Almacenamiento columnar, separación de storage/cómputo, arquitectura en árbol (Dremel)
2. Particionamiento y clustering
   - Partition pruning, clustering hasta 4 columnas
3. Costo: bytes escaneados vs. slots reservados
   - On-demand vs. capacity-based
4. Window functions anidadas y CTEs recursivos
   - Cuándo una window function necesita una subconsulta/CTE

## Sesión 03: Spark Core avanzado I — Catalyst y shuffle
1. Catalyst optimizer y Tungsten
   - Column pruning, predicate pushdown, reordenamiento de joins
   - Whole-stage code generation
2. Tipos de shuffle
   - Por agregación, por join, por repartición explícita
3. Leer planes físicos con `.explain()`
   - `Exchange`, `BroadcastHashJoin` vs `SortMergeJoin`, `PushedFilters`

## Sesión 04: Spark Core avanzado II — Skew y diagnóstico
1. Qué es skew, con un caso real (moneda dominante en `bank_transactions.csv`)
2. Cómo se ve un skew severo en el plan
   - Señales en el Spark UI (duración por task)
3. Tres estrategias de mitigación
   - Salting (con implementación en dos etapas)
   - Broadcast join
   - AQE (Adaptive Query Execution)
4. Por qué AQE no siempre es suficiente
   - Límites: skew en la primera lectura, umbrales de detección

## Sesión 05: Ingeniería de features a escala
1. Spark MLlib: `Pipeline`, `Transformer`, `Estimator`
   - La diferencia entre "transforma" y "aprende y transforma"
2. Encoding y escalado a escala
   - `StringIndexer`/`OneHotEncoder`, `StandardScaler`
   - El error de fuga de información (fit sobre todo el dataset)
3. Feature stores: qué problema resuelven
   - Training-serving skew

## Sesión 06: Entrenamiento de modelos distribuido
1. Algoritmos de MLlib y su paralelización
   - Regresión (gradiente distribuido), árboles (level-wise), GBT (secuencial)
2. Tuning de hiperparámetros con `CrossValidator`
   - El costo real: combinaciones × folds
3. Cuándo MLlib no alcanza: deep learning
   - Vertex AI Training, Horovod (panorama)

## Sesión 07: Lakehouse I — formatos y medallion
1. Parquet vs. ORC vs. Avro
2. Arquitectura medallion (bronze/silver/gold)
3. Por qué Parquet plano no es un lakehouse transaccional
   - Los tres problemas: corregir filas, ver el pasado, evolucionar esquema

## Sesión 08: Lakehouse II — transacciones y versionado
1. `MERGE INTO`: actualizar sin reescribir la tabla completa
2. Time travel: consultar un snapshot anterior
3. Evolución de esquema sin romper lectores existentes
4. Versionado de datasets y de modelos
   - Por qué es distinto a versionar código

## Sesión 09: Streaming I — fundamentos y setup
1. Windowing y watermarks
   - Cuánta tardanza tolerar antes de cerrar una ventana
2. Exactly-once vs. at-least-once
   - Exactly-once en el cálculo ≠ sin duplicados en el broker
3. Setup de Pub/Sub Lite
   - Por qué Lite y no Pub/Sub estándar (único conector oficial de Spark)

## Sesión 10: Streaming II — inferencia en tiempo real
1. Dos patrones de scoring en tiempo real
   - Modelo cargado en el stream vs. endpoint externo
2. Feature freshness
   - Timestamp del evento vs. momento de procesamiento
3. Lo que cambia respecto al lab de la Sesión 9
   - Mismo esqueleto + modelo agregado

## Sesión 11: Model serving y monitoreo
1. Patrones de serving
   - Batch, online (síncrono), streaming
   - Por qué Spark local, no el cluster, para el endpoint
2. Monitoreo de drift
   - Drift de datos vs. drift de modelo (concept drift)
   - Population Stability Index (PSI) y sus umbrales

## Sesión 12: MLOps con Airflow
1. Orquestación con Airflow
   - DAGs, dependencias, reintentos, decisión condicional (`BranchPythonOperator`)
2. Reentrenamiento programado vs. por triggers de drift
3. Dónde correr esto
   - Airflow standalone vs. Cloud Composer

## Sesión 13: Gobernanza, seguridad y capstone
1. IAM a nivel dataset/tabla
   - Mínimo privilegio, seguridad a nivel columna/fila
2. Data Catalog y linaje
   - Por qué escala con el éxito del programa de datos
3. Cumplimiento en contextos regulados
   - Explicabilidad, trazabilidad, retención/borrado
4. FinOps de un pipeline de ML a escala
   - Costo por etapa, costo de reentrenar vs. costo de degradación
5. El capstone técnico (presentación, máx. 15 min c/u)

---

## Mapa de progresión (para ver el hilo completo)

| Sesión | Construye sobre | Prepara para |
|---|---|---|
| 00 | — | Todo el curso (checkpoint obligatorio) |
| 01 | 00 | 03-04 (Spark Core parte de aquí) |
| 02 | 00 | Disciplina de costo usada en 08, 13 |
| 03 | 01 | 04 (mismos notebooks, ahora con skew real) |
| 04 | 03 | — |
| 05 | 01, 03-04 | 06, 09-12 (el `PipelineModel` se reusa en 4 sesiones más) |
| 06 | 05 | 08 (versionado), 10-12 (el modelo entrenado aquí se sirve/monitorea) |
| 07 | 05-06 (mismo dataset) | 08 (misma tabla) |
| 08 | 07 | 13 (linaje/versionado se menciona en gobernanza) |
| 09 | 05 (el `PipelineModel`) | 10 (mismo pipeline de streaming) |
| 10 | 09, 05-06 | 11 (los scores alimentan el monitoreo de drift) |
| 11 | 06, 10 | 12 (el DAG llama a este endpoint) |
| 12 | 05-11 (orquesta todo el ciclo) | 13 (capstone) |
| 13 | Todo el curso | — |
