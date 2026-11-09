# Diagnóstico del material existente

Revisión del 2026-11-05 sobre la rama local `plan2`, el sitio público y los archivos proporcionados. Es una revisión inicial de contenido/estructura, no una certificación de todos los laboratorios.

## Evidencia consultada

- Syllabus local: `/home/chema/Documents/syllabus_actualizado_sistemas_de_datos_distribuidos.md`; copia en [syllabus-fuente.md](syllabus-fuente.md).
- `README.md`, `REVISION_CURRICULAR.md`, `especialidad/TEMARIO.md`, slides y desarrollo seleccionados, constructor y reproductor web, configuración Firebase, catálogo de datasets y scripts MariaDB/SQL.
- Sitio `https://bigdata-up.web.app/`: HTML, `decks.json` y revisión con Chromium del catálogo y `#especialidad-06/8` (Medallion). Esas dos páginas no arrojaron errores de JavaScript en la comprobación. No se recorrieron todas las slides.
- `/home/chema/Downloads/Slides.zip`: inventario de siete PPTX y extracción del texto de sus 216 diapositivas. Varias páginas son imágenes: el texto extraído no permite evaluar sus gráficos; no se afirma una revisión visual completa de los originales.
- Drive público: inventario de carpeta y descarga únicamente de `metadata.json`, no de los datasets grandes. Snapshot preservado en [metadata-drive.snapshot.json](metadata-drive.snapshot.json).

## Hallazgos que cambian el diseño

| Hallazgo verificable | Implicación para el rediseño |
|---|---|
| README: Especialidad 9 sesiones/27 h + nivelación; Maestría 13/39 h | El pedido actual de 8×3 h por track exige rediseñar, no solo renumerar |
| Especialidad tiene práctica de Spark y Python en distintos recursos | Mover implementación de ingeniería a Maestría; conservar el criterio de arquitectura en Especialidad |
| El syllabus pone limpieza antes del SQL fast track | Enseñar SQL en S2 antes de pedir CTAS, casting y joins |
| El sitio publicado contiene **25 decks / 602 slides** al consultar; `REVISION_CURRICULAR.md` registra 350 | Hay documentación de otra versión; no reutilizar sus cifras de validación como evidencia actual |
| El build concatena slides, complementos y desarrollo y agrega bloques automáticos | Una sesión puede mezclar narrativas y repetir encabezados genéricos; adoptar fuente v2 explícita |
| El renderer elimina `v-click` y anima por tiempo; el clic del escenario navega | Implementar estados de revelado reales y controlar propagación de eventos |
| La slide Medallion publicada es una tabla con analogías y una referencia al ETL de tipo de cambio | La idea es rescatable; falta seguir un registro del mismo proyecto a través de las capas |
| El desarrollo publicado usa muchos títulos como «Caso de apertura — una decisión con consecuencias» | Titular con el dilema o conclusión concreta para esa sesión |
| El syllabus propone vista materializada con ventanas | Para la ruta base usar CTAS o vista lógica; la vista incremental tiene restricciones |
| El syllabus propone exportar «Top 50 clientes» y pedir insights | PROFECO no tiene clientes/ventas; cambiar a agregados de precios/cobertura. CSV con prompt no demuestra RAG |
| El sitio está configurado como Hosting; Firestore tiene reglas y reto SQL | Publicar HTML requiere Hosting; no hace falta trasladar las slides a Firestore |

La identidad visual actual ya tiene tipografía, tokens, tema oscuro y movimiento reducido. Son activos reutilizables. La prioridad es mejorar coherencia, densidad, explicación y participación, antes que añadir más animaciones.

## Qué rescatar de los siete PPTX

| Archivo en `Slides.zip` | Slides | Contenido recuperable para Especialidad | Adaptación necesaria |
|---|---:|---|---|
| `1. Introducción (1).pptx` | 16 | Diagnóstico del grupo, cinco V, valor y usos empresariales | Actualizar cifras externas; no adoptar automáticamente evaluación antigua |
| `1.2 Fuentes y manejo (1).pptx` | 38 | Formatos, schema-on-read, trazabilidad, lake/warehouse/lakehouse, OLTP/OLAP | Sustituir API histórica de Twitter por ejemplo estable; no equiparar automáticamente DSS con producto de datos |
| `1.3 Casos de uso y Arquitectura (1).pptx` | 22 | Personalización/latencia, finanzas, salud, on-prem/cloud y mapa de servicios | Añadir fuentes reales; distinguir ilustración sectorial de caso de éxito documentado |
| `SQL Fast track.pptx` | 48 | `employees`, SELECT/filtros/agregados/joins y problemas de duplicación | Separar instalación docente; corregir ejemplo de UPDATE; priorizar lectura/analítica sobre DML y subconsultas avanzadas |
| `Grandes_Bases_de_Datos_26.pptx` | 43 | Separación GCS/cómputo, tablas externas, particiones y decisión Hive/BigQuery | Reescribir lab para BigQuery; no trasladar literalmente bucketing de Hive a clustering; revisar afirmaciones de costo |
| `Spark_Explained_26.pptx` | 21 | Mapa conceptual de ejecución y paralelismo, si los gráficos se validan visualmente | Especialidad: demo conceptual breve. Código, tuning y Spark Core se reservan a Maestría |
| `Datos_Python_FastTrack.pptx` | 28 | Referencia para otra audiencia | No incluir nivelación Python obligatoria dentro de las 24 h de Especialidad |
| **Total** | **216** | | |

## MariaDB y `employees`: comportamiento real de los shells

Archivos revisados: `recursos/mariadb/crear_firewall_y_instancia.sh`, `startup-mariadb.sh`, `verificar_instalacion.sh`, `environment/mariadb-vscode-setup.md` y `recursos/sql-practica/employee_db_queries.sql`.

- El creador corre en Cloud Shell, crea firewall e instancia `mariadb-curso`, `e2-micro`, Ubuntu 22.04, disco de 30 GB, zona `us-central1-a`. El startup instala MariaDB y crea el usuario de clase.
- Debe ejecutarse desde `recursos/mariadb/`: la ruta `startup-mariadb.sh` es relativa. `employees` **no se clona ni carga automáticamente**.
- La conexión de alumnado documentada es SQLTools/VSCode a la IP externa. El túnel IAP es opcional, según el rango usado al crear la regla.
- Los shells actuales permiten por defecto el puerto 3306 desde cualquier origen y usan credencial didáctica compartida, por decisión explícita documentada en su README. No se alteraron en esta revisión. El README raíz y la revisión curricular describen un estado anterior distinto: **el código actual es la evidencia del comportamiento**.
- Si una regla ya existe, el script no reconcilia su rango; volver a invocarlo con otro argumento no demuestra que haya cambiado. Documentar el estado efectivo en la preparación docente.
- Para Especialidad, preparar `datacharmer/test_db` antes de S2 y comprobarlo con la conexión de alumno, no solo con root. La capacidad de `e2-micro` para una clase completa requiere ensayo de concurrencia; no se garantiza por la creación exitosa de una VM.
- `verificar_instalacion.sh` revisa servicio/puerto/log, pero no prueba conteos de `employees` ni consultas de la clase.
- El SQL existente mezcla vigencias históricas de salarios/títulos: las consultas por título necesitan una fecha de corte o regla temporal para no multiplicar observaciones. `COUNT(DISTINCT CONCAT(nombre, apellido))` no cuenta personas de forma fiable; usar `emp_no`.

No se provisionó ni modificó ninguna instancia en esta revisión.

## Qué sabemos del Drive y qué no

El archivo visible se llama `metadata.json` (153 KB aprox.), ID `1vC5h9Ea5d3GivmXoYGnPov6efnostY-1`. Su primer registro describe otro archivo también llamado `metadata.json` con ID distinto: no confundir ese registro con el fichero descargado.

Tiene **255 entradas**: 19 de archivo único y 236 de carpeta Parquet. Campos: ID, nombre, tipo, formato, tamaño reportado, cantidad de archivos internos, creación/modificación, URL, categoría y descripción. **19 descripciones están sin completar**; las 236 carpetas tienen categoría genérica `Dataset Cripto / Spark`, incluso activos de otros temas. No sumar tamaños del catálogo como si fueran datasets independientes: puede incluir carpetas anidadas o representaciones del mismo origen.

| Activo | `tamanio_mb` del catálogo | Uso propuesto |
|---|---:|---|
| `all_data.csv` | 19706.44 | Caso central confirmado; perfilar esquema y cobertura antes de escribir SQL definitivo |
| `quien_es_quien.csv` | 15414.27 | Comparación opcional de calidad; equivalencia con `all_data` no verificada aquí |
| `bank_transactions.csv` | 7511.06 | Reservar alternativa/ejercicios de Maestría; no inferir fraude confirmado |
| `Checkouts_by_Title_20250207.csv` | 10151.95 | Posible transferencia a otro sector |
| `http_sentiment_raw.csv` | 14540.90 | Posible ingeniería de datos en Maestría |
| `steam_reviews.csv` | 7793.22 | Posible texto/GenAI en Maestría |
| `employee_location.csv` | 16.19 | No asumir compatibilidad con `datacharmer/test_db` |

Este primer corte no inspeccionó filas de esos archivos ni sus licencias. Los esquemas descritos por el repo anterior son una hipótesis de trabajo, no una nueva validación. Antes de publicar SQL exacto, cerrar contrato de datos y guardar una muestra verificable.

## Límites de esta revisión

No se ejecutaron labs GCP, SQL sobre el dataset real, carga de MariaDB ni llamadas al modelo. No se hizo un nuevo build de las presentaciones actuales, porque el corte no modifica su código. Las cifras del sitio corresponden a la descarga pública de esta fecha. Las capturas de auditoría se tomaron en `/tmp`; el repositorio conserva los hallazgos y fuentes, no depende de esas rutas temporales para retomar.
