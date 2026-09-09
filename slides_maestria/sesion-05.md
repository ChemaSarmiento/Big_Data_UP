---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 05 — Entrenamiento de modelos distribuido"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 05: MLlib, CrossValidator, límites de Spark MLlib
---

# Sesión 05
## Entrenamiento de modelos distribuido

<div class="pt-6 text-sm opacity-60">
Se entrena, se compara, y se decide qué modelo justifica producción — con evidencia, no con "se ve bien el AUC"
</div>

---

# No todos los algoritmos se paralelizan igual

| Algoritmo | Estrategia |
|---|---|
| Regresión (lineal/logística) | Gradiente distribuido — cada worker calcula su porción, se suman |
| Árboles de decisión | *Level-wise* — todo un nivel de profundidad en paralelo |
| **Gradient Boosting** | Árboles **secuenciales** (cada uno corrige al anterior) — no paraleliza entre árboles |

<div v-click class="mt-6 text-sm opacity-70">
Por diseño, GBT es más lento de entrenar que Random Forest a la misma profundidad
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

Extender `04_pipeline_ml.ipynb`: envolver el Pipeline en un `CrossValidator`
y comparar contra un segundo algoritmo (`GBTClassifier`)

<div class="mt-8 p-4 border-l-4 border-blue-500">
Entregable: modelo entrenado + comparación de métricas + <b>una gráfica comparativa</b> (AUC/F1 por modelo, o curva ROC) + justificación
</div>

---
layout: center
class: text-center
---

# → Sesión 06

Data Lakes / Lakehouse — Parquet, medallion, y por qué Iceberg va más allá
