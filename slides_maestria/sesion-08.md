---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 08 — Data Lakes / Lakehouse II: transacciones y versionado"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 08: MERGE INTO, time travel, evolución de esquema, versionado
---

# Sesión 08
## Data Lakes / Lakehouse II
### Transacciones y versionado

<div class="pt-6 text-sm opacity-60">
La Sesión 7 dejó una tabla Iceberg lista — hoy se usan las tres operaciones que justifican que exista
</div>

---

# Lo que Iceberg SÍ puede hacer

<div class="grid grid-cols-1 gap-2 mt-6 text-left">

- <code>MERGE INTO</code> — solo las filas afectadas, sin reescribir la tabla
- Time travel — <code>SELECT * FROM tabla.snapshots</code>, consultar el pasado
- <code>ALTER TABLE ADD COLUMN</code> — sin tocar nada existente

</div>

---

# MERGE INTO, en acción

```sql
MERGE INTO local.curso_bigdata.transacciones_silver t
USING correcciones c
ON t.transaction_id = c.transaction_id
WHEN MATCHED THEN UPDATE SET t.currency = c.currency
```

<div v-click class="mt-4 text-sm opacity-70">
Internamente: Iceberg escribe SOLO archivos nuevos con las filas corregidas — no reescribe la tabla completa
</div>

---

# Time travel en acción

```sql {1-3|5-7}
SELECT snapshot_id, committed_at, operation
FROM local.curso_bigdata.transacciones_silver.snapshots
ORDER BY committed_at;

-- Consultar la tabla como estaba ANTES del MERGE
SELECT * FROM local.curso_bigdata.transacciones_silver
VERSION AS OF <snapshot_id>;
```

<div v-click class="mt-4 text-blue-500 font-bold">
"¿Qué decía esta tabla el día que se tomó esta decisión?" — Parquet plano no puede responder esto
</div>

---

# Versionar datos y modelos no es como versionar código

<v-clicks>

- Datasets: **GB, no KB** — snapshots de Iceberg evitan duplicar lo que no cambió
- Modelos: sin versionar el dataset + hiperparámetros, "¿con qué se entrenó esto?" es irrespondible en 6 meses
- `04_pipeline_ml.ipynb` guarda el `PipelineModel` **completo** — feature engineering incluido, no solo el algoritmo

</v-clicks>

---

# Lab de hoy

Retomar la tabla de la Sesión 7 y completar `06_lakehouse_iceberg.py`:

1. `MERGE INTO` — corrección simulada
2. Consultar el snapshot anterior (time travel)
3. `ALTER TABLE` — agregar columna sin romper nada
4. Escribir la capa **gold** agregada

<div class="mt-6 text-blue-500 font-bold">
Entregable: diagrama de arquitectura + pipeline versionado + evidencia de las tres operaciones
</div>

---
layout: center
class: text-center
---

# → Sesión 09

Streaming I — windowing, watermarks, setup de Pub/Sub Lite
