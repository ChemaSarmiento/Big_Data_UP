# Proyecto de práctica: Radar de Precios

> Un proyecto completo, imaginado como ejemplo de a qué se debería parecer el
> proyecto final — en ambos tracks. Usa datos reales ya catalogados en
> `recursos/datasets/README.md`, deliberadamente **distintos** al hilo de fraude
> bancario que ya recorre el curso (`bank_transactions.csv`), para que sirva como
> práctica genuina y no como repetir la demo de clase con otro nombre.

## La pregunta de negocio

**¿Se puede detectar, con datos de precios reportados por comercios, cuándo un
producto en una región específica muestra un patrón de alza anómala que sugiere
especulación o escasez incipiente — antes de que se vuelva noticia?**

## Por qué esto, y por qué ahora

México ha vivido episodios recurrentes de alzas especulativas y escasez
percibida — limón, aceite, tortilla, gas — donde el patrón de precio ya
mostraba señales en los reportes oficiales días antes de volverse un problema
mediático. **PROFECO (Procuraduría Federal del Consumidor) tiene el mandato
legal de monitorear esto**, y "Quién es Quién en los Precios" es exactamente el
programa que genera el dato que este proyecto usa — no es un caso hipotético,
es el mandato real de la institución dueña del dataset.

## A quién beneficia

- **PROFECO** — alertas tempranas para priorizar investigaciones, en vez de
  reaccionar después de que el alza ya es noticia.
- **Cadenas de retail** — ajustar inventario/abasto ante una señal temprana de
  demanda anómala en una región.
- **Consumidores** — una alerta pública ("este producto está subiendo de forma
  atípica en tu zona") con la misma lógica que ya usan apps de precios de
  gasolina.

## Los datos (ya reales, ya catalogados — sin buscar nada nuevo)

| Archivo | Tamaño | Rol en el proyecto |
|---|---|---|
| `all_data.csv` | 19.7 GB | Serie histórica de precios por producto/cadena/municipio — la fuente principal |
| `quien_es_quien.csv` | 15.4 GB | Mismo dato, sin limpiar (sin encabezados, `\N` como nulo) — ejercicio de calidad de datos real, no simulado |

Ambos solos ya superan los 15GB del requisito institucional — no hace falta
combinar más fuentes, aunque `carpetas_investigacion.csv` (CDMX) podría
añadirse después como señal de contexto social por zona.

## El pipeline, versión Maestría (técnico completo)

Mapeado a las sesiones donde cada pieza ya se enseña — no es tecnología nueva,
es la misma que ya construyen sesión por sesión, aplicada a una pregunta
distinta:

| Etapa | Qué se hace | Sesión que ya enseña esto |
|---|---|---|
| **Ingesta + limpieza** | Reconciliar `all_data.csv` con `quien_es_quien.csv` (mismo esquema, sin encabezados en el segundo) | `05_data_cleansing.ipynb` (S7-8, mismo patrón) |
| **Features** | Por producto+región+cadena: variación % día a día, volatilidad de ventana móvil (7/30 días), desviación vs. precio promedio nacional del mismo producto | Sesión 5 (Pipeline/Transformer/Estimator) |
| **Lakehouse** | Tabla Iceberg de precios, versionada por fecha de reporte — PROFECO corrige precios mal reportados, así que `MERGE INTO` aplica de verdad, no como ejercicio artificial | Sesiones 7-8 |
| **Modelo** | Detección de anomalías: z-score de la variación vs. la distribución histórica del mismo producto/región, o un `GBTClassifier` si se etiqueta una muestra de alzas históricas conocidas como positivas | Sesión 6 |
| **Streaming** | Simular reportes de precio llegando en tiempo real (mismo patrón que `producer_transacciones_stream.py`, adaptado a filas de precio) → alertas por ventana cuando la variación supera un umbral | Sesiones 9-10 |
| **Serving** | Endpoint que responde "¿este producto/región está en alerta ahora mismo?" | Sesión 11 |
| **Monitoreo** | El reto real aquí: distinguir **drift natural** (inflación, que sube el precio promedio con el tiempo, es normal) de **anomalía real** (alza puntual que no explica la inflación general) — el PSI de la Sesión 11 no basta solo, hay que combinarlo con la desviación estacional | Sesión 11-12 |
| **Orquestación** | DAG que reentrena el modelo de anomalías cada semana + dispara alertas del día | Sesión 12 |

**Capstone (Sesión 13):** el pipeline completo, con la distinción
drift-natural-vs-anomalía como el punto técnico más defendible frente al
jurado — es más interesante que el caso de fraude porque la "normalidad" se
mueve con el tiempo (inflación), no es estática.

## El mismo proyecto, versión Especialidad (low-code, mismo estándar institucional)

Misma pregunta de negocio, mismo dato — resuelto con las herramientas guiadas
del track:

| Etapa | Cómo se hace en Especialidad |
|---|---|
| **Carga** | `all_data.csv` subido directo a BigQuery (sin Spark) |
| **Análisis** | SQL con window functions (`AVG(...) OVER (PARTITION BY producto ORDER BY fecha ROWS BETWEEN 7 PRECEDING AND CURRENT ROW)`) — exactamente el patrón ya guiado en la Sesión 3 |
| **Visualización** | Looker Studio: mapa de alertas por estado/municipio, coloreado por severidad de variación — el mismo botón "Explorar con Looker Studio" de la Sesión 3 |
| **Apoyo técnico** | Si el equipo quiere ir más allá de SQL (ej. un umbral estadístico más sofisticado), se apoya en el equipo técnico del grupo — nunca escribiendo Spark desde cero |

El documento final es idéntico en estructura al de Maestría (resumen
ejecutivo, revisión de datos, proceso, resultados, a quién beneficia) — solo
cambia la profundidad de código de la sección de metodología.

## Cómo usar este documento

No es un notebook para correr — es la maqueta conceptual que responde "¿a qué
se debería parecer mi proyecto final?" antes de tener que decidirlo bajo
presión en la Sesión 5 (Maestría) o Sesión 3 (Especialidad). Referenciado desde
`sesion-00/README.md` de ambos tracks.

## Ver también

- [`recursos/datasets/README.md`](../datasets/README.md) — catálogo completo, incluyendo por qué `quien_es_quien.csv` = `all_data.csv` sin limpiar
- [`recursos/spark/05_data_cleansing.ipynb`](../spark/05_data_cleansing.ipynb) — el mismo ejercicio de reconciliación de esquema que este proyecto necesita
- [`recursos/hive/hive-queries.sql`](../hive/hive-queries.sql) Sección 3 — patrón de partition pruning aplicable a una tabla de precios por fecha
