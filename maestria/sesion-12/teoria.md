# Teoría — Sesión 12: MLOps con Airflow

> Segunda de dos sesiones de cierre técnico. La Sesión 11 dejó un endpoint y una
> señal de drift; hoy se conecta todo en un ciclo que se repite sin intervención
> manual — el último ingrediente antes del capstone.

## Orquestación con Airflow

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
  puerta_calidad (¿AUC >= 0.75?)
       ╱      ╲
desplegar   no_desplegar
```

`recursos/airflow/dags/mlops_pipeline_dag.py` implementa exactamente esto — la pieza
que un simple script secuencial (`recursos/etl-tipo-cambio/run_etl.py`) no puede dar:
reintentos automáticos por tarea, una decisión condicional real (`BranchPythonOperator`)
según el resultado de una tarea anterior, y visibilidad de qué falló y dónde, sin tener
que leer logs de un script monolítico de punta a punta.

## Reentrenamiento programado vs. por triggers de drift

El DAG de este curso corre en un schedule fijo (`@weekly`), pero el patrón de
producción real conecta `monitor_drift.py` (Sesión 11) como un disparador adicional:
si el PSI supera 0.25, se dispara el DAG manualmente en vez de esperar al ciclo
semanal. Es la misma idea de "puerta de calidad" aplicada del lado de los datos de
entrada, no solo del modelo de salida — dos señales distintas (tiempo transcurrido,
y evidencia de que el mundo cambió) que pueden justificar la misma acción.

## Dónde correr esto

- **Airflow standalone en la VM `e2-micro`** (Always Free) — la opción por
  default, ver `environment/gcp-setup.md`.
- **Cloud Composer** — funciona igual (mismo DAG, sin cambios), pero es el
  servicio más caro del curso; solo si el crédito de $300 alcanza y el grupo
  quiere ver el entorno gestionado real.

## Lo que este DAG demuestra que las Sesiones 3-11 no habían conectado

Cada sesión anterior tocó una pieza del ciclo por separado: features (Sesión 5),
entrenamiento (Sesión 6), lakehouse versionado (Sesión 7-8), streaming (Sesión 9-10),
serving y drift (Sesión 11). Hoy, por primera vez, todas esas piezas corren como
**un solo sistema automatizado** — la puerta de calidad (`AUC_MINIMO = 0.75`) es
exactamente el tipo de decisión que la Sesión 13 (Gobernanza) pide justificar: ¿por
qué ese umbral y no otro?

---

## Referencias

- [Apache Airflow — Concepts: DAGs, Operators, Tasks](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html)
- [Google Cloud — Cloud Composer overview](https://cloud.google.com/composer/docs/concepts/overview)
- [Google Cloud — MLOps: Continuous delivery and automation pipelines in machine learning](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)
