# Caso de apertura — una decisión con consecuencias

Caso hipotético: un lote histórico de transacciones tiene moneda equivocada. El reporte publicado debe corregirse y, además, debe poder reconstruirse exactamente el dato utilizado en la decisión anterior.

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Parquet organiza archivos; Iceberg añade metadatos de tabla y snapshots para gestionar versiones. Un snapshot identifica un estado de la tabla. Medallion describe responsabilidades de las capas, no garantiza calidad automáticamente. Bronze conserva origen, silver aplica contrato y gold responde una pregunta.

---

# Elegir bien exige reconocer el límite

Corregir filas puede reescribir archivos afectados; no equivale a editar bytes de una fila en sitio. Conservar snapshots consume espacio. El time travel depende de que los archivos referenciados sigan disponibles; borrar objetos a mano puede romper la historia.

---

# Laboratorio guiado — preparación y objetivo

Preparar runtime Iceberg compatible, warehouse GCS y muestra bancaria. S7 crea namespace/tabla y guarda snapshot; S8 reutiliza esa tabla, sin recrearla. Usar `06_lakehouse_iceberg.py` por bloques en notebook, no ejecutarlo completo en S8 porque `createOrReplace` reinicia la demostración.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — recuperar la tabla existente

Carga la tabla creada en S7 y confirma snapshot inicial. Verifica una clave única por transacción y un conjunto de correcciones con una fila por clave.

---

# Laboratorio · paso 2 — aplicar una corrección controlada

Crea una vista de correcciones con una muestra y aplica el MERGE del script. Guarda conteo de claves corregidas y snapshot posterior. Debe conservarse el número total de transacciones.

---

# Laboratorio — ejecuta y comprueba

Con el catálogo `local` configurado:
```sql
SELECT snapshot_id, committed_at, operation
FROM local.curso_bigdata.transacciones_silver.snapshots
ORDER BY committed_at;
SELECT currency, COUNT(*) AS n
FROM local.curso_bigdata.transacciones_silver
GROUP BY currency;
```
Guarda el ID anterior a la corrección; no uses un ID inventado.

---

# Laboratorio · paso 3 — reconstruir el antes

Consulta el snapshot guardado antes del cambio y la tabla actual. Compara únicamente las claves corregidas, no solo el promedio global. Atribuye la diferencia a la corrección explícita.

---

# Laboratorio · paso 4 — evolucionar sin borrar historia

Añade una columna mediante ALTER TABLE y prueba lectura de filas previas. Crea gold por moneda y horario, documentando unidades. Propón retención de snapshots acorde al caso.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar tabla, snapshot identificado y evidencia de conteos. El antes y después deben tener el mismo total y cambios solo en las claves autorizadas.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

Catálogo no aparece: verificar runtime, extensión y warehouse. MERGE ambiguo: hay varias correcciones para una clave. Snapshot ausente: revisa si recreaste la tabla o expiraste su historia. Nunca borres archivos del warehouse como limpieza parcial.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 60–90 minutos: diseñar particionado según patrones de consulta y revisar crecimiento de archivos/snapshots. El núcleo usa una muestra; la carga completa a escala se ejecuta con presupuesto fuera del bloque.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Laboratorio — corregir y comprobar el snapshot

Con la tabla existente y `correcciones` con ID único:

```sql
MERGE INTO local.curso_bigdata.transacciones_silver t
USING correcciones c ON t.transaction_id = c.transaction_id
WHEN MATCHED THEN UPDATE SET t.currency = c.currency;
```

Para reconstruir el estado previo en el notebook:

```python
antes = (spark.read.format("iceberg")
         .option("snapshot-id", SNAPSHOT_ANTES)
         .load("local.curso_bigdata.transacciones_silver"))
```

`SNAPSHOT_ANTES` es el ID registrado antes del MERGE. Comparar conteos y monedas de las claves corregidas; no recrear la tabla en este paso.

---

# Referencias — qué buscar en cada fuente

- [Lectura y escritura Parquet](https://archive.apache.org/dist/spark/docs/3.5.3/sql-data-sources-parquet.html).
- [Snapshots y consultas Iceberg](https://iceberg.apache.org/docs/1.6.1/spark-queries/).
- [Escrituras y MERGE Iceberg](https://iceberg.apache.org/docs/1.6.1/spark-writes/).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
