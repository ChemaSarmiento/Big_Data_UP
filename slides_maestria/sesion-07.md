---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 07 — Streaming e inferencia en tiempo real"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 07: windowing, watermarks, Pub/Sub Lite, scoring en el stream
---

# Sesión 07
## Streaming e inferencia en tiempo real

<div class="pt-6 text-sm opacity-60">
El modelo de la Sesión 4/5 se reutiliza sin cambios — lo que cambia es el contexto: datos que nunca terminan de llegar
</div>

---

# Windowing + watermark

```mermaid {scale: 0.6}
flowchart LR
    subgraph "Ventana 12:00-12:01"
    E1[evento 12:00:05]
    E2[evento 12:00:40]
    E3["evento 12:00:55<br/>(llega tarde, watermark 2min)"]
    end
    E1 --> R[Resultado ventana]
    E2 --> R
    E3 -.tolerado.-> R
```

```python
scoreadas
    .withWatermark("timestamp", "2 minutes")
    .groupBy(F.window("timestamp", "1 minute"))
    .count()
```

---

# Exactly-once ≠ sin duplicados en el broker

<v-clicks>

- El checkpoint + watermark dan exactly-once en el **cálculo de la ventana**
- Esa es una garantía distinta de "el mensaje nunca llegó dos veces"
- Esa segunda garantía la da **Pub/Sub Lite**, del lado del envío

</v-clicks>

<div v-click class="mt-8 p-4 border-l-4 border-blue-500">
Confundir ambas garantías lleva a asumir más seguridad de la que realmente se tiene
</div>

---

# Dos patrones de scoring en tiempo real

| Patrón | Cómo | Trade-off |
|---|---|---|
| **Modelo en el stream** | `PipelineModel` cargado una vez, aplicado directo | Baja latencia, se actualiza solo al reiniciar el job |
| Endpoint externo | `POST` HTTP por evento/microlote | Se actualiza sin tocar el streaming, a cambio de latencia de red |

<div v-click class="mt-6 text-sm opacity-70">
Este curso usa el primero en streaming (Sesión 7) y el segundo en serving (Sesión 8) — mismo modelo, comparación directa
</div>

---

# Feature freshness: un detalle que rompe modelos en producción

```python {1|3}
# BIEN: derivado del timestamp del EVENTO
.withColumn("hora_del_dia", F.hour("timestamp"))

# MAL: derivado del momento de PROCESAMIENTO
.withColumn("hora_del_dia", F.hour(F.current_timestamp()))
```

<div v-click class="mt-6 text-blue-500 font-bold">
Si el stream se atrasa, la versión "MAL" queda sistemáticamente equivocada
</div>

---

# Pipeline de hoy

```mermaid {scale: 0.55}
flowchart LR
    P[producer_transacciones_stream.py] -->|Pub/Sub Lite| S[07_streaming_scoring.py]
    S -->|PipelineModel S4/5| Score[Score por transacción]
    S --> W[Alertas por ventana 1min]
```

<div class="mt-6 text-blue-500 font-bold">
Entregable: pipeline funcionando end-to-end — captura de ventanas en vivo + Parquet de scores
</div>

---
layout: center
class: text-center
---

# → Sesión 08

Model serving, monitoreo y MLOps — endpoint, drift (PSI), Airflow
