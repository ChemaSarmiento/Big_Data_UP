# Sesión 03 — Spark Core avanzado I: Catalyst y shuffle

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Catalyst optimizer y Tungsten
2. Tipos de shuffle (por agregación, por join, por repartición explícita)
3. Lectura de planes físicos con `.explain()`

## Lab
Correr `02_dataframes.ipynb` (DataFrame API) y `03_spark_sql.ipynb` (SQL puro) sobre el mismo dataset, imprimir ambos planes con `.explain(mode="formatted")`, y confirmar que son equivalentes — ambos pasan por Catalyst. Identificar cada `Exchange` (shuffle) en el plan y explicar qué operación lo generó.

## Entregable
Capturas de los dos planes comparados + una lista de los shuffles identificados en cada uno, con la operación que los originó.

## Ejemplo / material de apoyo
`recursos/spark/02_dataframes.ipynb` y `03_spark_sql.ipynb` — ambos imprimen el plan físico antes de ejecutar. Esta sesión se queda en el diagnóstico (leer el plan); la Sesión 4 retoma exactamente este mismo par de notebooks para resolver un caso real de skew.

## Recursos vinculados
- [`recursos/spark/02_dataframes.ipynb`](../../recursos/spark/02_dataframes.ipynb)
- [`recursos/spark/03_spark_sql.ipynb`](../../recursos/spark/03_spark_sql.ipynb)

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-03.md`](../../slides_maestria/sesion-03.md) (Slidev) — `npx slidev sesion-03.md --open` desde `slides_maestria/`
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
