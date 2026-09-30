# Notebooks de Spark

Notebooks de PySpark para la clase, pensados para verse **en este orden**: cada uno se apoya en el anterior.

| # | Notebook | Qué se aprende | Datos | Cluster |
|---|---|---|---|---|
| 1 | [`PySpark_Intro`](PySpark_Intro.ipynb) | **Spark Core** (transformaciones vs. acciones, RDD, cache, plan de ejecución), **Spark SQL** y un primer modelo de ML | `war_tweets.txt` (tweets, JSON anidado, ~22 GB) | B |
| 2 | [`Fraud_Detection`](Fraud_Detection.ipynb) | ML con `Pipeline`: clustering (K-Means + PCA), clasificación (Random Forest, desbalance de clases) y detección de anomalías por error de reconstrucción | Tabla `bank_transactions` en BigQuery | B |
| 2b | [`Fraud_Detection_AML_HF`](Fraud_Detection_AML_HF.ipynb) | El mismo Bloque A/B/C de `Fraud_Detection`, sobre el dataset real de AML de IBM (desbalance ~0.10%, no sintético) | `HI-Small_Trans.csv` (~5M filas, 476 MB) vía Hugging Face | **B.1** |
| 3 | [`PySpark_NLP_Steam`](PySpark_NLP_Steam.ipynb) | Texto + ML: TF-IDF, regresión logística, qué palabras pesan, comparar contra un modelo con variables estructuradas | `steam_reviews.csv` (~7.8 GB) | B |
| 4 | [`PySpark_Recommenders`](PySpark_Recommenders.ipynb) | Recomendación con ALS: línea base, checkpoints, revisar si las recomendaciones tienen sentido | `animes.csv`, `reviews.csv` (anime) | B |

`outdated/` guarda versiones anteriores. En particular `PySpark_Models` fue reemplazado por `Fraud_Detection` (mismo contenido, con matplotlib en vez de Plotly y corregido).

## Cluster

Casi todos corren en el cluster de la **sección B** de [`MLOPS/README.md`](../MLOPS/README.md): Dataproc `2.1-ubuntu20`, master `e2-highmem-2`, 3 workers `e2-standard-2` (6 tareas en paralelo), con Jupyter por Component Gateway. Es un cluster **pequeño**: varios notebooks trabajan sobre una muestra o guardan el dato en Parquet la primera vez, y traen un parámetro (`FRACCION`, `K_MAX`, `MAX_ROWS`...) para escalar.

**`Fraud_Detection_AML_HF` es la excepción:** necesita `huggingface_hub` (y por transitividad `datasets`/`transformers`/`torch`), que no están en el cluster B. Usa el cluster de la **sección B.1** (mismo `MLOPS/README.md`), que instala esas librerías vía `hugging_face_deps.sh` como initialization action en los 3 nodos, sin tocar el script. El resto de notebooks **no** necesitan el cluster B.1 — usarlo para todos sería pagar workers más grandes sin razón.

Los notebooks se guardan en `gs://<TU-BUCKET>/notebooks` (propiedad `dataproc:jupyter.notebook.gcs.dir` al crear el cluster), así que sobreviven si se borra el cluster.

## Antes de correr

Cada notebook trae en su primera celdas las rutas que hay que ajustar a tu proyecto y bucket:

| Notebook | Qué necesita |
|---|---|
| `PySpark_Intro` | `gs://<BUCKET>/war_tweets.txt`. La primera vez, poner `CREAR_PARQUET = True` para crear `war_tweets_parquet` |
| `Fraud_Detection` | Tabla de BigQuery `PROJECT_ID.DATASET_ID.bank_transactions` (conector de BigQuery, incluido en Dataproc 2.1) |
| `PySpark_NLP_Steam` | `gs://<BUCKET>/steam/steam_reviews.csv`. La primera vez, `CONVERTIR_A_PARQUET = True` |
| `PySpark_Recommenders` | `gs://<BUCKET>/reviews/animes.csv` y `reviews.csv`; carpeta de checkpoints en el mismo bucket |
| `Fraud_Detection_AML_HF` | Nada previo — descarga `HI-Small_Trans.csv` de Hugging Face (`bbfizp/AMLSim-HI-Small`, sin login) y lo sube solo a `gs://<BUCKET>/raw/aml/`. Ajustar `BUCKET`; `DESCARGAR_DE_HF = False` en corridas posteriores para no repetir la descarga |

## Notas para dar la clase

- **Ejecuta las celdas en orden.** Varias dependen de variables o de datos creados antes.
- **Matplotlib:** los notebooks con gráficas traen una celda de compatibilidad (`RcParams._get`) que debe correr **antes** de importar `pyplot`. Plotly no se usa porque no funciona en este entorno sin acceso a internet.
- **Spark UI:** desde Component Gateway se puede ver cada Job/Stage; ayuda a entender qué acción dispara qué trabajo (ver el bloque de Spark Core en `PySpark_Intro`).
- **Reseñas y nombres de usuario:** los datos de reseñas traen nombres reales de usuario. Los notebooks muestran IDs numéricos; conviene no imprimir la columna de nombres antes de compartir pantalla o guardar salidas.
