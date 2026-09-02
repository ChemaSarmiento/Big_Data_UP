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
`recursos/spark/01_rdd_basico.py` — correrlo en vivo (`spark-submit --master local[*] 01_rdd_basico.py`) y comentar cada paso en voz alta: el grupo ve un `reduceByKey` agrupar transacciones por sucursal sin que nadie tenga que escribir código.

## Recursos vinculados
- [`recursos/spark/01_rdd_basico.py`](../../recursos/spark/01_rdd_basico.py) — para que el facilitador lo corra en vivo

## Slides
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
