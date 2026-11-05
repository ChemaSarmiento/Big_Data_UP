# Caso de apertura — una decisión con consecuencias

Caso hipotético: cada mañana llega un archivo de precios; al reejecutar el proceso, el dashboard duplica cifras. El flujo “corrió bien”, pero la decisión de compras quedó mal. ¿Qué control faltó?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

ETL conecta una fuente con un consumidor. Extract conserva origen; transform aplica reglas; load publica un resultado. Cada frontera necesita contrato y comprobación. Reejecutar sin duplicar la salida es una propiedad que se diseña, no algo que ocurre por usar una herramienta.

---

# Elegir bien exige reconocer el límite

Una tabla final correcta no basta si no puedes explicar filas rechazadas, fechas y cambios. Un dashboard atractivo tampoco demuestra un ETL válido. La secuencia de aprendizaje es entrada → control → transformación → salida → conclusión.

---

# Predice el resultado antes de comprobarlo

Al limpiar datos, 1000 filas de entrada producen 950 válidas y 30 rechazadas. ¿Publicar?

<div class="knowledge-check">
<button type="button" data-correct="false">Sí, el resultado se ve bien</button>
<button type="button" data-correct="true">No: faltan 20 filas por explicar</button>
<button type="button" data-correct="false">Sí, si el gráfico tiene título</button>
<p class="check-feedback" role="status" hidden data-explanation="La reconciliación no cuadra. Investiga filtros y joins antes de publicar una cifra confiable."></p>
</div>

---

# Laboratorio guiado — preparación y objetivo

Usar la muestra y notebook guiado de S4 para construir un ETL de precios coherente. No mezclar notebook de tipo de cambio y dashboard cripto como si fueran un pipeline único. Preparar CSV con producto, precio y estado.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — definir un contrato

Anota columnas, tipo de precio, campos obligatorios y regla de rechazo. Cuenta filas de entrada. Conserva una copia raw de la muestra sin modificar.

---

# Laboratorio · paso 2 — limpiar sin ocultar pérdidas

Normaliza precio y separa registros inválidos. Usa el código de controles; explica por qué un precio inválido no debe reemplazarse por cero.

---

# Laboratorio — ejecuta y comprueba

Con `df` del notebook de S4 y precio ya numérico:
```python
from pyspark.sql import functions as F
ok = F.col("precio").isNotNull() & (F.col("precio") > 0)
validas = df.filter(ok)
rechazadas = df.filter(~F.coalesce(ok, F.lit(False)))
assert df.count() == validas.count() + rechazadas.count()
validas.groupBy("estado").agg(F.count("*").alias("n")).show()
```
Añade controles de producto/presentación antes de comparar precios.

---

# Laboratorio · paso 3 — publicar una salida

Agrega precio promedio y observaciones por estado para un solo producto/presentación. Guarda el agregado en una ruta de prueba exclusiva; reejecuta con política explícita de reemplazo.

---

# Laboratorio · paso 4 — crear una conclusión visual

Grafica solo grupos comparables con etiquetas y unidades. Incluye conteo antes/después y rechazo. Otro equipo debe poder reconstruir el resultado con la misma entrada.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar diagrama, controles, resultado y gráfico. Se debe cumplir entrada = válidas + rechazadas. El diagrama debe describir lo que se ejecutó, no una arquitectura aspiracional.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Reejecución duplica: revisar append frente a reemplazo o claves. No cuadra el conteo: un filtro o join pierde/duplica filas. Resultado vacío: revisar producto seleccionado antes de publicar.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60 minutos: adaptar el flujo a una fuente real del proyecto. Las integraciones con APIs, MariaDB o dashboards externos son ejercicios adicionales, no requisitos del núcleo.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Lectura y escritura Parquet](https://archive.apache.org/dist/spark/docs/3.5.3/sql-data-sources-parquet.html).
- [El contexto da significado a los datos](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
