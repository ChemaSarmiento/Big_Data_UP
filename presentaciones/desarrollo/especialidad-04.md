# Caso de apertura — una decisión con consecuencias

Caso hipotético: un equipo compara precios de un producto entre estados y recomienda cambiar compras. Después descubre que mezcló presentaciones y tuvo pocos registros en un estado. ¿El promedio respondió la pregunta correcta?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Un DataFrame organiza filas y columnas; filtro y agregado definen una pregunta. La transformación construye un plan y la acción obtiene resultados. Antes de ejecutar, necesitas entender qué representa cada fila y qué unidades son comparables.

---

# Elegir bien exige reconocer el límite

Un promedio no elimina sesgo de cobertura. Comparar productos o presentaciones distintas confunde la conclusión. Conteos, nulos y fechas ayudan a evaluar si cada grupo tiene evidencia suficiente.

---

# Laboratorio guiado — preparación y objetivo

Abrir `recursos/especialidad/04_spark_guiado.ipynb`. Muestra CSV preparada con producto, precio y estado, notebook conectado a Spark. Solo se completan cuatro argumentos; instalar o crear cluster no pertenece al núcleo de 90 minutos.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — explorar y elegir

Ejecuta la celda de carga y mira cinco filas. Selecciona un producto y estado presentes. Anota unidad/presentación y cobertura de la muestra.

---

# Laboratorio · paso 2 — filtrar con intención

Completa PRODUCTO y ESTADO. Predice cuántas filas esperas y comprueba la salida. Si hay cero, investiga valores y espacios antes de cambiar la pregunta.

---

# Laboratorio · paso 3 — comparar grupos

Completa GRUPO con estado y MEDIDA con precio. Ordena promedios y lee observaciones junto a cada valor. Identifica un grupo con evidencia escasa.

---

# Laboratorio · paso 4 — comunicar con límites

Construye una gráfica de estados comparables. Pon título con conclusión observada, unidad y periodo. Añade una limitación y qué dato pedirías antes de actuar.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar notebook, gráfico y conclusión. Debe existir una relación explícita entre pregunta, filtro, agrupación y recomendación. No interpretar una muestra preparada como todo el mercado.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Precio nulo tras cast: revisar formato decimal o dato inválido. Valores mezclados: filtrar misma presentación. Gráfico espectacular con pocas filas: mostrar conteos y limitar alcance.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 45 minutos: repetir sobre otra muestra comparable y explicar qué cambió. La ejecución sobre fuente real completa del proyecto necesita presupuesto y apoyo técnico.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [RDD y ejecución distribuida](https://archive.apache.org/dist/spark/docs/3.5.3/rdd-programming-guide.html).
- [El contexto da significado a los datos](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
