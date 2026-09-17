# Sesión 09 — Presentación del proyecto final

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Presentación del proyecto final (máx. 15 min por equipo)
2. Retroalimentación cruzada
3. Siguientes pasos (para quien quiera profundizar, mención del track de Maestría)

## Actividad principal
Cada equipo presenta su solución a una pregunta de negocio real de su área, con datos reales (≥15GB) y al menos una visualización de las conclusiones — mismo estándar institucional que Maestría, con el código adaptado al nivel del track: low-code/guiado, no escrito desde cero.

## Entregable
Documento + presentación con la estructura institucional completa:
1. Resumen ejecutivo (incluye introducción).
2. Visión general: qué se hizo, limitaciones de la solución, propósito/alcance.
3. Revisión y uso de datos: origen, preparación, limpieza, integridad y limitaciones del dataset (≥15GB) elegido desde la Sesión 0.
4. Proceso de desarrollo: metodología del ETL guiado/low-code usado (Looker Studio, notebook completado, apoyo del equipo técnico — lo que se haya usado, mostrado explícitamente).
5. Resultados y conclusiones, con **al menos una visualización**.
6. A quién beneficia la solución y estimación de costo/riesgo.

## Ejemplo / material de apoyo
Usar la tabla de criterios de evaluación de `PROGRAMA.md` (Sección 5) como rúbrica explícita frente al grupo antes de que empiecen las presentaciones. Para la estructura exacta del documento, las instrucciones del proyecto final publicadas en la plataforma del curso son la referencia — Especialidad y Maestría entregan el mismo documento, solo cambia la profundidad de código de la Sección 4.

## Recursos vinculados
- [`../PROGRAMA.md`](../PROGRAMA.md) — Sección 5, criterios de evaluación
- [`../sesion-00/README.md`](../sesion-00/README.md) — dónde se sembró la selección del dataset
- [`recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb`](../../recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb) — referencia de visualización si el equipo no usó Looker Studio

## Slides
- **Deck nuevo:** [`slides.md`](slides.md) (Marp)

**Cómo presentar** (desde esta carpeta):
```bash
npx @marp-team/marp-cli slides.md -o slides.html   # exporta y abre slides.html en el navegador
```
Pantalla completa: F11 en el navegador. Flechas ←/→ para navegar entre slides.
Alternativa en PDF (modo presentación del lector): `npx @marp-team/marp-cli slides.md -o slides.pdf`.

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
