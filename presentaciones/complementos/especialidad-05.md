# Un pipeline necesita un contrato entre etapas

| Etapa | Pregunta de control | Evidencia |
|---|---|---|
| Extracción | ¿Llegó la fuente esperada? | Fecha de extracción y cantidad de registros |
| Transformación | ¿Se conservaron las reglas del negocio? | Nulos, duplicados y filas rechazadas |
| Carga | ¿El consumidor recibió el resultado correcto? | Conteo de salida y consulta de verificación |

**Discusión:** si el proceso corre dos veces con la misma entrada, ¿duplica las ventas del dashboard? Define la regla antes de programar el pipeline.


---

# Un ETL se acepta con evidencia en cada etapa

<figure data-infographic="etl-controles"></figure>

¿Qué control detectaría una extracción incompleta o una carga duplicada?

---

# La pregunta determina el gráfico

| Pregunta | Visual recomendado | Control de lectura |
|---|---|---|
| ¿Cuál es mayor? | Barras ordenadas | Origen cero y etiquetas directas |
| ¿Cómo cambia? | Línea temporal | Intervalos, unidades y cobertura |
| ¿Cómo se distribuye? | Histograma | Buckets y muestra explícitos |
| ¿Qué se relaciona? | Dispersión | No confundir relación con causalidad |

**Ejercicio:** toma un resultado del lab. Escribe primero la conclusión; después elige el gráfico que la demuestra.

---

# Destacar una conclusión reduce el esfuerzo de lectura

- Un título con hallazgo: «La partición redujo los bytes leídos»; agregar la magnitud solo cuando exista medición.
- Contexto neutral y un acento para lo relevante; el color comunica una razón.
- Etiquetas junto al dato, unidades y una nota con fuente/condiciones.
- Eliminar bordes, leyendas redundantes y decimales que no ayudan a decidir.

**Evitar:** gráficos 3D, escalas engañosas y flechas que afirmen causalidad sin evidencia. La elección no depende de una prohibición universal de un tipo de gráfico.


---

# Un producto de datos también puede ser un dashboard

El valor no exige un modelo de ML. Un dataset validado, un indicador o un dashboard pueden ser productos de datos si tienen consumidor, responsabilidad y una decisión definida.

**Ejemplo del curso:** fuente PROFECO → precios comparables → gráfico con una conclusión → decisión de compra.

La ruta de Maestría agrega un modelo cuando la pregunta lo justifica; la de Especialidad puede cerrar el ciclo con analítica guiada.
