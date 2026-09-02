# Programa: Big Data — Track Maestría en Ciencia de Datos
### 9 sesiones · 3 horas/semana · 27 horas totales · Entorno: GCP (free tier)

**Perfil de entrada:** estudiantes de maestría en ciencia de datos. Se asume dominio funcional de Python, SQL y estadística/ML "single-node" (pandas, scikit-learn). Linux/GCP básico se nivela como **prerequisito obligatorio** (Módulo 0), no dentro de las 27 horas de clase — aquí el tiempo se invierte en profundidad técnica, no en alfabetización.

**Diferencia clave vs. el track de Especialidad:** este programa no se detiene en "entender la arquitectura" — llega hasta **entrenar, servir y monitorear modelos sobre datos a escala**. Cada sesión tiene lab con código propio (no guiado/completado), y el capstone es un pipeline productivo con un modelo funcionando, no solo una propuesta.

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

## 3. Mapa general de las 9 sesiones

> Nota: "Managed Service for Apache Spark" es el nombre que Google le dio a Dataproc en 2026
> (unifica el antiguo Dataproc on Compute Engine y el Serverless for Apache Spark). Los
> comandos siguen siendo `gcloud dataproc ...` — ver `environment/gcp-setup.md`.

| # | Tema central | Servicio GCP principal (nombre 2026) |
|---|---|---|
| 1 | Arquitecturas distribuidas: HDFS, MapReduce, CAP, Spark vs MapReduce | Managed Service for Apache Spark |
| 2 | SQL distribuido avanzado: optimización, particionamiento, costo | BigQuery |
| 3 | Spark Core avanzado: tuning, shuffle, skew, Catalyst | Managed Service for Apache Spark |
| 4 | Ingeniería de features a escala (Spark MLlib pipelines) | Managed Service for Apache Spark |
| 5 | Entrenamiento de modelos distribuido + tuning de hiperparámetros a escala | Managed Service for Apache Spark + Vertex AI (intro) |
| 6 | Data Lakes / Lakehouse: Parquet, Iceberg/Delta, versionado de datos | Cloud Storage |
| 7 | Streaming + inferencia en tiempo real | Pub/Sub + Managed Service for Apache Spark |
| 8 | Model serving, monitoreo y MLOps (drift, latencia, orquestación) | Vertex AI / Airflow |
| 9 | Gobernanza, seguridad, costos + capstone técnico | IAM, Data Catalog |

---

## 4. Detalle sesión por sesión

### Sesión 1 — Arquitecturas distribuidas
- **Teoría:** HDFS, teorema CAP, MapReduce, por qué Spark lo reemplazó (in-memory, DAG scheduler).
- **Lab:** cluster de Managed Service for Apache Spark (Dataproc), MapReduce clásico vs Spark equivalente, lectura de logs de ejecución (YARN/Spark UI) para diagnosticar cuellos de botella.
- **Entregable:** benchmark propio (tiempos, uso de memoria) MapReduce vs Spark.

### Sesión 2 — SQL distribuido avanzado
- **Teoría:** motor de ejecución de BigQuery, particionamiento y clustering, slot allocation, costo por bytes escaneados vs por slots reservados.
- **Lab:** rediseñar una tabla mal particionada, medir la reducción de costo/latencia, escribir consultas analíticas con window functions anidadas y CTEs recursivos.
- **Entregable:** reporte de optimización (antes/después) con evidencia de costo.

### Sesión 3 — Spark Core avanzado
- **Teoría:** Catalyst optimizer y Tungsten, tipos de shuffle, causas de skew y estrategias de mitigación (salting, broadcast joins, repartición adaptativa — AQE).
- **Lab:** diagnosticar y resolver un job con skew severo sobre un dataset sintético desbalanceado, comparar plan de ejecución antes/después.
- **Entregable:** notebook con el diagnóstico y la solución aplicada, con métricas de mejora.

### Sesión 4 — Ingeniería de features a escala
- **Teoría:** feature engineering distribuido (Spark MLlib `Pipeline`, `Transformer`, `Estimator`), encoding y escalado a escala, introducción a feature stores (por qué existen, qué problema resuelven).
- **Lab:** construir un pipeline de features reproducible con Spark MLlib sobre un dataset de +5M filas (imputación, encoding, escalado, ensamblado de vector de features).
- **Entregable:** pipeline de features serializado y reproducible.

### Sesión 5 — Entrenamiento de modelos distribuido
- **Teoría:** algoritmos de Spark MLlib (regresión, árboles, gradient boosting) y cómo se paralelizan, estrategias de tuning de hiperparámetros a escala (`CrossValidator` distribuido), cuándo Spark MLlib no es suficiente (deep learning) y alternativas (Vertex AI Training, Horovod — panorama, no profundidad).
- **Lab:** entrenar y comparar 2-3 modelos con Spark MLlib sobre el pipeline de features de la Sesión 4, tuning con `CrossValidator`.
- **Entregable:** modelo entrenado + comparación de métricas + justificación del modelo elegido.

### Sesión 6 — Data Lakes / Lakehouse
- **Teoría:** Parquet vs ORC vs Avro, arquitectura medallion, formatos de tabla transaccionales (Iceberg/Delta) para ACID sobre el lake, versionado de datasets y de modelos (por qué es distinto a versionar código).
- **Lab:** migrar el pipeline de features a arquitectura medallion con versionado explícito de cada capa.
- **Entregable:** diagrama de arquitectura + pipeline versionado.

### Sesión 7 — Streaming e inferencia en tiempo real
- **Teoría:** windowing, watermarks, exactly-once vs at-least-once, patrones de scoring en tiempo real (modelo cargado en el stream vs llamada a un endpoint externo), feature freshness.
- **Lab:** pipeline de Spark Structured Streaming que consume de Pub/Sub, aplica el pipeline de features de la Sesión 4 y genera un score con el modelo de la Sesión 5.
- **Entregable:** pipeline de streaming con inferencia funcionando end-to-end.

### Sesión 8 — Model serving, monitoreo y MLOps
- **Teoría:** patrones de serving (batch, online, streaming), monitoreo de drift de datos y de modelo, orquestación del ciclo completo con Airflow (reentrenamiento programado, triggers por drift).
- **Lab:** desplegar el modelo de la Sesión 5 como endpoint (Vertex AI o serving simple vía API), instrumentar métricas básicas de monitoreo, armar el DAG de Airflow que conecta ingesta → features → entrenamiento → evaluación.
- **Entregable:** DAG de MLOps funcional + endpoint de modelo respondiendo.

### Sesión 9 — Gobernanza, seguridad y capstone
- **Teoría:** IAM a nivel dataset/tabla, Data Catalog, linaje de datos y de modelos, cumplimiento en contextos regulados (relevante para banca/finanzas), FinOps de un pipeline de ML a escala.
- **Actividad principal:** presentación del **capstone técnico** (20 min c/u): pipeline completo ingesta → features → entrenamiento → serving, con al menos un componente de streaming u orquestación.
- **Cierre:** temas de profundización sugeridos (Delta Lake/Iceberg avanzado, entrenamiento distribuido con GPUs, feature stores productivos, BigQuery ML).

---

## 5. Evaluación

| Componente | Peso |
|---|---|
| Labs entregables (el mejor de Sesiones 2–8) | 35% |
| Participación técnica en clase (code review entre pares) | 10% |
| Capstone técnico (pipeline + modelo funcionando + presentación) | 55% |

**Criterios del capstone:** pipeline reproducible en código (no solo notebook exploratorio), con al menos (1) ingesta distribuida, (2) feature engineering con Spark MLlib, (3) modelo entrenado y evaluado con métricas justificadas, (4) serving o inferencia batch programada, y (5) al menos un componente de streaming u orquestación con Airflow.

---

## 6. Notas de facilitación

- El ritmo es alto — no hay tiempo de clase para depurar errores básicos de Python/SQL; por eso el Módulo 0 se evalúa como filtro de entrada.
- Sesiones 3, 5 y 8 son las más pesadas — si el grupo requiere más tiempo, es mejor extender el programa a 10-11 sesiones que recortar contenido de estas tres.
- Fomentar code review entre pares en cada lab (10 min al final) — a este nivel, leer código de otros acelera más el aprendizaje que más ejercicios individuales.
