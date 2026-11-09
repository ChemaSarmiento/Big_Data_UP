# Clase independiente · BigQuery, arquitecturas y Medallion

Ejecutivos · 180 minutos · 26 slides. **Ruta local:** `/clase-bigquery/`. Al publicar desde plan3: `/refactor_especialidad/clase-bigquery/`. Esta clase no añade una novena sesión al curso de Especialidad.

Secuencia: BigQuery (30 min), propuestas de arquitectura (20), Medallion (20), pausa (10), laboratorio con all_data.csv (80), tarea de actualización (20). El laboratorio usa una muestra real reproducible, no el fixture ficticio del curso. La ruta docente permite cargar el archivo completo desde GCS antes de impartir.

## Materiales

- `index.html`: presentación interactiva; clic/flechas, índice, notas, laboratorio y PDF desde imprimir.
- `laboratorio.html`: pasos con ubicación en consola, consultas completas, resultados, recuperación y cierre.
- `tarea.html`: nuevo corte oficial, contrato de esquema, lotes, repetición, reconciliación y propuesta incremental.
- `recursos/`: CSV de4500 filas, manifiesto de muestreo, esquema, ocho archivos GoogleSQL, carga con bq y registro de rendimiento.
- `guion.py`: fuente editorial con tiempos y notas. `scripts/build-clase-bigquery.py` reutiliza el shell de S1 después del build editorial.

## Qué se comprobó

El origen público respondió HTTP206 con tamaño20663702126 bytes. Inspección del2026-11-09: tres ventanas de2MiB (inicio, mitad, final),1500 registros completos de15 campos por ventana. Método no aleatorio ni representativo; valores preservados, serializaciónCSV nueva. El SHA256 corresponde a la muestra, no al archivo completo. Periodos vistos2011/2014/2015 no prueban la cobertura global.

Se observaron4500 filas distintas,3000 municipios con espacios finales,0 rechazos según las reglas docentes y0 conflictos deprecio por producto/tienda/día en esta muestra. El par históricoREFRESCO/SPRITE/2L no retornable/Tlalpan/2014-03-19 aparece a15.10 y15.50MXN. No prueba inventario ni ahorro actual; no representa todas las tiendas.

Controles locales: `python3 presentaciones-v2/scripts/verify-all-data-sample.py`. Sintaxis analizada con sqlglot en dialectoBigQuery; esto no sustituye el motor. Navegador: `node presentaciones-v2/scripts/verify-clase-bigquery.mjs`; proyector/móvil, controles interactivos, enlaces y PDF. Artefactos `/tmp/bigdata-clase-bigquery/`.

**Pendiente:** ejecutar SQL/carga enBigQuery, medir jobs/bytes reales y perfilar el archivo completo. No se crearon recursos cloud ni se publicó esta clase durante su producción. Los scripts03/04 reconstruyen capas; no implementan actualización incremental. La tabla plana es un duplicado temporal exclusivo delbenchmark.

## Regenerar

Desde raíz, después de generar las sesiones editoriales:

```sh
python3 presentaciones-v2/scripts/build-clase-bigquery.py
python3 presentaciones-v2/scripts/catalogo.py
```

Para publicar, el workflow deplan3 ya incluye build y empaquetado. No ejecutar `muestrear-all-data.py` enCI: requiere red y puede cambiar la muestra si cambia el origen. La muestra guardada y su manifiesto son el punto reproducible del taller.
