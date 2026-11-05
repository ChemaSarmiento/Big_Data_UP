# Sesión 03 — SQL para analítica a escala

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. BigQuery desde la consola web
2. Cómo leer una consulta
3. Clustering y partitioning en BigQuery (particionar = analogía de archivero)
4. Cómo se ve el costo de una consulta

## Lab guiado
Comparar dos tablas con el mismo dato (`lab.sin_particion` vs. `lab.por_fecha`, cargadas de `bank_transactions.csv`) para comprobar en vivo que particionar reduce bytes leídos sin cambiar el resultado. Cierra con una exploración visual en Looker Studio.

## Entregable
Las consultas de comparación corridas en ambas tablas + confirmación de que el resultado es idéntico + una comparación visual de bytes facturados (dos barras) + el gráfico de Looker Studio de transacciones sospechosas por día.

## Ejemplo / material de apoyo
`bank_transactions.csv` (ver `recursos/datasets/README.md`, Sección 2 y 4 — es el dataset transversal del curso, también usado en el proyecto final si el equipo trabaja el caso banca/riesgo). **Prerequisito antes de clase:** el equipo técnico debe tener ya cargadas en BigQuery `lab.sin_particion` (la tabla completa, tal cual) y `lab.por_fecha` (los mismos datos, con `PARTITION BY DATE(timestamp)`) — el lab no funciona si estas dos tablas no existen de antemano. Para la visualización final: "Explorar con Looker Studio" desde los resultados de BigQuery, sin instalar nada ni escribir Python.

## Recursos vinculados
- [`recursos/datasets/README.md`](../../recursos/datasets/README.md) — `bank_transactions.csv`, esquema y por qué es el dataset transversal del curso

## Slides
- **Deck nuevo:** [`slides.md`](slides.md) (Marp)

**Cómo presentar** (desde esta carpeta):
```bash
npx @marp-team/marp-cli slides.md -o slides.html   # exporta y abre slides.html en el navegador
```
Pantalla completa: F11 en el navegador. Flechas ←/→ para navegar entre slides.
Alternativa en PDF (modo presentación del lector): `npx @marp-team/marp-cli slides.md -o slides.pdf`.

Material de apoyo (pptx original):
- `slides/05_sql_fasttrack.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
