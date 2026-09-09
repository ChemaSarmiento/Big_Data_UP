# Teoría — Sesión 07: Data Lakes / Lakehouse I — formatos y medallion

> Primera de dos sesiones sobre lakehouse. Hoy se prepara el terreno: formato de
> archivo, organización en capas, y por qué ninguna de las dos cosas por sí sola
> resuelve transacciones. La Sesión 8 resuelve eso con Iceberg a fondo.

## 1. Parquet vs. ORC vs. Avro

Tres formatos de archivo columnar/binario que compiten por el mismo espacio, con
diferencias de diseño que importan según el caso de uso:

| Formato | Diseño | Mejor para |
|---|---|---|
| **Parquet** | Columnar, con metadata de esquema embebida, compresión por columna | Analítica (leer pocas columnas de muchas) — el estándar de facto en el ecosistema Spark/BigQuery |
| **ORC** | Columnar, optimizado originalmente para Hive, con índices integrados a nivel de bloque | Cargas de trabajo muy pesadas en consultas con predicados (`WHERE`) sobre Hive/Hadoop clásico |
| **Avro** | Orientado a **filas**, no a columnas, con esquema evolutivo integrado (el esquema viaja con cada archivo) | Streaming e ingesta — cuando escribes fila por fila conforme llega, no en lote |

La elección de Parquet en este curso no es arbitraria: como el patrón de acceso es
"escribir en lote, leer analíticamente después", columnar gana. Avro tendría más
sentido si el patrón fuera "escribir evento por evento" — justo lo que ocurre en la
Sesión 9-10 (streaming), aunque ahí seguimos escribiendo el resultado a Parquet por
consistencia con el resto del pipeline.

## 2. Arquitectura medallion (bronze/silver/gold)

`recursos/etl-tipo-cambio/` (bronze en `data/raw/`, silver en `data/processed/`) y
`recursos/spark/05_data_cleansing.ipynb` (la misma idea, a escala real de 15GB,
convirtiendo `quien_es_quien.csv` — sin encabezados, con `\N` como nulo no estándar —
en una capa silver tipada) son la referencia real de este patrón. El detalle técnico
que vale la pena notar hoy: cada capa normalmente cambia de formato además de
calidad — bronze puede ser CSV/JSON crudo, silver y gold casi siempre son Parquet
(o, como se arma en el lab de hoy, Iceberg).

## 3. Por qué Parquet plano no es un lakehouse transaccional

Parquet resuelve el formato del archivo. No resuelve la **tabla** — un conjunto de
archivos Parquet en una carpeta no tiene transacciones, ni forma de saber qué versión
de la tabla estás leyendo si alguien la está escribiendo al mismo tiempo. Tres
problemas concretos que un lakehouse transaccional (Iceberg, Delta Lake) resuelve y
Parquet plano no:

- **Corregir un lote de filas ya cargado** — con Parquet plano, obliga a reescribir
  el archivo o la partición completa.
- **Ver el dato como estaba ayer** — con Parquet plano, solo si tú mismo guardaste una
  copia versionada manualmente.
- **Agregar una columna nueva** — con Parquet plano, rompe lectores que no esperan la
  columna nueva, o fuerza a versionar toda la carpeta.

La Sesión 8 resuelve las tres, con código real, sobre la tabla que se crea hoy. El
lab de hoy se queda en el primer paso: tener la tabla Iceberg lista y cargada —
`recursos/lakehouse-iceberg/06_lakehouse_iceberg.py`, primera mitad (hasta el
snapshot inicial, antes del `MERGE INTO`).

---

## Referencias

- [Apache Parquet — documentación oficial](https://parquet.apache.org/docs/)
- [Apache Avro — documentación oficial](https://avro.apache.org/docs/++version++/)
- [Databricks — Medallion Architecture explained](https://www.databricks.com/glossary/medallion-architecture)
- [Apache Iceberg — Table Spec (documentación oficial)](https://iceberg.apache.org/spec/)
