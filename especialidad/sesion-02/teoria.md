# Teoría — Sesión 02: Cómo funciona por dentro (sin código pesado)

> Hoy no vas a escribir nada. El objetivo es que cuando alguien diga "lo corrimos en
> el cluster" o "eso está corriendo en paralelo", tengas una imagen mental correcta de
> qué está pasando — no una caja negra.

## 1. Almacenamiento y cómputo distribuido, con analogías

**Analogía del almacenamiento — una biblioteca gigante, sin un solo edificio:**
Imagina que en vez de un edificio con todos los libros, tienes 100 bodegas más
pequeñas repartidas por la ciudad, cada una con una parte de la colección — y además,
cada libro tiene 3 copias guardadas en bodegas distintas, por si una bodega se incendia.
Eso es exactamente lo que hace Cloud Storage (o HDFS, su antecesor) con tus datos: los
parte y los reparte, con copias de seguridad automáticas.

**Analogía del cómputo distribuido — un equipo dividiendo tareas:**
Si te piden contar cuántas veces aparece la palabra "fraude" en 10,000 documentos, hay
dos formas de hacerlo: (a) una persona lee los 10,000 documentos uno por uno, o (b) 10
personas leen 1,000 documentos cada una, en paralelo, y al final suman sus resultados
parciales. La opción (b) es "cómputo distribuido" — y es exactamente lo que hace un
cluster de Spark cuando procesa un archivo de 20GB.

## 2. Qué es un cluster

Un cluster es, literalmente, un grupo de computadoras conectadas que trabajan como si
fueran una sola, más grande. Dos roles que vas a escuchar mencionar:

- **Nodo maestro (master):** coordina el trabajo — decide qué parte del trabajo le
  toca a cada nodo trabajador, y junta los resultados al final.
- **Nodos trabajadores (workers):** hacen el trabajo pesado, cada uno sobre su
  porción de los datos.

Cuando alguien "crea un cluster" en GCP (lo que hace el facilitador con
`recursos/managed-spark-cluster/`), literalmente está encendiendo varias máquinas
virtuales que se configuran automáticamente para trabajar juntas con estos dos roles.

## 3. Qué significa "procesar en paralelo"

Con la analogía de los 10,000 documentos: paralelo no significa "más rápido por
arte de magia" — significa **dividir el trabajo entre varios trabajadores que
avanzan al mismo tiempo**. Dos cosas que vale la pena saber, aunque nunca vayas a
tocar el código:

- Dividir el trabajo entre más máquinas ayuda hasta cierto punto — si el trabajo es
  muy pequeño, coordinar a 100 máquinas toma más tiempo que el ahorro que dan. Por
  eso un cluster de Spark no tiene sentido para un archivo de 10MB (sería como
  contratar 10 personas para leer un solo párrafo).
- Si una parte del trabajo tarda mucho más que las demás (por ejemplo, un documento
  gigante entre 9,999 documentos pequeños), el trabajador que le tocó ese documento
  se vuelve el cuello de botella — todos los demás terminan y esperan a que uno solo
  acabe. Esto se llama **skew** (desbalance), y es un tema que Maestría profundiza en
  su Sesión 3 — aquí solo necesitas reconocer el concepto si lo escuchas mencionar.

## En vivo: la demo de esta sesión

El facilitador va a correr `recursos/spark/01_rdd_basico.ipynb` en un cluster real (o
mostrar la salida ya corrida) — un `reduceByKey` contando palabras sobre tweets reales.
Es la versión en código de la analogía de los 10,000 documentos: cada trabajador cuenta
su porción, y al final se suman los resultados parciales.

---

## Referencias

- [Google Cloud — ¿Qué es un cluster de Dataproc? (video corto, oficial)](https://cloud.google.com/dataproc/docs/concepts/overview)
- [Apache Spark — Cluster Mode Overview (para quien quiera ver la versión técnica)](https://spark.apache.org/docs/latest/cluster-overview.html)
