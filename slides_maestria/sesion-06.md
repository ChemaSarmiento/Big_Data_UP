---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 06 — Entrenamiento de modelos distribuido"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 06: MLlib, CrossValidator, límites de Spark MLlib
---

# Sesión 06
## Entrenamiento de modelos distribuido

<div class="pt-6 text-sm opacity-60">
Se entrena, se compara, y se decide qué modelo justifica producción — con evidencia, no con "se ve bien el AUC"
</div>

---

# No todos los algoritmos se paralelizan igual

MLlib no reimplementa scikit-learn distribuido tal cual — cada algoritmo tiene
una estrategia de paralelización distinta.

| Algoritmo | Estrategia |
|---|---|
| Regresión (lineal/logística) | Gradiente distribuido — cada worker calcula su porción, se suman en cada iteración |
| Árboles de decisión | *Level-wise* — todas las decisiones de un mismo nivel de profundidad, en paralelo sobre el cluster |
| **Gradient Boosting** | Árboles **secuenciales** (cada uno corrige al anterior) — no paraleliza entre árboles |

<div v-click class="mt-6 text-sm opacity-70">
Por diseño, GBT es más lento de entrenar que Random Forest a la misma profundidad — no puede aprovechar paralelismo entre árboles
</div>

---

# CrossValidator: el costo real de "solo probar unos parámetros"

```python {1-6|8-13}
grid = (ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1, 1.0])
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
    .build())
# 3 x 3 = 9 combinaciones

cv = CrossValidator(
    estimator=pipeline,
    estimatorParamMaps=grid,
    numFolds=3,
)
modelo_cv = cv.fit(train_df)
# 9 combinaciones x 3 folds = 27 pipelines completos entrenados
```

<div v-click class="mt-4 text-blue-500 font-bold">
El costo crece linealmente con combinaciones × folds — empieza con una rejilla pequeña
</div>

---

# Cuándo Spark MLlib no alcanza

<v-clicks>

- MLlib paraleliza bien por **datos** — deep learning necesita paralelizar por **modelo** también
- **Vertex AI Training** — GPUs/TPUs gestionadas, la ruta recomendada en GCP
- **Horovod** — allreduce, el estándar fuera de un proveedor específico

</v-clicks>

<div v-click class="mt-8 p-4 border-l-4 border-blue-500">
Para datos tabulares (bank_transactions.csv), gradient boosting suele igualar o superar deep learning con una fracción del costo
</div>

---

# Lab de hoy

Cargar el pipeline de features de la Sesión 5, entrenar, y comparar contra un
segundo algoritmo

---

# Paso 1 — Cargar features y entrenar el baseline

```python
from pyspark.ml import PipelineModel
pipeline_features = PipelineModel.load("gs://<TU-BUCKET>/modelos/features_bank_transactions")

lr = LogisticRegression(featuresCol="features", labelCol="is_suspicious")
modelo_base = lr.fit(train_df)
auc_base = evaluador.evaluate(modelo_base.transform(test_df))
```

<div class="mt-4 text-sm opacity-70">
No se recalcula ni una sola feature — se carga el objeto guardado la sesión pasada
</div>

---

# Paso 2 — CrossValidator

```python
grid = (ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1, 1.0])
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
    .build())
cv = CrossValidator(estimator=lr, estimatorParamMaps=grid,
                     evaluator=evaluador, numFolds=3)
modelo_cv = cv.fit(train_df)
```

<div class="mt-4 text-sm opacity-70">
27 pipelines completos — no se colgó, solo tarda
</div>

---

# Paso 3 — Comparar contra GBTClassifier

```python
gbt = GBTClassifier(featuresCol="features", labelCol="is_suspicious")
modelo_gbt = gbt.fit(train_df)
auc_gbt = evaluador.evaluate(modelo_gbt.transform(test_df))
```

```python
plt.bar(["Regresión (CV)", "GBT"], [auc_cv, auc_gbt])
plt.ylabel("AUC"); plt.show()
```

<div class="mt-4 p-4 border-l-4 border-blue-500 font-bold">
Entregable: modelo entrenado + comparación de métricas con gráfica + justificación de un párrafo
</div>

---
layout: center
class: text-center
---

# → Sesión 07

Lakehouse I — formatos y medallion, el primer paso hacia Iceberg
