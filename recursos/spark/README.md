# Spark — de lo básico a pipelines de modelado

Mejora sobre `spark_notebooks/` del repo original. El problema del material anterior no
era el contenido (la progresión "básico → pipeline de modelado" ya era la correcta) sino
que estaba en notebooks sueltos sin una secuencia explícita. Aquí queda numerado y cada
script tiene un objetivo de aprendizaje único — para que un instructor pueda tomar
exactamente el archivo que corresponde a la sesión que está dando.

| Archivo | Sesión sugerida | Qué enseña |
|---|---|---|
| `01_rdd_basico.py` | Maestría S1 / Especialidad S4 | RDDs, transformaciones vs. acciones, evaluación perezosa |
| `02_dataframes.py` | Maestría S3 | DataFrame API, lectura de Parquet/CSV, `explain()` para leer el plan físico |
| `03_spark_sql.py` | Maestría S2 / S3 | Spark SQL, registrar vistas temporales, comparación con la DataFrame API |
| `04_pipeline_ml.py` | Maestría S4-S5 | `Pipeline` de Spark MLlib: imputación → encoding → escalado → modelo |

Cada script corre igual en un cluster de Managed Service for Apache Spark (Dataproc) o en modo local (`spark-submit --master local[*] archivo.py`),
para que se pueda probar antes de gastar crédito de GCP en un cluster real.

## Dataset de referencia

Todos los scripts asumen el dataset de transacciones sintéticas de `../datasets/` (ver
`recursos/datasets/README.md`) — así el mismo dataset atraviesa las 4 sesiones y el
capstone se siente como una continuación, no como un tema nuevo cada vez.
