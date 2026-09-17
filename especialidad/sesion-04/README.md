# Sesión 04 — Introducción a Spark

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Qué problema resuelve Spark que SQL no resuelve
2. Vocabulario mínimo: DataFrame, transformación, acción
3. Sin entrar a shuffle/optimización — eso es contenido de Maestría

## Lab guiado
Notebook "fill-in-the-blanks": completar líneas específicas de un pipeline ya armado y observar el resultado.

## Entregable
Notebook completado.

## Ejemplo / material de apoyo
Versión simplificada de `recursos/spark/02_dataframes.ipynb`: quitar las celdas de `.explain()` y el guardado en Parquet particionado (eso es Maestría), dejar solo lectura + `filter` + `groupBy` + `show()` para que el grupo complete los argumentos de cada función sobre el catálogo de precios PROFECO.

## Recursos vinculados
- [`recursos/spark/02_dataframes.ipynb`](../../recursos/spark/02_dataframes.ipynb) — usar como base para la versión simplificada

## Slides
- **Deck nuevo:** [`slides.md`](slides.md) (Marp)

**Cómo presentar** (desde esta carpeta):
```bash
npx @marp-team/marp-cli slides.md -o slides.html   # exporta y abre slides.html en el navegador
```
Pantalla completa: F11 en el navegador. Flechas ←/→ para navegar entre slides.
Alternativa en PDF (modo presentación del lector): `npx @marp-team/marp-cli slides.md -o slides.pdf`.

Material de apoyo (pptx original):
- `slides/07_spark_explained.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
