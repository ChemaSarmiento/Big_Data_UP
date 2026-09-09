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

# Lab de hoy

Desplegar `mlops_pipeline_dag.py` en Airflow y correrlo end-to-end:

ingesta → features → entrenamiento → evaluación → despliegue condicional

<div class="mt-8 text-blue-500 font-bold">
Entregable: DAG corriendo (captura del grafo en verde), conectado al endpoint de la Sesión 11
</div>

---
layout: center
class: text-center
---

# → Sesión 13

Gobernanza, seguridad y capstone técnico
