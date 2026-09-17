---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 12 — MLOps con Airflow"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 12: orquestación, DAG de MLOps, reentrenamiento por drift
---

# Sesión 12
## MLOps con Airflow

<div class="pt-6 text-sm opacity-60">
La Sesión 11 dejó un endpoint y una señal de drift — hoy se conecta todo en un ciclo automatizado
</div>

---

# El DAG de MLOps

```mermaid {scale: 0.55}
flowchart TD
    A[entrenamiento_y_features<br/>Dataproc] --> B[evaluar_metricas<br/>lee metrics.json]
    B --> C{puerta_calidad<br/>AUC >= 0.75?}
    C -->|sí| D[desplegar_modelo<br/>POST /reload]
    C -->|no| E[no_desplegar]
```

<div v-click class="mt-4 text-sm opacity-70">
mlops_pipeline_dag.py — reintentos automáticos, decisión condicional real, visibilidad de qué falló y dónde
</div>

---

# Por qué esto no es solo "el script de siempre"

<v-clicks>

- `run_etl.py` (etl-tipo-cambio) es secuencial — si algo falla, hay que leer el log completo
- Un DAG da dependencias explícitas + reintentos por tarea + una decisión condicional real
- El trigger de reentrenamiento puede ser **drift** (Sesión 11), no solo el schedule semanal

</v-clicks>

---

# Trece sesiones, un solo sistema

<div class="grid grid-cols-3 gap-2 mt-6 text-center text-xs">
<div class="p-2 border rounded">S5<br/>Features</div>
<div class="p-2 border rounded">S6<br/>Entrenamiento</div>
<div class="p-2 border rounded">S7-8<br/>Lakehouse</div>
<div class="p-2 border rounded">S9-10<br/>Streaming</div>
<div class="p-2 border rounded">S11<br/>Serving/drift</div>
<div class="p-2 border rounded border-blue-500">S12<br/>Airflow (hoy)</div>
</div>

<div v-click class="mt-8 text-blue-500 font-bold text-center">
Hoy, por primera vez, todas las piezas corren automatizadas como un solo sistema
</div>

---

# Paso 1 — Setup de Airflow

```bash
pip install apache-airflow apache-airflow-providers-google
airflow db init
airflow variables set gcp_project_id <PROJECT_ID>
airflow variables set gcp_bucket gs://<TU-BUCKET>
airflow variables set serving_host <host-del-endpoint>:8080
cp dags/mlops_pipeline_dag.py $AIRFLOW_HOME/dags/
airflow standalone
```

<div class="mt-4 text-sm opacity-70">
Deberías ver: Airflow standalone arranca y muestra una URL local
</div>

---

# Paso 2 — Disparar el DAG y ver el ciclo completo

Desde la UI: activar el DAG y disparar una corrida manual (trigger).

<div class="mt-4">
Vean el grafo en la UI — cada tarea se pone verde conforme termina. Esa es la
visibilidad que un script secuencial no da.
</div>

<div class="mt-4 text-sm opacity-70">
Si evaluar_metricas falla: confirmar que 04_pipeline_ml.ipynb escribió metrics.json en la ruta esperada
</div>

<div class="mt-6 p-4 border-l-4 border-blue-500 font-bold">
Entregable: DAG corriendo (captura del grafo en verde), conectado al endpoint de la Sesión 11
</div>

---
layout: center
class: text-center
---

# → Sesión 13

Gobernanza, seguridad y capstone técnico
