# Hive — consultas de ejemplo

Mejora sobre `hive/` del repo original: el problema no era el contenido de las queries
sino que faltaba el contexto de *por qué* se particiona/bucketiza de cierta forma. Aquí
cada bloque de `hive-queries.sql` trae el comentario de la decisión de diseño, no solo
el SQL.

`hive-queries.sql` tiene 3 secciones progresivas:
1. **Fundamentos con datos sintéticos** (transacciones/clientes) — igual que antes.
2. *(dentro de la sección 2)* joins y window functions.
3. **Caso real del curso: Carpetas de investigación de la FGJ CDMX** — rescatado de
   `hive_commands_updated.sql` del repo original. Ese archivo en realidad era Markdown
   con la extensión `.sql` puesta por error (por eso no corría como SQL); aquí quedó
   separado correctamente: el SQL vive en `hive-queries.sql`, la explicación conceptual
   (EXTERNAL vs. MANAGED, partitioning, bucketing) vive en este README.

## El dataset real: Carpetas de investigación (CDMX)

**Actualización:** `carpetas_investigacion.csv` (~226.9 MB) está directamente disponible
en el Drive del curso — ver `recursos/datasets/README.md`, Sección 2. No hace falta
descargarlo del portal de CDMX; súbelo directo desde ahí:

```bash
gsutil cp carpetas_investigacion.csv gs://<TU-BUCKET>/carpetas_investigacion/
```

Si en algún momento ese archivo queda desactualizado, la fuente oficial (pública, viva,
se actualiza cada mes) sigue siendo una buena alternativa:
**https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico**

## Conceptos clave (glosario del lab original)

- **EXTERNAL vs. MANAGED**: con `EXTERNAL`, Hive solo administra los metadatos — un
  `DROP TABLE` no borra los archivos en Cloud Storage. Con una tabla `MANAGED` (interna),
  si borras la tabla, se borran los archivos físicos también. En este curso, casi todas
  las tablas son `EXTERNAL` a propósito: nunca queremos que un error de SQL borre datos
  que vinieron de una fuente externa.
- **PARTITIONED BY**: crea subdirectorios físicos (`/tabla/anio=2025/mes=06/`) — permite
  que Hive lea solo las particiones relevantes a una consulta (*partition pruning*) en
  vez de escanear toda la tabla.
- **CLUSTERED BY (bucketing)**: distribuye los datos en un número fijo de archivos según
  un hash de columna — optimiza joins y muestreo cuando el patrón de acceso no se presta
  bien a particionar (por ejemplo, una columna con demasiados valores distintos).

## Nota sobre el entorno

En el entorno GCP del curso, Hive corre dentro de Managed Service for Apache Spark
(Dataproc) (que ya incluye Hive preinstalado con su metastore). No hace falta instalarlo
aparte como en el repo original — solo crear el cluster con
`gcloud dataproc clusters create` (ver `recursos/managed-spark-cluster/`) y conectarse al
metastore vía `beeline` o desde un notebook con `%%sql` (Jupyter en el cluster).
