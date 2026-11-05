# Caso de apertura — una decisión con consecuencias

Caso hipotético: un modelo evaluado en datos históricos parece excelente, pero falla al usarlo al mes siguiente. La imputación y las categorías se aprendieron antes de dividir datos. ¿El modelo recibió información del futuro?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Una transformación que aprende parámetros debe ajustarse con train. La mediana de imputación, el vocabulario categórico y la escala forman parte del estado del modelo. Separar por fecha antes del fit permite evaluar sobre un periodo posterior que no participó en ese aprendizaje.

---

# Elegir bien exige reconocer el límite

El pipeline reúne preprocesamiento y clasificador para mantener el mismo contrato en batch, stream y API. Repetir manualmente features en cada consumidor permite diferencias silenciosas. Una categoría nueva no equivale a un error de datos: necesita una política explícita.

---

# Laboratorio guiado — preparación y objetivo

Usar `04_pipeline_ml.ipynb`, `ml_common.py` y una muestra con ambos labels en train/test. Revisar rangos de timestamp y fijar el corte antes de métricas. Objetivo: guardar features y probar su reutilización en 90 minutos.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — validar el contrato

Comprueba columnas obligatorias, ID único, timestamp interpretable y label binario. Cuenta montos ausentes. No conviertas valores no numéricos a cero sin documentarlo.

---

# Laboratorio · paso 2 — separar antes de aprender

Ejecuta `read_transactions` y `temporal_split`. Guarda conteos y fechas de ambos periodos. Verifica que cada lado contiene las dos clases antes de continuar.

---

# Laboratorio — ejecuta y comprueba

En el notebook, con helper importado:
```python
from pyspark.ml import Pipeline
from ml_common import read_transactions, temporal_split, feature_stages
raw = read_transactions(spark, INPUT)
train_df, test_df = temporal_split(raw, CUTOFF)
features = Pipeline(stages=feature_stages()).fit(train_df)
features.transform(test_df).select("transaction_id", "features").show(3)
```
`INPUT` y `CUTOFF` se definen con la muestra real.

---

# Laboratorio · paso 3 — aprender y transformar

Crea un Pipeline con `feature_stages()`, ajústalo sobre train y transforma test sin fit. Inspecciona el vector y prueba una moneda no observada: el comportamiento debe seguir la política `handleInvalid`.

---

# Laboratorio · paso 4 — guardar y reabrir

Guarda features bajo un RUN_ID exclusivo, vuelve a cargarlas y compara salida sobre las mismas filas. Documenta esquema, corte y versión; no sobrescribas el artefacto de otro candidato.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar pipeline recargable, contrato y prueba de transformación sobre test futuro. La evidencia no es solo que se creó un directorio: es que la versión recargada transforma de manera consistente.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No hay ambas clases: revisa cobertura y corte; no cambies la fecha mirando la mejor métrica. Features incompatibles: comprueba nombres y tipos. Categoría nueva falla: verifica la política configurada en el pipeline.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60–90 minutos: ejecutar sobre >5M filas si la fuente lo permite. Registrar tiempo y costo; la muestra de clase explica el mecanismo, el run posterior aporta evidencia de escala.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Selección de modelos y tuning](https://spark.apache.org/docs/3.5.5/ml-tuning.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
