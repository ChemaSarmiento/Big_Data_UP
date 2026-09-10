# Facilitación — Sesión 07: Data Lakes / Lakehouse I — formatos y medallion

> Guion de 3 horas: talking points + lab guiado. Primera de dos sesiones de
> lakehouse — hoy se prepara el cluster con Iceberg y se crea la primera tabla. La
> Sesión 8 hace las operaciones transaccionales sobre esta misma tabla.

## Antes de empezar (facilitador)

El cluster de hoy necesita propiedades especiales de Iceberg que **no se pueden
agregar después** — si vas a crear el cluster en vivo, revisa
`recursos/lakehouse-iceberg/README.md` con anticipación y ten el comando de
creación completo listo para copiar/pegar, no lo improvises frente al grupo.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Hasta ahora han guardado datos en carpetas de Parquet. Funciona, pero tiene
> un límite: no hay transacciones. Si alguien corrige una fila mientras otro
> lee la tabla, no hay garantía de qué versión ven. Hoy empezamos a resolver
> eso — con Iceberg, el mismo tipo de tecnología que usan Netflix y Apple
> internamente para sus lakes."

**Pregunta de apertura:**

> "¿Cómo corregirían un error en un archivo Parquet de 7GB que ya está
> guardado, sin reescribirlo completo?"

(Déjalos intentar responder — la respuesta corta es "no se puede, con Parquet
plano". Es el gancho hacia Iceberg.)

**Ejemplo de actualidad:**

> "Apache Iceberg nació en Netflix específicamente porque sus tablas Hive de
> Parquet se volvían inmanejables a escala de petabytes — hoy es un proyecto
> Apache usado por Apple, Airbnb, LinkedIn. No es una tecnología de nicho."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Parquet vs ORC vs Avro (10 min)

Tabla rápida en el pizarrón. Pregunta: **"¿por qué este curso eligió Parquet y
no Avro, si Avro tiene mejor evolución de esquema integrada?"** (respuesta: el
patrón de acceso del curso es "escribir en lote, leer analíticamente" —
columnar gana; Avro tendría sentido si escribiéramos evento por evento, que es
justo lo que pasa en la Sesión 9-10).

### Medallion (10 min)

Repaso rápido — ya lo vieron conceptualmente en `recursos/etl-tipo-cambio/`.
Conecta explícito: "hoy vamos a construir la misma idea, pero con una capa
silver que sí es transaccional".

### Por qué Parquet plano no es un lakehouse (25 min)

Este es el corazón teórico de la sesión — dale tiempo real. Recorre los tres
problemas de `teoria.md` uno por uno, y para cada uno pregunta: **"¿cómo
resolverían esto hoy, con lo que ya saben?"** antes de decir que Iceberg lo
resuelve. Que sientan el problema antes de ver la solución.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Crear el cluster con runtime de Iceberg (25 min)

```bash
gcloud dataproc clusters create curso-cluster \
    --region=us-central1 --num-workers=3 \
    --properties="^#^spark:spark.jars.packages=org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1#spark:spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions#spark:spark.sql.catalog.local=org.apache.iceberg.spark.SparkCatalog#spark:spark.sql.catalog.local.type=hadoop#spark:spark.sql.catalog.local.warehouse=gs://$BUCKET_NAME/curso-bigdata/lakehouse"
```

**Deberías ver:** el cluster `RUNNING` con las propiedades de Iceberg aplicadas
— confírmalo corriendo `spark.sql("SHOW CATALOGS").show()` apenas esté listo,
debe aparecer `local` en la lista.

**Si `local` no aparece:** las propiedades no se aplicaron correctamente —
revisar que el separador `^#^` esté exacto (cambia el delimitador de `,` a `#`
porque la lista de paquetes Maven ya usa comas).

### Paso 2 — Cargar bronze y crear la tabla silver (40 min)

```python
bronze = spark.read.csv(RUTA_BANK_TRANSACTIONS, header=True, inferSchema=True)
bronze = bronze.withColumn("is_suspicious", F.col("is_suspicious").cast("int"))
bronze = bronze.withColumn("hora_del_dia", F.hour("timestamp"))

spark.sql("CREATE NAMESPACE IF NOT EXISTS local.curso_bigdata")
(
    bronze.select("transaction_id", "timestamp", "amount", "currency", "hora_del_dia", "is_suspicious")
    .writeTo("local.curso_bigdata.transacciones_silver")
    .using("iceberg")
    .partitionedBy("currency")
    .createOrReplace()
)
```

**Deberías ver:** la escritura completa sin error. Correr
`spark.table("local.curso_bigdata.transacciones_silver").count()` debe devolver
el mismo número de filas que el CSV original.

### Paso 3 — Confirmar el snapshot inicial (25 min)

```sql
SELECT snapshot_id, committed_at, operation
FROM local.curso_bigdata.transacciones_silver.snapshots;
```

**Talking point:** "Esta consulta no existe en Parquet plano — es la primera
evidencia de que ya no están trabajando con archivos sueltos, sino con una
tabla real con historia."

Que cada quien capture este resultado — es su entregable de hoy.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**No apagues el cluster hoy** — la Sesión 8 retoma exactamente este cluster y
esta tabla. Si el `--max-age` no alcanza hasta la próxima sesión, documenten el
comando de creación exacto para recrearlo idéntico.

**Entregable de hoy:** tabla Iceberg creada y cargada + captura del primer
snapshot.

**Puente a la Sesión 8:**

> "Tienen una tabla Iceberg con un solo snapshot. La próxima sesión la vamos a
> modificar, viajar en el tiempo dentro de ella, y agregarle una columna — las
> tres cosas que Parquet plano no puede hacer."

---

## Notas de costo GCP

- El cluster de hoy necesita configuración especial — si el grupo va a
  retomarlo en la Sesión 8, decidan como grupo si vale la pena dejarlo
  corriendo entre sesiones (revisando el costo/hora) o documentar el comando
  de recreación exacto.
