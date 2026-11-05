# Caso de apertura — una decisión con consecuencias

Caso hipotético: 99 tareas terminan rápido y una continúa varios minutos. La CPU promedio parece baja. ¿Hace falta otra máquina o una clave concentra el trabajo?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Skew significa distribución desigual del trabajo. Repartir por una clave muy frecuente puede concentrar datos en una partición. Promediar duración oculta esa cola; compara máximo, mediana y distribución de tasks.

En el ejemplo, un millón de filas sintéticas concentra 90% en una clave: se diseña para observar el fenómeno, no para acreditar datos reales.

---

# Elegir bien exige reconocer el límite

Broadcast evita repartir el lado grande cuando la dimensión pequeña cabe con margen. AQE ajusta partes del plan con estadísticas de ejecución, pero no resuelve cualquier forma de skew. Salting reparte una clave y luego exige recombinar correctamente; sin ese paso cambia la respuesta.

---

# Laboratorio guiado — preparación y objetivo

Retomar S3 y Spark UI. Preparar una dimensión pequeña de claves sin duplicados. Objetivo: diagnosticar y aplicar una mitigación correcta en 90 minutos; no implementar las tres desde cero.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — observar una distribución desigual

Ejecuta el ejemplo y muestra frecuencias por clave. Predice cuál dominará. Anota el número de particiones y la configuración AQE.

---

# Laboratorio · paso 2 — diagnosticar antes de corregir

Materializa un join con una dimensión pequeña y mira las tasks y el plan final. Si AQE ya evita el skew, registra ese resultado; no afirmes que el problema sigue presente solo porque fue diseñado así.

---

# Laboratorio — ejecuta y comprueba

Ejemplo sintético en Spark:
```python
from pyspark.sql import functions as F
skew = spark.range(1_000_000).withColumn(
    "clave", F.when(F.col("id") < 900_000, 0).otherwise(F.col("id") % 100))
skew.groupBy("clave").count().orderBy(F.desc("count")).show(5)
dim = spark.range(100).withColumnRenamed("id", "clave")
skew.join(F.broadcast(dim), "clave").explain("formatted")
```

---

# Laboratorio · paso 3 — probar una estrategia

Compara join normal y broadcast de la dimensión acotada. Para un agregado sesgado, bosqueja salting en dos etapas y verifica que sumas y conteos se conservan.

---

# Laboratorio · paso 4 — medir y justificar

Conserva entrada, acción y recursos. Compara al menos tres ejecuciones y muestra máximo/mediana de tasks. Defiende cuándo tu estrategia dejaría de ser segura.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar distribución de claves, diagnóstico, igualdad de resultados y medidas. Una mitigación que cambia el total es incorrecta aunque termine más rápido.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No aparece cola de tareas: la muestra o AQE pueden esconderla. Broadcast falla: el lado pequeño no cabe con margen. Salting cambia cifras: hay duplicación del lado de join o falta reagregación.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 90 minutos: implementar salting reproducible y comparar con AQE. Añade una prueba de igualdad de resultados y registra consumo de memoria.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Planes y optimización Spark](https://archive.apache.org/dist/spark/docs/3.5.3/sql-performance-tuning.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
