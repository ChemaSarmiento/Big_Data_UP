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

```python
correcciones = (
    spark.table("local.curso_bigdata.transacciones_silver")
    .filter(F.col("currency") == "USD").limit(1000)
    .withColumn("currency", F.lit("MXN"))
)
correcciones.createOrReplaceTempView("correcciones")
```

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

# Paso — Time travel real

```python
primer_snapshot_id = snapshots.first()["snapshot_id"]
antes_del_merge = (
    spark.read.format("iceberg")
    .option("snapshot-id", primer_snapshot_id)
    .load("local.curso_bigdata.transacciones_silver")
)
```

<div class="mt-4 text-sm opacity-70">
Deberías ver: al filtrar por currency='USD' sobre antes_del_merge, las 1000 filas siguen ahí — la tabla "recordó" cómo estaba
</div>

---

# Paso — Evolución de esquema + capa gold

```sql
ALTER TABLE local.curso_bigdata.transacciones_silver ADD COLUMN es_horario_nocturno BOOLEAN;
UPDATE local.curso_bigdata.transacciones_silver
SET es_horario_nocturno = (hora_del_dia < 6 OR hora_del_dia > 22);
```

```python
gold = (
    spark.table("local.curso_bigdata.transacciones_silver")
    .groupBy("currency", "es_horario_nocturno")
    .agg(F.count("*").alias("num_transacciones"), F.avg("amount").alias("monto_promedio"))
)
gold.writeTo("local.curso_bigdata.transacciones_gold").using("iceberg").createOrReplace()
```

<div class="mt-4 p-4 border-l-4 border-blue-500 font-bold">
Entregable: diagrama de arquitectura + pipeline versionado + evidencia de las tres operaciones (MERGE, snapshots antes/después, ALTER TABLE)
</div>

<div class="mt-2 text-sm opacity-70">
Ahora sí: apagar el cluster con Iceberg
</div>

---
layout: center
class: text-center
---

# → Sesión 09

Streaming I — windowing, watermarks, setup de Pub/Sub Lite
