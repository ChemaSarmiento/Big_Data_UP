# Teoría — Sesión 06: Data Lakes / Lakehouse

> El salto de esta sesión: un data lake bien organizado (medallion, formato columnar)
> sigue siendo un montón de archivos — sin transacciones. Un lakehouse le agrega
> garantías que hasta hace pocos años solo existían en bases de datos tradicionales.

## 1. Parquet vs. ORC vs. Avro

Tres formatos de archivo columnar/binario que compiten por el mismo espacio, con
diferencias de diseño que importan según el caso de uso:

| Formato | Diseño | Mejor para |
|---|---|---|
| **Parquet** | Columnar, con metadata de esquema embebida, compresión por columna | Analítica (leer pocas columnas de muchas) — el estándar de facto en el ecosistema Spark/BigQuery |
| **ORC** | Columnar, optimizado originalmente para Hive, con índices integrados a nivel de bloque | Cargas de trabajo muy pesadas en consultas con predicados (`WHERE`) sobre Hive/Hadoop clásico |
| **Avro** | Orientado a **filas**, no a columnas, con esquema evolutivo integrado (el esquema viaja con cada archivo) | Streaming e ingesta — cuando escribes fila por fila conforme llega, no en lote |

La elección de Parquet en este curso (`recursos/spark/04_pipeline_ml.ipynb`, el
lakehouse de esta sesión) no es arbitraria: como el patrón de acceso del curso es
"escribir en lote, leer analíticamente después", columnar gana. Avro tendría más
sentido si el patrón fuera "escribir evento por evento" — justo lo que sí ocurre en
la Sesión 7 (streaming), aunque ahí seguimos escribiendo el resultado a Parquet por
consistencia con el resto del pipeline.

## 2. Arquitectura medallion (bronze/silver/gold)

Mismo patrón conceptual que Especialidad (ver su `teoria.md` de esta sesión para la
analogía), pero aquí con la implementación real: `recursos/etl-tipo-cambio/` (bronze
en `data/raw/`, silver en `data/processed/`) y `recursos/spark/05_data_cleansing.ipynb`
(la misma idea, a escala real de 15GB, convirtiendo `quien_es_quien.csv` — sin
encabezados, con `\N` como nulo no estándar — en una capa silver tipada). El detalle
técnico que Especialidad no necesita pero Maestría sí: cada capa normalmente cambia de
formato además de calidad — bronze puede ser CSV/JSON crudo, silver y gold casi
siempre son Parquet (o, como en esta sesión, Iceberg).

## 3. Formatos de tabla transaccionales: Iceberg y Delta Lake

Parquet resuelve el formato del archivo. No resuelve la **tabla** — un conjunto de
archivos Parquet en una carpeta no tiene transacciones, ni forma de saber qué versión
de la tabla estás leyendo si alguien la está escribiendo al mismo tiempo. Ahí entran
los formatos de tabla transaccionales:

- **Apache Iceberg** (originado en Netflix) y **Delta Lake** (originado en Databricks)
  resuelven el mismo problema: agregar una capa de metadata transaccional sobre
  archivos Parquet, dando ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad) —
  las mismas garantías que una base de datos relacional, pero sobre un data lake.
- Concretamente, ambos permiten: **`MERGE INTO`** (actualizar filas específicas sin
  reescribir el archivo completo), **time travel** (consultar la tabla como estaba en
  un momento pasado, vía snapshots), y **evolución de esquema** (agregar/quitar
  columnas sin romper lectores existentes de la tabla).
- Este curso usa Iceberg (ver `recursos/lakehouse-iceberg/README.md` para el porqué
  específico de esa elección sobre Delta) — el mecanismo interno difiere entre ambos,
  pero el problema que resuelven y las garantías que dan son equivalentes.

`recursos/lakehouse-iceberg/06_lakehouse_iceberg.py` demuestra las tres operaciones
sobre la tabla de features de `bank_transactions.csv` — correrlo y comparar contra el
patrón de carpetas de `recursos/etl-tipo-cambio/` hace tangible por qué "Parquet bien
organizado" y "lakehouse transaccional" no son lo mismo.

## 4. Versionado de datasets y de modelos

Versionar código (git) es familiar. Versionar **datos** y **modelos** es un problema
distinto, con retos propios:

- **Datasets** cambian de tamaño (GB, no KB) — no se puede versionar un dataset de
  20GB con la misma estrategia que un archivo de texto en git. Iceberg/Delta resuelven
  esto con snapshots: cada escritura crea una nueva versión referenciable sin duplicar
  físicamente los datos que no cambiaron.
- **Modelos** necesitan versionarse junto con el dataset y los hiperparámetros que los
  produjeron — sin eso, "¿con qué datos se entrenó este modelo?" se vuelve
  irrespondible seis meses después. `recursos/spark/04_pipeline_ml.ipynb` guarda el
  `PipelineModel` completo (no solo los pesos) precisamente para que sea reproducible
  de punta a punta — feature engineering incluido, no solo el algoritmo final.

---

## Referencias

- [Apache Parquet — documentación oficial](https://parquet.apache.org/docs/)
- [Apache Avro — documentación oficial](https://avro.apache.org/docs/++version++/)
- [Apache Iceberg — Table Spec (documentación oficial)](https://iceberg.apache.org/spec/)
- [Delta Lake — documentación oficial](https://docs.delta.io/latest/index.html)
- [Databricks — Medallion Architecture explained](https://www.databricks.com/glossary/medallion-architecture)
