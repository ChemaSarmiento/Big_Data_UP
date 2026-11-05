# Caso de apertura — una decisión con consecuencias

Caso hipotético: dos personas ejecutan el mismo notebook y obtienen resultados diferentes. Una usa otro archivo y otra interpreta fechas en otra zona horaria. Antes de aprender Spark, ¿cómo hacemos comparable una práctica?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Un entorno reproducible incluye versión del código, intérprete, dependencias, entrada y configuración. Credenciales y permisos resuelven identidad/acceso; no son características del dataset. El crédito es un medio de financiar recursos, no una garantía de costo cero.

---

# Elegir bien exige reconocer el límite

La nivelación es asíncrona antes de S1. Instalar herramientas durante cada laboratorio desplaza el tiempo de aprendizaje. Validar acceso con un recurso pequeño permite descubrir permisos o incompatibilidades sin lanzar un cluster costoso.

---

# Laboratorio guiado — preparación y objetivo

Seguir `environment/gcp-setup.md`. Maestría verifica Python 3.11/Java 17 y ADC; Especialidad verifica consola y notebook preparado. Esta práctica pertenece al módulo previo, fuera de las 27/39 horas presenciales.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — identificar archivos y rutas

Abre la raíz del repo y ubica environment, recursos y presentaciones. Distingue path local de URI gs://. Registra branch plan2 y entrada exacta.

---

# Laboratorio · paso 2 — hacer una transformación pequeña

En Python cuenta nulos de una lista y en SQL agrupa una tabla de práctica. Explica tipos y el orden de ejecución. No uses una respuesta memorizada si cambias la entrada.

---

# Laboratorio · paso 3 — verificar acceso

Selecciona proyecto y revisa identidad activa, bucket y permiso mínimo. Comprueba saldo y presupuesto. No pegues claves o tokens en notebooks ni Git.

---

# Laboratorio · paso 4 — cerrar el checkpoint

Entrega captura del entorno y mini consulta interpretada. Si falta acceso, resuélvelo antes de S1. Activa crédito al comenzar prácticas cloud, evitando consumir días de prueba durante preparación local.

---

# Laboratorio — ¿qué demuestra el resultado?

El checkpoint acredita acceso y vocabulario mínimo. Poder abrir consola no demuestra que ADC funcione para un script; verificar ambos si la práctica los requiere.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Comando no existe: entorno equivocado. URI no abre en filesystem: es almacenamiento remoto. Permiso negado: revisar identidad y rol, no ampliar a Owner como solución rutinaria.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Estimar 60–120 minutos de preparación según experiencia. Es carga de planificación, no un tiempo medido con este grupo. Resolver bloqueos antes de reservar cómputo.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Crédito y límites de GCP](https://docs.cloud.google.com/free/docs/free-cloud-features).
- [Permisos y recursos IAM](https://docs.cloud.google.com/iam/docs/overview).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
