# Sesión 10 — Streaming II: inferencia en tiempo real

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Patrones de scoring en tiempo real (modelo en el stream vs. llamada a un endpoint externo)
2. Feature freshness

## Lab
Extender el consumidor de la Sesión 9: `07_streaming_scoring.py` carga el `PipelineModel` entrenado en la Sesión 6, lo aplica sobre el mismo stream de `producer_transacciones_stream.py`, y genera un score por transacción además del conteo por ventana — ahora filtrado a solo las transacciones marcadas como sospechosas.

## Entregable
Pipeline de streaming con inferencia funcionando end-to-end: captura de la consola con las ventanas de alertas actualizándose en vivo, y muestra del Parquet de scores generado.

## Ejemplo / material de apoyo
`recursos/streaming/07_streaming_scoring.py` — mismo esqueleto de la Sesión 9, con el `PipelineModel` de la Sesión 6 aplicado directo sobre el DataFrame en streaming.

## Recursos vinculados
- [`recursos/streaming/`](../../recursos/streaming/) — productor + consumidor con scoring
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — el `PipelineModel` que este lab carga y aplica

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-10.md`](../../slides_maestria/sesion-10.md) (Slidev) — `npx slidev sesion-10.md --open` desde `slides_maestria/`
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
