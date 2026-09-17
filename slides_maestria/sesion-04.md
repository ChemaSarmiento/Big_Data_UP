---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 04 — Spark Core avanzado II: skew y diagnóstico"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 04: skew, salting, broadcast join, AQE, diagnóstico completo
---

# Sesión 04
## Spark Core avanzado II
### Skew y diagnóstico

<div class="pt-6 text-sm opacity-60">
La Sesión 3 dejó el diagnóstico — hoy se resuelve el caso más común y más caro de performance distribuido
</div>

---

# Skew: cuando una clave concentra el trabajo

```mermaid {scale: 0.55}
flowchart TD
    W1[Worker 1: MXN<br/>2M filas] -->|tarda 10x más| Wait[Todos esperan]
    W2[Worker 2: USD<br/>50K filas] --> Wait
    W3[Worker 3: EUR<br/>30K filas] --> Wait
```

<div v-click class="mt-4">
El resto del cluster termina y <b>espera ocioso</b> a que uno solo acabe
</div>

<div v-click class="mt-4 text-sm opacity-70">
No se ve en un .count() global — hay que mirar la duración por task en el Spark UI
</div>

---

# Tres formas de mitigar skew

<v-clicks>

- **Salting** — sufijo aleatorio a la clave sesgada, repartiendo artificialmente
- **Broadcast join** — la tabla pequeña se copia entera a cada worker, sin shuffle
- **AQE** (Adaptive Query Execution) — Spark re-optimiza *durante* la corrida, con estadísticas reales

</v-clicks>

<div v-click class="mt-8 text-sm opacity-70">
AQE está activado por default desde Spark 3.x — reduce la necesidad de salting manual
</div>

---

# Salting, en código

```python {1-2|3-8|9-13}
df_salado = df.withColumn("salt", (F.rand() * 10).cast("int"))

resumen_parcial = (
    df_salado.groupBy("currency", "salt")
    .agg(F.sum("amount").alias("suma_parcial"))
)

resumen_final = (
    resumen_parcial.groupBy("currency")
    .agg(F.sum("suma_parcial").alias("suma_total"))
)
```

<div v-click class="mt-4 text-sm opacity-70">
La primera etapa reparte MXN en 10 sub-particiones; la segunda solo suma 10 resultados parciales
</div>

---

# AQE no siempre es suficiente

<v-clicks>

- Corrige skew **entre etapas**, con estadísticas reales de la etapa anterior
- No anticipa skew **dentro de la primera lectura** si el archivo ya viene desbalanceado
- Los umbrales de detección tienen defaults que a veces necesitan ajuste manual

</v-clicks>

<div v-click class="mt-8 p-4 border-l-4 border-blue-500">
El ejercicio de hoy resuelve "a mano" con salting explícito — para entender qué hace AQE automáticamente en otros casos
</div>

---

# Lab de hoy

Mismo par de notebooks de la Sesión 3 (`02_dataframes.ipynb`,
`03_spark_sql.ipynb`) — ahora con un caso real de skew sobre
`bank_transactions.csv`

---

# Paso 1 — Reproducir el skew

```python
df = spark.read.csv(RUTA_BANK_TRANSACTIONS, header=True, inferSchema=True)
df.groupBy("currency").count().show()  # confirmar el desbalance real
```

```python
resumen = df.groupBy("currency").agg(F.sum("amount"))
resumen.explain(mode="formatted")  # capturar el plan ANTES de corregir
```

<div class="mt-4 text-sm opacity-70">
<b>Deberías ver:</b> una moneda con órdenes de magnitud más filas que las demás
</div>

---

# Paso 2 — Aplicar salting

```python
df_salado = df.withColumn("salt", (F.rand() * 10).cast("int"))
resumen_parcial = df_salado.groupBy("currency", "salt").agg(F.sum("amount").alias("suma_parcial"))
resumen_final = resumen_parcial.groupBy("currency").agg(F.sum("suma_parcial").alias("suma_total"))
resumen_final.explain(mode="formatted")  # capturar el plan DESPUÉS
```

<div class="mt-4 text-sm opacity-70">
<b>Si no ves mejora:</b> confirma el skew real con <code>df.rdd.glom().map(len).collect()</code> antes de asumir que salting no funcionó
</div>

---

# Paso 3 — Comparar con broadcast join

```python
from pyspark.sql.functions import broadcast
resultado = df.join(broadcast(df_catalogo), "currency")
```

<div class="mt-6 text-blue-500 font-bold">
¿Cuándo elegirías salting sobre broadcast join, si ambos resuelven skew?
</div>

<div class="mt-4 p-4 border-l-4 border-blue-500 font-bold">
Entregable: notebook con diagnóstico + solución aplicada + métricas de mejora (plan antes/después + tiempos)
</div>

---
layout: center
class: text-center
---

# → Sesión 05

Ingeniería de features a escala — Pipeline, Transformer, Estimator de MLlib
