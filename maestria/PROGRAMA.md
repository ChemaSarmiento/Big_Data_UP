# Programa: Big Data — Track Maestría en Ciencia de Datos
### 13 sesiones · 3 horas/semana · 39 horas totales · Entorno: GCP (free tier)

**Perfil de entrada:** estudiantes de maestría en ciencia de datos. Se asume dominio funcional de Python, SQL y estadística/ML "single-node" (pandas, scikit-learn). Linux/GCP básico se nivela como **prerequisito obligatorio** (Módulo 0), no dentro de las 39 horas de clase — aquí el tiempo se invierte en profundidad técnica, no en alfabetización.

**Diferencia clave vs. el track de Especialidad:** este programa no se detiene en "entender la arquitectura" — llega hasta **entrenar, servir y monitorear modelos sobre datos a escala**. Cada sesión tiene lab con código propio (no guiado/completado), y el capstone es un pipeline productivo con un modelo funcionando, no solo una propuesta.

**Sobre las 13 sesiones (antes 9):** cuatro temas —Spark Core avanzado, Data Lakes/Lakehouse, Streaming, y Model serving/MLOps— se dividieron cada uno en dos sesiones completas de 3 horas en vez de comprimirse en una sola. Cada tema se cubre completo, sin recortes: la primera sesión de cada par deja el fundamento/setup, la segunda resuelve el caso real con lab completo.

---

## 1. Objetivo del programa

Al terminar, el estudiante podrá:
- Diseñar y justificar arquitecturas de datos distribuidos (storage, cómputo, streaming).
- Escribir y **optimizar** pipelines en Spark (tuning de shuffle, particionamiento, skew).
- Hacer **feature engineering e ingeniería de datos para ML a escala** (Spark MLlib / pipelines distribuidos).
- **Entrenar modelos sobre datasets que no caben en memoria** de una sola máquina.
- **Servir y monitorear modelos en producción** consumiendo datos de un pipeline de Big Data (drift, latencia, feature freshness).
- Orquestar el ciclo completo (ingesta → features → entrenamiento → serving) como un pipeline de MLOps.

---

## 2. Módulo 0 — Prerequisito obligatorio (antes de la Sesión 1)

A diferencia del track de Especialidad, aquí el Módulo 0 **se evalúa** con un checkpoint corto (quiz + mini-ejercicio) antes de admitir al estudiante a la Sesión 1, porque el ritmo desde el día uno es alto.

| Bloque | Contenido |
|---|---|
| Linux | Terminal avanzada, SSH, gestión de procesos, permisos |
| Python | Repaso rápido + estructuras de datos, comprehensions, manejo de excepciones |
| SQL | JOINs complejos, window functions, CTEs |
| GCP | Proyecto, `gcloud` CLI, IAM básico |

---

## 3. Mapa general de las 13 sesiones

> Nota: "Managed Service for Apache Spark" es el nombre que Google le dio a Dataproc en 2026
> (unifica el antiguo Dataproc on Compute Engine y el Serverless for Apache Spark). Los
> comandos siguen siendo `gcloud dataproc ...` — ver `environment/gcp-setup.md`.

| # | Tema central | Servicio GCP principal (nombre 2026) |
|---|---|---|
| 1 | Arquitecturas distribuidas: HDFS, MapReduce, CAP, Spark vs MapReduce | Managed Service for Apache Spark |
| 2 | SQL distribuido avanzado: optimización, particionamiento, costo | BigQuery |
| 3 | Spark Core I: Catalyst, tipos de shuffle, `.explain()` | Managed Service for Apache Spark |
| 4 | Spark Core II: skew — causas, salting, broadcast joins, AQE | Managed Service for Apache Spark |
| 5 | Ingeniería de features a escala (Spark MLlib pipelines) | Managed Service for Apache Spark |
| 6 | Entrenamiento de modelos distribuido + tuning de hiperparámetros a escala | Managed Service for Apache Spark + Vertex AI (intro) |
| 7 | Lakehouse I: Parquet/ORC/Avro, medallion, intro a Iceberg | Cloud Storage |
| 8 | Lakehouse II: MERGE INTO, time travel, evolución de esquema, versionado | Apache Iceberg |
| 9 | Streaming I: windowing, watermarks, setup de Pub/Sub Lite | Pub/Sub Lite + Managed Service for Apache Spark |
| 10 | Streaming II: scoring en tiempo real, feature freshness | Pub/Sub Lite + Managed Service for Apache Spark |
| 11 | Model serving y monitoreo: patrones de serving, drift (PSI) | Endpoint propio (FastAPI) |
| 12 | MLOps con Airflow: orquestación, reentrenamiento por drift | Airflow (standalone o Cloud Composer) |
| 13 | Gobernanza, seguridad, costos + capstone técnico | IAM, Data Catalog |

---

## 4. Detalle sesión por sesión

### Sesión 1 — Arquitecturas distribuidas
- **Teoría:** HDFS, teorema CAP, MapReduce, por qué Spark lo reemplazó (in-memory, DAG scheduler).
- **Lab:** cluster de Managed Service for Apache Spark (Dataproc), MapReduce clásico vs Spark equivalente, lectura de logs de ejecución (YARN/Spark UI) para diagnosticar cuellos de botella.
- **Entregable:** benchmark propio (tiempos, uso de memoria) MapReduce vs Spark.

### Sesión 2 — SQL distribuido avanzado
- **Teoría:** motor de ejecución de BigQuery, particionamiento y clustering, slot allocation, costo por bytes escaneados vs por slots reservados.
- **Lab:** rediseñar una tabla mal particionada, medir la reducción de costo/latencia, escribir consultas analíticas con window functions anidadas y CTEs recursivos.
- **Entregable:** reporte de optimización (antes/después) con evidencia de costo, incluyendo una gráfica de barras.

### Sesión 3 — Spark Core avanzado I: Catalyst y shuffle
- **Teoría:** Catalyst optimizer y Tungsten, tipos de shuffle (agregación, join, repartición explícita), lectura de planes físicos con `.explain()`.
- **Lab:** correr `02_dataframes.ipynb` (DataFrame API) y `03_spark_sql.ipynb` (SQL puro) sobre el mismo dataset, comparar planes de ejecución, identificar cada `Exchange` (shuffle) y su origen.
- **Entregable:** capturas de los dos planes comparados + lista de shuffles identificados.

### Sesión 4 — Spark Core avanzado II: skew y diagnóstico
- **Teoría:** causas de skew, señales en el Spark UI, tres estrategias de mitigación (salting, broadcast joins, AQE) y sus límites.
- **Lab:** diagnosticar y resolver un job con skew severo sobre un dataset sintético desbalanceado, retomando los notebooks de la Sesión 3, comparar plan de ejecución antes/después.
- **Entregable:** notebook con el diagnóstico y la solución aplicada, con métricas de mejora.

### Sesión 5 — Ingeniería de features a escala
- **Teoría:** feature engineering distribuido (Spark MLlib `Pipeline`, `Transformer`, `Estimator`), encoding y escalado a escala, introducción a feature stores (por qué existen, qué problema resuelven).
- **Lab:** construir un pipeline de features reproducible con Spark MLlib sobre un dataset de +5M filas (imputación, encoding, escalado, ensamblado de vector de features).
- **Entregable:** pipeline de features serializado y reproducible.

### Sesión 6 — Entrenamiento de modelos distribuido
- **Teoría:** algoritmos de Spark MLlib (regresión, árboles, gradient boosting) y cómo se paralelizan, estrategias de tuning de hiperparámetros a escala (`CrossValidator` distribuido), cuándo Spark MLlib no es suficiente (deep learning) y alternativas (Vertex AI Training, Horovod — panorama, no profundidad).
- **Lab:** entrenar y comparar 2-3 modelos con Spark MLlib sobre el pipeline de features de la Sesión 5, tuning con `CrossValidator`.
- **Entregable:** modelo entrenado + comparación de métricas (con gráfica comparativa) + justificación del modelo elegido.

### Sesión 7 — Lakehouse I: formatos y medallion
- **Teoría:** Parquet vs ORC vs Avro, arquitectura medallion, por qué Parquet plano en carpetas no es un lakehouse transaccional — introducción al problema que resuelven Iceberg/Delta.
- **Lab:** preparar el cluster con el runtime de Iceberg, cargar `bank_transactions.csv` como bronze y escribirlo como tabla Iceberg **silver** particionada (primera mitad de `recursos/lakehouse-iceberg/06_lakehouse_iceberg.py`).
- **Entregable:** tabla Iceberg creada y cargada + captura del snapshot inicial.

### Sesión 8 — Lakehouse II: transacciones y versionado
- **Teoría:** `MERGE INTO` a fondo, time travel, evolución de esquema sin romper lectores existentes, versionado de datasets y de modelos (por qué es distinto a versionar código).
- **Lab:** retomar la tabla de la Sesión 7 y completar `06_lakehouse_iceberg.py`: `MERGE INTO`, consulta de snapshot anterior, `ALTER TABLE`, capa gold agregada.
- **Entregable:** diagrama de arquitectura + pipeline versionado + evidencia de las tres operaciones transaccionales.

### Sesión 9 — Streaming I: fundamentos y setup
- **Teoría:** windowing, watermarks, exactly-once vs at-least-once, setup de Pub/Sub Lite (el único conector de Structured Streaming que Google mantiene oficialmente).
- **Lab:** crear topic/suscripción de Pub/Sub Lite, correr `producer_transacciones_stream.py` y `07a_streaming_conteo.py` — conteo de transacciones por ventana de 1 minuto, sin scoring todavía.
- **Entregable:** captura de las ventanas de conteo actualizándose en consola.

### Sesión 10 — Streaming II: inferencia en tiempo real
- **Teoría:** patrones de scoring en tiempo real (modelo cargado en el stream vs llamada a un endpoint externo), feature freshness.
- **Lab:** extender el consumidor de la Sesión 9 — `07_streaming_scoring.py` aplica el `PipelineModel` de la Sesión 6 sobre el mismo stream y calcula alertas por ventana con watermark.
- **Entregable:** pipeline de streaming con inferencia funcionando end-to-end.

### Sesión 11 — Model serving y monitoreo
- **Teoría:** patrones de serving (batch, online, streaming), monitoreo de drift de datos y de modelo (Population Stability Index).
- **Lab:** desplegar el modelo de la Sesión 6 como endpoint (`recursos/serving/serve_fraude.py`, FastAPI), correr `monitor_drift.py` sobre los scores del streaming de la Sesión 10.
- **Entregable:** endpoint de modelo respondiendo + corrida de monitoreo de drift con PSI interpretado.

### Sesión 12 — MLOps con Airflow
- **Teoría:** orquestación del ciclo completo con Airflow (DAGs, dependencias, reintentos), reentrenamiento programado vs. triggers por drift.
- **Lab:** desplegar `recursos/airflow/dags/mlops_pipeline_dag.py` y correrlo end-to-end — ingesta → features → entrenamiento → evaluación → despliegue condicional según una puerta de calidad de AUC, que recarga el endpoint de la Sesión 11.
- **Entregable:** DAG de MLOps funcional corriendo, conectado al endpoint.

### Sesión 13 — Gobernanza, seguridad y capstone
- **Teoría:** IAM a nivel dataset/tabla, Data Catalog, linaje de datos y de modelos, cumplimiento en contextos regulados (relevante para banca/finanzas), FinOps de un pipeline de ML a escala.
- **Actividad principal:** presentación del **capstone técnico** (máx. 15 min c/u — mismo límite institucional que Especialidad): pipeline completo ingesta → features → entrenamiento → serving, con al menos un componente de streaming u orquestación, visualizaciones sobre los resultados y evidencia de pruebas.
- **Cierre:** temas de profundización sugeridos (Delta Lake/Iceberg avanzado, entrenamiento distribuido con GPUs, feature stores productivos, BigQuery ML).

---

## 5. Evaluación

| Componente | Peso |
|---|---|
| Labs entregables (el mejor de Sesiones 2–12) | 35% |
| Participación técnica en clase (code review entre pares) | 10% |
| Capstone técnico (pipeline + modelo funcionando + presentación) | 55% |

**Criterios del capstone** (documento + presentación ≤15 min, formato institucional — ver las instrucciones del proyecto final publicadas en la plataforma del curso): pipeline reproducible en código (no solo notebook exploratorio) sobre un dataset real ≥15GB, con al menos (1) ingesta distribuida, (2) feature engineering con Spark MLlib, (3) modelo entrenado y evaluado con métricas justificadas, (4) serving o inferencia batch programada, (5) al menos un componente de streaming u orquestación con Airflow, (6) **al menos una visualización** de los resultados/conclusiones (no basta con una tabla de métricas), y (7) evidencia de **pruebas** (al menos: validación de la calidad del dato de entrada, y comparación de métricas antes/después de cada optimización — Sesiones 3-4 ya dejan ese hábito). El documento sigue la estructura institucional: resumen ejecutivo, visión general, revisión y uso de datos, proceso de desarrollo (metodología y pruebas), resultados y conclusiones — con el código entregado o mostrado.

---

## 6. Notas de facilitación

- El ritmo es alto — no hay tiempo de clase para depurar errores básicos de Python/SQL; por eso el Módulo 0 se evalúa como filtro de entrada.
- Los pares 3-4, 7-8, 9-10 y 11-12 eran, hasta hace poco, una sola sesión cada uno — se dividieron precisamente porque no cabían completos en 3 horas. No los vuelvas a comprimir: cada mitad tiene su propio ritmo (teoría → break → lab) y su propio entregable.
- Al crear un cluster nuevo cada sesión (S1, S3, S4, S5, S6, S7, S8), revisa `gcloud dataproc clusters list` **antes** de empezar — es común que alguien deje uno prendido de la sesión anterior.
- Fomentar code review entre pares en cada lab (10 min al final) — a este nivel, leer código de otros acelera más el aprendizaje que más ejercicios individuales.
