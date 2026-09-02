# Sesión 03 — Spark Core avanzado

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Catalyst optimizer y Tungsten
2. Tipos de shuffle
3. Causas de skew y mitigación (salting, broadcast joins, AQE)
4. Lectura de planes físicos con `.explain()`

## Lab
Diagnosticar y resolver un job con skew severo sobre un dataset sintético desbalanceado, comparando el plan de ejecución antes y después de la corrección.

## Entregable
Notebook con el diagnóstico y la solución aplicada, con métricas de mejora.

## Ejemplo / material de apoyo
`recursos/spark/02_dataframes.py` y `03_spark_sql.py` — ambos imprimen el plan físico con `.explain(mode="formatted")` antes de ejecutar, exactamente la herramienta de diagnóstico que se usa en este lab. Correr los dos scripts sobre el mismo dataset y comparar planes es un buen punto de partida.

## Recursos vinculados
- [`recursos/spark/02_dataframes.py`](../../recursos/spark/02_dataframes.py)
- [`recursos/spark/03_spark_sql.py`](../../recursos/spark/03_spark_sql.py)

## Slides
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
