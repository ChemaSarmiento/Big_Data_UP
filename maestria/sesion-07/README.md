# Sesión 07 — Streaming e inferencia en tiempo real

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. Windowing y watermarks
2. Exactly-once vs. at-least-once
3. Patrones de scoring en tiempo real (modelo en el stream vs. llamada a un endpoint externo)
4. Feature freshness

## Lab
Pipeline de Spark Structured Streaming que consume de Pub/Sub, aplica el pipeline de features de la Sesión 4 y genera un score con el modelo de la Sesión 5.

## Entregable
Pipeline de streaming con inferencia funcionando end-to-end.

## Ejemplo / material de apoyo
`recursos/etl-cripto/` no es streaming real, pero sí introduce el patrón más cercano dentro del curso: un segundo Extract que depende de una decisión tomada por un Transform anterior ("top movers"). Es un buen punto de partida conceptual antes de pasar a Structured Streaming, donde esa misma idea ocurre continuamente en vez de una sola vez.

## Recursos vinculados
- [`recursos/etl-cripto/`](../../recursos/etl-cripto/) — patrón de enriquecimiento en dos rondas
- [`recursos/etl-cripto/FLUJO.md`](../../recursos/etl-cripto/FLUJO.md) — diagrama del flujo

## Slides
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
