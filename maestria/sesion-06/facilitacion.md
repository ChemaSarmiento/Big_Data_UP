# Facilitación — Sesión 06: Entrenamiento de modelos distribuido

> Guion de 3 horas: talking points + lab guiado. Retoma el pipeline de features de
> la Sesión 5 — hoy se entrena de verdad, se compara, y se defiende una elección
> de modelo con evidencia.

## Antes de empezar (facilitador)

```bash
gcloud dataproc clusters list --region=us-central1
```

Van 5 sesiones creando/usando clusters (S1, S3, S4, S5, S6).

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Vamos a entrenar 2-3 modelos hoy, y la parte cara no va a ser 'quién obtiene
> el mejor AUC' — va a ser entender cuánto cuesta, en tiempo de cluster, cada
> combinación de hiperparámetros que prueban. `CrossValidator` puede entrenar
> docenas de pipelines completos sin que se den cuenta si no hacen la cuenta
> antes."

**Pregunta de apertura:**

> "Si prueban 3 valores de un hiperparámetro y 3 de otro, con validación cruzada
> de 3 folds, ¿cuántos pipelines completos se entrenan en total?"

(Déjalos calcular: 3×3×3 = 27. Es el número que van a ver correr en vivo.)

**Ejemplo de actualidad:**

> "Los sistemas de scoring de crédito de la banca real casi siempre usan
> modelos interpretables (regresión logística, árboles poco profundos) en vez
> de los más 'poderosos' — porque un regulador puede exigir explicar por qué se
> negó un crédito. Hoy van a comparar exactamente ese trade-off: poder
> predictivo vs. interpretabilidad."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Cómo se paraleliza cada algoritmo (15 min)

Recorre la tabla de `teoria.md` (regresión, árboles, gradient boosting).
Pregunta clave: **"¿por qué Gradient Boosting es más lento de entrenar que
Random Forest a la misma profundidad, si ambos son 'árboles'?"** (GBT entrena
secuencial — cada árbol corrige al anterior, no se puede paralelizar entre
árboles).

### CrossValidator y su costo real (15 min)

Escribe el cálculo en el pizarrón junto con el grupo: `len(grid) × numFolds`.
Es el momento de conectar con el hábito de costo que vienen construyendo desde
la Sesión 2 (BigQuery) — aquí el "costo" es tiempo de cluster, no bytes
escaneados, pero la disciplina de estimar antes de correr es la misma.

### Cuándo MLlib no alcanza (15 min)

Menciona Vertex AI Training y Horovod como panorama — sin profundizar, es
información de contexto, no un tema evaluado. Cierra con el punto de
`teoria.md`: para datos tabulares, gradient boosting suele igualar a deep
learning con una fracción del costo.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Cargar el pipeline de features de la Sesión 5 (10 min)

```python
from pyspark.ml import PipelineModel
pipeline_features = PipelineModel.load("gs://<TU-BUCKET>/modelos/features_bank_transactions")
```

**Talking point:** "Noten que no estamos recalculando ni una sola feature —
literalmente cargamos el objeto que guardaron la sesión pasada."

### Paso 2 — Entrenar el primer modelo, sin tuning (20 min)

```python
from pyspark.ml.classification import LogisticRegression
lr = LogisticRegression(featuresCol="features", labelCol="is_suspicious")
modelo_base = lr.fit(train_df)
auc_base = evaluador.evaluate(modelo_base.transform(test_df))
print(f"AUC baseline: {auc_base:.4f}")
```

**Deberías ver:** un AUC razonable (>0.6) como punto de partida — esto es la
línea base contra la que todo lo demás se compara.

### Paso 3 — Envolver en CrossValidator (35 min)

```python
grid = (ParamGridBuilder()
    .addGrid(lr.regParam, [0.01, 0.1, 1.0])
    .addGrid(lr.elasticNetParam, [0.0, 0.5, 1.0])
    .build())
cv = CrossValidator(estimator=lr, estimatorParamMaps=grid,
                     evaluator=evaluador, numFolds=3)
modelo_cv = cv.fit(train_df)
```

**Advertencia explícita antes de correr:** "Esto va a tardar varios minutos —
son 27 pipelines. No es que se haya colgado."

**Si tarda demasiado para el tiempo de clase:** reducir la rejilla a 2×2 en vivo
y explicar por qué (menos combinaciones = menos tiempo, mismo concepto).

### Paso 4 — Comparar contra GBTClassifier (25 min)

```python
from pyspark.ml.classification import GBTClassifier
gbt = GBTClassifier(featuresCol="features", labelCol="is_suspicious")
modelo_gbt = gbt.fit(train_df)
auc_gbt = evaluador.evaluate(modelo_gbt.transform(test_df))
```

```python
import matplotlib.pyplot as plt
plt.bar(["Regresión (CV)", "GBT"], [auc_cv, auc_gbt])
plt.ylabel("AUC")
plt.show()
```

**Deberías ver:** una gráfica comparando ambos modelos — esto **es** el
entregable de hoy, no un extra.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** modelo entrenado + comparación de métricas con gráfica +
justificación de un párrafo de por qué eligieron uno sobre el otro.

**Puente a la Sesión 7:**

> "Ya tienen un modelo entrenado y un pipeline de features. La próxima sesión
> no vamos a mejorar el modelo — vamos a resolver un problema distinto: ¿dónde
> vive todo esto de forma que se pueda corregir, versionar, y auditar? Ahí
> entra el lakehouse."

---

## Notas de costo GCP

- `CrossValidator` con una rejilla grande es la operación más cara en tiempo de
  cluster de todo el curso hasta ahora — si el grupo es numeroso y cada quien
  corre su propio `CrossValidator` completo, considera coordinar turnos o
  reducir la rejilla para todos.
