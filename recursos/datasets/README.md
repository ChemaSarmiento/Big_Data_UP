# Datasets de ejemplo para el curso

El repo original no traía un dataset propio reutilizable entre sesiones (los notebooks
usaban archivos sueltos, ej. `Spain_Tenders_20220129.ipynb`). Aquí se proponen datasets
reales, gratuitos y ya probados en el ecosistema de GCP, más un generador de datos
sintéticos para cuando el dataset real es demasiado grande para el free tier.

## 1. Dataset principal transversal (recomendado)

**NYC Taxi & Limousine Trips** — disponible directamente como dataset público de
BigQuery (`bigquery-public-data.new_york_taxi_trips`), sin necesidad de descargar nada.
Es el dataset más usado en cursos de Big Data precisamente porque ya está en BigQuery,
tiene volumen real (cientos de millones de filas) y se puede recortar por fecha para
que cada lab controle cuánto procesa. Útil para las sesiones de SQL distribuido, Spark
y Data Lakes.

```sql
SELECT COUNT(*) FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022`;
```

## 2. Dataset orientado a finanzas/fraude (para el contexto bancario del curso)

Como el público del curso viene mayormente de banca/riesgo, estos dos hacen que el
capstone se sienta relevante desde el día 1:

- **Credit Card Fraud Detection** (Kaggle, `mlg-ulb/creditcardfraud`) — ~285,000
  transacciones, altamente desbalanceado (0.17% fraude), variables ya anonimizadas
  (PCA). Ideal para el pipeline de ML de la Sesión 4-5 de Maestría porque ya trae una
  columna binaria de fraude lista para usar como `label`.
- **Home Credit Default Risk** (Kaggle) — más grande y con múltiples tablas
  relacionadas (aplicación, historial de buró, pagos previos), lo que lo hace mejor
  para practicar joins a escala en Hive/Spark SQL, no solo un modelo simple.

Ambos se descargan de Kaggle (requiere cuenta gratuita) y se suben a Cloud Storage con
`gsutil cp` para usarse igual que cualquier otro dataset del curso.

## 3. Generador de datos sintéticos (para los scripts de `recursos/spark/` y `recursos/hive/`)

Los scripts de ejemplo (`transacciones.csv`) asumen columnas `sucursal, tipo_transaccion,
monto, cliente_id, es_fraude, fecha`. Si se prefiere no depender de Kaggle (por ejemplo,
en la Sesión 1 antes de que todos tengan cuenta de Kaggle configurada), este generador
produce un CSV compatible:

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 500_000

df = pd.DataFrame({
    "id_transaccion": range(n),
    "fecha": pd.date_range("2024-01-01", periods=n, freq="min"),
    "sucursal": np.random.choice(["sucursal_norte", "sucursal_sur", "sucursal_centro"], n),
    "tipo_transaccion": np.random.choice(["retiro", "deposito", "transferencia"], n),
    "monto": np.round(np.random.exponential(1000, n), 2),
    "cliente_id": [f"CLI{i:06d}" for i in np.random.randint(0, 20_000, n)],
})
df["es_fraude"] = ((df["monto"] > 8000) & (np.random.rand(n) < 0.3)).astype(int)

df.to_csv("transacciones.csv", index=False)
```

## 4. Otros datasets públicos de BigQuery útiles como alternativa/complemento

- `bigquery-public-data.chicago_taxi_trips` — alternativa más ligera al de NYC.
- `bigquery-public-data.ga4_obfuscated_sample_ecommerce` — datos de e-commerce (Google
  Merchandise Store), útil si se quiere variar el caso de negocio en Especialidad.
- GDELT (`gdelt-bq.gdeltv2`) — eventos globales actualizados cada 15 min, bueno como
  ejemplo de dataset que crece constantemente para la sesión de streaming.

Todos son consultables gratis dentro del 1 TB/mes del Always Free tier de BigQuery.

## 5. Dataset real del curso: Carpetas de investigación (CDMX)

El repo original (`hive/hive_commands.sql`, `hive_commands_updated.sql`) usaba tres
datasets propios subidos a un bucket del curso (`public-bucket-up-2022`): carpetas de
investigación (criminalidad), logs HTTP con sentimiento, y correos corporativos
sintéticos. **No pude verificar si ese bucket sigue activo** desde mi entorno (sin salida
a internet). Para el de criminalidad, hay una alternativa mejor de todos modos: la fuente
**oficial**, pública y actualizada mensualmente:

**Carpetas de investigación FGJ CDMX** —
https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico

Ver `recursos/hive/hive-queries.sql` (Sección 3) para el lab completo con este dataset,
incluyendo partitioning y bucketing.

Si el bucket original (`public-bucket-up-2022`) sigue vivo, los otros dos datasets
(`http_sentiment_raw.csv`, `email.csv`) también sirven — pero antes de usarlos en clase,
confirma que el bucket responda (`gsutil ls gs://public-bucket-up-2022/`).

## 6. Datos macro y de mercado (para variar el caso de negocio, especialmente Especialidad)

- **FRED** (Federal Reserve Economic Data) — API gratuita sin necesidad de tarjeta,
  indicadores macro (inflación, tasas, empleo). Buena para la Sesión 1 de Especialidad
  ("¿cuándo sí se justifica Big Data?") con datos que la audiencia de banca reconoce.
- **S&P 500 histórico** (Kaggle, varios datasets bajo ese nombre) — precios diarios de
  las empresas del S&P 500, útil para series de tiempo y feature engineering financiero.
- **Open Banking Tracker** (GitHub, `AperiData/open-banking-tracker` y proyectos
  relacionados) — snapshots diarios de APIs de open banking del Reino Unido (Barclays,
  HSBC, Lloyds, NatWest, Santander). Consistente con el interés bancario del grupo, y es
  data real de producción de bancos, no sintética.

## 7. Sobre el Drive que compartiste

El folder de Google Drive que mandaste (`Archivos_Big_Data`) pide inicio de sesión para
listar su contenido — no lo pude explorar automáticamente desde aquí (ni con el enlace
público, ni buscándolo). Si me compartes los nombres de archivo o los datasets que ya
tenías propuestos ahí, los reviso y los integro a esta lista; si prefieres, también
puedo trabajar a partir de una exportación en CSV/texto del listado de esa carpeta.
