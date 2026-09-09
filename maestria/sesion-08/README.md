# Sesión 08 — Data Lakes / Lakehouse II: transacciones y versionado

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. `MERGE INTO` — actualizar sin reescribir la tabla completa
2. Time travel — consultar un snapshot anterior
3. Evolución de esquema sin romper lectores existentes
4. Versionado de datasets y de modelos

## Lab
Retomar la tabla Iceberg creada en la Sesión 7 y completar la segunda mitad de `06_lakehouse_iceberg.py`: aplicar `MERGE INTO` (corrección simulada), consultar el snapshot anterior al merge (time travel), agregar una columna con `ALTER TABLE` sin romper la tabla, y escribir la capa gold agregada.

## Entregable
Diagrama de arquitectura + pipeline versionado + evidencia de las tres operaciones transaccionales (capturas del `MERGE INTO`, la consulta de snapshots antes/después, y el `ALTER TABLE`).

## Ejemplo / material de apoyo
`recursos/lakehouse-iceberg/06_lakehouse_iceberg.py` completo — script corrido de punta a punta hoy. `recursos/spark/04_pipeline_ml.ipynb` es la referencia de "versionar un modelo completo" (no solo el algoritmo, el `PipelineModel` entero) — el mismo principio de versionado, aplicado a un objeto distinto.

## Recursos vinculados
- [`recursos/lakehouse-iceberg/`](../../recursos/lakehouse-iceberg/) — tabla Iceberg real (MERGE INTO, time travel, evolución de esquema)
- [`recursos/hive/hive-queries.sql`](../../recursos/hive/hive-queries.sql) — tabla particionada (Sección 3.2), para contraste sin transacciones
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — versionado de modelos

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-08.md`](../../slides_maestria/sesion-08.md) (Slidev) — `npx slidev sesion-08.md --open` desde `slides_maestria/`
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
