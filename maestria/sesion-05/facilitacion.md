# Facilitación — Sesión 05: Ingeniería de features a escala

> Guion de 3 horas: talking points + lab guiado paso a paso. Los bloques de tiempo
> son un punto de partida, no una camisa de fuerza — el grupo manda. Todo lo técnico
> ya vive en `recursos/spark/04_pipeline_ml.ipynb`; este documento es *cómo enseñarlo
> en vivo*, no una repetición de la teoría (ver `teoria.md` para eso).

## Antes de empezar (facilitador, 10 min antes de que llegue el grupo)

```bash
gcloud dataproc clusters list --region=us-central1
```

**Por qué esto primero:** para la Sesión 5, ya van 4 sesiones creando clusters (S1,
S3, S4). Es común que alguien del grupo se haya olvidado uno prendido desde la semana
pasada — revisa esto *tú*, no asumas que `--max-idle=1h` atrapó todos los casos.
Si encuentras uno huérfano, bórralo antes de que arranque la sesión.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura, dilo casi textual:**

> "La semana pasada optimizamos consultas y diagnosticamos shuffle. Hoy hacemos algo
> distinto: convertir una tabla de transacciones bancarias en algo que un algoritmo
> pueda entender. Esa conversión — de dato crudo a feature — es, según varias
> encuestas de la industria (Kaggle State of ML, Google), donde los equipos de ML
> pasan **60-80% de su tiempo**. No entrenando modelos. Preparando datos."

**Pregunta para abrir discusión (dales 2 min en parejas antes de pedir respuestas):**

> "¿Qué información usarían ustedes, como humanos, para sospechar que una
> transacción es fraude, sin ver el resultado de ningún modelo?"

Espera respuestas tipo "monto muy alto", "hora rara", "país distinto al usual". Úsalas
para aterrizar: **eso que acaban de describir es exactamente feature engineering** —
convertir intuición de dominio en una columna que el modelo puede consumir.

**Ejemplo de industria/actualidad (dilo después del ejercicio anterior):**

> "Stripe Radar y los sistemas de AML de la banca real no usan 'el monto' tal cual —
> usan **features de velocidad** (cuántas transacciones hizo este usuario en los
> últimos 10 minutos) y **features de red** (con cuántas cuentas distintas ha
> transaccionado). Nuestro pipeline de hoy es la versión de curso de exactamente
> ese tipo de ingeniería — más simple, mismo principio."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

Sigue `teoria.md` como guion de contenido. Aquí el *cómo* explicarlo:

### Pipeline / Transformer / Estimator (15 min)

**Analogía para dar antes de la definición formal:**

> "Piensen en una línea de ensamblaje de una fábrica. Cada estación hace una cosa:
> una pinta, otra atornilla, otra empaca. El `Pipeline` de Spark es esa línea de
> ensamblaje. Un `Transformer` es una estación que ya sabe qué hacer — no necesita
> aprender nada, solo ejecuta. Un `Estimator` es una estación que *primero* tiene que
> aprender viendo unas piezas de muestra (`.fit()`), y después queda configurada como
> Transformer para el resto de la línea."

Escribe en el pizarrón/slide (ya está en `slides_maestria/sesion-05.md`) el diagrama
de 6 etapas. Pregunta al grupo: **"¿cuáles de estas 6 etapas creen que son
Estimators, y cuáles Transformers puros?"** — respuesta: `StringIndexer`,
`StandardScaler` y el modelo (`LogisticRegression`) son Estimators porque aprenden
de los datos; `OneHotEncoder`* y `VectorAssembler` son Transformers puros.

<sub>*Nota técnica para ti, no para el grupo: `OneHotEncoder` en Spark ML es
técnicamente un Estimator porque necesita conocer el número de categorías — pero
conceptualmente se comporta como transformación fija una vez fit. No vale la pena
esta distinción en clase, genera confusión sin aportar.</sub>

### El error de fuga de información (10 min)

Este es el punto que más vale la pena que quede clavado. Escribe las dos líneas de
código lado a lado (ya están en el slide) y pregunta:

> "¿Cuál de estas dos líneas es la correcta, y por qué la otra es un error que un
> modelo en producción no perdona?"

Deja que discutan 3 minutos antes de resolver. **El objetivo no es que memoricen la
regla — es que la próxima vez que vean `.fit()` en cualquier contexto, se pregunten
"¿sobre qué datos exactamente?"**

### Encoding y escalado a escala (10 min)

Punto técnico que vale la pena mencionar en voz alta: `StringIndexer` necesita ver
*todas* las categorías antes de asignar índices — pregúntale al grupo:

> "Si `currency` tiene 200 monedas distintas repartidas en 7.5GB de datos, ¿cómo cree
> Spark que hay 200 categorías sin leer las 7.5GB completas?"

(Respuesta: sí, tiene que hacer un paso de agregación distribuida sobre todo el
dataset antes de poder indexar — es exactamente lo que van a ver correr en el lab.)

### Feature stores (10 min)

No hay lab de esto — es panorama. Cuéntalo como anécdota, no como definición:

> "Imaginen que en su empresa hay 5 equipos de ML distintos, y cada uno calcula
> 'antigüedad del cliente en días' con su propia lógica, ligeramente distinta. Un día,
> el modelo de fraude empieza a fallar en producción — y nadie sabe por qué, porque
> entrenó con una definición de la feature y en producción se está calculando otra.
> Eso se llama *training-serving skew*, y un feature store existe únicamente para que
> esto no pase — una sola definición, para todos."

---

## Bloque 3 — Break (1:00–1:10, 10 min)

**No lo saltes.** A la hora de una sesión de 3 horas con contenido denso, el grupo
necesita este corte — y tú necesitas revisar que todos tengan el cluster accesible
antes de empezar el lab.

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 0 — Verificación de entorno (5 min)

```bash
gcloud config get-value project
gcloud dataproc clusters describe curso-cluster --region=us-central1 --format="value(status.state)"
```

**Deberías ver:** `RUNNING`. Si dice `ERROR` o no existe, créalo ahora con
`recursos/managed-spark-cluster/README.md` (opción A) — no dejes que el grupo espere
7-10 min de creación de cluster en silencio; mientras arranca, adelanta el Paso 1
en modo lectura de código.

**Recordatorio de costo, dilo en voz alta:**

> "Este cluster cuesta mientras está prendido, no mientras procesa. Al terminar el
> lab de hoy, lo apagamos juntos — no lo dejen para 'después'."

### Paso 1 — Abrir el notebook y ubicar el dataset (10 min)

```python
RUTA = "gs://<TU-BUCKET>/raw/bank_transactions/bank_transactions.csv"
df = spark.read.csv(RUTA, header=True, inferSchema=True)
df.select("amount", "currency", "hora_del_dia", "is_suspicious").show(5)
```

**Deberías ver:** 5 filas, con `hora_del_dia` ya como entero (0-23) y `is_suspicious`
como 0/1.

**Si falla con `Path does not exist`:** el dataset no se subió a su bucket. Pausa aquí
y verifica con `gsutil ls gs://<TU-BUCKET>/raw/bank_transactions/` — es más rápido
resolverlo ahora que cuando ya vayan 3 celdas adelante.

**Pregunta de verificación de comprensión antes de seguir:**

> "¿Por qué `hora_del_dia` ya viene calculada en vez de venir en el CSV original?"

(Respuesta: se deriva con `F.hour("timestamp")` — es la primera feature *creada*, no
solo *leída*. Buen momento para que noten la diferencia.)

### Paso 2 — Construir el Pipeline, etapa por etapa (45 min)

**No pegues las 6 etapas de un jalón.** Constrúyelas una por una, corriendo
`.transform()` sobre cada Transformer individual antes de meterlo al Pipeline
completo — así el grupo *ve* qué hace cada pieza por separado.

```python
# 1. Imputer — corre esto solo, muestra el antes/después
imputer = Imputer(inputCols=["amount", "hora_del_dia"],
                   outputCols=["amount_imputado", "hora_del_dia_imputada"])
imputer.fit(df).transform(df).select(
    "amount", "amount_imputado"
).where("amount IS NULL").show(5)
```

**Deberías ver:** filas donde `amount` es null pero `amount_imputado` tiene un valor
(la media). Si el `WHERE` no devuelve filas, es porque este dataset no tiene nulos en
`amount` — menciónalo al grupo en vez de que se pregunten por qué la celda "no
muestra nada": no es un error, es que el dato ya llegó limpio en esa columna.

```python
# 2-3. Indexer + Encoder — mostrar el vector disperso resultante
indexer = StringIndexer(inputCol="currency", outputCol="currency_idx", handleInvalid="keep")
encoder = OneHotEncoder(inputCols=["currency_idx"], outputCols=["currency_ohe"])
```

Pregunta antes de correr: **"¿cuántas columnas nuevas creen que genera el
OneHotEncoder si hay 5 monedas distintas?"** — deja que alguien se equivoque diciendo
"5" y corrige con el resultado real (son vectores dispersos, no 5 columnas densas).

```python
# 4-5. Assembler + Scaler
assembler = VectorAssembler(
    inputCols=["amount_imputado", "hora_del_dia_imputada", "currency_ohe"],
    outputCol="features_raw")
scaler = StandardScaler(inputCol="features_raw", outputCol="features")

# 6. Armar el Pipeline completo — AHORA sí, todo junto
pipeline = Pipeline(stages=[imputer, indexer, encoder, assembler, scaler])
modelo_features = pipeline.fit(df)
df_features = modelo_features.transform(df)
df_features.select("features").show(5, truncate=False)
```

**Deberías ver:** una columna `features` con vectores densos/dispersos de Spark ML
(formato `(n,[índices],[valores])`). Es normal que el grupo se confunda con este
formato la primera vez — explícalo en el pizarrón antes de seguir, no lo dejes pasar
como "ya lo van a entender".

### Paso 3 — Guardar el pipeline (10 min)

```python
modelo_features.write().overwrite().save("gs://<TU-BUCKET>/modelos/features_bank_transactions")
```

**Talking point de cierre técnico:**

> "Esto que acaban de guardar no es un archivo de configuración — es el pipeline
> *completo, ya entrenado*. La Sesión 6 lo va a cargar tal cual para entrenar el
> modelo encima. La Sesión 10 lo va a volver a cargar para aplicarlo a datos que
> llegan en tiempo real. Es el mismo objeto las tres veces — no lo van a reescribir."

### Paso 4 — Verificación de reproducibilidad (15 min)

Ejercicio guiado adicional, no está en el notebook base — agrégalo tú en vivo:

```python
# Cargar el pipeline guardado y aplicarlo a una muestra nueva
from pyspark.ml import PipelineModel
modelo_cargado = PipelineModel.load("gs://<TU-BUCKET>/modelos/features_bank_transactions")
muestra_nueva = df.sample(0.001, seed=99)
resultado = modelo_cargado.transform(muestra_nueva)
resultado.select("features").show(3, truncate=False)
```

**Por qué este paso importa más de lo que parece:** demuestra en vivo que el
Pipeline guardado es reusable sobre datos que nunca vio en el `.fit()` original —
la propiedad central que hace posible la Sesión 10 (streaming). Si tienen tiempo
corto, este es el paso que se puede comprimir a demo del facilitador en vez de
que todos lo corran.

### Errores comunes de este lab

| Error | Causa típica | Solución |
|---|---|---|
| `Path does not exist` | Bucket mal escrito o dataset no subido | `gsutil ls` para verificar |
| Job se queda "colgado" en el Assembler | Cluster con muy pocos workers para 7.5GB | Verificar `--num-workers=3` en la creación del cluster |
| `Column 'hora_del_dia' does not exist` | Se saltaron la celda de `F.hour("timestamp")` | Revisar que corrieron las celdas en orden |

---

## Bloque 5 — Cierre y entregable (2:40–3:00, 20 min)

**Recordatorio de apagado, en voz alta y verificado en pantalla:**

```bash
gcloud dataproc clusters delete curso-cluster --region=us-central1
```

**Entregable de hoy:** pipeline de features serializado y reproducible — ya lo
tienen en `gs://<TU-BUCKET>/modelos/features_bank_transactions`. No hay entrega
adicional de código, el archivo guardado *es* el entregable.

**Pregunta de cierre para abrir la Sesión 6:**

> "La próxima sesión vamos a entrenar 2-3 modelos sobre este mismo pipeline. ¿Alguien
> ya tiene una hipótesis de qué feature va a pesar más para detectar fraude?"

(No la respondas hoy — es el gancho de apertura de la Sesión 6.)

---

## Notas de costo GCP (resumen para el facilitador)

- Cluster estándar (`e2-highmem-2` + 3×`e2-standard-2`, ~1.5h de uso hoy): dentro del
  presupuesto normal de una sesión, pero es la 4ª vez que se crea uno en el curso —
  vale la pena recordar al grupo cuánto llevan consumido del crédito de $300 hasta
  ahora (`Billing → Reports` en la consola).
- Si el grupo es grande y cada quien crea su propio cluster en vez de compartir uno,
  el costo se multiplica — considera clusters compartidos por equipo de 3-4 personas
  para esta sesión en particular.
