---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 13 — Gobernanza, seguridad y capstone"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 13: IAM, Data Catalog, cumplimiento, FinOps, capstone técnico
---

# Sesión 13
## Gobernanza, seguridad y capstone

<div class="pt-6 text-sm opacity-60">
Cómo un pipeline de curso se vuelve algo que un equipo de banca podría operar de verdad
</div>

---

# IAM a nivel tabla, no solo proyecto

<v-clicks>

- Módulo 0: IAM de proyecto — quién crea/borra recursos
- Hoy: **mínimo privilegio** por dataset/columna/fila
- Ej: un analista ve montos, no nombres completos sin enmascarar

</v-clicks>

<div v-click class="mt-8 text-blue-500 font-bold">
"Todos con Owner porque es más simple" — exactamente lo que un auditor rechaza
</div>

---

# Data Catalog + linaje

```mermaid {scale: 0.6}
flowchart LR
    Raw[Dato crudo] -->|linaje| Bronze
    Bronze -->|linaje| Silver
    Silver -->|linaje| Gold[Dashboard]
```

<div v-click class="mt-6">
Con 5 datasets, cualquiera recuerda qué hay en cada uno. Con 500, sin catálogo nadie sabe qué existe.
</div>

---

# Cumplimiento en banca: tres exigencias reales

| Exigencia | Por qué |
|---|---|
| **Explicabilidad** | Negar una transacción real necesita justificación, no solo un score |
| **Trazabilidad** | Cada predicción rastreable hasta modelo + dato exactos |
| **Retención/borrado** | Un lake particionado facilita borrar por petición del titular |

<div v-click class="mt-4 text-sm opacity-70">
Regresión logística (Sesión 6) tiene ventaja aquí: coeficientes directamente interpretables
</div>

---

# FinOps: el costo es una decisión técnica disfrazada

<v-clicks>

- ¿Cuánto cuesta cada etapa del DAG? (ingesta, entrenamiento, serving)
- Reentrenar tiene costo explícito — **no** reentrenar con drift tiene costo implícito
- La puerta de calidad (AUC mínimo) **es** una decisión de FinOps

</v-clicks>

---

# El capstone: demostrar que las 8 sesiones son un solo sistema

<div class="grid grid-cols-2 gap-2 mt-6 text-sm">
<div class="p-2 border rounded">✓ Ingesta distribuida</div>
<div class="p-2 border rounded">✓ Features con MLlib</div>
<div class="p-2 border rounded">✓ Modelo evaluado</div>
<div class="p-2 border rounded">✓ Serving programado</div>
<div class="p-2 border rounded">✓ Streaming/orquestación</div>
<div class="p-2 border rounded border-blue-500">✓ Visualización</div>
<div class="p-2 border rounded border-blue-500">✓ Evidencia de pruebas</div>
</div>

<div class="mt-8 text-blue-500 font-bold text-center">
Máx. 15 minutos — mismo límite institucional que Especialidad
</div>

---
layout: center
class: text-center
---

# Fin del programa técnico

Profundización sugerida: Iceberg/Delta avanzado · GPUs distribuidas · feature stores productivos · BigQuery ML
