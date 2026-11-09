# Syllabus: Sistemas de Datos Distribuidos (SDD)

## Resumen Ejecutivo del Programa

Este programa ha sido modernizado para responder a las exigencias actuales del mercado de tecnología y datos. Evoluciona de arquitecturas tradicionales de procesamiento distribuido hacia un **Ecosistema Moderno de Datos en la Nube**, integrando **Data Lakehouses**, **Arquitectura Medallion**, **PySpark**, **Procesamiento en Tiempo Real**, y la convergencia de Big Data con **Modelos de Lenguaje Grande (LLMs)** y **Generación Aumentada por Recuperación (RAG)**.

El curso se estructura en dos modalidades de aprendizaje adaptadas a perfiles diferenciados, utilizando un entorno de laboratorio común basado en **Google Cloud Platform (GCP)** (con el fondo de 300 USD por estudiante) y organizado alrededor de un **Proyecto Final Incremental**.

---

## 🎯 Estructura de Tracks

| Métrica / Aspecto | Track 1: Especialidad | Track 2: Maestría en Ciencia de Datos |
| :--- | :--- | :--- |
| **Perfil Destino** | Ejecutivo, Negocio, Product Owner, Manager | Técnico, Data Engineer, Data Scientist, MLOps | 
| **Enfoque Principal** | Gobernanza, Valor de Negocio, Consultas y GenAI | Arquitectura, Pipelines, PySpark, Streaming y ML/LLMs |
| **Profundidad de Código** | SQL Esencial, Visualización y No-Code/Low-Code | PySpark, SQL Avanzado, APIs, Scripts de Automatización |
| **Entorno GCP** | BigQuery, Looker Studio, Vertex AI Studio | Dataproc, Cloud Storage, Pub/Sub, BigQuery, Vertex AI |

---

## Track 1: Especialidad (Perfil Ejecutivo y de Negocio)

**Objetivo:** Comprender el ecosistema moderno de datos en la nube, gobernar los activos de datos y extraer valor de negocio mediante arquitecturas avanzadas y herramientas de análisis, sin requerir programación en código complejo.

### Módulo 1: Introducción al Ecosistema Cloud y Big Data
* Conceptos clave de Cloud Computing y aprovisionamiento del entorno GCP.
* Evolución del almacenamiento: Del Data Warehouse tradicional al Data Lake y Data Lakehouse.
* Casos de uso empresariales de Big Data (Banca, Retail, Salud, Logística).

### Módulo 2: Arquitectura y Gestión de Datos
* Paradigmas modernos de ingesta y transformación: ETL vs. ELT.
* Arquitectura Medallion simplificada: Entendiendo la propuesta de valor de las capas **Bronze** (datos crudos), **Silver** (datos limpiados) y **Gold** (agregados de negocio).
* Gobierno de datos, calidad, seguridad, compliance y privacidad en la nube (GDPR/HIPAA).

### Módulo 3: Acceso y Consulta de Grandes Datos (SQL Fast Track)
* Bases de datos distribuidas y motor de BigQuery en GCP.
* **SQL Fast Track:** Fundamentos de SQL para analistas y ejecutivos.
* Consultas esenciales, agregaciones, filtros y joins sobre grandes volúmenes de datos.

### Módulo 4: Análisis Avanzado y GenAI en los Negocios
* Fundamentos de Machine Learning para la toma de decisiones empresariales.
* Introducción a los Modelos de Lenguaje Grande (LLMs) y la Inteligencia Artificial Generativa.
* Concepto de RAG (Retrieval-Augmented Generation) aplicado a datos corporativos.
* Visualización de datos y dashboards ejecutivos (Looker Studio / Tableau).

### 🏆 Proyecto Final Incremental (Track 1)
* **Descripción:** Diseñar y justificar una arquitectura de datos (Data Lakehouse) para resolver un problema de negocio real.
* **Entregables:**
  1. Documento de diseño arquitectónico y estrategia de gobernanza.
  2. Consultas SQL sobre un dataset pre-cargado en BigQuery para responder preguntas clave de negocio.
  3. Dashboard ejecutivo interactivo con los hallazgos principales.

---

## Track 2: Maestría en Ciencia de Datos (Perfil Técnico e Ingeniería)

**Objetivo:** Desarrollar habilidades avanzadas de ingeniería de datos, procesamiento distribuido en masa, streaming en tiempo real y despliegue de infraestructura para alimentar modelos de Machine Learning y sistemas GenAI/LLM.

### Módulo 1: Infraestructura Cloud y Modern Data Stack
* Configuración avanzada y administración de recursos en GCP (Storage, IAM, Quotas).
* Diseños e implementación práctica de Data Lakes y Data Lakehouses.
* Construcción técnica de la **Arquitectura Medallion**:
  * Capa Bronze: Almacenamiento inmutable y formatos abiertos (Parquet/Delta/Iceberg).
  * Capa Silver: Desduplicación, esquemas estrictos y limpieza automatizada.
  * Capa Gold: Modelado dimensional y tablas optimizadas para consulta/ML.

### Módulo 2: Procesamiento Distribuido a Escala (Apache Spark)
* Arquitectura de Apache Spark y PySpark (vs. MapReduce tradicional).
* RDDs, DataFrames y optimización de planes de ejecución (Catalyst Optimizer, Tungsten).
* **SQL Avanzado en Spark:** Consultas analíticas complejas, funciones de ventana (Window Functions) y optimización de JOINs a gran escala.

### Módulo 3: Procesamiento en Tiempo Real (Streaming)
* Fundamentos de arquitecturas Lambda y Kappa.
* Event Driven Architectures y mensajería distribuida (Google Pub/Sub / Apache Kafka).
* Procesamiento continuo con **Spark Structured Streaming** e integración con capas Silver/Gold.

### Módulo 4: Integración de Big Data, MLOps y GenAI / LLMs
* Machine Learning a escala con Spark MLlib y Vertex AI.
* Generación Aumentada por Recuperación (RAG) sobre Big Data:
  * Embeddings masivos y bases de datos vectoriales.
  * Conexión de Datalakes corporativos con LLMs para consulta en lenguaje natural.

### 🏆 Proyecto Final Incremental (Track 2)
* **Descripción:** Implementación End-to-End de un pipeline de Big Data y su integración con modelos predictivos o de GenAI.
* **Entregables:**
  1. Pipeline de ingesta en tiempo real o por lotes (Batch/Streaming) en GCP Cloud Storage / Pub/Sub.
  2. Scripts de procesamiento en **PySpark** estructurados bajo la **Arquitectura Medallion** (Bronze ➔ Silver ➔ Gold).
  3. Exposición del dataset Gold en BigQuery y consumo desde un modelo predictivo o pipeline RAG con LLMs.

---

## 🛠️ Tecnologías y Herramientas del Curso

* **Cloud Provider:** Google Cloud Platform (GCP)
* **Motores de Datos:** Google BigQuery, Cloud Dataproc
* **Procesamiento Distribuido:** Apache Spark (PySpark, Spark SQL, Structured Streaming)
* **Almacenamiento y Formatos:** GCP Cloud Storage, Parquet / Delta Lake
* **Mensajería:** Google Cloud Pub/Sub
* **IA y Analítica:** Vertex AI, Python, SQL, Looker Studio

# Guía de Laboratorios Prácticos (Proyecto Incremental)

Para asegurar la cohesión del proyecto a lo largo de las 8 sesiones, utilizaremos un **Dataset de Retail / E-commerce** (por ejemplo, el dataset público de *Olist* o uno sintético de ventas). Este dominio permite casos de uso de negocio claros (KPIs, retención, ventas) y retos técnicos reales (volumen, uniones complejas, predicción).

---

## Track 1: Especialidad (Perfil Ejecutivo / Negocio)
**Objetivo del Proyecto:** Construir un Data Warehouse analítico básico, crear un Dashboard directivo y utilizar GenAI para extraer insights de negocio.
**Herramientas Principales:** Google Cloud Storage (GCS), BigQuery (UI), Looker Studio, Vertex AI Studio.

### Sesión 1: Setup y Primer Contacto con la Nube
*   **Actividad:** Activación del crédito de 300 USD en GCP y configuración inicial.
*   **Laboratorio:** 
    *   Crear un Proyecto en GCP ("retail-analytics-prod").
    *   Familiarización con la consola y configuración de alertas de facturación (Billing Alerts) para no exceder el presupuesto.
    *   Crear un bucket en Google Cloud Storage (GCS).
*   **Entregable Incremental:** Entorno de GCP listo, seguro y presupuestado.

### Sesión 2: Ingesta de Datos Crudos (Capa Bronze)
*   **Actividad:** Cargar la historia de la empresa en la nube.
*   **Laboratorio:**
    *   Subir archivos CSV (Clientes, Órdenes, Pagos, Productos) manualmente al bucket de GCS.
    *   En BigQuery, crear un Dataset llamado `retail_bronze`.
    *   Crear "Tablas Externas" en BigQuery que apunten a los CSVs en GCS.
*   **Entregable Incremental:** Datos accesibles mediante SQL sin haberlos duplicado físicamente en la base de datos.

### Sesión 3: Limpieza y Refinamiento (Capa Silver)
*   **Actividad:** Estandarizar la información para el análisis.
*   **Laboratorio:**
    *   Usar SQL en BigQuery para identificar nulos y duplicados.
    *   Crear un Dataset `retail_silver`.
    *   Usar `CREATE TABLE AS SELECT (CTAS)` para guardar versiones limpias de las tablas, estandarizando formatos de fecha y texto (ej. mayúsculas/minúsculas).
*   **Entregable Incremental:** Tablas nativas en BigQuery, limpias y optimizadas para consultas más rápidas.

### Sesión 4: Exploración Analítica (SQL Fast Track I)
*   **Actividad:** Responder las primeras preguntas del negocio.
*   **Laboratorio:**
    *   Ejercicios prácticos con `SELECT`, `WHERE` y `GROUP BY`.
    *   Preguntas a resolver: *¿Cuántas órdenes hay por estado/región?*, *¿Cuáles son los 10 productos más vendidos?*, *¿Cuál es el ticket promedio por mes?*.
*   **Entregable Incremental:** Un script SQL con las consultas exploratorias base guardado en BigQuery.

### Sesión 5: El Modelo de Negocio / Data Mart (Capa Gold)
*   **Actividad:** Consolidar toda la información en una "Gran Tabla de Verdad".
*   **Laboratorio:**
    *   Uso de `JOINs` para unir Clientes + Órdenes + Pagos.
    *   Creación de un Dataset `retail_gold`.
    *   Crear una Vista Materializada (`datamart_ventas_kpi`) utilizando CTEs (`WITH`) y Window Functions para calcular promedios móviles de ventas a 7 días y rankear a los mejores clientes.
*   **Entregable Incremental:** Tabla analítica final (Capa Gold) lista para ser consumida por herramientas de BI.

### Sesión 6: Visualización Directiva (Looker Studio)
*   **Actividad:** Dar vida a los datos para la toma de decisiones.
*   **Laboratorio:**
    *   Conectar Looker Studio nativamente con la vista `datamart_ventas_kpi` de BigQuery.
    *   Diseñar un Dashboard interactivo: 
        *   Tarjetas de KPI (Total Ventas, Usuarios Activos).
        *   Gráfico de series de tiempo (Ventas por mes).
        *   Mapa geográfico de calor (Ventas por estado).
        *   Filtros interactivos (Por categoría de producto, rango de fechas).
*   **Entregable Incremental:** Dashboard funcional y publicado.

### Sesión 7: GenAI para Insights Ejecutivos
*   **Actividad:** Usar Inteligencia Artificial para resumir hallazgos.
*   **Laboratorio:**
    *   Exportar un resumen estadístico desde BigQuery a CSV (ej. "Top 50 clientes y su comportamiento").
    *   Ingresar a Vertex AI Studio (Multimodal prompt).
    *   Crear un prompt ejecutivo: *"Eres un analista de ventas. Analiza estos datos e identifica 3 anomalías y redacta un correo para el CEO proponiendo una campaña de marketing."*
*   **Entregable Incremental:** Reporte generado por IA integrado al análisis final.

### Sesión 8: Presentación del Proyecto Final
*   **Actividad:** Role-play ejecutivo.
*   **Laboratorio:** No hay código nuevo. Se simula una junta directiva donde el alumno expone el problema, muestra el Dashboard en Looker Studio y comparte los insights generados por la IA para justificar una decisión de negocio.

---

## Track 2: Maestría en Ciencia de Datos (Perfil Técnico / Ingeniería)
**Objetivo del Proyecto:** Construir un pipeline distribuido End-to-End procesando datos en batch/streaming con PySpark, aplicando optimizaciones técnicas y preparando vectores para LLMs.
**Herramientas Principales:** GCS, Dataproc (PySpark), Cloud Pub/Sub, BigQuery.

### Sesión 1: Infraestructura y Ecosistema Hadoop/Cloud
*   **Actividad:** Desplegar la infraestructura como código (o vía CLI).
*   **Laboratorio:**
    *   Uso de Google Cloud Shell / SDK.
    *   Crear una estructura de Data Lake en GCS con buckets lógicos: `raw-zone`, `staging-zone`, `analytics-zone`.
    *   Aprovisionar un clúster de Dataproc con JupyterLab habilitado.
*   **Entregable Incremental:** Infraestructura base operativa.

### Sesión 2: Ingesta y Optimización de Formatos (Capa Bronze)
*   **Actividad:** Traducir datos crudos a formatos de Big Data.
*   **Laboratorio:**
    *   Cargar dataset crudo (CSVs) de E-commerce al bucket `raw-zone`.
    *   Abrir Jupyter Notebook en Dataproc.
    *   Escribir el primer script en PySpark para leer los CSVs y escribirlos en formato **Parquet** (o Delta/Iceberg si se prefiere) en la `staging-zone`. 
*   **Entregable Incremental:** Pipeline básico de compresión y columnarización (Capa Bronze).

### Sesión 3: Transformaciones Distribuidas (PySpark Core)
*   **Actividad:** Manipulación de DataFrames y limpieza a escala.
*   **Laboratorio:**
    *   Lectura de los archivos Parquet.
    *   Aplicación de transformaciones *Narrow* y *Wide*.
    *   Casteo de tipos de datos, eliminación de registros corruptos.
    *   Manejo de esquemas estrictos (`StructType`).
*   **Entregable Incremental:** Script PySpark que garantiza la calidad técnica del dato.

### Sesión 4: Joins Avanzados y Feature Engineering (Capa Silver)
*   **Actividad:** Unir los dominios de datos optimizando el rendimiento.
*   **Laboratorio:**
    *   Unir la tabla de `Ventas` (Grande) con la tabla de `Productos` (Pequeña).
    *   Implementar un **Broadcast Hash Join** en PySpark para optimizar el cruce de `Productos`.
    *   Crear features temporales usando Window Functions en PySpark (ej. *días desde la última compra por cliente*).
    *   Escribir el resultado particionado por `año/mes` en la `analytics-zone` (Capa Silver).
*   **Entregable Incremental:** Dataset Silver enriquecido y particionado estratégicamente.

### Sesión 5: Streaming de Datos (Arquitectura Lambda/Kappa)
*   **Actividad:** Procesar transacciones en tiempo real.
*   **Laboratorio:**
    *   Crear un tópico en Google Cloud Pub/Sub (`order-events`).
    *   Usar un script en Python para publicar mensajes JSON simulando compras en vivo.
    *   Escribir un script con **Spark Structured Streaming** que escuche el tópico de Pub/Sub, aplique un *Tumbling Window* de 1 minuto para calcular ventas por minuto y lo imprima en consola (o memoria).
*   **Entregable Incremental:** Módulo de streaming funcional integrado al ecosistema.

### Sesión 6: Machine Learning Distribuido (Spark MLlib)
*   **Actividad:** Entrenar un modelo sobre el cluster.
*   **Laboratorio:**
    *   Leer los datos limpios de la `analytics-zone`.
    *   Usar `pyspark.ml` para crear un Pipeline (StringIndexer, VectorAssembler).
    *   Entrenar un modelo de Random Forest para predecir si un cliente hará *Churn* (abandono) basado en su histórico de compras.
    *   Evaluar el modelo (Area Under ROC) y guardarlo en GCS.
*   **Entregable Incremental:** Modelo predictivo entrenado de forma distribuida.

### Sesión 7: Preparación de Datos para LLMs (Vectorización)
*   **Actividad:** Conectar el ecosistema Big Data con GenAI.
*   **Laboratorio:**
    *   Extraer el catálogo de productos (descripciones en texto) con PySpark.
    *   Utilizar una UDF (User Defined Function) en Pandas/Spark que consuma una API de Embeddings (o un modelo Open Source pequeño) para convertir las descripciones de texto en *Vectores (Embeddings)*.
    *   Guardar este dataset vectorizado en BigQuery (Capa Gold) listo para ser consumido por un sistema de búsqueda semántica (RAG).
*   **Entregable Incremental:** Catálogo de productos vectorizado (Cimentación para RAG).

### Sesión 8: Pipeline End-to-End y Defensa Técnica
*   **Actividad:** Unificar el flujo y defender las decisiones de ingeniería.
*   **Laboratorio:**
    *   Empaquetar los scripts de PySpark usando `spark-submit`.
    *   Revisión teórica de cómo se orquestaría esto en Apache Airflow (Cloud Composer).
    *   Presentación final: Explicar la arquitectura DAG, justificar el uso de particionamiento, explicar cómo se resolvió el *data skewness* y presentar el pipeline corriendo de principio a fin.