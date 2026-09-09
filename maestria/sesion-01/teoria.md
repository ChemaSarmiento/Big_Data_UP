# Teoría — Sesión 01: Arquitecturas distribuidas

> Esta sesión es la base conceptual de todo lo que sigue: si HDFS, CAP y MapReduce no
> quedan sólidos aquí, Spark (Sesión 3 en adelante) se va a sentir como "aprender la
> sintaxis de una API" en vez de entender qué problema resuelve por debajo.

## 1. HDFS: NameNode, DataNode, replicación, bloques

HDFS (Hadoop Distributed File System) resuelve un problema físico: un archivo de 10TB
no cabe en el disco de una sola máquina, y aunque cupiera, leerlo secuencialmente
tomaría horas. La solución es partir el archivo en pedazos y repartirlos.

- **Bloques:** un archivo se corta en bloques de tamaño fijo (típicamente 128MB en
  Hadoop clásico). Cada bloque se guarda como un archivo independiente en el sistema
  de archivos local de alguna máquina del cluster.
- **DataNode:** la máquina que efectivamente guarda los bloques en su disco local.
  Un cluster tiene muchos DataNodes.
- **NameNode:** el "índice" — no guarda datos, guarda *metadata*: qué archivo se
  compone de qué bloques, y en qué DataNodes vive cada bloque. Es el punto único que
  hay que consultar antes de leer o escribir cualquier archivo.
- **Replicación:** cada bloque se guarda, por default, 3 veces en DataNodes distintos.
  No es redundancia por paranoia — es la estrategia de tolerancia a fallos: los discos
  duros fallan constantemente a esta escala (miles de discos = fallas casi diarias
  estadísticamente), y perder un DataNode no debe perder datos.

**Por qué importa hoy:** Cloud Storage (lo que usa este curso en vez de HDFS on-prem)
resuelve el mismo problema con el mismo principio — partición + replicación — pero
como servicio administrado. Entender HDFS es entender *por qué* Cloud Storage está
diseñado como está, no una pieza de museo.

## 2. Teorema CAP

Formulado por Eric Brewer (2000), dice que un sistema distribuido de datos solo puede
garantizar **dos de tres** propiedades al mismo tiempo, nunca las tres:

- **C**onsistencia — todos los nodos ven el mismo dato al mismo tiempo.
- **A**vailability (disponibilidad) — el sistema siempre responde, aunque algún nodo
  haya fallado.
- **P**artition tolerance (tolerancia a particiones) — el sistema sigue funcionando
  aunque la red entre nodos se corte.

En la práctica, **P no es opcional** — en cualquier sistema distribuido real, la red
eventualmente se va a particionar (falla un switch, se cae un data center). Entonces
la decisión real es entre **C y A**: si la red se parte, ¿el sistema prefiere seguir
respondiendo con datos posiblemente desactualizados (AP), o prefiere dejar de responder
hasta poder garantizar consistencia (CP)?

| Sistema | Elección típica | Por qué |
|---|---|---|
| BigQuery (consultas analíticas) | CP | Prefieres esperar a que la consulta esté completa y correcta |
| Sistemas de caché/sesión (ej. Cassandra en modo default) | AP | Prefieres una respuesta rápida aunque esté un poco desactualizada |

## 3. MapReduce: map, shuffle, reduce

El paradigma que popularizó Google (paper original: Dean & Ghemawat, 2004) para
procesar datos distribuidos sin que el programador tenga que pensar en paralelización
manual:

1. **Map:** cada máquina procesa su porción de datos de forma independiente, emitiendo
   pares `(clave, valor)`. Ejemplo, contar palabras: cada máquina lee su pedazo de texto
   y emite `(palabra, 1)` por cada palabra que encuentra.
2. **Shuffle:** el framework redistribuye esos pares entre las máquinas, de forma que
   *todos* los pares con la misma clave terminen en la misma máquina. Esta es la etapa
   más cara — implica mover datos por la red entre máquinas.
3. **Reduce:** cada máquina agrega los valores que le tocaron por clave. Siguiendo el
   ejemplo: suma todos los `1`s de cada palabra para obtener el conteo total.

`recursos/spark/01_rdd_basico.ipynb` implementa exactamente esto con `reduceByKey`
sobre `war_tweets.txt` — correrlo y leer el plan de ejecución es la mejor forma de
internalizar estas tres etapas antes de abstraerlas con Spark.

## 4. Por qué Spark reemplazó a MapReduce puro

Dos limitaciones concretas de MapReduce clásico que Spark resuelve:

- **Todo pasa por disco.** Cada etapa de MapReduce lee y escribe a HDFS — incluso
  jobs encadenados (el resultado de un MapReduce alimenta al siguiente) pagan ese
  costo de I/O a disco en cada paso. Spark mantiene los datos intermedios **en
  memoria** (RDDs — Resilient Distributed Datasets) cuando es posible, evitando esa
  escritura/lectura repetida — el paper original de Spark (Zaharia et al., NSDI 2012)
  reporta hasta 100x de mejora en cargas de trabajo iterativas (como entrenar un
  modelo, que relee el mismo dataset muchas veces).
- **Un DAG, no un job por paso.** MapReduce obliga a expresar todo como una secuencia
  rígida de map→reduce. Spark construye un **DAG (grafo acíclico dirigido)** de
  transformaciones y decide el plan de ejecución óptimo completo antes de correr nada
  — puede fusionar pasos, evitar shuffles innecesarios, y paralelizar lo que sea
  paralelizable sin que el programador lo orqueste a mano.

El lab de esta sesión (crear un cluster, correr un word count en MapReduce clásico y
su equivalente en Spark, comparar tiempos) hace tangible esta diferencia en vez de
solo describirla.

---

## Referencias

- [Ghemawat, Gobioff, Leung — The Google File System (2003)](https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf) — el paper detrás del diseño de HDFS
- [Dean, Ghemawat — MapReduce: Simplified Data Processing on Large Clusters (2004)](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf)
- [Brewer — Towards Robust Distributed Systems (CAP, 2000)](https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf)
- [Zaharia et al. — Resilient Distributed Datasets (Spark, NSDI 2012)](https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf)
- [Apache Spark — Cluster Mode Overview (docs oficiales)](https://spark.apache.org/docs/latest/cluster-overview.html)
