# Sesión 05 — Entrenamiento de modelos distribuido

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Algoritmos de Spark MLlib (regresión, árboles, gradient boosting) y su paralelización
2. Tuning de hiperparámetros a escala con `CrossValidator` distribuido
3. Cuándo Spark MLlib no alcanza (deep learning) y alternativas: Vertex AI Training, Horovod (panorama)

## Lab
Entrenar y comparar 2-3 modelos con Spark MLlib sobre el pipeline de features de la Sesión 4, con tuning vía `CrossValidator`.

## Entregable
Modelo entrenado + comparación de métricas + justificación del modelo elegido, con **una gráfica comparativa** (barras de AUC/F1 por modelo, o curva ROC superpuesta de ambos) — es la misma evidencia que después se reusa en el capstone (Sesión 9), donde el documento final exige visualizaciones sobre las conclusiones.

## Ejemplo / material de apoyo
Extender `recursos/spark/04_pipeline_ml.ipynb`: ya entrena una `LogisticRegression` dentro del `Pipeline` sobre `bank_transactions.csv` y reporta AUC — el ejercicio de esta sesión es envolver ese mismo `Pipeline` en un `CrossValidator` con una rejilla de hiperparámetros y comparar contra un segundo algoritmo (por ejemplo `GBTClassifier`).

## Recursos vinculados
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb)
- [`recursos/managed-spark-cluster/hugging_face_deps.sh`](../../recursos/managed-spark-cluster/hugging_face_deps.sh) — si el modelo elegido requiere transformers/torch

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-05.md`](../../slides_maestria/sesion-05.md) (Slidev) — `npx slidev sesion-05.md --open` desde `slides_maestria/`
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
