---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 08 — Model serving, monitoreo y MLOps"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 08: serving, drift (PSI), Airflow
---

# Sesión 08
## Model serving, monitoreo y MLOps

<div class="pt-6 text-sm opacity-60">
Un modelo que nadie puede consultar no sirve, y uno sin monitoreo se degrada sin que nadie note. Hoy se cierra el ciclo.
</div>

---

# Tres patrones de serving

| Patrón | Latencia | Ejemplo en el curso |
|---|---|---|
| Batch | Minutos/horas, sin restricción por petición | — |
| **Online (síncrono)** | &lt;1s por petición | `serve_fraude.py` — `POST /score` |
| Streaming | Continuo, sin petición explícita | Sesión 7 |

<div v-click class="mt-6 text-sm opacity-70">
serve_fraude.py carga el PipelineModel en Spark local — un cluster completo tiene overhead de coordinación que lo hace mal candidato para responder 1 petición rápido
</div>

---

# Drift: el modelo se degrada sin que nadie lo note

```mermaid {scale: 0.6}
flowchart LR
    T[Datos de entrenamiento] -.compara.-> R[Referencia]
    P[Lote reciente de producción] -.compara.-> R
    R --> PSI["PSI"]
    PSI -->|"< 0.1"| OK[Sin drift relevante]
    PSI -->|"0.1 - 0.25"| W[Vigilar]
    PSI -->|"> 0.25"| RT[Reentrenar]
```

<div v-click class="mt-4 text-sm opacity-70">
monitor_drift.py — Population Stability Index sobre `amount`, 10 buckets de percentiles
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
- El trigger de reentrenamiento puede ser **drift**, no solo el schedule semanal

</v-clicks>

---

# Lab de hoy

1. Desplegar el endpoint (`serve_fraude.py`)
2. Correr `monitor_drift.py` sobre los scores de la Sesión 7
3. Desplegar el DAG en Airflow

<div class="mt-8 text-blue-500 font-bold">
Entregable: DAG corriendo + endpoint respondiendo + corrida de monitoreo con PSI interpretado
</div>

---
layout: center
class: text-center
---

# → Sesión 09

Gobernanza, seguridad y capstone técnico
