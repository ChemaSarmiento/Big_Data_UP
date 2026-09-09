# Teoría — Sesión 08: Model serving, monitoreo y MLOps

> El modelo de la Sesión 5 no sirve de nada si nadie puede consultarlo, y va a dejar
> de ser bueno tarde o temprano sin que nadie lo note, salvo que exista monitoreo. Hoy
> se cierra el ciclo completo.

## 1. Patrones de serving

Tres formas distintas de "poner un modelo a trabajar", cada una con un caso de uso
propio:

- **Batch:** el modelo se aplica sobre un lote completo de datos, en un horario
  programado (ej. cada noche, sobre todas las transacciones del día). No hay
  restricción de latencia por petición — el trabajo completo puede tardar minutos u
  horas.
- **Online (síncrono):** el modelo responde a peticiones individuales en tiempo real,
  típicamente vía un endpoint HTTP — `recursos/serving/serve_fraude.py` es este
  patrón: cada `POST /score` espera una respuesta en menos de un segundo.
- **Streaming:** el modelo se aplica sobre un flujo continuo de eventos, sin peticiones
  individuales explícitas — el patrón de la Sesión 7 (`07_streaming_scoring.py`).

La decisión de diseño de `serve_fraude.py` — cargar el `PipelineModel` en una
SparkSession **local**, dentro del mismo proceso de la API, en vez de en el cluster de
Dataproc — es exactamente el trade-off de "online" vs. "batch": un cluster completo
tiene overhead de coordinación que lo hace mal candidato para responder una sola
petición HTTP rápido; libera ese mismo cluster para lo que sí necesita paralelismo real
(entrenar, o procesar un lote de millones de filas).

## 2. Monitoreo de drift

Un modelo entrenado con datos de un momento dado empieza a degradarse en cuanto el
mundo real se aleja de esos datos — **drift**. Dos tipos:

- **Drift de datos:** la distribución de las features de entrada cambia (ej. el monto
  promedio de las transacciones sube por inflación, o cambia el comportamiento de
  fraude por una nueva técnica de ataque) — el modelo sigue funcionando técnicamente,
  pero sobre datos distintos a los que aprendió.
- **Drift de modelo (concept drift):** la relación misma entre features y el resultado
  cambia — lo que antes predecía fraude ya no lo hace, porque el patrón de fraude
  cambió, no solo su frecuencia.

`recursos/serving/monitor_drift.py` mide drift de datos con el **Population Stability
Index (PSI)**: compara la distribución de una feature (`amount`) entre el set de
entrenamiento y un lote reciente de producción, en 10 buckets de percentiles. Es un
solo número interpretable, sin asumir una forma particular de la distribución — el
estándar de la industria para esto:

```
PSI < 0.1   → sin drift relevante
0.1 – 0.25  → drift moderado, vigilar
> 0.25      → drift significativo, considerar reentrenar
```

## 3. Orquestación con Airflow

Un modelo en producción necesita un ciclo que se repita sin intervención manual:
ingesta → features → entrenamiento → evaluación → despliegue (si pasa la evaluación).
Airflow expresa este ciclo como un **DAG** (grafo acíclico dirigido) de tareas con
dependencias explícitas:

```
entrenamiento_y_features (Dataproc)
        │
        ▼
  evaluar_metricas (lee metrics.json)
        │
        ▼
  puerta_calidad (¿AUC >= umbral?)
       ╱      ╲
desplegar   no_desplegar
```

`recursos/airflow/dags/mlops_pipeline_dag.py` implementa exactamente esto — la pieza
que un simple script secuencial (`recursos/etl-tipo-cambio/run_etl.py`) no puede dar:
reintentos automáticos por tarea, una decisión condicional real (`BranchPythonOperator`)
según el resultado de una tarea anterior, y visibilidad de qué falló y dónde, sin tener
que leer logs de un script monolítico de punta a punta.

**Reentrenamiento por triggers de drift:** el DAG de este curso corre en un schedule
fijo (`@weekly`), pero el patrón de producción real conecta `monitor_drift.py` como un
disparador adicional — si el PSI supera 0.25, se dispara el DAG manualmente en vez de
esperar al ciclo semanal. Es la misma idea de "puerta de calidad" aplicada del lado de
los datos de entrada, no solo del modelo de salida.

---

## Referencias

- [Google Cloud — ML serving patterns overview](https://cloud.google.com/architecture/ml-on-gcp-best-practices)
- [Google Cloud — Vertex AI Model Monitoring (drift/skew)](https://cloud.google.com/vertex-ai/docs/model-monitoring/overview)
- [Apache Airflow — Concepts: DAGs, Operators, Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Google Cloud — MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
