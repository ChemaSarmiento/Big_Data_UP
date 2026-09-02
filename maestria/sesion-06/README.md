# Sesión 06 — Data Lakes / Lakehouse

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Parquet vs. ORC vs. Avro
2. Arquitectura medallion (bronze / silver / gold)
3. Formatos de tabla transaccionales (Iceberg/Delta) para ACID sobre el lake
4. Versionado de datasets y de modelos

## Lab
Migrar el pipeline de features de la Sesión 4 a arquitectura medallion, con versionado explícito de cada capa.

## Entregable
Diagrama de arquitectura + pipeline versionado.

## Ejemplo / material de apoyo
`recursos/etl-tipo-cambio/` ya sigue el patrón bronze (`data/raw/` JSON crudo) → silver (`data/processed/` CSV limpio y validado) → gold (la tabla en MariaDB). Es el mismo patrón medallion que este lab pide migrar a Cloud Storage con Parquet particionado. `recursos/spark/05_data_cleansing.ipynb` es el mismo patrón a escala real: convierte `quien_es_quien.csv` (crudo, sin encabezados, con `\N`) en una capa silver tipada y particionada.

## Recursos vinculados
- [`recursos/etl-tipo-cambio/`](../../recursos/etl-tipo-cambio/) — patrón bronze/silver/gold ya implementado
- [`recursos/spark/05_data_cleansing.ipynb`](../../recursos/spark/05_data_cleansing.ipynb) — bronze/silver a escala real (15 GB)
- [`recursos/hive/hive-queries.sql`](../../recursos/hive/hive-queries.sql) — tabla particionada (Sección 3.2)

## Slides
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
