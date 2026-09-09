# Teoría — Sesión 04: Spark Core avanzado II — Skew y diagnóstico

> Segunda de dos sesiones sobre el motor interno de Spark. La Sesión 3 dejó el
> diagnóstico (leer un plan, identificar shuffles); hoy se resuelve el caso más común
> y más caro de performance distribuido: una clave que concentra el trabajo.

## 1. Qué es skew, con un caso real

**Skew** (desbalance) ocurre cuando una clave concentra muchas más filas que las
demás — el trabajador que procesa esa clave se convierte en cuello de botella mientras
el resto del cluster espera ocioso. Es la causa #1 de "mi job tarda 10x más de lo que
debería" en producción, y es engañoso de detectar solo con `.count()` o promedios:
el trabajo total puede verse balanceado en agregado, mientras una sola partición carga
el 80% del tiempo real.

**Ejemplo concreto sobre `bank_transactions.csv`:** si la mayoría de las transacciones
del dataset están en `MXN` y solo una fracción pequeña en otras monedas, un
`groupBy("currency")` reparte casi todo el trabajo a una sola partición — las demás
particiones (`USD`, `EUR`, etc.) terminan en segundos, la partición de `MXN` puede
tardar minutos, y el job completo espera a que termine esa sola partición.

## 2. Cómo se ve un skew severo en el plan

Antes de corregir, hay que confirmar que el problema es skew y no otra cosa (cluster
subdimensionado, I/O lento). Señales en el Spark UI (no solo en `.explain()`):

- Una tarea (*task*) dentro de una etapa (*stage*) tarda notablemente más que las
  demás — visible en la pestaña "Stages" del Spark UI, columna de duración por task.
- El tamaño de datos leído/escrito (*shuffle read/write*) de esa tarea es
  desproporcionadamente mayor que el resto.

`.explain(mode="formatted")` (Sesión 3) confirma *dónde* ocurre el shuffle; el Spark
UI confirma *si está desbalanceado* — son dos herramientas complementarias, no una
sustituye a la otra.

## 3. Tres estrategias de mitigación

| Estrategia | Cómo funciona | Cuándo usarla |
|---|---|---|
| **Salting** | Se agrega un sufijo aleatorio a la clave sesgada antes del shuffle (ej. `"MXN"` → `"MXN_0"`, `"MXN_1"`, ...), repartiendo artificialmente esa clave entre más particiones, y se agrega en dos etapas | Cuando una sola clave (ej. una moneda dominante) concentra la mayoría de las filas |
| **Broadcast join** | Si una de las dos tablas del join es pequeña (cabe en memoria de cada worker), se envía una copia completa a cada nodo en vez de hacer shuffle de ambas | Join entre una tabla grande y una tabla de catálogo/dimensión pequeña — el patrón más común en la práctica |
| **AQE** (Adaptive Query Execution) | Spark re-optimiza el plan de ejecución *durante* la corrida, con estadísticas reales (no estimadas) — puede convertir un shuffle join en broadcast join sobre la marcha, o repartir automáticamente particiones desbalanceadas | Activado por default desde Spark 3.x (`spark.sql.adaptive.enabled`); reduce la necesidad de salting manual en muchos casos |

### Salting, en código

```python
from pyspark.sql import functions as F

# Antes: groupBy("currency") concentra casi todo en la partición "MXN"
# Después: se agrega un salt aleatorio (0-9) para repartir esa clave en 10 sub-particiones
df_salado = df.withColumn("salt", (F.rand() * 10).cast("int"))
resumen_parcial = (
    df_salado.groupBy("currency", "salt")
    .agg(F.sum("amount").alias("suma_parcial"))
)
# Segunda etapa: agregar los resultados parciales por clave real, sin el salt
resumen_final = (
    resumen_parcial.groupBy("currency")
    .agg(F.sum("suma_parcial").alias("suma_total"))
)
```

**Por qué funciona:** la primera agregación reparte el trabajo de `MXN` entre 10
particiones distintas (por el salt), y la segunda agregación —mucho más barata—
solo suma 10 resultados parciales por moneda en vez de procesar millones de filas
en una sola partición.

## 4. Por qué AQE no siempre es suficiente

AQE ayuda mucho, pero tiene límites que vale la pena conocer antes de asumir que
"ya no hace falta pensar en skew":

- AQE detecta y corrige skew **entre etapas** (usando estadísticas reales de la etapa
  anterior) — no puede anticipar skew *dentro* de la primera lectura de datos si el
  archivo de origen ya viene desbalanceado por partición física.
- El umbral de qué cuenta como "partición sesgada" (`skewedPartitionFactor`,
  `skewedPartitionThresholdInBytes`) tiene defaults razonables, pero en datasets muy
  grandes (como `bank_transactions.csv`, 7.5GB) puede necesitar ajuste manual.

El ejercicio de hoy resuelve el caso "a mano" con salting explícito precisamente para
entender qué está haciendo AQE automáticamente en otros casos — no tiene sentido
depender de una herramienta que no se entiende.

---

## Referencias

- [Databricks — Handling Data Skew in Apache Spark](https://www.databricks.com/blog/2020/12/16/managing-data-skew-in-apache-spark.html)
- [Apache Spark — Adaptive Query Execution](https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution)
- [Apache Spark — Monitoring and Instrumentation (Spark UI)](https://spark.apache.org/docs/latest/monitoring.html)
