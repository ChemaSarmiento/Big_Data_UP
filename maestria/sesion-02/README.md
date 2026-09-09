# Sesión 02 — SQL distribuido avanzado

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Motor de ejecución de BigQuery
2. Particionamiento y clustering de tablas
3. Slot allocation: costo por bytes escaneados vs. por slots reservados
4. Window functions anidadas y CTEs recursivos

## Lab
Rediseñar una tabla mal particionada y medir la reducción de costo/latencia; escribir consultas analíticas con window functions anidadas y CTEs recursivos.

## Entregable
Reporte de optimización (antes/después) con evidencia de costo, incluyendo **una gráfica de barras** (bytes escaneados o tiempo de ejecución, tabla sin particionar vs. particionada) — no basta con el número en texto, el reporte debe poder leerse de un vistazo. Usar `matplotlib`/`pandas.plot` directo en el mismo notebook de BigQuery (2-3 líneas: los resultados de `EXPLAIN`/`bytesProcessed` ya vienen como valores numéricos, no requieren transformación).

## Ejemplo / material de apoyo
`recursos/hive/hive-queries.sql`, Sección 3 — el mismo principio (partition pruning) pero en Hive sobre el dataset real de Carpetas de investigación de la FGJ CDMX: compara el tiempo de una consulta sobre la tabla sin particionar (3.1) contra la particionada por año/mes (3.2/3.3). Para el formato de la gráfica, `recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb` (función `create_dashboard()`) es la referencia de estilo que se reutiliza en el resto del curso — mismo patrón, aquí solo con dos barras.

## Recursos vinculados
- [`recursos/hive/hive-queries.sql`](../../recursos/hive/hive-queries.sql) — Sección 3
- [`recursos/datasets/README.md`](../../recursos/datasets/README.md) — datasets de BigQuery público
- [`recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb`](../../recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb) — referencia de estilo para la gráfica antes/después

## Slides
- `slides/05_sql_fasttrack.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
