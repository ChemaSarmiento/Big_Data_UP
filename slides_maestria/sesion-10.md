---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 10 — Streaming II: inferencia en tiempo real"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 10: scoring en tiempo real, feature freshness
---

# Sesión 10
## Streaming II
### Inferencia en tiempo real

<div class="pt-6 text-sm opacity-60">
El modelo de la Sesión 6 se reutiliza sin cambios — mismo pipeline de la Sesión 9, con scoring agregado
</div>

---

# Dos patrones de scoring en tiempo real

| Patrón | Cómo | Trade-off |
|---|---|---|
| **Modelo en el stream** | `PipelineModel` cargado una vez, aplicado directo | Baja latencia, se actualiza solo al reiniciar el job |
| Endpoint externo | `POST` HTTP por evento/microlote | Se actualiza sin tocar el streaming, a cambio de latencia de red |

<div v-click class="mt-6 text-sm opacity-70">
Este curso usa el primero hoy y el segundo en serving (Sesión 11) — mismo modelo, comparación directa
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
    S -->|PipelineModel S5/6| Score[Score por transacción]
    S --> W[Alertas por ventana 1min]
```

<div v-click class="mt-4 text-sm opacity-70">
Mismo esqueleto de la Sesión 9 (07a_streaming_conteo.py) + el modelo cargado
</div>

<div class="mt-6 text-blue-500 font-bold">
Entregable: pipeline funcionando end-to-end — captura de ventanas en vivo + Parquet de scores
</div>

---
layout: center
class: text-center
---

# → Sesión 11

Model serving y monitoreo — endpoint, drift (PSI)
