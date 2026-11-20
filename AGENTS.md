# Instrucciones para trabajar en este repositorio

## Objetivo y orden de trabajo

- Rediseñar el curso con el syllabus moderno de Sistemas de Datos Distribuidos.
- Primero Especialidad: **8 sesiones de 3 horas**, perfil ejecutivo, SQL esencial y código guiado. Después Maestría: también 8 sesiones de 3 horas, con profundidad de ingeniería.
- Ocho sesiones están implementadas en `presentaciones-v2/`. **Estado editorial actual (segunda ronda): S1–S7 rehechas (28/28/24/28/25/27/26 slides); S8 NO se ha rehecho y sigue con la versión anterior (menciona equipos, dataset compartido y fechas; pendiente). Total 210.** El usuario rechazó la repetición de estructura del primer lote y pidió narrativa/visualización efectiva, paso a paso. El piloto permanece como referencia histórica.
- Fuente curricular prioritaria: `docs/rediseno-especialidad/syllabus-especialidad-fuente.md`, copia exacta de `~/Documents/syllabus_especialidad.md`. Leer también `docs/rediseno-especialidad/propuesta-editorial-s01-s03.md`. Mantener SQL S2 como adaptación pedagógica explícita, Bronze S3 y Silver S4.
- Antes de nuevos decks, leer el kit preservado en `docs/rediseno-especialidad/identidad-chema/`: voz, referentes, storytelling, visualizacion y presentaciones. Colores/typografías del kit; composiciones elegidas por mensaje, no todos los slides como dos tarjetas. Menos de25 palabras es objetivo narrativo, con excepciones legibles para SQL/tablas/labs. Una idea principal y un foco de color.
- **Fuentes de edición:** S1–S7 usan `presentaciones-v2/editorial/sNN.py` (+ `sNN.css/js`; helpers y laboratorios compartidos en `guion.py`, que S1 aún usa para sus slides de laboratorio), generado con `scripts/build-editorial.py [N]` (un argumento = solo esa sesión). S2–S8 guías usan `contenido.json`; solo S8 generan slides desde ese JSON. S1 guía y ficha son HTML directo. `scripts/build.py` debe preservar los decks/notas/README de S1–S7. Regenerar catálogo después. QA: `verify-editorial.mjs` para S1–S7, `verify-course.mjs` para S8. Ensayo cloud y paquetes reales siguen pendientes.
- **Caso guiado desde S3 (decisión del usuario):** `war_tweets.txt` del Drive (JSON Lines de Twitter/snscrape, 22.04 GiB; 6,798,932 tweets del 16 al 27 de marzo de 2022; el 16 es día parcial; sin retweets; no es muestra representativa). Uso **académico**: datos tal cual, sin seudonimizar; se trabajan temas satélite de negocio (energía, alimentos, aviación, sanciones, cadena de suministro, mercados). **Cada alumno crea sus propios datos en su propio proyecto**: copia el archivo de Drive a su bucket con el cuaderno de Colab del curso (Drive → Storage; no está en el repo) y construye Bronze → Silver → Gold en sus datasets `tweets_bronze/silver/gold`. Nada se lee de proyectos o buckets ajenos. Cifras de referencia: `presentaciones-v2/recursos/tweets/verdad.json`. Sin actividades de equipo ni entregables H hasta el cierre del curso.
- Leer primero [checkpoints.md](checkpoints.md), [PLAN_ESPECIALIDAD.md](PLAN_ESPECIALIDAD.md) y el [syllabus de Especialidad](docs/rediseno-especialidad/syllabus-especialidad-fuente.md).
- Las peticiones posteriores del usuario prevalecen sobre estas instrucciones. Distinguir decisiones confirmadas de propuestas.

## Estado previo y cuidado del trabajo

- La revisión empezó en `plan2`; por petición del usuario se creó y activó **`plan3`** para los cambios del rediseño. Hay modificaciones locales del usuario. Revisar `git status --short` y el diff antes de editar.
- No descartar, sobrescribir, guardar en stash ni revertir cambios ajenos para facilitar el trabajo.
- Los materiales anteriores siguen como referencia hasta completar su sustitución. No renumerar automáticamente las sesiones antiguas: su estructura no corresponde a las nuevas ocho.
- El diagnóstico inicial está en [diagnostico.md](docs/rediseno-especialidad/diagnostico.md).
- No crear recursos con costo, publicar, hacer push ni modificar Firestore como consecuencia de una revisión documental. Si el usuario pide después esas acciones, su autorización define el alcance.

## Reglas pedagógicas y editoriales

- Español claro. Una pregunta de negocio y una evidencia observable por bloque.
- **Cole Nussbaumer Knaflic:** conclusión explícita en el título, contexto y unidades, etiquetas directas, quitar ruido, énfasis visual deliberado. No inventar hallazgos para llenar una gráfica.
- **Nancy Duarte / Resonate:** audiencia protagonista, tensión entre situación actual y posibilidad de mejora, demostración y acción final. Aplicar como arco narrativo, sin copiar material de los libros.
- Incluir teoría suficiente para explicar decisiones; evitar tanto las listas de vocabulario como las recetas sin explicación.
- Cada laboratorio debe indicar: prerrequisitos, ubicación en la interfaz, acción exacta, código completo, salida esperada, comprobación, error frecuente y recuperación, entregable y cierre de recursos.
- Separar diapositivas legibles para proyección, guía extensa de laboratorio y notas del docente. No ocultar instrucciones necesarias en notas privadas.
- Sesiones 1–7 alternan ejemplo guiado y transferencia al proyecto propio de cada equipo (dataset distinto); sesión 8 presenta y defiende, sin introducir nueva infraestructura. Leer `PROPUESTA_SLIDES_ESPECIALIDAD.md` y `docs/rediseno-especialidad/proyectos-diversos.md`.
- El trabajo actual es **solo Especialidad**. ML: como máximo una distinción conceptual breve (10 min) para cubrir el syllabus; sin entrenamiento, código/modelos, métricas técnicas ni entregable predictivo. La práctica de IA es GenAI/evidencia y el concepto RAG.
- Especialidad **incluye Spark/PySpark** de forma guiada desde S3 (JSON → Parquet; equivalencia con SQL en S4). Sigue fuera: despliegue de modelos y streaming programado.

## Datos, métricas y rigor

- El catálogo público se llama **`metadata.json`**; el usuario lo recordó como `metadatos.json`. El snapshot está en `docs/rediseno-especialidad/metadata-drive.snapshot.json`.
- Ese inventario registra activos, tamaños y enlaces; **no valida esquemas, licencias, procedencia ni calidad**. No tratar los nombres como prueba de contenido.
- En PROFECO, una observación de precio no es una venta. No calcular ingresos, ticket de compra, demanda, margen o inflación oficial sin las fuentes y metodología correspondientes.
- Comparar producto + marca + presentación/unidad, geografía y periodo compatibles. Registrar cobertura y fecha histórica; no recomendar compras actuales usando precios antiguos.
- No sumar versiones/copias de un dato para aparentar volumen. No imponer un mínimo de 15 GB como requisito nuevo: aparece en el material anterior y falta confirmar su vigencia institucional.
- Distinguir resultado medido, dato ilustrativo y beneficio reportado por una empresa/proveedor. Toda cifra externa debe tener fuente verificable.
- Resumir un CSV con un LLM no equivale a RAG. Mostrar recuperación y evidencia citada si se usa ese nombre.

## Implementación de las presentaciones, al iniciar producción

- HTML interactivo estático, navegación por clic y teclado, revelado controlado por clic, fade de entrada/salida y diagramas progresivos. Respetar `prefers-reduced-motion`.
- No hacer avanzar la presentación al seleccionar/copiar código ni al interactuar con formularios, enlaces o controles de diagramas.
- Añadir enlaces profundos, índice, pantalla completa, modo laboratorio, descarga de código y versión imprimible con todo el contenido revelado.
- Reutilizar lo útil de `presentaciones/` y sus tokens visuales. La v2 debe tener una fuente única por sesión; evitar concatenar teoría, complementos y desarrollo con heurísticas de títulos.
- `presentaciones/dist/` es salida generada: editar fuentes, no el resultado del build.
- `firebase.json` publica HTML mediante **Firebase Hosting**. Firestore sirve la funcionalidad del reto SQL; las slides no necesitan una base de datos.
- Conservar el reto SQL y la Maestría existente mientras se desarrolla Especialidad v2 de forma aislada.

## Cloud y verificación

- Los US$300 son crédito de prueba de GCP, no un plan mensual. Verificar condiciones, elegibilidad, vigencia, región, cuotas y disponibilidad de modelos antes de clase.
- Las alertas de presupuesto no detienen el gasto. Los labs deben incluir estimación de bytes, límites apropiados, expiración y cierre.
- No obligar a descargar archivos de ~19 GB en laptops o almacenamiento persistente de Cloud Shell; preparar la fuente grande en GCS y una muestra reproducible.
- **El SQL de Especialidad (S2) se aprende en MariaDB con `employees`** (datacharmer test_db) en una VM del propio alumno, creada con `recursos/mariadb/` (e2-micro, usuario de curso `big_data_user`; tarda ~14 min en instalar y ~3.5 min en cargar employees), para no gastar BigQuery. BigQuery entra desde S3 con datos pequeños-medianos propios. UNNEST y CTE se enseñan en S4.
- **Proyecto GCP de referencia del docente: `big-data-lunes-2026-1`** (solo para medir/ensayar; el material de alumno no lo nombra). Allí se construyeron `tweets_bronze/silver/gold` (Silver: tweets, autores, hashtags; Gold: tema_dia, hashtags_dia, autores_alcance, aplicaciones_dia, actividad_hora, conversacion_dia), se ensayó Dataproc Serverless y MariaDB/employees. Existen además una VM `mariadb-curso` apagada y la regla `allow-mariadb-curso` de una clase previa. Crear recursos con costo exige autorización explícita del usuario en el chat. Data Studio es el nombre actual de Looker Studio.
- Verificar cada deck con navegador: legibilidad, interacción, enlaces, diagramas, movimiento reducido y ausencia de recortes; verificar labs con evidencia real antes de decir que corren end-to-end.
- Las comprobaciones locales no demuestran una ejecución en GCP. Registrar límites y pasos pendientes.

## Recuperación del trabajo

- Actualizar `checkpoints.md` al completar un bloque: fecha, archivos, decisiones, validaciones, pendientes y siguiente paso concreto.
- Mantener fuentes y fecha de consulta en `docs/rediseno-especialidad/fuentes.md`.
- No marcar aprobado, implementado, probado en cloud o publicado algo que solo esté propuesto.

## Publicación desde plan3

- El rediseño se empaqueta en `/refactor_especialidad/` por `scripts/package-refactor.py`, después del build existente. Ver `docs/rediseno-especialidad/publicacion.md`.
- El workflow de plan3 publica Hosting al hacer push. El workflow antiguo en plan2 aún podría sustituir el sitio si se dispara desde esa rama; usar plan3 para esta publicación.
- Los cambios locales previos del sitio antiguo quedan fuera del commit de esta sección. No incorporarlos automáticamente al próximo push.

## Clase emergente independiente

- `presentaciones-v2/clase-bigquery/`: ejecutivos,180 min; BigQuery → arquitecturas y Medallion → laboratorio all_data.csv → tarea de actualización. No altera las ocho sesiones.
- Fuente: `clase-bigquery/guion.py`; generador `scripts/build-clase-bigquery.py` después de build-editorial. Guía y tarea se generan allí; SQL/CSV son recursos fuente separados. Workflow y package-refactor incluyen la carpeta para el siguiente push.
- Muestra REAL de4500 filas extraída de tres ventanas deall_data, con manifiesto/hash. No mezclarla con el fixture ficticio de16 filas del curso; son paquetes distintos. No extrapolar cobertura ni calidad al archivo entero.
- BigQuery no ejecutado aún: controles locales de muestra, parserGoogleSQL y navegador no sustituyen ensayo cloud. La carga completa requiereGCS preparado por el docente; no bajar20.7GB aCloud Shell.


## Reglas editoriales vigentes (usuario, 2026-11-19)

- Texto para el alumno individual y repetible: sin fechas de calendario, sin «el docente», sin trabajo en equipo, sin entregas H en S1–S7.
- Cada concepto se explica antes de usarse; S1 es introducción (sin Medallion/Spark/dashboards/RAG). Una sola slide de laboratorio por sesión; laboratorios de 6 pasos y 70 min (dónde, acción, costo, código, salida real, comprobación, error frecuente).
- Tiempos: Abrir 0–15, Comprender 15–50, Aplicar 50–70, Pausa 70–80, Laboratorio 80–150, Cerrar 150–180.
- Generadores: `build-editorial.py [N]` (S1–S7, módulos `editorial/sNN.py`), `build.py [N]` (guías S2–S8), `catalogo.py`; verificación: `verify-editorial.mjs` (ONLY=N), `verify-resources.py`, `verify-hosting.mjs`.
