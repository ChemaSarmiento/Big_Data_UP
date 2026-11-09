# Instrucciones para trabajar en este repositorio

## Objetivo y orden de trabajo

- Rediseñar el curso con el syllabus moderno de Sistemas de Datos Distribuidos.
- Primero Especialidad: **8 sesiones de 3 horas**, perfil ejecutivo, SQL esencial y código guiado. Después Maestría: también 8 sesiones de 3 horas, con profundidad de ingeniería.
- Ocho sesiones están implementadas en `presentaciones-v2/`. **Estado editorial actual: S1–S7 rediseñadas (27/28/26/27/27/27/27 slides); S8 mantienen versión base. Total203.** El usuario rechazó la repetición de estructura del primer lote y pidió narrativa/visualización efectiva, paso a paso. El piloto permanece como referencia histórica.
- Fuente curricular prioritaria: `docs/rediseno-especialidad/syllabus-especialidad-fuente.md`, copia exacta de `~/Documents/syllabus_especialidad.md`. Leer también `docs/rediseno-especialidad/propuesta-editorial-s01-s03.md`. Mantener SQL S2 como adaptación pedagógica explícita, Bronze S3 y Silver S4.
- Antes de nuevos decks, leer el kit preservado en `docs/rediseno-especialidad/identidad-chema/`: voz, referentes, storytelling, visualizacion y presentaciones. Colores/typografías del kit; composiciones elegidas por mensaje, no todos los slides como dos tarjetas. Menos de25 palabras es objetivo narrativo, con excepciones legibles para SQL/tablas/labs. Una idea principal y un foco de color.
- **Fuentes de edición:** S1–S7 usan `presentaciones-v2/editorial/guion.py`, generado con `scripts/build-editorial.py`. S2–S8 guías usan `contenido.json`; solo S8 generan slides desde ese JSON. S1 guía y ficha son HTML directo. `scripts/build.py` debe preservar los decks/notas/README de S1–S7. Regenerar catálogo después. QA: `verify-editorial.mjs` para S1–S7, `verify-course.mjs` para S8. Ensayo cloud y paquetes reales siguen pendientes.
- Caso **guiado** de Especialidad confirmado por el usuario: **PROFECO, precios y decisiones de compra**, usando `all_data.csv` del Drive. El usuario aclaró que **cada equipo debe usar un dataset distinto para el proyecto final**; no confundir ejemplo común con proyecto obligatorio. `employees` de datacharmer en MariaDB/GCP es el puente para aprender SQL.
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
- Especialidad no requiere Python, Spark, despliegue de modelos ni streaming programado. Explicar su función y sus trade-offs con diagramas y demostraciones acotadas.

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
- Mantener separados SQL de MariaDB y GoogleSQL. Probar código en el motor al que se destina.
- Revisar los shells actuales antes de explicar infraestructura. El flujo actual instala MariaDB, pero no carga automáticamente `employees`. No cambiar sus decisiones docentes durante el trabajo editorial.
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
