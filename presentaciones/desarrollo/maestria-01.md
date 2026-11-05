# Caso de apertura — una decisión con consecuencias

Caso hipotético: una organización procesa logs cada noche. Al duplicar el volumen, el trabajo termina después de la hora en que se necesita el reporte. ¿Dividir el trabajo entre más máquinas resuelve el problema, o la coordinación será el nuevo cuello de botella?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

El driver construye y coordina el plan; los executors ejecutan tareas sobre particiones. Una transformación describe trabajo y una acción lo desencadena. La distribución ayuda cuando el trabajo útil supera la coordinación, la transferencia y la lectura.

En una agregación por clave, los conteos parciales deben reunirse. Esa frontera explica el shuffle y anticipa por qué añadir nodos no reduce todos los tiempos por igual.

---

# Elegir bien exige reconocer el límite

CAP se interpreta durante una partición de red: el sistema no puede garantizar simultáneamente la consistencia definida por el teorema y una respuesta disponible para toda petición. No significa escoger permanentemente dos letras.

Una muestra pequeña puede ser más rápida en una sola máquina. Ese resultado no invalida Spark: obliga a justificar escala, recuperación y plazo de entrega.

---

# Laboratorio guiado — preparación y objetivo

Usa `recursos/spark/01_rdd_basico.ipynb` y la receta del cluster temporal. Antes de clase: acceso, CSV o texto de muestra y entorno compatible. Objetivo: explicar particiones y medir un conteo, no convertir el tiempo de creación del cluster en tiempo del algoritmo.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — predecir el recorrido

Dibuja entrada → particiones → conteo local → agrupación por palabra → resultado. Marca dónde se envían datos entre nodos. Predice qué cambiará al pasar de dos a cuatro particiones.

---

# Laboratorio · paso 2 — ejecutar dos configuraciones

Corre el mismo conteo con dos y cuatro particiones, materializando el resultado con una acción. Haz una ejecución de calentamiento y tres medidas por configuración. Conserva tamaño, número de nodos y condiciones de caché.

---

# Laboratorio — ejecuta y comprueba

En un notebook con `spark` disponible:
```python
from collections import Counter
lines = ["dato dato nube", "nube escala"]
rdd = spark.sparkContext.parallelize(lines, 2)
counts = (rdd.flatMap(str.split).map(lambda w: (w, 1))
          .reduceByKey(lambda a, b: a + b))
assert dict(counts.collect()) == dict(Counter(" ".join(lines).split()))
```
Este ejemplo sintético verifica el mecanismo; no acredita escala real.

---

# Laboratorio · paso 3 — leer el trabajo real

En Spark UI identifica jobs, stages y tasks. Asocia la agrupación con su frontera de intercambio. Distingue duración total, lectura y shuffle; no atribuyas toda diferencia al paralelismo.

---

# Laboratorio · paso 4 — defender una arquitectura

Comprueba igualdad de conteos. Redacta una recomendación para el plazo del caso: máquina única, batch distribuido o cambio del almacenamiento. Indica cuál experimento falta para extrapolar a mayor volumen.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar un diagrama anotado y una tabla de medidas. El conteo debe ser idéntico; el tiempo puede mejorar o empeorar. La explicación debe conectar la diferencia con tareas, transferencia o lectura.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No aparece un job: falta una acción. El primer tiempo es mucho mayor: separa inicialización. Hay más tareas pero ninguna mejora: revisa tamaño de la muestra y overhead. No compares MapReduce y Spark con entradas o configuraciones distintas.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60–90 minutos: repetir con un archivo mayor y comparar una implementación MapReduce preparada. Un benchmark completo de ambos motores va fuera del núcleo si requiere instalar Hadoop o desarrollar el job desde cero.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [RDD y ejecución distribuida](https://archive.apache.org/dist/spark/docs/3.5.3/rdd-programming-guide.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
