# Proyecto de práctica: Radar de Señales Globales

> Un segundo ejemplo de a qué se debería parecer el proyecto final — complementario a
> [`recursos/proyecto-ejemplo/`](../proyecto-ejemplo/README.md) (Radar de Precios), no un
> reemplazo. Ese proyecto parte de un CSV masivo ya descargado (19.7 GB) — la etapa de
> "obtención de datos" ya está resuelta. **Este proyecto hace lo contrario a propósito:**
> construye esa etapa desde cero, combinando varias APIs públicas y gratuitas en vivo, para
> practicar el flujo completo (ingesta → persistencia → procesamiento) tal como lo vive un
> equipo de datos real, y para que cada una de las 5 V's tenga una fuente concreta que la
> demuestre — no solo una definición en un slide.

## La pregunta de negocio

**¿Un evento global (un sismo mayor, un pico de eventos negativos en las noticias
mundiales, un pico anómalo de edición en Wikipedia sobre un tema) se refleja — y en
cuánto tiempo — en el tipo de cambio peso-dólar o en la volatilidad del mercado cripto?**

Es la misma lógica que ya usan mesas de trading y áreas de riesgo: monitorear señales no
financieras (noticias, actividad sísmica, atención pública) como indicador adelantado de
movimiento financiero — antes de que el movimiento ya esté en el precio.

## Por qué estas fuentes, y no otras

Se eligieron 5 fuentes, **todas gratuitas, todas verificadas en 2026**, cada una ancla al
menos una de las 5 V's de forma real, no forzada:

| Fuente | V que demuestra | Por qué |
|---|---|---|
| **GDELT** (BigQuery público) | **Volumen** | Cientos de millones de eventos globales, actualizado cada 15 min, consultable directo en BigQuery sin descargar un solo archivo — volumen real sin necesidad de almacenarlo tú mismo. |
| **Wikipedia EventStreams** | **Velocidad** | Stream en vivo (Server-Sent Events) de cada edición a cualquier wiki de Wikimedia en el mundo — miles de eventos por minuto, sin key, sin límite. Streaming real, no un batch disfrazado. |
| **USGS Earthquake API** | **Velocidad** + **Veracidad** | Feed en tiempo real de sismicidad global, sin key, sin cuota. Y un caso de veracidad genuino: la magnitud de un mismo sismo **se revisa y corrige** en las horas posteriores conforme llegan más lecturas de sensores — no es un valor estático. |
| **OpenAQ v3** | **Variedad** + **Veracidad** | Calidad del aire de miles de sensores en el mundo (otro dominio, otro formato). Requiere key gratuita. Tiene huecos y fallas de calibración documentados — otro caso real de veracidad, distinto al de USGS. |
| **Frankfurter** + **CoinGecko** *(ya en el repo)* | **Variedad** (estructurado) + **Valor** | Tipo de cambio y mercado cripto — la señal financiera que se busca explicar. Ya usadas en [`recursos/etl-tipo-cambio/`](../etl-tipo-cambio/README.md) y [`recursos/etl-cripto/`](../etl-cripto/README.md); este proyecto las reutiliza en vez de reinventarlas. |

**Opcional (nivel 2, no obligatorio):** los eventos de GDELT traen un campo `SOURCEURL`
con el artículo de noticia original — extraer el titular de esas URLs completa la tercera
pata de Variedad (no estructurado: texto libre) sin depender de una API nueva.

## Las fuentes, con endpoint y autenticación exactos

| Fuente | Endpoint | Auth | Formato | Frecuencia |
|---|---|---|---|---|
| GDELT | `gdelt-bq.gdeltv2.events` / `.gkg` (dataset público de BigQuery) | Ninguna — solo tu proyecto de GCP | Tablas SQL | Actualiza cada 15 min |
| Wikipedia EventStreams | `https://stream.wikimedia.org/v2/stream/recentchange` | Ninguna | SSE / JSON por línea | Continuo |
| USGS Earthquakes | `https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson/all_hour.geojson` (o `/all_day`, `/2.5_week`, etc.) | Ninguna | GeoJSON | Actualiza cada minuto |
| OpenAQ | `https://api.openaq.org/v3/...` | API key gratis — registro en https://explore.openaq.org | JSON | Bajo demanda |
| Frankfurter | `https://api.frankfurter.app/latest?from=USD&to=MXN` | Ninguna | JSON | Bajo demanda |
| CoinGecko | `https://api.coingecko.com/api/v3/simple/price?...` | Ninguna (tier público) | JSON | Bajo demanda, rate-limited |
| Banxico SIE *(opcional, upgrade de Frankfurter)* | `https://www.banxico.org.mx/SieAPIRest/service/v1/` | Token gratis por correo | JSON | Bajo demanda |

## Arquitectura, 100% en free tier de GCP

Ningún componente de este diseño requiere salir del *Always Free* — los límites exactos
(verificados en 2026, pueden cambiar, revisar antes de arrancar):

| Componente | Rol | Límite gratis |
|---|---|---|
| **Cloud Storage** | Capa bronze — JSON/GeoJSON crudo tal como llega de cada API | 5 GB-mes |
| **Compute Engine `e2-micro`** | Un listener persistente y ligero (Python) conectado al stream de Wikipedia — mismo patrón que [`recursos/streaming/producer_transacciones_stream.py`](../streaming/producer_transacciones_stream.py), pero consumiendo en vez de produciendo | 1 instancia/mes en `us-central1`, `us-west1` o `us-east1` |
| **Cloud Scheduler + Cloud Functions** | Polling periódico de USGS, OpenAQ, Frankfurter y CoinGecko (cada 5-15 min), escribe a Cloud Storage | 3 jobs de Scheduler + 2M invocaciones de Functions/mes |
| **Pub/Sub** *(opcional)* | Desacopla el listener de Wikipedia de quien lo procesa — mismo patrón conceptual de Sesión 9-10 (streaming) | 10 GB/mes |
| **BigQuery** | GDELT se consulta directo (sin ingesta); tablas propias silver/gold con los features cruzados | 1 TB de consultas/mes + 10 GB de storage |
| **Managed Service for Apache Spark** *(Maestría)* / **BigQuery SQL** *(Especialidad)* | Procesamiento: features por ventana de tiempo, join entre señal de evento y movimiento financiero | Se paga por uso — usar clusters efímeros, igual que en el resto del curso |
| **Looker Studio** | Visualización — mapa de sismos + eventos, serie de tiempo de tipo de cambio con anotaciones de eventos | Gratis |

**Guardrails de costo (importantes incluso en free tier):**
- GDELT es enorme — **nunca** `SELECT *` sin filtrar por `SQLDATE`/partición, o se agota el
  TB gratis de BigQuery en una sola consulta.
- Apagar la VM `e2-micro` cuando no esté en uso activo, aunque sea gratis — buena práctica,
  no hábito de "total es gratis, no importa".
- La alerta de presupuesto de [`environment/gcp-setup.md`](../../environment/gcp-setup.md)
  aplica igual aquí — configúrala desde el día 1.

## El pipeline, versión Maestría (técnico completo)

| Etapa | Qué se hace | Sesión que ya enseña esto |
|---|---|---|
| **Ingesta streaming** | Listener de Wikipedia EventStreams en la VM `e2-micro`, escribiendo lotes a Cloud Storage (o Pub/Sub) | Sesiones 9-10 (mismo patrón que `producer_transacciones_stream.py`) |
| **Ingesta batch/polling** | Cloud Functions programadas (Scheduler) para USGS, OpenAQ, Frankfurter, CoinGecko | Sesión 1 (fuentes de datos) |
| **Data Lake (bronze)** | JSON/GeoJSON crudo en Cloud Storage, particionado por fecha/hora de ingesta | Sesión 1, Sesión 6 |
| **Features** | Por ventana de tiempo (ej. 1h): conteo de sismos por magnitud, `AvgTone` promedio de GDELT, conteo de ediciones de Wikipedia, variación % de tipo de cambio/cripto en la misma ventana | Sesión 5 (Pipeline/Transformer/Estimator) |
| **Lakehouse** | Tabla Iceberg de features cruzados por ventana de tiempo — se vuelve a calcular conforme llegan correcciones (ej. magnitud de sismo revisada) | Sesiones 7-8 |
| **Modelo** | Correlación/regresión: ¿la variación de tipo de cambio en la ventana `t+1` se explica por las señales de la ventana `t`? (Granger causality simplificado, o un modelo de regresión con lag) | Sesión 6 |
| **Serving** | Endpoint que responde "¿hay una señal de riesgo elevada ahora mismo?" con el score más reciente | Sesión 11 |
| **Monitoreo** | Reto real: los sismos y picos de noticias son eventos raros (clase desbalanceada) — el modelo puede parecer bueno solo por predecir "sin riesgo" casi siempre; hay que vigilar recall sobre los eventos reales, no solo accuracy | Sesión 11-12 |
| **Orquestación** | Para este proyecto de práctica, mantener la orquestación ligera (Cloud Scheduler directo) para no salirse del free tier — Airflow/Cloud Composer (Sesión 12) es la opción para el proyecto final con presupuesto real | Sesión 12 |

**Capstone (Sesión 13):** el punto técnico más defendible es la corrección de veracidad —
que el pipeline reprocese features cuando USGS actualiza la magnitud de un sismo horas
después es un caso real de *late-arriving data*, el mismo problema que enfrenta cualquier
pipeline financiero cuando llega una corrección.

## El mismo proyecto, versión Especialidad (low-code)

| Etapa | Cómo se hace en Especialidad |
|---|---|
| **Ingesta** | Un Cloud Function simple (o incluso Apps Script programado) que llama cada API y guarda el JSON en Cloud Storage — sin Spark |
| **Carga a BigQuery** | `bq load` o la consola web, directo desde Cloud Storage — GDELT no requiere carga, ya está en BigQuery |
| **Análisis** | SQL con window functions sobre ventanas de tiempo — mismo patrón ya guiado en la Sesión 3 |
| **Visualización** | Looker Studio: mapa de sismos coloreado por magnitud + serie de tiempo de tipo de cambio con marcadores en los días de mayor actividad — el mismo botón "Explorar con Looker Studio" de la Sesión 3 |
| **Apoyo técnico** | Si el equipo quiere el listener de streaming de Wikipedia (el único pedazo que no es 100% low-code), se apoya en el equipo técnico del grupo |

## Cómo usar este documento

No es un notebook para correr — es la maqueta conceptual de un proyecto que demuestra las
5 V's con fuentes reales, gratuitas y verificadas, para decidir con qué armar el proyecto
final antes de tener que improvisarlo bajo presión. Referenciado desde `sesion-00/README.md`
de ambos tracks, junto a `recursos/proyecto-ejemplo/`.

## Ver también

- [`recursos/proyecto-ejemplo/`](../proyecto-ejemplo/README.md) — el otro modelo de
  proyecto final, partiendo de un dataset masivo ya descargado en vez de APIs en vivo
- [`recursos/etl-tipo-cambio/`](../etl-tipo-cambio/README.md) y
  [`recursos/etl-cripto/`](../etl-cripto/README.md) — las piezas de tipo de cambio/cripto
  que este proyecto reutiliza tal cual
- [`recursos/streaming/producer_transacciones_stream.py`](../streaming/producer_transacciones_stream.py) —
  el patrón de listener persistente que el ingestor de Wikipedia EventStreams debe seguir
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — alerta de presupuesto,
  imprescindible antes de dejar corriendo cualquier polling programado
- [`recursos/datasets/README.md`](../datasets/README.md), Sección 7 — alternativas
  públicas ya en BigQuery (NYC Taxi, GitHub, NOAA) si se prefiere no depender de APIs en vivo
