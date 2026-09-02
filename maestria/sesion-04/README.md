# Sesión 04 — Ingeniería de features a escala

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Feature engineering distribuido: `Pipeline`, `Transformer`, `Estimator` de Spark MLlib
2. Encoding y escalado a escala
3. Introducción a feature stores: qué problema resuelven

## Lab
Construir un pipeline de features reproducible con Spark MLlib sobre un dataset de +5M filas (imputación, encoding, escalado, ensamblado de vector de features).

## Entregable
Pipeline de features serializado y reproducible.

## Ejemplo / material de apoyo
`recursos/spark/04_pipeline_ml.ipynb` — Pipeline completo de MLlib (`Imputer` → `StringIndexer`/`OneHotEncoder` → `VectorAssembler` → `StandardScaler` → modelo) sobre `bank_transactions.csv`, listo para correr o extender con más features de `recursos/datasets/`.

## Recursos vinculados
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb)
- [`recursos/datasets/README.md`](../../recursos/datasets/README.md) — Credit Card Fraud / Home Credit Default Risk

## Slides
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
