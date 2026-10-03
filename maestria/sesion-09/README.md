# Sesión 09 — Streaming I: fundamentos y setup

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Tiempo de evento, ventanas y watermark
2. Reentregas, deduplicación y recuperación con checkpoint
3. Pub/Sub estándar → puente Python → JSON GCS → Spark

## Lab
Seguir `recursos/streaming/README.md`: topic/suscripción estándar, puente de persistencia, productor acotado y consumidor de conteo. Medir ventanas, latencia y un evento repetido/tardío.

## Entregable
Captura de ventanas + explicación de evento/procesamiento + prueba de reentrega y recuperación. Documentar límites de la garantía; consola no demuestra exactly-once.

## Ejemplo / material de apoyo
`pubsub_to_gcs.py` persiste antes de ACK. `stream_common.py` declara esquema y deduplica por ID dentro del watermark. `07a_streaming_conteo.py` agrupa por minuto/moneda.

## Recursos vinculados
- [`recursos/streaming/`](../../recursos/streaming/) — productor + consumidor de conteo
- [`recursos/etl-cripto/FLUJO.md`](../../recursos/etl-cripto/FLUJO.md) — puente conceptual desde batch

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-09.md`](../../slides_maestria/sesion-09.md) (Slidev)

**Cómo presentar** (desde `slides_maestria/`, `npm install` una sola vez):
```bash
npx slidev sesion-09.md --open
```
Abre un servidor local en modo presentación. Flechas/espacio para avanzar (incluye los `v-click`), `f` pantalla completa, `o` vista de overview. Atajos completos y export a PDF/PPTX: [`slides_maestria/README.md`](../../slides_maestria/README.md).
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
