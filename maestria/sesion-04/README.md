# Sesión 04 — Spark Core avanzado II: skew y diagnóstico

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Causas de skew (desbalance de datos)
2. Estrategias de mitigación: salting, broadcast joins, AQE
3. Diagnóstico completo: plan de ejecución antes/después de corregir

## Lab
Diagnosticar y resolver un job con **skew severo** sobre un dataset sintético desbalanceado, retomando `02_dataframes.ipynb`/`03_spark_sql.ipynb` de la Sesión 3 — ahora sí con un caso donde el plan revela el problema, no solo se lee.

## Entregable
Notebook con el diagnóstico (plan de ejecución "antes"), la solución aplicada, y métricas de mejora (plan "después" + tiempos comparados).

## Ejemplo / material de apoyo
Mismo par de notebooks de la Sesión 3, ahora extendidos con un dataset desbalanceado a propósito (una moneda o sucursal que concentra la mayoría de las filas). Correr los dos (uno sobre PROFECO, otro sobre transacciones bancarias) y comparar planes antes/después de aplicar salting o broadcast join es el ejercicio central.

## Recursos vinculados
- [`recursos/spark/02_dataframes.ipynb`](../../recursos/spark/02_dataframes.ipynb)
- [`recursos/spark/03_spark_sql.ipynb`](../../recursos/spark/03_spark_sql.ipynb)

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-04.md`](../../slides_maestria/sesion-04.md) (Slidev) — `npx slidev sesion-04.md --open` desde `slides_maestria/`
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
