# Spark — de lo básico a pipelines de modelado

Mejora sobre `spark_notebooks/` del repo original. El problema del material anterior no
era el contenido (la progresión "básico → pipeline de modelado" ya era la correcta) sino
que estaba en notebooks sueltos sin una secuencia explícita, usando buckets de un
semestre anterior. Aquí queda numerado, cada notebook tiene un objetivo de aprendizaje
único, y todos usan datasets reales del Drive del curso — sin necesidad de generar
nada sintético.

| Notebook | Sesión sugerida | Dataset | Qué enseña |
|---|---|---|---|
| `01_rdd_basico.ipynb` | Maestría S1 / Especialidad S4 | `war_tweets.txt` (~22.6 GB) | RDDs, word count, y cuándo usar `read.json()` para JSON con esquema anidado real |
| `02_dataframes.ipynb` | Maestría S3 | `all_data.csv` — PROFECO (~19.7 GB) | DataFrame API, `explain()` para leer el plan físico, guardado particionado |
| `03_spark_sql.ipynb` | Maestría S2 / S3 | `bank_transactions.csv` (~7.5 GB) | Spark SQL, vistas temporales, window functions |
| `04_pipeline_ml.ipynb` | Maestría S4-S5 | `bank_transactions.csv` (~7.5 GB) | `Pipeline` de Spark MLlib: imputación → encoding → escalado → modelo |
| `05_data_cleansing.ipynb` | Maestría S6 | `quien_es_quien.csv` (~15.4 GB) | Esquema sin encabezados, nulos no estándar (`\N`), estandarización de tipos y texto |

Se cambió de `.py` a `.ipynb` a propósito: estos datasets son grandes (7-22 GB) y corren
mejor en un cluster con Jupyter habilitado (`--optional-components=JUPYTER`, ver
`recursos/managed-spark-cluster/`), donde se puede inspeccionar el resultado de cada
celda antes de pasar a la siguiente — no tiene sentido correr un script de punta a
punta contra 20 GB de datos sin ver los resultados intermedios.

## Sobre `war_tweets.txt`: el JSON no es plano

Al inspeccionar el esquema real (`printSchema()`), `war_tweets.txt` no es un JSON plano
con 4-5 campos — cada tweet trae `user`, `quotedTweet`, `inReplyToUser`, `media`, etc.
como structs anidados varios niveles. `01_rdd_basico.ipynb` sí funciona parseando a mano
con RDDs (`content` es un campo de primer nivel), pero agrega una sección final que
muestra `spark.read.json()` con selección por notación de punto
(`user.username`, `user.followersCount`) para cuando sí hace falta un campo anidado —
es la forma correcta de leer este archivo en un pipeline real, una vez entendido el
concepto de RDD.

## `quien_es_quien.csv` es el mismo dataset que `all_data.csv`, sin limpiar

Comparando una muestra real de ambos archivos: mismas 15 columnas, mismo orden, mismos
valores — solo que `quien_es_quien.csv` no trae encabezados (`_c0`..`_c14`) y usa `\N`
(el marcador de nulo de MySQL) en vez de un valor vacío real. `05_data_cleansing.ipynb`
reconstruye el esquema comparando contra `all_data.csv` y limpia ambos problemas — es
el ejercicio de ingeniería de datos "sucio" que ya describía `recursos/datasets/README.md`.

## Por qué `03` y `04` comparten dataset

`bank_transactions.csv` es el dataset transversal del curso (ver
`recursos/datasets/README.md`, Sección 3) — la misma progresión que antes se hacía con
datos sintéticos de fraude, ahora sobre el dato real: primero se analiza con SQL
(`03_spark_sql.ipynb`, ranking de transacciones sospechosas), después se entrena el
modelo (`04_pipeline_ml.ipynb`, prediciendo `is_suspicious`). El capstone se siente
como una continuación del mismo hilo, no un dataset nuevo por sesión.

**Nota de diseño en `04`:** la columna `suspicious_pattern` no se usa como feature —
solo tiene valor cuando `is_suspicious = true`, así que incluirla sería fuga de
información (el modelo vería la respuesta disfrazada de pregunta).

## Antes de correr estos notebooks

Sube el dataset correspondiente a Cloud Storage y reemplaza `gs://<TU-BUCKET>/...` por
tu ruta real — ver `recursos/datasets/README.md` Sección 5.
