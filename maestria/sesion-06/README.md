# Sesión 06 — Data Lakes / Lakehouse

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Parquet vs. ORC vs. Avro
2. Arquitectura medallion (bronze / silver / gold)
3. Formatos de tabla transaccionales (Iceberg/Delta) para ACID sobre el lake
4. Versionado de datasets y de modelos

## Lab
Migrar la tabla de features de `bank_transactions.csv` (Sesión 4/5) a una tabla **Iceberg** real con `06_lakehouse_iceberg.py`, y demostrar sobre ella las tres cosas que Parquet plano en carpetas no puede hacer sin reescribir todo: `MERGE INTO`, time travel y evolución de esquema.

## Entregable
Diagrama de arquitectura + pipeline versionado + capturas de las tres demostraciones del script (el MERGE, la consulta de snapshots antes/después, y el `ALTER TABLE` sin romper la tabla).

## Ejemplo / material de apoyo
`recursos/lakehouse-iceberg/06_lakehouse_iceberg.py` — script completo, corre sobre el mismo `bank_transactions.csv` de las Sesiones 4/5. `recursos/etl-tipo-cambio/` (bronze `data/raw/` → silver `data/processed/` → gold en MariaDB) y `recursos/spark/05_data_cleansing.ipynb` (mismo patrón a escala real sobre `quien_es_quien.csv`) siguen siendo la referencia de "medallion con Parquet plano" — útiles para contrastar en vivo contra la tabla Iceberg: mismo problema, un nivel de madurez distinto.

## Recursos vinculados
- [`recursos/lakehouse-iceberg/`](../../recursos/lakehouse-iceberg/) — tabla Iceberg real (MERGE INTO, time travel, evolución de esquema)
- [`recursos/etl-tipo-cambio/`](../../recursos/etl-tipo-cambio/) — patrón bronze/silver/gold con Parquet plano, para contraste
- [`recursos/spark/05_data_cleansing.ipynb`](../../recursos/spark/05_data_cleansing.ipynb) — bronze/silver a escala real (15 GB)
- [`recursos/hive/hive-queries.sql`](../../recursos/hive/hive-queries.sql) — tabla particionada (Sección 3.2)

## Slides
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
