# Sesión 13 — Gobernanza, seguridad y capstone técnico

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. IAM a nivel dataset/tabla
2. Data Catalog, linaje de datos y de modelos
3. Cumplimiento en contextos regulados (banca/finanzas)
4. FinOps de un pipeline de ML a escala
5. Presentación del capstone técnico (máx. 15 min c/u)

## Actividad principal
Presentación del capstone técnico (máx. 15 min c/u): pipeline completo ingesta → features → entrenamiento → serving, con al menos un componente de streaming u orquestación, visualizaciones de los resultados y evidencia de pruebas.

## Entregable
Documento + presentación con la estructura institucional completa (resumen ejecutivo, visión general, revisión y uso de datos, proceso de desarrollo con metodología y pruebas, resultados y conclusiones) más el pipeline reproducible en código: (1) ingesta distribuida, (2) feature engineering con Spark MLlib, (3) modelo entrenado y evaluado, (4) serving o inferencia batch programada, (5) streaming u orquestación con Airflow, (6) **al menos una visualización** de las conclusiones, (7) evidencia de **pruebas** (validación de calidad de datos + comparación de métricas antes/después de al menos una optimización).

## Ejemplo / material de apoyo
`recursos/mariadb/crear_firewall_y_instancia.sh` es en sí mismo un caso de estudio de gobernanza/seguridad: compara el diseño original (`0.0.0.0/0` abierto, passwords hardcodeadas) contra el rediseño (rango de IAP, credenciales generadas en tiempo de ejecución) — buen material de discusión para la sesión. Para el requisito de visualización y pruebas del capstone, el hilo completo Sesión 6 → 11 ya deja el material: gráficas de comparación de métricas (S6), `monitor_drift.py` con PSI (S11) sirve tanto de "prueba" (¿el dato de entrada se parece al de entrenamiento?) como de visualización si se grafica.

## Recursos vinculados
- [`recursos/mariadb/README.md`](../../recursos/mariadb/README.md) — antes/después de seguridad
- [`recursos/serving/monitor_drift.py`](../../recursos/serving/monitor_drift.py) — evidencia de pruebas de calidad de datos (PSI)
- [`recursos/spark/04_pipeline_ml.ipynb`](../../recursos/spark/04_pipeline_ml.ipynb) — `metrics.json`, base para la comparación antes/después

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-13.md`](../../slides_maestria/sesion-13.md) (Slidev) — `npx slidev sesion-13.md --open` desde `slides_maestria/`
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
