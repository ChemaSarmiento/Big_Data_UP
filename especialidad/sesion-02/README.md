# Sesión 02 — Cómo funciona por dentro (sin código pesado)

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Almacenamiento y cómputo distribuido, explicado con analogías (biblioteca, equipo dividiendo tareas)
2. Qué es un cluster
3. Qué significa "procesar en paralelo"

## Actividad
Demo en vivo: el facilitador corre un job distribuido y el grupo interactúa (cambia parámetros simples, observa el efecto en tiempo/recursos).

## Entregable
Ninguno formal; quiz corto de conceptos.

## Ejemplo / material de apoyo
`recursos/spark/01_rdd_basico.ipynb` — correrlo en el cluster (o mostrar la salida ya corrida) es exactamente el nivel de este track: el grupo ve un `reduceByKey` contar palabras sobre tweets reales sin que nadie tenga que escribir código. Si el cluster real es demasiado para una demo en vivo, usar una muestra pequeña del archivo (`head -n 1000 war_tweets.txt`) para que corra en segundos.

## Recursos vinculados
- [`recursos/spark/01_rdd_basico.ipynb`](../../recursos/spark/01_rdd_basico.ipynb) — para que el facilitador lo corra en vivo

## Slides
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
