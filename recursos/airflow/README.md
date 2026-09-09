# Orquestación MLOps con Airflow

Material técnico de Maestría Sesión 8: un DAG de Airflow real, no solo un script
con etapas separadas. `recursos/etl-tipo-cambio/run_etl.py` sigue siendo útil
para introducir la idea de "cada etapa es una función independiente" — el paso
que falta, y que este DAG sí da, es la orquestación en sí: reintentos,
dependencias explícitas entre tareas, y una decisión condicional (desplegar o no)
según el resultado de una tarea anterior.

## `dags/mlops_pipeline_dag.py`

Conecta el ciclo completo que pide el criterio del capstone (Sección 5 de
`maestria/PROGRAMA.md`): ingesta → features → entrenamiento → evaluación →
despliegue condicional.

```
entrenamiento_y_features (Dataproc, corre 04_pipeline_ml.py)
        │
        ▼
  evaluar_metricas (lee gs://.../modelos/metrics.json)
        │
        ▼
  puerta_calidad (¿AUC >= 0.75?)
       ╱      ╲
desplegar   no_desplegar
(POST /reload
al endpoint de
recursos/serving/)
```

La puerta de calidad (`AUC_MINIMO = 0.75`) es exactamente el tipo de decisión que
Sesión 9 (Gobernanza) pide justificar: ¿por qué ese umbral y no otro? Buen tema de
discusión antes de la presentación del capstone.

## Dónde correrlo

- **Airflow standalone en la VM `e2-micro`** (Always Free) — la opción por
  default, ver `environment/gcp-setup.md`.
- **Cloud Composer** — funciona igual (mismo DAG, sin cambios), pero es el
  servicio más caro del curso; solo si el crédito de $300 alcanza y el grupo
  quiere ver el entorno gestionado real.

## Setup mínimo

```bash
pip install apache-airflow apache-airflow-providers-google
airflow db init
airflow variables set gcp_project_id <PROJECT_ID>
airflow variables set gcp_bucket gs://<TU-BUCKET>
airflow variables set serving_host <host-del-endpoint>:8080
cp dags/mlops_pipeline_dag.py $AIRFLOW_HOME/dags/
airflow standalone
```

## Ver también

- [`recursos/spark/04_pipeline_ml.ipynb`](../spark/04_pipeline_ml.ipynb) — el job que este DAG dispara, incluyendo la celda que escribe `metrics.json`.
- [`recursos/serving/`](../serving/) — el endpoint que este DAG recarga al desplegar.
