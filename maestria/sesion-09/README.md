# Sesión 09 — Streaming I: fundamentos y setup

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Windowing y watermarks
2. Exactly-once vs. at-least-once
3. Setup de Pub/Sub Lite (topic, suscripción) y primer stream corriendo

## Lab
Crear el topic y la suscripción de Pub/Sub Lite, correr `producer_transacciones_stream.py` (publica `bank_transactions.csv` simulando llegada en tiempo real), y correr `07a_streaming_conteo.py` — un consumidor de Structured Streaming que solo cuenta transacciones por ventana de 1 minuto, sin scoring todavía. El objetivo es ver windowing/watermarks funcionar en vivo antes de agregar el modelo la próxima sesión.

## Entregable
Captura de las ventanas de conteo actualizándose en consola + confirmación de que el productor y el consumidor corrieron simultáneamente sin errores.

## Ejemplo / material de apoyo
`recursos/streaming/07a_streaming_conteo.py` — Structured Streaming real sobre Pub/Sub Lite (el conector oficial de Google para Spark; Pub/Sub estándar no tiene uno), aislando windowing/watermark del scoring. `recursos/etl-cripto/` sigue siendo útil como puente conceptual desde batch.

## Recursos vinculados
- [`recursos/streaming/`](../../recursos/streaming/) — productor + consumidor de conteo
- [`recursos/etl-cripto/FLUJO.md`](../../recursos/etl-cripto/FLUJO.md) — puente conceptual desde batch

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-09.md`](../../slides_maestria/sesion-09.md) (Slidev) — `npx slidev sesion-09.md --open` desde `slides_maestria/`
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
