# Primera revisión editorial · Especialidad S1–S3

Propuesta implementada localmente para revisión; no aprobación pedagógica ni validación cloud. Rama plan3. Fuente curricular prioritaria: [syllabus de Especialidad preservado](syllabus-especialidad-fuente.md), suministrado después del syllabus general. El curso es de ocho sesiones de tres horas; este corte cambia únicamente las primeras tres presentaciones y alinea sus guías.

## El cambio de enfoque

La primera versión tenía contenido suficiente pero convertía casi todas las ideas en dos paneles. El rediseño empieza por lo que la audiencia debe decidir. Una pantalla muestra una comparación, una relación o una acción; la voz explica el matiz y la guía conserva instrucciones extensas. La cantidad de pantallas responde al relato: S1 tiene 27, S2 tiene 28 y S3 tiene 26.

Identidad aplicada desde `~/Downloads/chema_id_kit.zip`: papel #f6f4ef, tinta #14213d, azul #1b3a6b y señal #d62839; variantes oscuras del mismo kit. Source Serif 4 para títulos, IBM Plex Sans para lectura e IBM Plex Mono para código/cifras, alojadas localmente con sus licencias. Imagen firma de Mandelbrot del kit en la apertura; diagramas propios editables para enseñar mecanismos. No hacen falta imágenes generadas para sustituir una relación que conviene dibujar.

El kit propone menos de 25 palabras por slide: se aplica como objetivo de síntesis para enunciados y aperturas, con excepciones explícitas para SQL, tablas, etiquetas de diagramas y comprobaciones de laboratorio. La legibilidad se verifica en proyector; no se reduce el tamaño para hacer caber prosa. No se fuerza el mismo número de palabras ni el mismo número de slides por sesión.

## Arcos narrativos

| Sesión | Gran idea | Tensión y giro | Acción final |
|---|---|---|---|
| 1. Una compra merece evidencia | Una decisión defendible permite recorrer la evidencia hasta su fuente. | Votar entre arroz de 24 y 38 MXN; revelar peso y fecha. La comparación por kg cambia el orden y deja pendiente el periodo. | Formular una decisión propia y comprobar proyecto, presupuesto y bucket. |
| 2. Una consulta también puede contar mal | SQL conserva la pregunta cuando se define grano, población y vigencia. | Tres filas salariales parecen tres empleados. La unión revela que se trata de una persona con historia. | Entregar consultas comentadas, control de cardinalidad y pregunta propia. |
| 3. El archivo debe sobrevivir a tus conclusiones | Conservar origen, versión y lectura permite revisar una decisión. | Un reporte corto oculta una lectura grande; una copia «arreglada» impide reconstruir qué llegó. | Bronze consultable, manifiesto y estadísticas observadas del job. |

Duarte aporta el contraste entre la situación actual y la posibilidad deseada; la audiencia decide antes del revelado. Knaflic aporta títulos que afirman algo, comparaciones con unidad y periodo, barras desde cero y etiquetas directas. Se retoma el dilema inicial al cerrar y se pide una acción concreta. No se reproducen diagramas ni texto de los libros.

## Correspondencia con el syllabus específico

| Contenido del syllabus | Tratamiento en estas sesiones |
|---|---|
| Módulo 1: Cloud y aprovisionamiento | S1: responsabilidades, GCP, crédito, proyecto, presupuesto, GCS. |
| Warehouse, lake y lakehouse | S1: garantías y elección; evitar afirmar que el laboratorio implementa un lakehouse completo. |
| Banca, retail, salud y logística | S1: Mercado Libre y casos HSBC, Mayo Clinic, UPS Capital; fuentes al pie y límites en notas. |
| Módulo 2: SQL y BigQuery | S2: SQL Fast Track en MariaDB/ employees; S3: lectura externa y motor distribuido de BigQuery. |
| Módulo 3: ETL/ELT y Medallion | S1 presenta el mapa; S3 explica ETL/ELT e implementa Bronze. Silver y Gold siguen en S4/S5. |
| Gobierno, calidad, privacidad | S1: responsables; S3: contrato, procedencia, permisos y conservación. S4 profundiza gobierno y contexto regulatorio. |
| Módulo 4: BI, LLM, RAG, ML conceptual | Se conserva en S6/S7. No se adelanta entrenamiento ni código de ML. |
| Entregables finales | Arquitectura/gobierno, SQL sobre fuente propia y dashboard; GenAI como complemento revisado. |

El documento nuevo tiene una diferencia interna: el módulo de SQL precede a arquitectura, pero los laboratorios ponen Bronze en S2, Silver en S3 y SQL en S4. Se mantiene la adaptación ya acordada: **S1 entorno → S2 SQL → S3 Bronze → S4 Silver → S5 Gold → S6 BI → S7 GenAI → S8 defensa**. Enseñar SQL antes de CTAS permite comprender y comprobar las transformaciones. No se omiten Bronze ni Silver; se desplazan sus laboratorios.

La guía del syllabus propone un dataset retail compartido y la tabla de herramientas menciona Python/PySpark. Prevalecen las aclaraciones del usuario: **dataset distinto por equipo**, PROFECO solo como caso guiado, Especialidad con poco código. Las primeras tres sesiones no exigen Python ni Spark. ML sigue limitado a la distinción conceptual breve de S7. No se implementa la vista materializada con funciones de ventana del ejemplo del syllabus sin comprobar restricciones; Gold mantiene tabla analítica guiada.

## Ritmo y trabajo de clase

Cada sesión conserva 180 minutos: apertura15, conceptos30, demostración/casos20, pausa10, laboratorio55, transferencia al proyecto30, entrega/cierre20. Las notas llevan tiempos y preguntas antes de revelar. Los laboratorios mantienen pasos de 5+8+12+12+10+8 minutos con enlace profundo desde las slides.

- S1 alterna portada con imagen, recibos, barras, cifra con restricciones, dibujo de distribución, matriz de almacenamiento y arquitectura progresiva. La ficha editable vive fuera de la proyección para dar espacio a la discusión.
- S2 alterna miniaturas de tablas, consulta/salida, diagrama de llaves, demostración de filtro y conmutador INNER/LEFT. La interacción local muestra filas ficticias; ejecutar SQL real sigue ocurriendo en MariaDB.
- S3 usa mapa de objeto/tabla, ETL frente a ELT, muestras crudas, diagrama de acceso y modelo de lectura/salida. El botón LIMIT no pretende medir costos ni simular el optimizador.

Cada pantalla de práctica enseña una acción o una comprobación. El código completo continúa descargable. Las guías corrigen nombres de archivos de Bronze y sincronizan la distribución de Q1–Q6 con el deck.

## Qué se rescató de las referencias

Del sitio publicado `bigdata-up.web.app`, consultado mediante su `decks.json`: el contraste reporte mensual/alerta operativa; la analogía de documentos repartidos y trabajo desigual; el grano en SQL; el contraste de LIMIT con lectura. Se quitaron estadísticas globales sin valor para la decisión y frases que confundían cloud con una escala determinada. La comparación de tablas pequeñas se desarrolla en una demostración visible.

La URL de directorio de León devuelve 404. Su [índice vigente](https://www.leonpalafox.com/courses/deep-learning/) enlaza [Introducción](https://www.leonpalafox.com/slides/deep-learning/class-01-introduccion.html) y [CNN](https://www.leonpalafox.com/slides/deep-learning/class-02-redes-convolucionales.html). Se revisaron el HTML y la presentación en navegador: lienzo16:9, títulos amplios, diagramas, alternancia clara/oscura, navegación y revelado. Se toma esa disciplina espacial; no se copia identidad, contenido, logotipo universitario ni código del reproductor. Nuestro avance sigue siendo manual.

## Qué revisar al presentar

En el intro, detenerse tras la votación del arroz: ¿la sala propone normalizar antes de ver la gráfica? En SQL, ¿puede predecir las filas antes del filtro y el LEFT JOIN? En Bronze, ¿distingue bytes leídos de filas devueltas? Esas respuestas evalúan claridad mejor que contar animaciones.

Los decks y las guías están listos para revisión local. Siguen pendientes el ensayo con cuenta GCP/MariaDB de alumno, el perfilado de PROFECO y la preparación de paquetes reales distintos por equipo. El fixture demuestra el mecanismo, no hallazgos reales ni procesamiento masivo. No se publicó ni se cambió Firestore/Firebase.
