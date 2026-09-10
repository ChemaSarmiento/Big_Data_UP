# Facilitación — Sesión 08: Data Lakes / Lakehouse II — transacciones y versionado

> Guion de 3 horas: talking points + lab guiado. Retoma la tabla Iceberg de la
> Sesión 7 — hoy se usan las tres operaciones que justifican que exista un formato
> de tabla transaccional.

## Antes de empezar (facilitador)

Confirma que el cluster/tabla de la Sesión 7 sigue disponible. Si se recreó el
cluster, correr primero la primera mitad de `06_lakehouse_iceberg.py` (Paso 1-2
de la Sesión 7) antes de que llegue el grupo, para no perder tiempo de clase
repitiendo el setup.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "La sesión pasada dejamos una tabla Iceberg con un solo snapshot. Hoy la
> vamos a corregir sin reescribirla, consultarla como estaba antes de la
> corrección, y agregarle una columna sin romper nada — las tres cosas que la
> semana pasada dijimos que Parquet plano no puede hacer."

**Pregunta de apertura:**

> "En un banco real, ¿qué pasaría si un error en los datos de fraude de ayer se
> descubre hoy? ¿Cómo lo corregirían sin perder el registro de qué decía la
> tabla cuando se tomaron decisiones basadas en el dato con error?"

**Ejemplo de actualidad:**

> "Esto no es hipotético — es exactamente el tipo de requisito que un auditor
> financiero exige: poder reconstruir qué decían los datos en un momento
> específico del pasado, sin importar qué correcciones se aplicaron después."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### MERGE INTO a fondo (15 min)

Escribe la sintaxis en el pizarrón y pregunta: **"¿qué creen que hace Iceberg
internamente cuando corre esto — reescribe todo el archivo, o algo más
inteligente?"** (respuesta: identifica los archivos afectados, escribe SOLO
archivos nuevos con las filas corregidas, actualiza la metadata).

### Time travel (15 min)

Demo conceptual antes del lab: dibuja una línea de tiempo con 2-3 snapshots y
pregunta qué pasaría si consultan cada uno. Conecta con la pregunta de
apertura sobre auditoría.

### Evolución de esquema (10 min)

Punto rápido con la analogía: "un lector viejo sigue funcionando viendo la
tabla sin la columna nueva; uno nuevo la ve sin fricción — porque el esquema es
parte de la metadata versionada, no algo que se infiere del archivo".

### Versionado de datasets y modelos (5 min)

Conecta con el `PipelineModel` de la Sesión 5/6 — mismo principio de
versionado, aplicado a un objeto distinto.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — MERGE INTO (30 min)

```python
correcciones = (
    spark.table("local.curso_bigdata.transacciones_silver")
    .filter(F.col("currency") == "USD").limit(1000)
    .withColumn("currency", F.lit("MXN"))
)
correcciones.createOrReplaceTempView("correcciones")
```

```sql
MERGE INTO local.curso_bigdata.transacciones_silver t
USING correcciones c
ON t.transaction_id = c.transaction_id
WHEN MATCHED THEN UPDATE SET t.currency = c.currency
```

**Deberías ver:** el `MERGE` corre sin error. Confirmar contando filas con
`currency = 'USD'` antes y después — debe haber 1000 menos.

### Paso 2 — Time travel (30 min)

```sql
SELECT snapshot_id, committed_at, operation
FROM local.curso_bigdata.transacciones_silver.snapshots
ORDER BY committed_at;
```

```python
primer_snapshot_id = snapshots.first()["snapshot_id"]
antes_del_merge = spark.read.format("iceberg").option("snapshot-id", primer_snapshot_id).load("local.curso_bigdata.transacciones_silver")
```

**Deberías ver:** al filtrar por `currency = 'USD'` sobre `antes_del_merge`,
las 1000 filas siguen ahí — la tabla "recordó" cómo estaba antes del `MERGE`.

**Pregunta de verificación:** "¿por qué esto no duplicó los datos, si ahora
tenemos dos versiones consultables de la tabla?" (los archivos que no cambiaron
se reusan entre snapshots — solo se escribieron archivos nuevos para las 1000
filas corregidas).

### Paso 3 — Evolución de esquema + capa gold (30 min)

```sql
ALTER TABLE local.curso_bigdata.transacciones_silver ADD COLUMN es_horario_nocturno BOOLEAN;
```
```sql
UPDATE local.curso_bigdata.transacciones_silver
SET es_horario_nocturno = (hora_del_dia < 6 OR hora_del_dia > 22);
```

```python
gold = (
    spark.table("local.curso_bigdata.transacciones_silver")
    .groupBy("currency", "es_horario_nocturno")
    .agg(F.count("*").alias("num_transacciones"), F.avg("amount").alias("monto_promedio"))
)
gold.writeTo("local.curso_bigdata.transacciones_gold").using("iceberg").createOrReplace()
```

**Deberías ver:** la tabla gold agregada, lista para un dashboard.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Ahora sí, apagar el cluster** (Iceberg y todo):

```bash
gcloud dataproc clusters delete curso-cluster --region=us-central1
```

**Entregable de hoy:** diagrama de arquitectura + pipeline versionado +
evidencia de las tres operaciones (capturas del MERGE, snapshots antes/después,
ALTER TABLE).

**Puente a la Sesión 9:**

> "Todo lo que hicimos hasta ahora fue sobre datos que ya estaban completos,
> esperando en un archivo. La próxima sesión cambia el juego: datos que llegan
> continuamente, sin fin. Es un tipo de sesión distinto — más de setup de
> infraestructura que de código puro."

---

## Notas de costo GCP

- Dos sesiones seguidas (7 y 8) usando el mismo cluster con Iceberg — asegúrate
  de que se apague hoy, no lo dejen "por si acaso" para una sesión futura que ya
  no lo necesita.
