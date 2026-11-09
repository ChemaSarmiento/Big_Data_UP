# Syllabus: Sistemas de Datos Distribuidos para Especialidad
(SDD)

## Resumen Ejecutivo del Programa

Este programa ha sido modernizado para responder a las exigencias actuales del mercado de tecnología y datos. Evoluciona de arquitecturas tradicionales de procesamiento distribuido hacia un **Ecosistema Moderno de Datos en la Nube**, integrando **Data Lakehouses**, **Arquitectura Medallion**, **PySpark**, **Procesamiento en Tiempo Real**, y la convergencia de Big Data con **Modelos de Lenguaje Grande (LLMs)** y **Generación Aumentada por Recuperación (RAG)**.

El curso se estructura en dos modalidades de aprendizaje adaptadas a perfiles diferenciados, utilizando un entorno de laboratorio común basado en **Google Cloud Platform (GCP)** (con el fondo de 300 USD por estudiante) y organizado alrededor de un **Proyecto Final Incremental**.


## 🎯 Estructura de Track

| Métrica / Aspecto | Track 1: Especialidad | 
| :--- | :--- | 
| **Perfil Destino** | Ejecutivo, Negocio, Product Owner, Manager | 
| **Enfoque Principal** | Gobernanza, Arquitecturas de datos, Preparación de Datos, Medallion, Valor de Negocio, ETL, Consultas y GenAI | 
| **Profundidad de Código** | SQL, Visualización y Low-Code, Python, PySpark| 
| **Entorno GCP** | BigQuery, Looker Studio, Vertex AI Studio, VM |

---

## Track 1: Especialidad (Perfil Ejecutivo y de Negocio)

**Objetivo:** Comprender el ecosistema moderno de datos en la nube, gobernar los activos de datos y extraer valor de negocio mediante arquitecturas avanzadas y herramientas de análisis, sin requerir programación en código complejo.

### Módulo 1: Introducción al Ecosistema Cloud y Big Data
* Conceptos clave de Cloud Computing y aprovisionamiento del entorno GCP.
* Evolución del almacenamiento: Del Data Warehouse tradicional al Data Lake y Data Lakehouse.
* Casos de uso empresariales de Big Data (Banca, Retail, Salud, Logística).


### Módulo 2: Acceso y Consulta de Grandes Datos (SQL Fast Track)
* Bases de datos distribuidas y motor de BigQuery en GCP.
* **SQL Fast Track:** Fundamentos de SQL para analistas y ejecutivos, ganar nivel para entender estructuras y crear queries a partir de preguntas de negocio.
* Consultas esenciales, agregaciones, filtros y joins sobre grandes volúmenes de datos.


### Módulo 3: Arquitectura y Gestión de Datos
* Paradigmas modernos de ingesta y transformación: ETL vs. ELT.
* Arquitectura Medallion simplificada: Entendiendo la propuesta de valor de las capas **Bronze** (datos crudos), **Silver** (datos limpiados) y **Gold** (agregados de negocio).
* Gobierno de datos, calidad, seguridad, compliance y privacidad en la nube (GDPR/HIPAA).

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
