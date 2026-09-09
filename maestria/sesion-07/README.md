# Sesión 07 — Streaming e inferencia en tiempo real

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Windowing y watermarks
2. Exactly-once vs. at-least-once
3. Patrones de scoring en tiempo real (modelo en el stream vs. llamada a un endpoint externo)
4. Feature freshness

## Lab
Correr `producer_transacciones_stream.py` (publica `bank_transactions.csv` a Pub/Sub Lite, simulando llegada en tiempo real) y `07_streaming_scoring.py` (Structured Streaming, aplica el `PipelineModel` de la Sesión 4/5 y genera un score por transacción + un conteo de alertas por ventana de 1 minuto).

## Entregable
Pipeline de streaming con inferencia funcionando end-to-end: captura de la consola con las ventanas de alertas actualizándose en vivo, y muestra del Parquet de scores generado.

## Ejemplo / material de apoyo
`recursos/streaming/07_streaming_scoring.py` — Structured Streaming real sobre Pub/Sub Lite (el conector oficial de Google para Spark; Pub/Sub estándar no tiene uno). `recursos/etl-cripto/` sigue siendo útil como puente conceptual antes de este lab: introduce, en batch, la idea de un segundo paso que depende de una decisión tomada por el paso anterior — la misma idea que aquí ocurre de forma continua, no una sola vez.

## Recursos vinculados
- [`recursos/streaming/`](../../recursos/streaming/) — productor + consumidor de streaming real
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — el `PipelineModel` que este lab carga y aplica
- [`recursos/etl-cripto/FLUJO.md`](../../recursos/etl-cripto/FLUJO.md) — puente conceptual antes del lab

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-07.md`](../../slides_maestria/sesion-07.md) (Slidev) — `npx slidev sesion-07.md --open` desde `slides_maestria/`
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
