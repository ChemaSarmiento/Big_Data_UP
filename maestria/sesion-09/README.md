# Sesión 09 — Gobernanza, seguridad y capstone técnico

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)

## Índice
1. IAM a nivel dataset/tabla
2. Data Catalog, linaje de datos y de modelos
3. Cumplimiento en contextos regulados (banca/finanzas)
4. FinOps de un pipeline de ML a escala
5. Presentación del capstone técnico (20 min c/u)

## Actividad principal
Presentación del capstone técnico: pipeline completo ingesta → features → entrenamiento → serving, con al menos un componente de streaming u orquestación.

## Entregable
Pipeline reproducible en código con: (1) ingesta distribuida, (2) feature engineering con Spark MLlib, (3) modelo entrenado y evaluado, (4) serving o inferencia batch programada, (5) streaming u orquestación con Airflow.

## Ejemplo / material de apoyo
`recursos/mariadb/crear_firewall_y_instancia.sh` es en sí mismo un caso de estudio de gobernanza/seguridad: compara el diseño original (`0.0.0.0/0` abierto, passwords hardcodeadas) contra el rediseño (rango de IAP, credenciales generadas en tiempo de ejecución) — buen material de discusión para la sesión.

## Recursos vinculados
- [`recursos/mariadb/README.md`](../../recursos/mariadb/README.md) — antes/después de seguridad

## Slides
- `slides/03_casos_de_uso_arquitectura.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
