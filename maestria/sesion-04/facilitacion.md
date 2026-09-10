# Facilitación — Sesión 04: Spark Core avanzado II — Skew y diagnóstico

> Guion de 3 horas: talking points + lab guiado. Retoma directamente el par de
> notebooks de la Sesión 3 — hoy sí se resuelve un caso real. Es la sesión más
> técnica del curso hasta este punto; dale el ritmo que necesite, el break está
> puesto exactamente a la mitad por algo.

## Antes de empezar (facilitador)

```bash
gcloud dataproc clusters list --region=us-central1
```

Ya van 3 sesiones creando/usando clusters (S1, S3, S4) — revisa huérfanos.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "La causa #1 de 'mi job de producción tarda 10 veces más de lo que debería'
> no es un cluster subdimensionado — es una sola clave que concentra la
> mayoría del trabajo, mientras el resto del cluster espera con los brazos
> cruzados. Hoy van a diagnosticar y resolver exactamente eso, con evidencia,
> no a prueba y error."

**Pregunta de apertura:**

> "Si `bank_transactions.csv` tiene 90% de sus filas en `MXN` y el resto
> repartido en 5 monedas más, ¿qué esperan que pase si agrupan por moneda en un
> cluster de 3 workers?"

**Ejemplo de actualidad:**

> "Este es exactamente el tipo de problema que hace que un pipeline de Black
> Friday de un retailer se caiga —no por volumen total, sino porque una sola
> categoría de producto concentra el tráfico y desbalancea el cluster."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Qué es skew, con el caso real (10 min)

Usa el ejemplo de `teoria.md` (MXN dominando `bank_transactions.csv`) — es
literalmente el dataset que van a usar hoy, no un ejemplo abstracto.

### Cómo se ve en el Spark UI (10 min)

Demo en vivo: abre el Spark UI de un job con skew (si tienes uno preparado de
antemano, mejor) y señala la pestaña Stages, columna de duración por task.
Pregunta: **"¿cuál de estas tasks es la sospechosa, y por qué?"**

### Tres estrategias de mitigación (20 min)

Recorre la tabla de `teoria.md` (salting, broadcast join, AQE) y, para salting,
escribe el código en vivo explicando cada línea — no lo pegues de un jalón:

```python
df_salado = df.withColumn("salt", (F.rand() * 10).cast("int"))
```

Pregunta antes de seguir: **"¿por qué 10 y no 2, o 100?"** (más salt = más
paralelismo pero más overhead de la segunda agregación — es un trade-off, no un
número mágico).

### Límites de AQE (5 min)

Punto rápido: AQE no anticipa skew en la primera lectura si el archivo de
origen ya viene desbalanceado.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Reproducir el skew (20 min)

```python
df = spark.read.csv(RUTA_BANK_TRANSACTIONS, header=True, inferSchema=True)
df.groupBy("currency").count().show()  # confirmar el desbalance real
```

**Deberías ver:** una moneda con órdenes de magnitud más filas que las demás.

```python
resumen = df.groupBy("currency").agg(F.sum("amount"))
resumen.explain(mode="formatted")  # capturar el plan ANTES de corregir
```

### Paso 2 — Aplicar salting (30 min)

```python
df_salado = df.withColumn("salt", (F.rand() * 10).cast("int"))
resumen_parcial = df_salado.groupBy("currency", "salt").agg(F.sum("amount").alias("suma_parcial"))
resumen_final = resumen_parcial.groupBy("currency").agg(F.sum("suma_parcial").alias("suma_total"))
resumen_final.explain(mode="formatted")  # capturar el plan DESPUÉS
```

**Deberías ver:** el mismo resultado que el Paso 1, pero con tiempos de
ejecución medibles distintos (revisar en el Spark UI, no solo el `.explain()`).

**Si no ven mejora:** el dataset de prueba puede no tener suficiente skew real
— confirmar con `.count()` por partición
(`df.rdd.glom().map(len).collect()`) antes de asumir que salting no funcionó.

### Paso 3 — Comparar con broadcast join (20 min)

Si el caso lo permite (join contra una tabla pequeña de catálogo), mostrar la
alternativa:

```python
from pyspark.sql.functions import broadcast
resultado = df.join(broadcast(df_catalogo), "currency")
```

**Pregunta:** "¿cuándo elegirían salting sobre broadcast join, si ambos
resuelven skew?" (broadcast solo aplica si una tabla es pequeña; salting sirve
para skew dentro de una sola tabla grande).

### Paso 4 — Documentar el entregable (20 min)

Cada quien arma su notebook final: plan antes, plan después, tiempos medidos,
y una frase explicando qué estrategia usaron y por qué.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Recordatorio de apagado del cluster.**

**Entregable de hoy:** notebook con diagnóstico + solución aplicada + métricas
de mejora (plan antes/después + tiempos).

**Puente a la Sesión 5:**

> "Hoy resolvimos un problema de performance. La próxima sesión cambiamos de
> tema — dejamos de optimizar cómputo y empezamos a construir features para un
> modelo. Va a sentirse como un tipo de trabajo distinto, pero el mismo
> `bank_transactions.csv` que hoy diagnosticaron es el que van a usar."

---

## Notas de costo GCP

- Esta es la sesión más pesada en cómputo hasta ahora — el dataset completo
  (7.5GB) con varias corridas de comparación (antes/después, salting,
  broadcast) puede acumular tiempo de cluster. Considera trabajar sobre una
  muestra (`df.sample(0.1)`) para las iteraciones de prueba y solo correr el
  dataset completo para la captura final del entregable.
