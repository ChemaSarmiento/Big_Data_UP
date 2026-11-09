# Fuentes y registro de consulta

Consultadas el **2026-11-05**. Este registro apoya el plan y orienta la producción: no demuestra que los labs estén ejecutados. Usar enlaces directos por slide/guía cuando se escriban; verificar de nuevo interfaces, modelos y precios antes de clase.

## Fuentes del encargo

| Fuente | Evidencia y límites |
|---|---|
| [Syllabus moderno preservado](syllabus-fuente.md) | Copia sin modificaciones del archivo local indicado por el usuario. Es fuente de objetivos; la secuencia propuesta ajusta prerrequisitos y carga cognitiva |
| [Repositorio, rama plan2](https://github.com/ChemaSarmiento/Big_Data_UP/tree/plan2) | Revisado desde el checkout local; hay cambios locales previos, no se afirma identidad con el remoto |
| [Sitio actual](https://bigdata-up.web.app/) y [contenido de decks](https://bigdata-up.web.app/decks.json) | Consulta pública y revisión visual parcial con Chromium. 25 decks/602 slides al consultar |
| [Carpeta Drive](https://drive.google.com/drive/folders/1oKaHqT3DhwyLlE3wYbbQ5nJBQb_uckZj) | Inventario visible; no se descargaron datos grandes |
| [metadata.json del Drive](https://drive.google.com/file/d/1vC5h9Ea5d3GivmXoYGnPov6efnostY-1/view) | 255 entradas; [snapshot local](metadata-drive.snapshot.json). No contiene contratos de esquema ni licencias |
| [all_data.csv](https://drive.google.com/file/d/1dLxKFxawXTTaqCDr9Y9YpYdWTpOhol42/view) | Fuente central elegida; tamaño reportado, no perfilado en esta revisión |
| `~/Downloads/Slides.zip` | Siete PPTX, 216 slides; inventario y extracción de texto. Las páginas basadas en imágenes necesitan revisión visual posterior |

## Narrativa y visualización

- **Cole Nussbaumer Knaflic**, [so what?](https://www.storytellingwithdata.com/blog/2017/3/22/so-what): fundamenta explicitar el mensaje de cada visual y su relevancia para la audiencia. Aplicación propuesta: títulos con mensaje, contexto y conclusiones defendibles.
- **Nancy Duarte**, [Resonate, página oficial del libro](https://www.duarte.com/resources/books/resonate/): respalda el papel de la audiencia como protagonista y la estructura de conflicto, resolución y acción. El plan adapta estos principios al arco del curso.
- **Duarte**, [Delivering dynamic virtual presentations](https://www.duarte.com/blog/dynamic-virtual-presentations/): recomienda claridad, variedad y una idea por pantalla; ayuda a convertir el plan en una experiencia de clase. Los enlaces antiguos de `5-ways-to-resonate-remotely` y `content-virtual-communication` redirigen aquí: no usar sus extractos históricos como citas del contenido actual.

Los libros *Storytelling with Data* y *Resonate* son marcos solicitados por el usuario. No se ha afirmado acceso al texto completo de los libros ni se han reproducido sus ilustraciones.

## Arquitectura, SQL y operación

| Referencia oficial | Uso en el curso |
|---|---|
| [Databricks: Medallion architecture](https://docs.databricks.com/aws/en/lakehouse/medallion) | Patrón de capas con refinamiento progresivo. La ruta docente en GCS/BigQuery no implementa automáticamente todas las capacidades de un lakehouse |
| [datacharmer/test_db](https://github.com/datacharmer/test_db) | Origen del ejemplo `employees`, instalación y pruebas del dataset. MariaDB e importación se comprobarán antes de S2 |
| [GCP Free Trial](https://docs.cloud.google.com/free/docs/free-cloud-features) | Crédito de prueba US$300/90 días, elegibilidad y restricciones; separar Free Trial de Free Tier. Revisar qué servicios/modelos cubre |
| [Budgets and budget alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets) | Las alertas sirven para seguimiento; no confundirlas con un límite de gasto. La documentación también distingue otras modalidades de presupuesto según servicio |
| [BigQuery: estimate and control costs](https://docs.cloud.google.com/bigquery/docs/best-practices-costs) | Estimar bytes y acotar consultas; verificar limitaciones de fuentes externas. Enseñar que `LIMIT` no equivale a ahorrar escaneo |
| [BigQuery: Cloud Storage external tables](https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage) | Esquema, formato, permisos y ubicación compatible de bucket/dataset |
| [BigQuery: logical and materialized views](https://docs.cloud.google.com/bigquery/docs/logical-materialized-view-overview) | Elegir una vista lógica o una tabla para la base de Gold |
| [BigQuery: create materialized views](https://docs.cloud.google.com/bigquery/docs/materialized-views-create) | Restricciones de SQL de vistas incrementales, incluidas ventanas; no trasladar literalmente el ejemplo del syllabus |
| [Interfaz de prompts de GCP](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart) | El enlace de Vertex AI redirige al quickstart de Agent Studio al consultar. Verificar etiqueta real de consola, permisos y modelo antes de producir capturas |
| [RAG overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-overview) | El enlace redirige a la documentación de RAG Engine en Gemini Enterprise Agent Platform. Se usa para aclarar el patrón; no se exige desplegar ese producto en Especialidad |

No se fijaron tarifas, nombres de modelos ni rutas de botones de una interfaz que todavía no se ha ensayado con la cuenta de clase. Los laboratorios finales deberán incluir esos detalles y fecha de prueba.

## Fichas iniciales de casos externos

### Mercado Libre — analítica consumible

- **Fuente:** [How Mercado Libre Builds Upon a Continuous Intelligence Ecosystem with BigQuery and Looker](https://cloud.google.com/blog/products/data-analytics/improving-retail-using-bigquery-and-looker), 2022-04-08.
- **Autor:** Jorge Vidaurre, Technical Leader, Data & Analytics, Mercado Libre, en Google Cloud Blog.
- **Qué respalda:** uso conjunto de BigQuery y Looker dentro de su ecosistema de analítica.
- **Aplicación didáctica:** S1/S3/S6, del almacenamiento al consumo de evidencia.
- **Límite:** Looker no es Looker Studio; no atribuir al caso un diseño Medallion ni resultados de rentabilidad que no se hayan verificado.

### Carrefour — compartir con gobierno

- **Fuente:** [Privacy-preserving data sharing now generally available with BigQuery data clean rooms](https://cloud.google.com/blog/products/data-analytics/bigquery-data-clean-rooms-now-generally-available), 2024-04-05.
- **Publicador:** Google Cloud; incluye testimonio de Guillaume Blaquiere, Group Data Architect de Carrefour.
- **Qué respalda:** experiencia reportada de colaboración de datos con controles de protección.
- **Aplicación didáctica:** S4/S5, qué contratos, responsables y restricciones hacen falta antes de compartir.
- **Límite:** un testimonio de proveedor no constituye una auditoría independiente; Especialidad no despliega una clean room.

### UPS Capital — decisiones apoyadas por analítica y modelos

- **Fuente:** [UPS leverages BigQuery and Striim for AI-secured package delivery](https://cloud.google.com/blog/products/data-analytics/ups-leverages-bigquery-and-striim-for-ai-secured-package-delivery), 2024-05-22.
- **Autores:** Pinaki Mitra (UPS Capital) y Alok Pareek (Striim), en Google Cloud Blog.
- **Qué respalda:** integración reportada de datos/analítica/modelos para riesgo en entregas.
- **Aplicación didáctica:** S1/S7, relacionar latencia y herramientas con la decisión que se quiere mejorar.
- **Límite:** no demostrar RAG ni trasladar beneficios al caso de precios; separar predicción y generación de texto.

### Carrefour — trabajo generativo

- **Fuente:** [Real-world gen AI use cases from the world's leading organizations](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders), página consultada con fecha editorial 2026-04-22, sección de agentes creativos.
- **Publicador:** Google Cloud; recopilación dinámica, no ficha técnica exhaustiva.
- **Qué respalda:** uso reportado de Vertex AI para Carrefour Marketing Studio y creación de campañas.
- **Aplicación didáctica:** S7, distinguir automatización de contenido, análisis cuantitativo y validación humana.
- **Límite:** buscar una ficha técnica más profunda durante producción si se quieren cifras de impacto o decisiones de arquitectura. No convertir el plazo de despliegue reportado en evidencia de ROI.

## Procedencia de snapshots

| Archivo | SHA-256 |
|---|---|
| `syllabus-fuente.md` | `52d357cfc11a54d73274094682d00d09a7f2e679194daf939346915ba132708f` |
| `metadata-drive.snapshot.json` | `568f299dbf43dceebc08d98fc5a766977e7c0d563a6e785190679076ffc4be4e` |

Los timestamps del catálogo corresponden a los activos registrados; la fecha de este snapshot es la de consulta. El catálogo contiene un registro de otro `metadata.json`: el ID de descarga correcto está registrado arriba.

## Consulta para el piloto local

El 2026-11-05 se volvieron a consultar el artículo de Mercado Libre y la guía de presupuestos de esta lista. Se añadió [gcloud config get](https://docs.cloud.google.com/sdk/gcloud/reference/config/get), documentación actual del comando de lectura `gcloud config get project`, utilizado en el piloto. El shell anterior del repo usa `get-value`; se conserva sin editar. La guía del piloto distingue lectura de configuración de creación manual de presupuesto. No constituye un ensayo en la cuenta GCP de clase.

## Ampliación del guion de Especialidad · 2026-11-05

- [HSBC Risk Advisory Tool](https://cloud.google.com/customers/hsbc-risk-advisory-tool): caso de proveedor sobre decisiones de riesgo con Cloud Storage, Dataflow y BigQuery. Uso: tarjeta sectorial S1 y diseño S3. No trasladar beneficios al proyecto ni exigir modelos financieros.
- [Mayo Clinic: plataforma de datos con BigQuery y Variant Transforms](https://cloud.google.com/blog/products/data-analytics/genome-data-analytics-with-google-cloud), 2020-08-13: caso histórico de datos genómicos, almacenamiento y control de acceso. Uso: sectores S1/gobierno S4; no enseñar APIs históricas como instrucciones actuales ni usar datos clínicos de personas en clase.
- [Comisión Europea: principios del GDPR](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en): finalidad, minimización y responsabilidad como conceptos de gobierno; no se afirma aplicación automática a cualquier dataset del curso.
- [HHS: entidades cubiertas y business associates](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html): delimita el contexto de HIPAA. Uso conceptual S4; no presentar cloud como certificación automática de cumplimiento.
- [Conexión de BI con BigQuery](https://docs.cloud.google.com/looker/docs/studio/connect-to-google-bigquery): al consultar redirige a documentación bajo Data Studio. Mantener la referencia de Looker Studio del syllabus y verificar etiqueta/UI de la cuenta antes de producir la guía de S6.

Los datasets candidatos de proyectos diversos se apoyan en el inventario preservado, no en una nueva inspección de filas. Sus preguntas/KPIs son propuestas sujetas a perfilado. ML en Especialidad queda en distinción conceptual breve; no hay práctica ni evaluación de entrenamiento o predicción.

## Producción de S1 · 2026-11-05

Se consultaron [creación de proyectos](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects), [creación de buckets](https://docs.cloud.google.com/storage/docs/creating-buckets), prueba GCP y presupuestos para completar la guía de seis pasos. Las instrucciones no se ejecutaron en una cuenta cloud durante este corte. `presentaciones-v2/especialidad-01/catalogo-candidatos.json` conserva ocho entradas seleccionadas del snapshot original, con sus campos sin reinterpretar. El formulario del proyecto no asigna ni valida esas fuentes.

## Producción de S2–S8 · 2026-11-05

Se consultaron las referencias oficiales de tablas externas, scripts GoogleSQL, vistas materializadas, conector BigQuery/BI, interfaz de prompts GCP, RAG y contextos GDPR/HIPAA ya enlazadas en este registro. Las fichas de casos mantienen referencias directas en las slides pertinentes y las guías. No se incorporan cifras nuevas de ROI ni se presenta cumplimiento normativo como consecuencia automática de usar cloud.

`presentaciones-v2/recursos/precios-ilustrativos.csv` y su corpus son material original docente con resultados esperados comprobados localmente. No derivan de filas del Drive ni de una ejecución de LLM. SQLglot se usó como comprobación estática auxiliar; la ejecución cloud y MariaDB real siguen pendientes. La búsqueda de S7 es local por términos con IDs explícitos, sin modelos/embeddings ni generación automática.

## Revisión editorial S1–S3 · 2026-11-05

- Syllabus prioritario: `~/Documents/syllabus_especialidad.md`, preservado sin modificaciones en `syllabus-especialidad-fuente.md`. SHA256: `5dfdee5b827a4d46cb0429f1aabf323443957668a95f90fb3baf761b0cd0d95d`. Documenta Especialidad; mantiene diferencias internas entre orden de módulos y prácticas, resueltas explícitamente en la propuesta editorial.
- Kit suministrado: `~/Downloads/chema_id_kit.zip`. Leídos README, voz, referentes, storytelling, visualizacion, presentaciones, voz-y-delivery, CSS y tokens. Se preservaron textos pertinentes en `identidad-chema/`; imagen firma y fuentes en `presentaciones-v2/identidad/`. La firma proviene del kit; no se generó ni buscó una imagen que pudiera confundirse con datos del curso.
- [Aula publicada](https://bigdata-up.web.app/): índice, app y decks.json consultados. Recuperados ejemplos de restricciones, reparto, historial/joins y LIMIT. No se copiaron afirmaciones cuantitativas sin respaldo ni se modificó el sitio.
- [Índice vigente de León Palafox](https://www.leonpalafox.com/courses/deep-learning/): la ruta `/slides/deep-learning/` devuelve404; las clases sí responden. [Introducción](https://www.leonpalafox.com/slides/deep-learning/class-01-introduccion.html) y [CNN](https://www.leonpalafox.com/slides/deep-learning/class-02-redes-convolucionales.html) revisadas como referencia de composición y mecanismos. Introducción inspeccionada en Chromium. No se copió código, contenido ni identidad.
- Casos Mercado Libre, HSBC, Mayo Clinic y UPS Capital reutilizan las referencias registradas arriba. Las figuras son esquemas didácticos, no reproducciones completas de sus arquitecturas; las conclusiones de transferencia se identifican como interpretación docente.
- Tipografías Google Fonts y licencias OFL descargadas para presentación offline. No hay API, analítica de uso ni servicio externo necesario para reproducir los decks.


## Sesión4 · verificación de fuentes · 2026-11-05

- [SAFE_CAST](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting): conversión con NULL ante error de ejecución; no corrige contenido ni evita toda incompatibilidad estática.
- [Particiones](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables): filtro elegible permite pruning; el fixture pequeño no demuestra ahorro.
- [Comisión Europea](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en) y [HHS](https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html): principios GDPR y alcance HIPAA contextual; sin diagnóstico legal del proyecto.
- [Carrefour, publicación Google Cloud2024](https://cloud.google.com/blog/products/data-analytics/bigquery-data-clean-rooms-now-generally-available): testimonio de colaboración/protección, sin ROI cuantificado ni garantía para el laboratorio. Diagramas propios conceptuales.


## S5 · Gold

Consultados GoogleSQL ROW_NUMBER y BigQuery materialized-views-create (enlaces en las slides). Uso: interpretar selección y advertir que soporte de materialización depende de modalidad/consulta. Caso Mercado Libre reutiliza fuente2022 ya registrada, sin atribuirle nuestro modelo ni ROI. Dataset de precios sigue siendo fixture ficticio.


### S6 · consulta del 2026-11-05

- [Conector BigQuery](https://docs.cloud.google.com/data-studio/connect-to-google-bigquery): selección de proyecto/dataset/tabla, facturación y permisos según credenciales. La ruta anterior de Looker Studio redirige a Data Studio; conservar referencia al nombre utilizado en el syllabus. Verificar interfaz antes de impartir.
- [Cole Nussbaumer Knaflic: so what?](https://www.storytellingwithdata.com/blog/2017/3/22/so-what): títulos con mensaje y atención orientada al hallazgo. Aplicación docente propia, sin copiar gráficos.
- Caso Mercado Libre: se reutiliza la fuente documentada en S5; BigQuery y Looker. La transferencia pedagógica sobre audiencia es interpretación docente, sin atribuir el prototipo del curso a la empresa.


### S7 · consulta del 2026-11-05

- [Google Cloud, prompts en Studio](https://docs.cloud.google.com/gemini-enterprise-agent-platform/agent-studio/quickstart): referencia vigente de interfaz, modelo y envío; la guía conserva el nombre Vertex AI Studio del syllabus. No se fija un modelo ni precio sin verificar la cuenta. Ruta documentada Studio > New > Chat > New chat. Revisar Settings / Detect build intent para evitar evaluaciones adicionales de construcción que no requiere el curso.
- [Google Cloud, RAG](https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/rag-engine/rag-overview): patrón de recuperación y generación. El curso usa búsqueda local por términos y transferencia humana; no despliega RAG Engine ni infraestructura vectorial.
- [Casos de Google Cloud: Carrefour Marketing Studio](https://cloud.google.com/transform/101-real-world-generative-ai-use-cases-from-industry-leaders): uso reportado de Vertex AI para campañas. Se omiten cifras promocionales; la revisión del borrador es aplicación pedagógica propia, no un resultado atribuido al caso.
