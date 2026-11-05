# Caso de apertura — una decisión con consecuencias

Caso hipotético: dos áreas publican cifras distintas sobre el mismo periodo. Una usa una carga reciente, otra un snapshot viejo; ninguna puede explicar permisos, calidad o costo. ¿Cómo confiar en la decisión?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Gobierno define propiedad, acceso, significado y trazabilidad. Un catálogo ayuda a encontrar y entender datos; no reemplaza validaciones ni responsabilidades. Linaje conecta fuente, transformaciones y consumidor para identificar dónde se introdujo una diferencia.

---

# Elegir bien exige reconocer el límite

Seguridad y calidad son dimensiones distintas: tener acceso autorizado no garantiza datos correctos. Un rol amplio simplifica una demo, pero agranda el impacto de un error. La retención exige justificar qué historia necesitas conservar y cuánto cuesta.

---

# Laboratorio guiado — preparación y objetivo

Taller integrado de gobernanza y revisión del proyecto. Preparar diagrama, contrato y una cifra cuya fuente pueda rastrearse. No crear nuevos servicios cloud para la discusión.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — rastrear una cifra

Elige una conclusión del caso o proyecto y retrocede hasta raw. Anota dataset, periodo, versión y transformaciones. Marca el primer punto donde las dos áreas difieren.

---

# Laboratorio · paso 2 — asignar responsabilidades

Define dueño del dato, consumidor y responsable de corregir. Especifica quién puede leer, escribir y borrar; justifica permisos por acción, no por cargo genérico.

---

# Laboratorio · paso 3 — poner límites al costo

Lista cómputo, almacenamiento, consultas e ingesta. Calcula horas previstas y retención; usa tarifas verificadas para tu configuración. No trates la asignación US$300 como cotización.

---

# Laboratorio · paso 4 — defender y cerrar

Presenta una decisión con evidencia visual y riesgo residual. Guarda artefactos, verifica recursos y propone cierre. Otro equipo debe encontrar una limitación y una pregunta de control.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar matriz de responsabilidad/acceso, linaje de una cifra y decisión de costo. Una lista de nombres de servicios no acredita gobernanza.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No puedes rastrear una cifra: falta versión o transformación registrada. Todas las personas tienen el mismo permiso: revisar acciones necesarias. Presupuesto desconocido: estimar recursos/hora y registrar supuestos, sin inventar una tarifa.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60 minutos: revisión cruzada del proyecto y amenaza de borrado accidental. Para el capstone, programar otra defensa si el número de equipos rebasa el tiempo disponible.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Permisos y recursos IAM](https://docs.cloud.google.com/iam/docs/overview).
- [Crédito y límites de GCP](https://docs.cloud.google.com/free/docs/free-cloud-features).
- [El contexto da significado a los datos](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
