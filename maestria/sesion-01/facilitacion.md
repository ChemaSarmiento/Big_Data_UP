# Facilitación — Sesión 01: Arquitecturas distribuidas

> Guion de 3 horas: talking points + lab guiado. Esta es la primera sesión técnica
> real del track — el tono que establezcas hoy (rigor + código real, sin miedo a
> las herramientas de diagnóstico) define cómo va a funcionar el resto del curso.

## Antes de empezar (facilitador)

Primera vez que el grupo crea un cluster — dedica tiempo extra a que cada quien
lo haga con éxito, no lo hagas tú por ellos. Ten a la mano `recursos/managed-spark-cluster/README.md` proyectado.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "En 2003, Google publicó un paper describiendo cómo maneja archivos que no
> caben en un solo disco. Ese paper — el Google File System — es literalmente el
> ancestro de lo que van a usar hoy en Cloud Storage. No es historia por
> curiosidad: entender por qué se diseñó así explica comportamientos que van a
> ver toda la maestría."

**Pregunta de apertura:**

> "Si tuvieran que guardar un archivo de 10TB y garantizar que sobrevive a que
> se dañe un disco duro, ¿cómo lo harían con lo que ya saben de bases de datos
> tradicionales?"

**Ejemplo de actualidad:**

> "Cada vez que Netflix recomienda algo, o que un banco corre un modelo de
> fraude sobre millones de transacciones, hay una arquitectura distribuida
> detrás resolviendo exactamente el problema que vamos a ver hoy: partir el
> trabajo entre muchas máquinas sin perder consistencia ni tolerancia a fallos."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### HDFS: bloques, replicación, NameNode/DataNode (15 min)

Dibuja el diagrama en vivo (o usa el slide) mientras narras: "un archivo de 10TB
se parte en bloques de 128MB, cada bloque se guarda 3 veces en máquinas
distintas". Pregunta: **"¿por qué 3 copias y no 2, o 5?"** — deja que
especulen (la respuesta real es un balance costo/riesgo: 3 réplicas da alta
disponibilidad sin triplicar el costo de más).

### CAP: por qué P no es opcional (15 min)

Este es el punto más denso de la sesión — dale tiempo. Escribe las tres letras
grandes y pregunta al grupo qué creen que significa cada una **antes** de
explicar. Luego la pregunta clave:

> "La red *siempre* se va a partir eventualmente — un cable se corta, un switch
> falla. Entonces la decisión real nunca es entre las tres — es entre C y A.
> BigQuery, que van a usar la próxima sesión, ¿creen que elige C o A?"

(Respuesta: CP — prefiere esperar a tener el dato completo y correcto antes de
responder.)

### MapReduce y por qué Spark lo reemplazó (15 min)

Talking point con el dato del paper:

> "El paper original de Spark, de 2012, reporta hasta 100x de mejora sobre
> MapReduce clásico en cargas iterativas. La razón no es magia — es que
> MapReduce escribe a disco entre cada etapa, y Spark mantiene los datos en
> memoria cuando puede. Hoy lo vamos a medir con nuestras propias manos, no solo
> a creerlo del paper."

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Crear el cluster (20 min)

```bash
export BUCKET_NAME=<tu-bucket>
gcloud dataproc clusters create curso-cluster \
    --region=us-central1 --num-workers=3 \
    --optional-components=JUPYTER,ZEPPELIN --enable-component-gateway \
    --max-idle=1h --max-age=3h
```

**Deberías ver:** el cluster pasa a estado `RUNNING` en 7-10 minutos. Mientras
esperan, adelanta la explicación del Paso 2 en modo lectura de código —no dejes
7 minutos de silencio.

**Si falla por cuota:** revisar `gcloud compute regions describe us-central1`
antes — es más común de lo que parece en cuentas nuevas.

### Paso 2 — Word count: MapReduce clásico vs. Spark (40 min)

Correr `recursos/spark/01_rdd_basico.ipynb` — primero la sección de RDDs
(equivalente a MapReduce), después la de `read.json()`.

```python
# Equivalente conceptual a MapReduce: map -> shuffle -> reduce, explícito
conteo = (
    sc.textFile("gs://<TU-BUCKET>/war_tweets.txt")
    .flatMap(lambda linea: linea.split())
    .map(lambda palabra: (palabra, 1))
    .reduceByKey(lambda a, b: a + b)
)
conteo.take(10)
```

**Talking point mientras corre:** "Fíjense en el Spark UI mientras esto corre —
la pestaña Stages les muestra exactamente las etapas de map y de shuffle que
acabamos de escribir en código. No es una caja negra."

**Deberías ver:** una lista de tuplas `(palabra, conteo)`. Si el archivo completo
(22GB) tarda demasiado para la demo en vivo, usar una muestra (`head -n 100000`)
subida aparte — acláralo antes de que el grupo piense que algo falló.

### Paso 3 — Leer los logs para diagnosticar (30 min)

Abrir el Spark UI (componente gateway del cluster) en vivo. Mostrar la pestaña
"Stages" y preguntar: **"¿cuál etapa tardó más, y por qué creen que fue esa?"**

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Recordatorio de apagado:**

```bash
gcloud dataproc clusters delete curso-cluster --region=us-central1
```

**Entregable de hoy:** benchmark propio (tiempos, uso de memoria) MapReduce vs
Spark — capturar del Spark UI antes de borrar el cluster.

**Puente a la Sesión 2:**

> "Hoy procesamos un archivo de texto plano. La próxima sesión hacemos lo
> mismo conceptualmente, pero sobre una tabla estructurada de 146 millones de
> filas, con SQL — y sin necesitar un cluster propio."

---

## Notas de costo GCP

- Primer cluster del curso — recuérdales explícitamente el `--max-idle=1h
  --max-age=3h` y por qué está ahí.
- Si alguien tiene problemas creando el cluster, no dejes que reintenten en
  silencio varias veces — cada intento fallido puede dejar recursos parciales
  cobrando.
