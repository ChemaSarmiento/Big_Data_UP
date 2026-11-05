# Caso de apertura — una decisión con consecuencias

Caso hipotético: dos candidatos tienen ROC-AUC similar, pero generan cantidades muy distintas de falsas alarmas. El equipo solo puede revisar una fracción de los casos. ¿Cuál modelo conviene realmente?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

La selección de hiperparámetros es una comparación entre candidatos. Con dos valores y dos folds hay cuatro ajustes y un refit; ampliar la rejilla multiplica cómputo. El pipeline completo se reajusta dentro de cada fold. El test futuro queda reservado para la evaluación final, no para elegir una configuración.

---

# Elegir bien exige reconocer el límite

ROC-AUC resume ordenamiento, no decide un umbral de acción. En clases desbalanceadas, acompaña PR-AUC con prevalencia y precisión/recall. La CV aleatoria dentro de train no reproduce necesariamente el futuro: si importa deriva temporal, usa bloques de validación y explica el límite del ejercicio.

---

# Predice el resultado antes de comprobarlo

¿Qué debe usarse para seleccionar hiperparámetros?

<div class="knowledge-check">
<button type="button" data-correct="false">El test futuro</button>
<button type="button" data-correct="true">Validación dentro de train</button>
<button type="button" data-correct="false">La métrica más alta de cualquier periodo</button>
<p class="check-feedback" role="status" hidden data-explanation="El test futuro se reserva para evaluación final. Usarlo repetidamente para elegir un ganador introduce sesgo de selección."></p>
</div>

---

# Laboratorio guiado — preparación y objetivo

Retomar entrada, corte y features de S5. Núcleo: baseline LR y búsqueda de dos valores sobre una muestra acotada. Rejillas amplias y comparación de varios algoritmos se programan después; no se prometen 27 ajustes en 35 minutos.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — definir el criterio antes de correr

Declara métrica de selección, periodo de validación, costo de falso positivo y capacidad de revisión. Calcula prevalencia de train sin usarla para redefinir el test.

---

# Laboratorio · paso 2 — entrenar el baseline

Ejecuta el CLI de `ML_REPRODUCIBLE.md` con RUN_ID nuevo y conserva el pipeline completo, métricas y referencia. Este candidato es también el artefacto seguro para S10–S12.

---

# Laboratorio — ejecuta y comprueba

Ejercicio acotado, dentro de train:
```python
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import BinaryClassificationEvaluator
lr = LogisticRegression(labelCol="is_suspicious", maxIter=20)
grid = ParamGridBuilder().addGrid(lr.regParam, [0.01, 0.1]).build()
eval_pr = BinaryClassificationEvaluator(labelCol="is_suspicious", metricName="areaUnderPR")
cv = CrossValidator(estimator=Pipeline(stages=feature_stages()+[lr]),
    estimatorParamMaps=grid, evaluator=eval_pr, numFolds=2, parallelism=1, seed=42)
```
Este ejercicio aleatorio no prueba estabilidad temporal.

---

# Laboratorio · paso 3 — limitar la búsqueda

En el notebook configura dos valores de `regParam`, dos folds y `parallelism=1`. Estima tiempo con un ajuste pequeño. Si el estimado excede el bloque, reduce muestra y documenta la decisión.

---

# Laboratorio · paso 4 — evaluar una vez y guardar

Selecciona dentro de train, evalúa el ganador en test futuro y guarda métricas de ese candidato. Compara con baseline en un gráfico con periodos y prevalencia. No atribuyas métricas del baseline al ganador.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar un candidato reproducible, gráfica ROC/PR y justificación ligada al costo de errores. Si no mejora al baseline, conservarlo puede ser la decisión correcta.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Una métrica falla: busca clase única o scores inválidos. El tuning agota tiempo: calcula ajustes × folds y reduce alcance antes de gastar. El ganador no carga en streaming: guardaste solo el clasificador y faltan transformaciones.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 2–3 horas: GBT y una rejilla más amplia, con presupuesto y validación temporal. Si se exige hacer todo desde cero en vivo, este laboratorio necesita una sesión técnica adicional; no cabe en el núcleo de tres horas.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Selección de modelos y tuning](https://spark.apache.org/docs/3.5.5/ml-tuning.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
