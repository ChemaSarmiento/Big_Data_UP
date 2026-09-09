# Sesión 08 — Model serving, monitoreo y MLOps

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Patrones de serving (batch, online, streaming)
2. Monitoreo de drift de datos y de modelo
3. Orquestación del ciclo completo con Airflow (reentrenamiento programado, triggers por drift)

## Lab
Desplegar el modelo de la Sesión 5 como endpoint (`recursos/serving/serve_fraude.py`), correr `monitor_drift.py` sobre los scores que produce el streaming de la Sesión 7, y desplegar `mlops_pipeline_dag.py` en Airflow — el DAG conecta ingesta → features → entrenamiento → evaluación → despliegue condicional (recarga el endpoint solo si el AUC nuevo pasa el umbral).

## Entregable
DAG de MLOps corriendo en Airflow (captura del grafo con las tareas en verde) + endpoint de modelo respondiendo a `/score` + una corrida de `monitor_drift.py` con su PSI interpretado.

## Ejemplo / material de apoyo
`recursos/airflow/dags/mlops_pipeline_dag.py` — DAG real con `DataprocSubmitJobOperator` + una puerta de calidad (`BranchPythonOperator`) que decide desplegar o no según el AUC. `recursos/serving/serve_fraude.py` — endpoint FastAPI que carga el `PipelineModel` de la Sesión 4/5. `recursos/etl-tipo-cambio/` y `recursos/etl-cripto/` (etapas como funciones separadas) siguen siendo la referencia conceptual de "por qué el código ya viene listo para orquestarse" antes de ver el DAG real.

## Recursos vinculados
- [`recursos/airflow/`](../../recursos/airflow/) — DAG de MLOps completo
- [`recursos/serving/`](../../recursos/serving/) — endpoint de modelo + monitoreo de drift (PSI)
- [`recursos/etl-tipo-cambio/run_etl.py`](../../recursos/etl-tipo-cambio/run_etl.py) — orquestador de referencia, más simple
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — nota sobre Cloud Composer vs. Airflow standalone

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-08.md`](../../slides_maestria/sesion-08.md) (Slidev) — `npx slidev sesion-08.md --open` desde `slides_maestria/`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
