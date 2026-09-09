# Sesión 07 — Data Lakes / Lakehouse I: formatos y medallion

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Parquet vs. ORC vs. Avro
2. Arquitectura medallion (bronze/silver/gold)
3. Por qué Parquet plano en carpetas no es un lakehouse transaccional — introducción a Iceberg/Delta

## Lab
Preparar el cluster con el runtime de Iceberg (propiedades del cluster, ver `recursos/lakehouse-iceberg/README.md`) y crear la primera tabla Iceberg: cargar `bank_transactions.csv` como bronze y escribirlo como tabla `silver` particionada — la primera mitad de `06_lakehouse_iceberg.py`, hasta el snapshot inicial (antes del `MERGE INTO`).

## Entregable
Tabla Iceberg creada y cargada + captura del primer snapshot (`SELECT * FROM tabla.snapshots`).

## Ejemplo / material de apoyo
`recursos/etl-tipo-cambio/` (bronze `data/raw/` → silver `data/processed/`) y `recursos/spark/05_data_cleansing.ipynb` siguen siendo la referencia de "medallion con Parquet plano" — el contraste directo contra lo que se arma hoy con Iceberg. La Sesión 8 retoma esta misma tabla para las operaciones transaccionales.

## Recursos vinculados
- [`recursos/lakehouse-iceberg/`](../../recursos/lakehouse-iceberg/) — setup del cluster y primera carga
- [`recursos/etl-tipo-cambio/`](../../recursos/etl-tipo-cambio/) — patrón bronze/silver/gold con Parquet plano, para contraste
- [`recursos/spark/05_data_cleansing.ipynb`](../../recursos/spark/05_data_cleansing.ipynb) — bronze/silver a escala real (15 GB)

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-07.md`](../../slides_maestria/sesion-07.md) (Slidev) — `npx slidev sesion-07.md --open` desde `slides_maestria/`
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
