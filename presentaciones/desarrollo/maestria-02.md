# Caso de apertura — una decisión con consecuencias

Caso hipotético: un tablero pregunta por viajes de un mes, pero consulta todo el histórico cada vez. El resultado tiene pocas filas y aun así cuesta más de lo esperado. ¿Por qué `LIMIT 10` no garantiza una lectura barata?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

La cantidad de filas devueltas y el trabajo de lectura son cosas distintas. Elegir columnas y filtrar la partición permite reducir datos leídos. El filtro debe corresponder a la columna de particionado; no basta que el SQL parezca selectivo.

En el laboratorio se mantienen las mismas filas y el mismo agregado: cambia la organización física, no la pregunta.

---

# Elegir bien exige reconocer el límite

Particionar ayuda cuando las consultas recortan por esa clave. Muchas particiones diminutas o filtros sobre otra columna pueden aportar poco. Clustering organiza bloques dentro de la tabla: complementa, pero no sustituye, una elección adecuada de partición.

La latencia depende también de caché y recursos: registra bytes y tiempo por separado.

---

# Laboratorio guiado — preparación y objetivo

Preparar en BigQuery dos tablas de la misma muestra: `lab.sin_particion` y `lab.por_fecha`, con columnas `fecha DATE`, `zona STRING`, `importe FLOAT64`; la segunda particionada por `fecha`. Revisar esquema y fechas disponibles. Usar límite de bytes facturados antes de ejecutar; el bloque guiado dura 90 minutos.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — formular una consulta justa

Elige un mes realmente presente. Predice si cambiará el conteo, los bytes o ambos. Haz dry run o revisa la estimación en el editor para las dos versiones. No ejecutes si rebasa el límite acordado.

---

# Laboratorio · paso 2 — comparar sin cambiar la pregunta

Ejecuta el SQL mostrado en ambas tablas cambiando solo el nombre. Guarda bytes procesados, bytes facturados y duración en detalles del job. Desactiva caché de resultados en la comparación de ejecución y anota esa condición.

---

# Laboratorio — ejecuta y comprueba

Reemplaza `MI_PROYECTO` y las fechas según tu muestra:
```sql
SELECT zona, COUNT(*) AS viajes, SUM(importe) AS total
FROM `MI_PROYECTO.lab.por_fecha`
WHERE fecha >= DATE '2025-01-01'
  AND fecha < DATE '2025-02-01'
GROUP BY zona;
```
Repite sobre `lab.sin_particion`; guarda la evidencia del job.

---

# Laboratorio · paso 3 — leer e interpretar

Comprueba que cada zona tiene el mismo conteo y suma en ambas tablas. Calcula un ranking por zona en una segunda CTE; una ventana opera sobre las filas producidas por la agregación, no elimina la necesidad de un filtro temprano.

---

# Laboratorio · paso 4 — comunicar la evidencia

Construye dos barras de bytes procesados con cero y unidades visibles. Titula con la conclusión observada. Si no hay ahorro, documenta el resultado y revisa la partición; no dibujes la mejora esperada como si hubiera ocurrido.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar SQL, igualdad de resultados y una comparación visual con configuración y fechas. La evidencia principal es el trabajo evitado para la misma pregunta, no una cifra de precio sin contexto.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No hay filas: consulta MIN/MAX de fecha sobre la muestra preparada. Los bytes no bajan: revisa el particionado y el filtro. Tiempo demasiado pequeño: comprueba si el job utilizó caché. No interpretes una tabla de resultados corta como prueba de lectura pequeña.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60–90 minutos: añadir clustering por zona y una consulta con ventana. Dejar CTEs recursivas como ejercicio separado: no son necesarias para demostrar partition pruning.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Optimizar cómputo en BigQuery](https://docs.cloud.google.com/bigquery/docs/best-practices-performance-compute).
- [Estimar y controlar consultas](https://docs.cloud.google.com/bigquery/docs/best-practices-costs).
- [Funciones de ventana SQL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/window-function-calls).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
