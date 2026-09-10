# Sesión 12 — MLOps con Airflow

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Orquestación del ciclo completo con Airflow
2. Reentrenamiento programado y triggers por drift

## Lab
Desplegar `mlops_pipeline_dag.py` en Airflow (standalone en la VM `e2-micro` o Cloud Composer) y correrlo end-to-end: ingesta → features → entrenamiento → evaluación → despliegue condicional, que recarga el endpoint de la Sesión 11 vía `POST /reload` si el AUC pasa el umbral.

## Entregable
DAG de MLOps corriendo en Airflow (captura del grafo con las tareas en verde), conectado al endpoint de la Sesión 11.

## Ejemplo / material de apoyo
`recursos/airflow/dags/mlops_pipeline_dag.py` — DAG real con `DataprocSubmitJobOperator` + una puerta de calidad (`BranchPythonOperator`) que decide desplegar o no según el AUC leído de `metrics.json` (escrito por `recursos/spark/04_pipeline_ml.ipynb`).

## Recursos vinculados
- [`recursos/airflow/`](../../recursos/airflow/) — DAG de MLOps completo
- [`recursos/serving/serve_fraude.py`](../../recursos/serving/serve_fraude.py) — el endpoint que este DAG recarga
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — nota sobre Cloud Composer vs. Airflow standalone

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-12.md`](../../slides_maestria/sesion-12.md) (Slidev) — `npx slidev sesion-12.md --open` desde `slides_maestria/`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
