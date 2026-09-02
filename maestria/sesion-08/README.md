# Sesión 08 — Model serving, monitoreo y MLOps

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Patrones de serving (batch, online, streaming)
2. Monitoreo de drift de datos y de modelo
3. Orquestación del ciclo completo con Airflow (reentrenamiento programado, triggers por drift)

## Lab
Desplegar el modelo de la Sesión 5 como endpoint (Vertex AI o serving simple vía API), instrumentar métricas básicas de monitoreo, y armar el DAG de Airflow que conecta ingesta → features → entrenamiento → evaluación.

## Entregable
DAG de MLOps funcional + endpoint de modelo respondiendo.

## Ejemplo / material de apoyo
`recursos/etl-cripto/` y `recursos/etl-tipo-cambio/` ya están escritos como etapas independientes (`extract.py`, `transform.py`, `load.py` / funciones equivalentes) — exactamente la forma en la que se estructura un DAG de Airflow, con cada etapa como una `PythonOperator` separada.

## Recursos vinculados
- [`recursos/etl-tipo-cambio/run_etl.py`](../../recursos/etl-tipo-cambio/run_etl.py) — orquestador de referencia
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — nota sobre Cloud Composer vs. Airflow standalone

## Slides
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
