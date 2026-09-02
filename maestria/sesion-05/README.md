# Sesión 05 — Entrenamiento de modelos distribuido

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Algoritmos de Spark MLlib (regresión, árboles, gradient boosting) y su paralelización
2. Tuning de hiperparámetros a escala con `CrossValidator` distribuido
3. Cuándo Spark MLlib no alcanza (deep learning) y alternativas: Vertex AI Training, Horovod (panorama)

## Lab
Entrenar y comparar 2-3 modelos con Spark MLlib sobre el pipeline de features de la Sesión 4, con tuning vía `CrossValidator`.

## Entregable
Modelo entrenado + comparación de métricas + justificación del modelo elegido.

## Ejemplo / material de apoyo
Extender `recursos/spark/04_pipeline_ml.ipynb`: ya entrena una `LogisticRegression` dentro del `Pipeline` sobre `bank_transactions.csv` y reporta AUC — el ejercicio de esta sesión es envolver ese mismo `Pipeline` en un `CrossValidator` con una rejilla de hiperparámetros y comparar contra un segundo algoritmo (por ejemplo `GBTClassifier`).

## Recursos vinculados
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb)
- [`recursos/managed-spark-cluster/hugging_face_deps.sh`](../../recursos/managed-spark-cluster/hugging_face_deps.sh) — si el modelo elegido requiere transformers/torch

## Slides
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
