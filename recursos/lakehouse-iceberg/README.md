# Lakehouse transaccional con Apache Iceberg

Material técnico de Maestría Sesión 6. Un data lake con Parquet bien organizado en
carpetas (`raw/`→`processed/`, ver `recursos/etl-tipo-cambio/`) resuelve
almacenamiento y formato columnar, pero no resuelve transacciones: corregir un
lote de filas ya cargado, ver el dato como estaba ayer, o agregar una columna sin
romper a quien ya lee la tabla. Ese es el problema que resuelve un lakehouse
transaccional (Iceberg/Delta), y este script lo demuestra sobre el mismo
`bank_transactions.csv` que ya atraviesa las Sesiones 4 y 5.

## Por qué Iceberg y no Delta Lake

Ambos resuelven el mismo problema (ACID sobre archivos en un lake). Se eligió
**Iceberg** para este curso porque tiene mejor soporte nativo en GCP: BigQuery
puede leer tablas Iceberg directamente vía BigLake, sin pasar por Spark — un
puente natural hacia la Sesión 2 (SQL distribuido) si se quiere profundizar.

## Qué demuestra `06_lakehouse_iceberg.py` que Parquet plano no puede

| Operación | Con Parquet en carpetas (`etl-tipo-cambio/`) | Con Iceberg (este script) |
|---|---|---|
| Corregir un lote de filas ya cargado | Reescribir el archivo/partición completa | `MERGE INTO` solo sobre las filas afectadas |
| Ver el dato como estaba ayer | Solo si guardaste una copia versionada tú mismo | `SELECT ... FROM tabla.snapshots` + time travel, gratis |
| Agregar una columna nueva | Rompe lectores que no esperan la columna nueva, o forzar a versionar toda la carpeta | `ALTER TABLE ... ADD COLUMN`, sin tocar los archivos ya escritos |

## Cluster requerido

Ver el bloque de configuración al inicio de `06_lakehouse_iceberg.py` — necesita el
runtime de Iceberg (`iceberg-spark-runtime`) y la extensión SQL de Iceberg en las
propiedades del cluster de `recursos/managed-spark-cluster/`.

## Correr

```bash
spark-submit --master yarn 06_lakehouse_iceberg.py --bucket gs://<TU-BUCKET>
```

## Ver también

- [`recursos/spark/04_pipeline_ml.ipynb`](../spark/04_pipeline_ml.ipynb) — de donde viene `bank_transactions.csv` ya con `hora_del_dia` derivada.
- [`recursos/etl-tipo-cambio/`](../etl-tipo-cambio/) — el mismo patrón bronze/silver/gold, pero con Parquet plano — útil para contrastar directamente contra este script en clase.
