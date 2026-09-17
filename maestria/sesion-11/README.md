# Sesión 11 — Model serving y monitoreo

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Patrones de serving (batch, online, streaming)
2. Monitoreo de drift de datos y de modelo

## Lab
Desplegar el modelo de la Sesión 6 como endpoint (`recursos/serving/serve_fraude.py`, FastAPI) y correr `monitor_drift.py` (Population Stability Index) sobre los scores que produce el streaming de la Sesión 10.

## Entregable
Endpoint de modelo respondiendo a `POST /score` + una corrida de `monitor_drift.py` con su PSI interpretado.

## Ejemplo / material de apoyo
`recursos/serving/serve_fraude.py` — endpoint FastAPI que carga el `PipelineModel` de la Sesión 5/6 en una SparkSession local. `recursos/serving/monitor_drift.py` — PSI sobre `amount`, comparando el set de entrenamiento contra un lote reciente de producción.

## Recursos vinculados
- [`recursos/serving/`](../../recursos/serving/) — endpoint de modelo + monitoreo de drift (PSI)
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — el modelo que este endpoint sirve

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-11.md`](../../slides_maestria/sesion-11.md) (Slidev)

**Cómo presentar** (desde `slides_maestria/`, `npm install` una sola vez):
```bash
npx slidev sesion-11.md --open
```
Abre un servidor local en modo presentación. Flechas/espacio para avanzar (incluye los `v-click`), `f` pantalla completa, `o` vista de overview. Atajos completos y export a PDF/PPTX: [`slides_maestria/README.md`](../../slides_maestria/README.md).
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
