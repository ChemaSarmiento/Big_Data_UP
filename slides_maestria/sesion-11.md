---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 11 — Model serving y monitoreo"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 11: patrones de serving, drift (PSI)
---

# Sesión 11
## Model serving y monitoreo

<div class="pt-6 text-sm opacity-60">
Un modelo que nadie puede consultar no sirve, y uno sin monitoreo se degrada sin que nadie note
</div>

---

# Tres patrones de serving

| Patrón | Latencia | Ejemplo en el curso |
|---|---|---|
| Batch | Minutos/horas, sin restricción por petición | — |
| **Online (síncrono)** | &lt;1s por petición | `serve_fraude.py` — `POST /score` |
| Streaming | Continuo, sin petición explícita | Sesión 10 |

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

<div v-click class="mt-4 text-blue-500 font-bold">
PSI > 0.25 es la señal que la Sesión 12 conecta a un disparador real de reentrenamiento
</div>

---

# Lab de hoy

1. Desplegar el endpoint (`serve_fraude.py`)
2. Correr `monitor_drift.py` sobre los scores de la Sesión 10

<div class="mt-8 text-blue-500 font-bold">
Entregable: endpoint respondiendo + corrida de monitoreo con PSI interpretado
</div>

---
layout: center
class: text-center
---

# → Sesión 12

MLOps con Airflow — orquestando todo el ciclo
