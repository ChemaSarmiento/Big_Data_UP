# Teoría — Sesión 05: Entrenamiento de modelos distribuido

> La Sesión 4 dejó las features listas. Hoy se entrena, se compara, y se decide qué
> modelo justifica llevar a producción — con evidencia, no con "se ve bien el AUC".

## 1. Algoritmos de MLlib y su paralelización

MLlib no reimplementa scikit-learn distribuido tal cual — cada algoritmo tiene una
estrategia de paralelización distinta, porque no todos los algoritmos se paralelizan
de la misma forma:

- **Regresión (lineal/logística):** se entrena con descenso de gradiente distribuido —
  cada worker calcula el gradiente sobre su porción de datos, y se agregan (suman) los
  gradientes parciales en cada iteración antes de actualizar los pesos del modelo.
- **Árboles de decisión:** MLlib usa una estrategia de particionamiento por niveles
  (*level-wise*) — en vez de construir un árbol nodo por nodo secuencialmente (como
  scikit-learn en una sola máquina), calcula todas las decisiones de un mismo nivel de
  profundidad en paralelo sobre todo el cluster antes de pasar al siguiente nivel.
- **Gradient Boosting (`GBTClassifier`):** entrena árboles de forma *secuencial* (cada
  árbol corrige los errores del anterior — no se puede paralelizar entre árboles), pero
  cada árbol individual sí se entrena de forma distribuida con la estrategia de arriba.
  Por diseño, GBT es más lento de entrenar que Random Forest a la misma profundidad,
  porque no puede aprovechar paralelismo entre árboles.

## 2. Tuning de hiperparámetros con `CrossValidator`

`CrossValidator` combina dos ideas: validación cruzada (entrenar y evaluar sobre
varios splits del dataset, no solo uno, para una estimación más confiable del
desempeño) y búsqueda de hiperparámetros (probar varias combinaciones de parámetros
y quedarse con la mejor).

```python
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator

grid = (
    ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1, 1.0])
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
    .build()
)

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=grid,
    evaluator=BinaryClassificationEvaluator(labelCol="is_suspicious"),
    numFolds=3,
)
modelo_cv = cv.fit(train_df)  # entrena len(grid) * numFolds modelos completos
```

**El costo real:** con 9 combinaciones de la rejilla anterior y 3 folds, esto entrena
27 pipelines completos — cada uno repitiendo todo el feature engineering de la Sesión 4.
A escala distribuida esto es viable porque cada entrenamiento individual usa el
cluster completo, pero el costo total (tiempo de cluster, y en GCP, dinero) crece
linealmente con `len(grid) * numFolds` — vale la pena empezar con una rejilla pequeña.

## 3. Cuándo MLlib no alcanza: deep learning

MLlib está optimizado para algoritmos que se paralelizan bien por *datos* (cada worker
ve una porción distinta del dataset). Deep learning necesita paralelizar por *modelo*
además de por datos — redes con millones de parámetros no caben ni se entrenan
eficientemente con la misma estrategia. Dos alternativas que este curso solo menciona
como panorama (no las implementa):

- **Vertex AI Training** — entrenamiento gestionado en GCP, con soporte nativo para
  GPUs/TPUs y frameworks como PyTorch/TensorFlow — la ruta recomendada si el curso
  necesitara deep learning real sobre GCP.
- **Horovod** — framework open-source (originado en Uber) para entrenamiento
  distribuido de redes neuronales sobre múltiples GPUs/máquinas, usando
  comunicación *allreduce* en vez de la estrategia map-reduce de MLlib — el estándar
  de facto para deep learning distribuido fuera de un proveedor cloud específico.

La pregunta que importa no es "¿cuál es mejor?" sino "¿mi problema necesita esto?" —
para tabular/estructurado (como `bank_transactions.csv`), gradient boosting o
regresión logística suelen igualar o superar a deep learning con una fracción del
costo de cómputo. Deep learning se justifica en datos no estructurados (imágenes,
texto libre, audio) — fuera del alcance de este capstone.

---

## Referencias

- [Apache Spark MLlib — Classification and Regression](https://spark.apache.org/docs/latest/ml-classification-regression.html)
- [Apache Spark MLlib — Model selection and hyperparameter tuning](https://spark.apache.org/docs/latest/ml-tuning.html)
- [Google Cloud — Vertex AI Training overview](https://cloud.google.com/vertex-ai/docs/training/overview)
- [Sergeev, Del Balso — Horovod: fast and easy distributed deep learning (paper, 2018)](https://arxiv.org/abs/1802.05799)
