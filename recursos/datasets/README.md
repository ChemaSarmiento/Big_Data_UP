# Datasets del curso

Catálogo real, tomado del Drive del curso (`Archivos_Big_Data`). Reemplaza la versión
anterior de este archivo, que proponía datasets públicos genéricos (BigQuery público,
Kaggle) porque no había podido ver qué datos ya tenías preparados. Esos quedan abajo
como **alternativa** (Sección 5) para quien no tenga acceso al Drive.

## 1. Datasets de escala masiva (>10 GB — para Managed Service for Apache Spark/Dataproc)

Todos requieren un cluster real, no caben cómodamente en un notebook local — son el
material de las sesiones de Spark Core, Data Lakes y features a escala.

| Archivo | Tamaño | Columnas clave | Para qué sirve |
|---|---|---|---|
| `war_tweets.txt` | ~22.6 GB | JSON anidado real: `url`, `date`, `content`, `user.username`, `user.followersCount`, `quotedTweet` (struct), `media` (array de structs), etc. — no es plano | NLP a gran escala, análisis de sentimiento, tendencias geopolíticas, desinformación. Bueno para RDDs (parseo manual de `content`) y para enseñar `read.json()` con esquema anidado — ver `recursos/spark/01_rdd_basico.ipynb`. |
| `all_data.csv` | ~19.7 GB | `producto`, `presentacion`, `marca`, `categoria`, `catalogo`, `precio`, `fechaRegistro`, `cadenaComercial`, `giro`, `nombreComercial`, `direccion`, `estado`, `municipio`, `latitud`, `longitud` | Catálogo completo de PROFECO ("Quién es Quién en los Precios"). Analítica de retail, inflación, agregaciones geoespaciales por municipio/cadena. |
| `quien_es_quien.csv` | ~15.4 GB | Sin encabezados (`_c0`..`_c14`), `\N` como marcador de nulo. **Mismas 15 columnas y mismo orden que `all_data.csv`** — ver Sección 3. | Ejercicio de ingeniería de datos "sucio" a propósito: parseo, data cleansing, estandarización de esquema sobre Spark. Notebook completo: `recursos/spark/05_data_cleansing.ipynb`. |
| `http_sentiment_raw.csv` | ~14.5 GB | `id`, `date`, `user`, `pc`, `url`, `content`, `content.1` | Logs de navegación web corporativa, análisis comportamental, filtrado de contenido. |
| `Checkouts_by_Title_20250207.csv` (+ `checkouts_seattle.zip`, ~2.3 GB) | ~10.2 GB | `UsageClass`, `CheckoutType`, `MaterialType`, `CheckoutYear/Month`, `Checkouts`, `Title`, `ISBN`, `Subjects` | Serie de tiempo de consumo cultural (Biblioteca Pública de Seattle) — pronóstico de demanda, patrones de préstamo. |

## 2. Datasets especializados (finanzas, ciberseguridad, recomendación)

| Archivo | Tamaño | Columnas clave | Para qué sirve |
|---|---|---|---|
| `bank_transactions.csv` | ~7.5 GB | `transaction_id`, `timestamp`, `from_*`, `to_*`, `amount`, `currency`, `is_suspicious`, `suspicious_pattern` | **El dataset principal del curso** (ver Sección 4) — detección de fraude/AML, redes transaccionales, alertas de riesgo. Ya trae `is_suspicious` como label, listo para ML. |
| `steam_reviews.csv` | ~7.8 GB | `app_id`, `app_name`, `review`, `recommended`, `author.*` | Industria de videojuegos, correlación entre tiempo jugado y satisfacción. |
| `email.csv` | ~1.35 GB | metadatos de correo | Ciberseguridad, insider threat. |
| `kddcup.data` | ~708 MB | tráfico TCP/IP | Detección de intrusiones de red — dataset clásico de ciberseguridad. |
| `carpetas_investigacion.csv` | ~226.9 MB | `delito`, `alcaldia_hechos`, `geopoint`, etc. | Delitos CDMX — ya usado en `recursos/hive/hive-queries.sql` Sección 3. Antes apuntaba al portal oficial de CDMX; el archivo del Drive es el mismo dato, ya descargado. |
| `employee_location.csv` | ~16.2 MB | geolocalización | Análisis geoespacial de riesgo/seguridad patrimonial, complemento del anterior. |
| `animes.csv`, `profiles.csv`, `reviews.csv` (trilogía anime) | ~674 MB combinados | esquema relacional | Modelos de recomendación y segmentación de usuarios — es el dataset que ya usaba `spark_notebooks/PySpark_Recommenders.ipynb` del repo original. |

## 3. `quien_es_quien.csv` = `all_data.csv`, sin limpiar

Confirmado con una muestra real de ambos archivos: mismas 15 columnas, mismo orden.
`quien_es_quien.csv` las trae sin encabezado (`_c0`..`_c14`) y con `\N` (el marcador de
nulo de MySQL) donde `all_data.csv` tendría un valor real o vacío:

| Columna real | Posición | Ejemplo visto |
|---|---|---|
| `producto` | `_c0` | `CUADERNO FORMA ITALIANA` |
| `presentacion` | `_c1` | `96 HOJAS PASTA DURA` |
| `marca` | `_c2` | `ESTRELLA` |
| `categoria` | `_c3` | `MATERIAL ESCOLAR` |
| `catalogo` | `_c4` | `UTILES ESCOLARES` |
| `precio` | `_c5` | `25.9` |
| `fechaRegistro` | `_c6` | `\N` (nulo) |
| `cadenaComercial` | `_c7` | `ABASTECEDORA LUMEN` |
| `giro` | `_c8` | `PAPELERIAS` |
| `nombreComercial` | `_c9` | `ABASTECEDORA LUMEN SA DE CV` |
| `direccion` | `_c10` | `CANNES No. 6 ESQ. NIZA` |
| `estado` | `_c11` | `DISTRITO FEDERAL` |
| `municipio` | `_c12` | `TLALPAN` (con espacios de relleno en el crudo) |
| `latitud` | `_c13` | `19.29699` |
| `longitud` | `_c14` | `-99.12542` |

Este mapeo ya está aplicado en `recursos/spark/05_data_cleansing.ipynb` — probado con
esta misma muestra antes de entregarlo.

## 4. Dataset transversal del curso: `bank_transactions.csv`

Igual que en la versión anterior de este archivo (que usaba un generador sintético de
transacciones bancarias), aquí sí existe ya el dato real — mismo propósito, sin tener que
simular nada. Es el dataset que atraviesa `recursos/spark/03_spark_sql.ipynb` y
`04_pipeline_ml.ipynb`: primero se analiza con SQL (ranking de transacciones sospechosas
por ventana), después se usa para entrenar el modelo de fraude.

## 5. Asignación por perfil de alumno

Si el grupo es heterogéneo (más relevante en Especialidad), conviene repartir por
sector de interés en vez de que todos usen el mismo dataset:

| Perfil | Dataset asignado | Por qué |
|---|---|---|
| Consultores retail / macroeconomía | `all_data.csv` (19.7 GB) | Precios, competencia, inflación — vocabulario que ya conocen. |
| Banca / riesgo / compliance | `bank_transactions.csv` (7.5 GB) | Detección de patrones sospechosos con window functions — es además el dataset transversal del curso. |
| Ciberseguridad / TI | `war_tweets.txt` (22.5 GB) o `http_sentiment_raw.csv` (14.5 GB) | Procesamiento distribuido de texto no estructurado, a la escala real que justifica Spark. |

## 6. Cómo subir estos archivos a tu proyecto

Descárgalos del Drive del curso y súbelos a Cloud Storage (no a BigQuery directo, son
CSV/texto crudo — eso es justamente parte del ejercicio de la Sesión 6, Data Lakes):

```bash
gsutil cp bank_transactions.csv gs://<TU-BUCKET>/raw/bank_transactions/
```

Para los de >10 GB, sube desde una VM o Cloud Shell con buena banda ancha, no desde tu
laptop — o usa `gsutil -m cp` para paralelizar la subida.

## 7. Alternativas públicas y pesadas (si no tienes acceso al Drive del curso)

Estas no requieren el Drive — quedan como respaldo si compartes este repo fuera del
contexto del curso, o si alguien pierde acceso a los archivos originales. Se agregaron
opciones más pesadas (>1 GB) para que sigan siendo material real de Big Data, no
datasets de práctica pequeños:

- **NYC Taxi & Limousine Trips** (`bigquery-public-data.new_york_taxi_trips`) — mismo
  volumen y propósito que `all_data.csv`, pero ya vive en BigQuery, sin descargar nada.
- **GitHub Activity Data** (`bigquery-public-data.github_repos`) — metadata e historia
  de 2.8M+ repos públicos, varios TB en BigQuery. Alternativa para el perfil de TI si
  `war_tweets.txt` no está disponible.
- **Wikipedia dumps** (completos, con historial de ediciones) — datasets de texto masivo
  para NLP, alternativa a `war_tweets.txt`/`http_sentiment_raw.csv`.
- **Amazon Reviews** (Stanford, ~11 GB, 35M reviews) — alternativa de retail/NLP a
  `steam_reviews.csv` o `all_data.csv`.
- **NOAA weather data** (BigQuery público, 9,000 estaciones) — series de tiempo masivas,
  buena alternativa si se quiere variar el caso de negocio lejos de retail/finanzas.
- **Credit Card Fraud Detection** (Kaggle, `mlg-ulb/creditcardfraud`) — alternativa
  pequeña (285K filas) a `bank_transactions.csv` si el free tier no alcanza para 7.5 GB.
- **Carpetas de investigación FGJ CDMX** (oficial, actualizado mensualmente) —
  https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico
  — misma data que `carpetas_investigacion.csv` del Drive, por si ese archivo queda
  desactualizado con el tiempo.
- **FRED**, **S&P 500 histórico** (Kaggle), **Open Banking Tracker** (GitHub) — datos
  macro/mercado para variar el caso de negocio en Especialidad.

## 8. Generador sintético (solo si nada de lo anterior está disponible)

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 500_000

df = pd.DataFrame({
    "transaction_id": range(n),
    "timestamp": pd.date_range("2024-01-01", periods=n, freq="min"),
    "amount": np.round(np.random.exponential(1000, n), 2),
    "currency": np.random.choice(["MXN", "USD"], n),
})
df["is_suspicious"] = ((df["amount"] > 8000) & (np.random.rand(n) < 0.3)).astype(int)
df.to_csv("bank_transactions_sintetico.csv", index=False)
```

Mismo esquema mínimo que `bank_transactions.csv`, para que cualquier notebook de
`recursos/spark/` corra igual sin depender del Drive.
