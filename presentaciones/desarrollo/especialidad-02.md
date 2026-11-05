# Caso de apertura — una decisión con consecuencias

Caso hipotético: diez personas cuentan palabras de un documento dividiendo páginas. Al reunir resultados descubren que no acordaron mayúsculas ni puntuación. ¿Qué debe compartirse para que el total sea correcto?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Distribuir una tarea exige separar trabajo y luego combinar resultados con reglas coherentes. Partición no significa una respuesta independiente: el resultado final puede requerir reunir la misma clave. El tiempo total incluye reparto, cálculo y coordinación.

---

# Elegir bien exige reconocer el límite

Más trabajadores no garantizan menor demora: algunos pueden recibir más páginas o claves que otros. Una partición muy grande domina el cierre. La analogía permite reconocer skew sin implementar tuning.

---

# Laboratorio guiado — preparación y objetivo

Usar conteo de palabras preparado y una muestra pequeña. Actividad guiada en la misma sesión; no se requiere escribir infraestructura. Observar entrada, tareas y resultado.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — repartir y acordar

Divide un texto entre equipos y acuerda tratamiento de mayúsculas y signos. Cada equipo entrega palabra/conteo, no su interpretación libre.

---

# Laboratorio · paso 2 — reunir por clave

Combina los conteos de la misma palabra. Identifica qué información necesita viajar entre equipos y qué puede resumirse localmente.

---

# Laboratorio · paso 3 — observar Spark

Abre `01_rdd_basico.ipynb`, ejecuta la muestra y cambia el número de particiones. Cuenta tareas y compara con la analogía; la respuesta debe conservarse.

---

# Laboratorio · paso 4 — crear un desequilibrio

Entrega más texto a un equipo y observa cuánto tarda el cierre. Dibuja por qué el promedio no identifica al último trabajador. Relaciona el ejemplo con particiones reales.

---

# Laboratorio — ¿qué demuestra el resultado?

Entrega diagrama de reparto/reunión y explicación del resultado. Debe distinguirse paralelismo de trabajo total y señalarse una fuente de desigualdad.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Conteos distintos: se aplicaron reglas diferentes o se omitieron fragmentos. Spark no muestra trabajo: falta una acción. Un ejemplo pequeño no prueba que un cluster sea más rápido.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 30 minutos: repetir con texto de otra fuente y documentar normalización. Comparar el resultado con un conteo local sencillo.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [RDD y ejecución distribuida](https://archive.apache.org/dist/spark/docs/3.5.3/rdd-programming-guide.html).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
