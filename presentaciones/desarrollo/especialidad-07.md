# Caso de apertura — una decisión con consecuencias

Caso hipotético: un negocio pide “todo en tiempo real”. Su decisión principal se toma una vez al día, pero las alertas de operación necesitan minutos. ¿Debe todo el pipeline tener la misma latencia?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Batch procesa conjuntos delimitados; un flujo requiere trabajo continuo sobre eventos y estado. La latencia útil depende del tiempo en que alguien puede actuar. Producir un número antes no aporta valor si nadie lo utiliza ni confía en su estabilidad.

---

# Elegir bien exige reconocer el límite

Streaming añade recuperación, eventos tardíos y duplicados. Una ventana todavía abierta puede cambiar. El costo incluye operación continua, no solo velocidad de cálculo. La arquitectura del curso es de microlotes: no promete respuesta instantánea.

---

# Laboratorio guiado — preparación y objetivo

Demo guiada con `recursos/streaming/README.md` y ambiente preparado. No se requiere montar broker, puente y Spark desde cero en este track. Objetivo: seguir eventos y decidir si la demora se justifica.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — elegir la acción

Define quién recibe el dato y cuánto puede esperar. Distingue revisión diaria de alerta operativa. No definas “real time” sin una unidad de tiempo.

---

# Laboratorio · paso 2 — seguir eventos

Observa ID, timestamp del evento y momento en que aparece en la salida. Dibuja productor, almacenamiento y procesamiento.

---

# Laboratorio · paso 3 — introducir una anomalía

Observa un ID repetido y un evento tardío. Predice si el tablero debe cambiar. Explica por qué la llegada por duplicado no representa dos transacciones nuevas.

---

# Laboratorio · paso 4 — comparar alternativas

Completa una matriz batch, microlotes y online. Recomienda la más sencilla que permite actuar a tiempo y señala qué fallaría si el flujo se detiene.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar decisión de latencia y diagrama de un evento. La evidencia debe conectar demora con una acción real y reconocer costo de operación.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Nada aparece: verificar si la ventana ya finalizó. Latencia sin medida: registrar evento y observación, no usar “rápido”. Conteo duplicado: discutir el contrato de ID y el horizonte.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 30 minutos: identificar un proceso del proyecto donde batch sea suficiente y otro donde una menor demora cambie la decisión.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Tiempo de evento, estado y recuperación](https://archive.apache.org/dist/spark/docs/3.5.3/structured-streaming-programming-guide.html).
- [Reentrega y confirmación Pub/Sub](https://docs.cloud.google.com/pubsub/docs/subscribe-best-practices).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
