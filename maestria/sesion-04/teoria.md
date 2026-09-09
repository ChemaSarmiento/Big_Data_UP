# Teoría — Sesión 04: Ingeniería de features a escala

> El puente entre "procesar datos" (Sesiones 1-3) y "entrenar modelos" (Sesión 5). Si
> el feature engineering está mal hecho aquí, ningún modelo lo compensa después.

## 1. Spark MLlib: Pipeline, Transformer, Estimator

MLlib organiza el feature engineering y el modelado alrededor de tres abstracciones,
diseñadas para que todo el flujo (desde datos crudos hasta predicción) sea un solo
objeto reproducible:

- **Transformer** — toma un DataFrame y devuelve otro DataFrame transformado, sin
  necesidad de "aprender" nada de los datos primero. `VectorAssembler` (junta varias
  columnas en un solo vector de features) es un Transformer: la operación es la misma
  sin importar los datos que le pases.
- **Estimator** — un algoritmo que *aprende* de los datos vía `.fit()`, y como
  resultado produce un Transformer ya ajustado. `StandardScaler` es un Estimator:
  `.fit()` calcula la media y desviación estándar de tus datos de entrenamiento, y el
  Transformer resultante (`StandardScalerModel`) aplica esa transformación aprendida a
  cualquier DataFrame nuevo — incluyendo datos que nunca vio en el entrenamiento.
- **Pipeline** — encadena Transformers y Estimators en una sola secuencia. Al llamar
  `.fit()` sobre el Pipeline completo, cada Estimator interno aprende en orden, y el
  resultado es un `PipelineModel`: un solo objeto que reproduce *exactamente* la misma
  secuencia de transformaciones sobre datos nuevos, sin tener que recordar manualmente
  el orden ni los parámetros aprendidos de cada paso.

`recursos/spark/04_pipeline_ml.ipynb` implementa exactamente esta secuencia —
`Imputer → StringIndexer → OneHotEncoder → VectorAssembler → StandardScaler → modelo`
— sobre `bank_transactions.csv`. Vale la pena notar que ese mismo `PipelineModel`
guardado se reutiliza sin cambios en la Sesión 7 (streaming) y la Sesión 8 (serving) —
es el mismo objeto, no una reimplementación.

## 2. Encoding y escalado a escala

Dos transformaciones estándar, pero que a escala distribuida tienen matices:

- **Encoding** (convertir categorías en números): `StringIndexer` asigna un entero a
  cada categoría distinta, y `OneHotEncoder` convierte ese entero en un vector binario
  disperso. El detalle que importa a escala: `StringIndexer` necesita ver *todas* las
  categorías posibles antes de asignar índices — sobre un dataset de millones de filas,
  eso implica un paso de agregación distribuida (`.fit()` no es gratis).
- **Escalado** (`StandardScaler`, `MinMaxScaler`): normaliza el rango de valores
  numéricos. El error común es calcular la media/desviación sobre *todo* el dataset
  (incluyendo el set de prueba) antes de dividir en train/test — eso es fuga de
  información: el modelo "ve" estadísticas del conjunto que se supone evalúa a ciegas.
  El patrón correcto es `.fit()` solo sobre `train_df`, y aplicar ese mismo
  `StandardScalerModel` (ya aprendido) sobre `test_df` — exactamente lo que hace el
  `Pipeline` cuando se estructura bien.

## 3. Feature stores: qué problema resuelven

Un feature store es un sistema centralizado para calcular, guardar y servir features
— pensado para un problema muy concreto que aparece cuando hay *varios* modelos en
producción: sin un feature store, cada equipo recalcula sus propias features desde
cero, con lógica ligeramente distinta, lo que produce **inconsistencia
entrenamiento-servicio** (training-serving skew) — el modelo se entrenó con una
definición de "hora_del_dia" y en producción se calcula con otra ligeramente distinta,
degradando el modelo sin que nadie note por qué.

Un feature store resuelve esto con dos garantías: (1) una sola definición de cada
feature, calculada una vez y reutilizada por todos los modelos, y (2) *feature
freshness* consistente entre el pipeline de entrenamiento (batch) y el de inferencia
en tiempo real (lo que la Sesión 7 va a necesitar). Este curso no implementa un feature
store real (Feast, Vertex AI Feature Store) — el `PipelineModel` guardado cumple un rol
similar a pequeña escala (una sola definición reutilizada en S4, S7 y S8), pero vale la
pena reconocer la diferencia: un `PipelineModel` sirve un modelo; un feature store sirve
*features* a muchos modelos.

---

## Referencias

- [Apache Spark MLlib — ML Pipelines (docs oficiales)](https://spark.apache.org/docs/latest/ml-pipeline.html)
- [Apache Spark MLlib — Extracting, transforming and selecting features](https://spark.apache.org/docs/latest/ml-features.html)
- [Google Cloud — Vertex AI Feature Store overview](https://cloud.google.com/vertex-ai/docs/featurestore/overview)
- [Feast — Feature Store for Machine Learning (documentación del proyecto open-source)](https://docs.feast.dev/)
