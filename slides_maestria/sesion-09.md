---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 09 — Streaming I: fundamentos y setup"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 09: windowing, watermarks, exactly-once, setup de Pub/Sub Lite
---

# Sesión 09
## Streaming I
### Fundamentos y setup

<div class="pt-6 text-sm opacity-60">
Datos que nunca terminan de llegar — hoy el mecanismo, sin modelo todavía. La Sesión 10 agrega el scoring.
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
transacciones
    .withWatermark("timestamp", "2 minutes")
    .groupBy(F.window("timestamp", "1 minute"), "currency")
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

# Por qué Pub/Sub Lite

<v-clicks>

- Spark no tiene conector nativo para Pub/Sub estándar
- **Pub/Sub Lite sí** — el único conector oficial de Google para Structured Streaming
- Se cobra por capacidad reservada, no por mensaje (no es Always Free)

</v-clicks>

```bash
gcloud pubsub lite-topics create transacciones-stream --location=us-central1-a --partitions=1 --per-partition-bytes=30GiB
gcloud pubsub lite-subscriptions create transacciones-stream-sub --location=us-central1-a --topic=transacciones-stream
```

---

# Lab de hoy

```mermaid {scale: 0.55}
flowchart LR
    P[producer_transacciones_stream.py] -->|Pub/Sub Lite| S[07a_streaming_conteo.py]
    S --> W[Conteo por ventana 1min]
```

Deliberadamente **sin modelo** — para ver windowing/watermarks funcionar solos.

<div class="mt-6 text-blue-500 font-bold">
Entregable: captura de las ventanas de conteo actualizándose en consola
</div>

---
layout: center
class: text-center
---

# → Sesión 10

Streaming II — inferencia en tiempo real con el modelo de la Sesión 6
