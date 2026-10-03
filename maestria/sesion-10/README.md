# Sesión 10 — Streaming II: inferencia en tiempo real

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Modelo completo en streaming vs endpoint
2. Hora del evento y consistencia de features
3. Evidencia versionada de scores y alertas

## Lab
Retomar la ruta de S9 con un STREAM_RUN nuevo y el pipeline completo de S6. `07_streaming_scoring.py` guarda probabilidad escalar, decisión y modelo_uri; no ajusta transformaciones sobre el stream.

## Entregable
Scores Parquet + ventanas + comparación de inputs batch/stream + latencia observada. Asociar candidato y métricas al mismo RUN_ID.

## Ejemplo / material de apoyo
`recursos/streaming/README.md` contiene todos los comandos del puente, productor y job; checkpoints separados para cada consulta.

## Recursos vinculados
- [`recursos/streaming/`](../../recursos/streaming/) — productor + consumidor con scoring
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — el `PipelineModel` que este lab carga y aplica

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-10.md`](../../slides_maestria/sesion-10.md) (Slidev)

**Cómo presentar** (desde `slides_maestria/`, `npm install` una sola vez):
```bash
npx slidev sesion-10.md --open
```
Abre un servidor local en modo presentación. Flechas/espacio para avanzar (incluye los `v-click`), `f` pantalla completa, `o` vista de overview. Atajos completos y export a PDF/PPTX: [`slides_maestria/README.md`](../../slides_maestria/README.md).
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
