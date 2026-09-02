# Sesión 01 — Arquitecturas distribuidas

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. HDFS: NameNode/DataNode, replicación, bloques
2. Teorema CAP
3. Paradigma MapReduce (map / shuffle / reduce)
4. Por qué Spark reemplazó a MapReduce puro (in-memory computing, DAG scheduler)

## Lab
Crear un cluster de Managed Service for Apache Spark (Dataproc), correr un word count en MapReduce clásico y su equivalente en Spark, leer los logs de ejecución (YARN/Spark UI) para diagnosticar cuellos de botella.

## Entregable
Benchmark propio (tiempos, uso de memoria) MapReduce vs Spark.

## Ejemplo / material de apoyo
`recursos/spark/01_rdd_basico.py` — el mismo contraste MapReduce-vs-Spark del lab, ya escrito: agrupa transacciones por sucursal con `reduceByKey` y explica en comentarios qué pasaría en Hadoop MapReduce puro en cada paso.

## Recursos vinculados
- [`recursos/spark/01_rdd_basico.py`](../../recursos/spark/01_rdd_basico.py)
- [`recursos/managed-spark-cluster/`](../../recursos/managed-spark-cluster/) — comandos de creación de cluster

## Slides
- `slides/01_introduccion.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
