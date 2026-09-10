# Sesión 00 — Nivelación

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Linux esencial: qué es una terminal, navegación básica (analogía a un explorador de archivos)
2. Python esencial: qué es una variable, un notebook, cómo correr una celda
3. SQL esencial: SELECT / WHERE / GROUP BY — lo suficiente para leer una consulta
4. Acceso a la consola web de GCP (sin instalar nada localmente) — pasos 1-3 de [`environment/gcp-setup.md`](../../environment/gcp-setup.md) (cuenta, proyecto, alerta de presupuesto); no hace falta instalar `gcloud` en este track, todo se hace desde la consola web.

## Actividad
Autoevaluación informal (no se filtra acceso, es puramente introductoria) — el objetivo es que nadie llegue en blanco a la Sesión 1.

## Entregable
Ninguno formal.

## Ejemplo / material de apoyo
`recursos/sql-practica/employee_db_queries.sql` — las primeras 3-4 consultas (exploración básica, sin joins todavía) son un buen punto de entrada: se leen y se corren, no hace falta escribirlas desde cero.

## Mirando hacia el proyecto final
No hay que decidirlo hoy, pero conviene tenerlo en mente desde la primera sesión: el proyecto final pide una pregunta de negocio específica respondida con datos reales (≥15GB, procesamiento y visualizaciones). [`recursos/datasets/README.md`](../../recursos/datasets/README.md), Sección 5, sugiere una asignación de dataset por sector (retail, banca/riesgo, ciberseguridad) — es un buen punto de partida para ir pensando en qué pregunta de tu propia industria te gustaría contestar para la Sesión 9.

## Recursos vinculados
- [`recursos/sql-practica/`](../../recursos/sql-practica/) — SQL de nivelación
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — creación de cuenta/proyecto GCP
- [`recursos/datasets/README.md`](../../recursos/datasets/README.md) — catálogo de datasets reales, Sección 5 (asignación por perfil)

## Slides
- **Deck nuevo:** [`slides.md`](slides.md) (Marp) — `npx @marp-team/marp-cli slides.md -o out.pdf`
- `slides/04_python_fasttrack.pptx`
- `slides/05_sql_fasttrack.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
