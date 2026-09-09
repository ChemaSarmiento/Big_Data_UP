# Teoría — Sesión 08: Data Lakes / Lakehouse II — transacciones y versionado

> Segunda de dos sesiones sobre lakehouse. La Sesión 7 dejó una tabla Iceberg lista;
> hoy se usan las tres operaciones que justifican que exista un formato de tabla
> transaccional en vez de solo Parquet bien organizado.

## 1. `MERGE INTO`: actualizar sin reescribir la tabla completa

En un data lake de Parquet plano, corregir un lote de filas ya cargado obliga a
reescribir el archivo o la partición completa — no hay forma de tocar solo las filas
afectadas. Un formato de tabla transaccional resuelve esto con `MERGE INTO`, la misma
sintaxis conceptual de un upsert en una base de datos relacional, pero operando sobre
archivos Parquet subyacentes:

```sql
MERGE INTO local.curso_bigdata.transacciones_silver t
USING correcciones c
ON t.transaction_id = c.transaction_id
WHEN MATCHED THEN UPDATE SET t.currency = c.currency
```

Internamente, Iceberg no reescribe todo el archivo — identifica qué archivos
contienen las filas afectadas, escribe *nuevos* archivos solo con esas filas
corregidas, y actualiza la metadata de la tabla para apuntar a la combinación correcta
de archivos viejos (sin tocar) y nuevos (con la corrección). Ese mecanismo de
metadata es justo lo que hace posible el punto 2.

## 2. Time travel: consultar un snapshot anterior

Cada escritura a una tabla Iceberg (incluyendo un `MERGE INTO`) crea un nuevo
**snapshot** — un punto en el tiempo con su propia versión completa y consistente de
la tabla, sin duplicar físicamente los datos que no cambiaron. Esto permite consultar
la tabla exactamente como estaba antes de una operación:

```sql
SELECT snapshot_id, committed_at, operation
FROM local.curso_bigdata.transacciones_silver.snapshots
ORDER BY committed_at;

SELECT * FROM local.curso_bigdata.transacciones_silver
VERSION AS OF <snapshot_id>;
```

**Por qué esto no es solo una curiosidad técnica:** es la base de auditoría real en
un contexto regulado (banca, salud) — "¿qué decía esta tabla el día que se tomó esta
decisión de negocio?" es una pregunta que Parquet plano no puede responder sin que
alguien haya guardado copias manualmente.

## 3. Evolución de esquema sin romper lectores existentes

```sql
ALTER TABLE local.curso_bigdata.transacciones_silver ADD COLUMN es_horario_nocturno BOOLEAN;
```

Con Parquet plano, agregar una columna nueva rompe cualquier proceso que ya lee la
tabla asumiendo el esquema anterior, o fuerza a versionar la carpeta entera. Iceberg
resuelve esto porque el esquema es parte de la metadata versionada de la tabla, no
algo inferido del archivo — un lector antiguo sigue funcionando (ve la tabla sin la
columna nueva en snapshots anteriores a la migración), y uno nuevo la ve sin fricción.

## 4. Versionado de datasets y de modelos

Versionar código (git) es familiar. Versionar **datos** y **modelos** es un problema
distinto:

- **Datasets** cambian de tamaño (GB, no KB) — no se puede versionar un dataset de
  20GB con la misma estrategia que un archivo de texto en git. Los snapshots de
  Iceberg resuelven esto de forma nativa: cada escritura crea una nueva versión
  referenciable sin duplicar físicamente los datos que no cambiaron.
- **Modelos** necesitan versionarse junto con el dataset y los hiperparámetros que los
  produjeron — sin eso, "¿con qué datos se entrenó este modelo?" se vuelve
  irrespondible seis meses después. `recursos/spark/04_pipeline_ml.ipynb` guarda el
  `PipelineModel` completo (no solo los pesos) precisamente para que sea reproducible
  de punta a punta — feature engineering incluido, no solo el algoritmo final.

---

## Referencias

- [Apache Iceberg — Table Spec (documentación oficial)](https://iceberg.apache.org/spec/)
- [Apache Iceberg — Spark Writes (MERGE INTO)](https://iceberg.apache.org/docs/latest/spark-writes/)
- [Apache Iceberg — Spark Queries (time travel)](https://iceberg.apache.org/docs/latest/spark-queries/#time-travel)
- [Delta Lake — documentación oficial (para contraste)](https://docs.delta.io/latest/index.html)
