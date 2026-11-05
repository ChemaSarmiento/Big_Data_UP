# Caso de apertura — una decisión con consecuencias

Caso hipotético: dos equipos escriben el mismo agregado, uno con DataFrame API y otro con SQL. Uno afirma que SQL siempre será más lento. ¿La sintaxis determina el motor o debemos comparar los planes?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Spark traduce expresiones a un plan lógico y luego elige un plan físico. En fuentes compatibles, selección de columnas y filtros reducen trabajo. `explain("formatted")` muestra la estrategia, no el tiempo que tardará. Una acción y métricas de ejecución completan la evidencia.

---

# Elegir bien exige reconocer el límite

Un `Exchange` marca redistribución; puede ser necesario para reunir claves. El objetivo no es eliminar todos los exchanges, sino evitar trabajo que no cambia el resultado. Cachear solo ayuda si se reutiliza el resultado y el costo de materializarlo se amortiza.

---

# Predice el resultado antes de comprobarlo

Dos expresiones producen el mismo plan físico. ¿Qué esperarías?

<div class="knowledge-check">
<button type="button" data-correct="false">SQL siempre es más lento</button>
<button type="button" data-correct="true">Pueden tener rendimiento equivalente</button>
<button type="button" data-correct="false">DataFrame siempre evita shuffle</button>
<p class="check-feedback" role="status" hidden data-explanation="La sintaxis no demuestra una ventaja. Compara la misma acción, entrada y configuración; luego mide."></p>
</div>

---

# Laboratorio guiado — preparación y objetivo

Usar `02_dataframes.ipynb` y `03_spark_sql.ipynb` sobre la misma muestra bancaria. Guardar Parquet con `currency` y `amount`. Objetivo: comparar API y SQL y explicar un shuffle, dentro de 90 minutos.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — predecir las operaciones

Antes de ejecutar, marca lectura, filtro, agrupación y acción. Predice qué columnas necesita el agregado y qué claves deben reunirse.

---

# Laboratorio · paso 2 — contrastar expresiones equivalentes

Ejecuta las dos versiones del código. Guarda ambos planes y comprueba igualdad de resultados ordenados. Repite manteniendo caché y particiones constantes.

---

# Laboratorio — ejecuta y comprueba

Con `df` cargado:
```python
from pyspark.sql import functions as F
a = df.filter("amount > 0").groupBy("currency").agg(F.sum("amount").alias("total"))
df.createOrReplaceTempView("tx")
b = spark.sql("SELECT currency, SUM(amount) total FROM tx WHERE amount > 0 GROUP BY currency")
a.explain("formatted"); b.explain("formatted")
assert a.orderBy("currency").collect() == b.orderBy("currency").collect()
```

---

# Laboratorio · paso 3 — reducir lectura innecesaria

Compara seleccionar solo `currency` y `amount` frente a leer todas las columnas. Busca `ReadSchema` y filtros en el plan. Mide una acción; crear un DataFrame no mide el procesamiento.

---

# Laboratorio · paso 4 — explicar el Exchange

Anota el intercambio que exige `groupBy`. Compara duración y bytes de shuffle. Justifica si la mejora viene de lectura, red o CPU; una captura del plan sola no demuestra velocidad.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar planes anotados, igualdad de resultados y medidas. Si API y SQL producen el mismo plan, esa es una conclusión válida y más útil que una preferencia por sintaxis.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

El tiempo casi es cero: mediste construcción del plan. Resultados distintos: revisa filtro, tipos y nulos. Un `.count()` puede permitir optimizaciones distintas a materializar todos los agregados: mide la misma acción en ambos casos.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60 minutos: comparar dos joins y justificar broadcast usando tamaño real del lado pequeño. No fuerces broadcast de una tabla que no cabe en memoria.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Planes y optimización Spark](https://archive.apache.org/dist/spark/docs/3.5.3/sql-performance-tuning.html).
- [Lectura y escritura Parquet](https://archive.apache.org/dist/spark/docs/3.5.3/sql-data-sources-parquet.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
