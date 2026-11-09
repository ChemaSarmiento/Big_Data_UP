# Checkpoints del rediseño del curso

## Estado para retomar

**Último corte:** 2026-11-05 · Rama plan3 · S1–S7 rediseñadas, 189 slides; curso 203. S7 GenAI lista para revisión local. S8 conserva base; validación cloud pendiente.

Leer, en este orden:

1. [AGENTS.md](AGENTS.md): alcance y reglas de continuidad.
2. [PLAN_ESPECIALIDAD.md](PLAN_ESPECIALIDAD.md): propuesta completa de 8×3 h.
   Complementar con [PROPUESTA_SLIDES_ESPECIALIDAD.md](PROPUESTA_SLIDES_ESPECIALIDAD.md) y [proyectos diversos](docs/rediseno-especialidad/proyectos-diversos.md): especificación vigente para producción.
3. [Diagnóstico](docs/rediseno-especialidad/diagnostico.md): evidencia sobre el material actual.
4. [Propuesta editorial S1–S3](docs/rediseno-especialidad/propuesta-editorial-s01-s03.md): relato, identidad y alineación curricular vigentes. El storyboard inicial es histórico.
5. [Fuentes](docs/rediseno-especialidad/fuentes.md): fuentes externas, snapshots y límites.

## Decisiones confirmadas por el usuario

- Dos tracks: Especialidad ejecutiva, poco código; Maestría técnica de ciencia de datos.
- 8 sesiones de 3 horas y proyecto integrador; ambos tracks usarán el crédito de US$300 de GCP.
- Trabajar Especialidad primero y Maestría después.
- Alineación con el syllabus moderno; arquitectura Medallion, grandes datos y posible integración de LLM.
- SQL para Especialidad con `employees` de datacharmer, en MariaDB sobre GCP, reutilizando el flujo docente existente.
- Slides HTML interactivas: clics, fades, diagramas, teoría, ejemplos, laboratorio guiado con código exacto y casos externos verificables.
- Aplicar principios de Cole Nussbaumer Knaflic y Nancy Duarte (*Resonate*).
- Secuencia de trabajo solicitada: **plan → revisión → producción de slides**.
- **Elección explícita:** PROFECO, precios y decisiones de compra, como caso **guiado** de Especialidad. **Aclaración posterior:** el proyecto final no usa los mismos datos para todos; cada equipo tendrá dataset distinto.
- **Alcance reiterado:** solo se desarrolla Especialidad. ML no es laboratorio ni entregable; el syllabus se cubre con una distinción conceptual breve entre predicción y generación.

## Propuestas que aún no están aprobadas como programa final

- Orden S1 arquitectura/setup; S2 SQL; S3 Bronze; S4 Silver; S5 Gold; S6 dashboard; S7 GenAI/RAG didáctico; S8 defensa.
- Canasta comparable como decisión central; zona, periodo, productos y reglas dependen del perfilado.
- Trabajo en equipos de 2–3; defensas de 7+3 min, hasta 10 equipos en la agenda propuesta.
- Rúbrica de 100 puntos; no se cambiaron ponderaciones institucionales.
- Objetivo operativo de costo inferior a US$60 por equipo/proyecto, pendiente cotización/ensayo; no es garantía ni tope automático.
- Fuentes v2 aisladas y piloto HTML de 8–12 slides antes de producir el conjunto completo.

## CP-001 — Revisión y plan inicial

**Completado en este corte:**

- Lectura del syllabus local, preservado sin editar en `docs/rediseno-especialidad/syllabus-fuente.md`.
- Revisión del mapa actual, código del constructor/reproductor y configuración Hosting/Firestore.
- Inventario y extracción de texto de siete PPTX / 216 slides del ZIP. No se inspeccionaron visualmente todas sus páginas.
- Consulta pública del Drive; archivo encontrado: **`metadata.json`**, no `metadatos.json`. Snapshot de 255 entradas preservado en `docs/rediseno-especialidad/metadata-drive.snapshot.json`.
- Comprobación del sitio publicado: 25 decks/602 slides al consultar. Chromium abrió catálogo y slide Medallion sin errores JS en esas páginas; capturas revisadas visualmente. No es una validación exhaustiva del sitio.
- Revisión de los shells MariaDB: instalación automatizada; carga de `employees` separada; configuración de acceso didáctica explícita en el repo. Sin modificación de infraestructura.
- Fuentes oficiales y casos externos consultados; límites registrados en `fuentes.md`.
- Creación de `AGENTS.md`, plan, diagnóstico, storyboard, fuentes y este registro.

**Hallazgos que no se deben perder:**

- Especialidad actual tiene 9 sesiones + nivelación; no cabe sin rediseño en el nuevo límite.
- El reproductor actual elimina `v-click` al construir y revela por tiempo; clic cambia de slide. La nueva interacción requiere estados de pasos y protección de controles/código.
- El catálogo Drive no trae columnas ni licencias y tiene descripciones/categorías genéricas. `all_data.csv` ~19 GB es candidato confirmado, pero falta validar filas y cobertura.
- PROFECO aporta precios, no ventas. No reutilizar KPIs del syllabus de e-commerce sin adaptar su semántica.
- Medallion sobre GCS/BigQuery no prueba una implementación completa de lakehouse.
- Gold debe empezar con CTAS/vista lógica; no asumir soporte de ventanas en vistas materializadas incrementales.
- CSV + prompt no equivale a RAG; Especialidad tendrá recuperación visible de evidencia en una demo acotada.
- La URL `web.app` corresponde a Firebase Hosting. Firestore pertenece al reto SQL, no al almacenamiento necesario de slides.
- El requisito ≥15 GB aparece en material anterior, no ha sido reconfirmado como condición del programa nuevo.

**Verificación del corte realizada:** enlaces relativos locales resueltos; catálogo JSON de 255 entradas válido; snapshots idénticos a las fuentes consultadas; agendas suman 180 minutos y rúbrica suma 100 puntos; `git diff --check` sin errores. Los seis archivos previamente modificados conservan sus conteos de diff y no fueron editados por este corte. No se ejecutaron tests de Spark/Airflow ni se reconstruyó el sitio por este cambio exclusivamente documental. No se ejecutaron laboratorios end-to-end en GCP.

## Cambios locales que ya existían al iniciar

No fueron creados ni modificados por este corte; conservarlos:

```text
 M especialidad/sesion-04/README.md
 M especialidad/sesion-04/slides.md
 M firebase.json
 M presentaciones/app.js
 M presentaciones/desarrollo/especialidad-04.md
 M slides_maestria/build-web.mjs
?? presentaciones/notebooks/
```

## Siguiente paso concreto

Abrir `http://localhost:4183/especialidad-01/` tras iniciar servidor sobre `presentaciones-v2`. Revisar primero apertura, gráfica del arroz y arquitectura; luego SQL y Bronze. Incorporar feedback antes de extender el rediseño a S4–S8. Ensayar después GCP/MariaDB con alumno y paquetes reales distintos. Estado vigente: **CP-008**; los cortes anteriores son historia.

No volver a preguntar si todos deben usar PROFECO ni producir Maestría en este alcance: PROFECO es ejemplo guiado, cada proyecto tiene otra fuente y el trabajo actual es exclusivamente Especialidad.

## CP-002 — Primer piloto local

**Petición:** «Hagamos entonces el primer piloto local».

**Implementado:**

- Ruta aislada `presentaciones-v2/piloto/`, sin build ni dependencias de red para presentar. No se modificó el sitio anterior ni Firebase.
- Diez pantallas seleccionadas del storyboard: dilema, contexto, paralelismo, almacenamiento/cómputo, OLTP/OLAP, Medallion, cobertura, Mercado Libre, paso de laboratorio y ficha de decisión.
- Revelado por clic, retroceso por paso, fades, movimiento reducido, enlaces `#slide/paso`, índice, pantalla completa y notas por pantalla.
- Dos interacciones de escenario, protección de selección/copia de código, formulario con persistencia local y descarga JSON.
- Guía extensa `laboratorio.html`, comando de solo lectura descargable, impresión de todos los revelados y adaptación móvil con scroll vertical.
- `verify.mjs` usa Playwright/Chromium ya instalado en `slides_maestria/`; artefactos en `/tmp/bigdata-plan3-piloto/`.

**Verificado:** recorrido automatizado de diez pantallas a 1440×900, 1280×720 y 390×844; sin errores JS ni solicitudes fallidas; sin desbordamiento horizontal ni scroll en las dos resoluciones de proyección. En móvil hay scroll vertical previsto. Se comprobaron pasos, retroceso, recarga, historial, controles aislados, selección de código, descargas shell/JSON, persistencia, índice, diálogos, movimiento reducido y visibilidad de todos los pasos al imprimir. Capturas de portada, Medallion y cobertura inspeccionadas; PDF exportado con diez páginas. Sintaxis JS/shell y recursos locales comprobados. El test detectó y se corrigió el avance al limpiar una selección de texto.

**Límites:** no se perfiló `all_data.csv`; los precios/coberturas son ilustrativos. No se ejecutó el comando gcloud en una cuenta, ni se verificó creación de presupuesto o llegada de correo. El paso está contrastado con documentación. No se crearon recursos, publicaron slides, hicieron commits ni push. La guía de Sites se aplicó en su modalidad local.

**Para retomar:** desde la raíz ejecutar `python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2/piloto` y abrir `http://localhost:4183`. Para QA, ejecutar `node presentaciones-v2/piloto/verify.mjs` con el servidor en marcha. Revisar ritmo, tamaño de letra y cantidad de teoría con el usuario; luego perfilar datos y completar S1–S2.

## Pendientes que requieren información o ensayo

- Cantidad de alumnos/equipos, acceso y elegibilidad de créditos.
- Vigencia de evaluación institucional y mínimo de volumen heredado.
- Capacidad de la VM MariaDB para conexiones simultáneas y carga previa de `employees`.
- Esquema real de PROFECO, permiso para reutilizarlo y periodo con canasta completa.
- Región, disponibilidad de modelo/interfaz GCP y presupuesto medido.
- Casos externos: profundizar fichas donde se necesiten métricas. Para Duarte usar la página oficial de *Resonate* y el artículo vigente registrados en `fuentes.md`, evitando citas de extractos antiguos que hoy redirigen.

## CP-003 — Guiones completos de Especialidad y diversidad de proyectos

**Petición:** proponer las slides y laboratorios considerando el syllabus, tras valoración positiva del piloto. Durante el trabajo el usuario aclaró que los datasets del proyecto final deben ser distintos y reiteró que solo estamos haciendo Especialidad.

**Resultado documental:** `PROPUESTA_SLIDES_ESPECIALIDAD.md` v0.3, ocho guiones en `docs/rediseno-especialidad/sesiones/01.md`–`08.md` y `proyectos-diversos.md`. Son 210 slides propuestas (28×7 + 14), no decks implementados. S1–S7 tienen laboratorio de 55 min y transferencia de 30 min al proyecto propio; S8 tiene agenda de defensa/auditoría/cierre de 180 min.

**Decisiones actuales:** PROFECO para explicar en clase; employees para SQL; un origen/dataset distinto por equipo para el proyecto. No confundir otro formato/filtro del mismo archivo con un nuevo origen. Catálogo de candidatos pendiente de perfilado/asignación; no prometer diversidad validada por contar nombres de archivos. El docente entrega paquetes de datos y SQL base, no traslada preparación de ingeniería al ejecutivo.

**ML revisado:** 10 min conceptuales del syllabus en S7 para distinguir describir/predecir/generar y responsabilidad. Sin entrenamiento, código de modelos, métricas técnicas, predicción obligatoria ni puntos de ML. Práctica de IA: GenAI, evidencia, verificación y demostración asistida de recuperación/generación con paso humano explícito. No se trabajó el programa de Maestría.

**Archivos de continuidad actualizados:** `AGENTS.md`, `PLAN_ESPECIALIDAD.md`, este registro y `fuentes.md`. Los slides piloto y los snapshots fuente permanecen intactos. Se añadieron referencias oficiales para banca/salud, privacidad y BI.

**Verificación documental:** enlaces relativos resueltos; ocho guiones con 210 IDs únicos y consecutivos; laboratorios de S1–S7 suman 55 min; agendas de clase y defensa suman 180 min. `git diff --check` sin errores y los seis archivos previamente modificados mantienen sus conteos de diff. No se ejecutó build ni se probaron labs cloud por este corte de propuesta.

**Siguiente producción recomendada:** S1 completa usando el piloto; S2 con SQL probado en MariaDB; preparación de paquetes distintos antes de S3. Antes de cerrar la asignación, conocer tamaño del grupo y confirmar viabilidad/origen/permisos de cada paquete. La propuesta es revisable y no altera ponderación institucional ni publica recursos.

## CP-004 — Deck completo de Especialidad S1

**Petición:** «genera el primer deck para revisar localmente».

**Implementado:** `presentaciones-v2/especialidad-01/` con 28 slides E01-01…E01-28, seis pasos de laboratorio, notas por slide, guía HTML imprimible, plantilla H1 y extracto real de ocho registros del inventario. Reutiliza la dirección visual del piloto sin modificar su ruta. Estilos base copiados a `presentaciones-v2/compartido/base.css`; ajustes específicos y reproductor independientes para S1.

**Alcance:** cinco V, escala/paralelismo, cloud, OLTP/OLAP, warehouse/lake/lakehouse, Medallion, batch/streaming conceptual, casos externos, preparación GCP y transferencia al dataset propio. Formulario de slide 24 guarda/exporta una fuente candidata, audiencia y evidencia; no reserva ni valida asignaciones. No hay entrenamiento ni entregable ML. Las instrucciones de GCP requieren acciones manuales del alumno; el sitio no crea recursos.

**Verificado:** Chromium recorrió las 28 slides completamente reveladas a 1440×900, 1280×720 y 390×844; sin errores JS/solicitudes fallidas ni overflow horizontal. Sin scroll en las dos vistas de proyección; scroll vertical previsto en móvil. Navegación, pasos, retroceso, teclado después de controles, selección/teclado en código, persistencia/dataset propio, descargas, índice/notas/guía, historial/recarga y movimiento reducido comprobados. PDF A4 horizontal de 28 páginas generado; capturas de arquitectura, casos, formulario y móvil inspeccionadas. Sintaxis JS/shell y recursos locales comprobados. Artefactos: `/tmp/bigdata-plan3-sesion01/`. Script reproducible: `presentaciones-v2/especialidad-01/verify.mjs`.

**Para revisar:** desde raíz, `python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2`; abrir `http://localhost:4183/especialidad-01/`. Servir la carpeta padre, porque la base CSS está en `compartido/`. El servidor de QA se detiene al terminar; el README explica cómo iniciarlo. También funciona `index.html` bajo `file://`, con posibles restricciones del navegador para copiar/guardar.

**Límites y siguiente paso:** no se ejecutaron recursos GCP, no se validó la guía con cuenta de alumno ni se perfiló PROFECO. No hay publicación, commit o push. Revisar S1 con el usuario; incorporar sus ajustes y luego producir S2 con SQL probado y MariaDB preparada. El material anterior y sus seis diffs locales permanecen preservados.

## CP-005 — Curso local completo de Especialidad

**Petición:** «genera todas las sesiones», dentro del alcance vigente de Especialidad. Se conservaron S1 y piloto; se implementaron S2–S8 y un catálogo local de ocho sesiones.

**Resultado:** 210 slides (28×7 + 14), guías completas, notas, entregables, fuentes y descargas. Código/datos de apoyo en `presentaciones-v2/recursos/`; contenido editorial explícito por sesión en `contenido.json`; generación con `scripts/build.py`, índice con `scripts/catalogo.py`. `README.md` de esa carpeta explica uso y límites. Solo Especialidad; sin entrenamiento ni entregable ML. Cada equipo conserva un dataset propio distinto para el proyecto, con adaptación docente de su esquema y KPIs.

**Material ilustrativo:** CSV y manifiesto de precios creado para el curso, no filas del Drive. 16 de entrada = una copia exacta + dos rechazadas + 13 válidas. Gold: A150/B160 completas; C54 es subtotal de 3/5, costo completo desconocido. SQL separado de MariaDB para employees y GoogleSQL para Bronze/Silver/Gold/BI. Scripts curso_* con escritura explícita, sin ejecutarlos en GCP. Se proporcionan matriz de gobierno, diccionario KPI, wireframe, prompt, corpus de fichas, auditorías, plantilla de defensa y rúbrica.

**Interacción:** revelado/fades y teclado; demo INNER/LEFT con persona sin coincidencia, historial de salario, reconciliación, filtro de cobertura, recuperación por términos con fichas/IDs, reloj de defensa manual y registros H2–H8 con persistencia local/descarga. Recuperación y generación son pasos separados con traspaso humano; no se afirma un RAG automático. La respuesta de contingencia está marcada como texto docente escrito a mano, no salida real de un modelo.

**Verificado:** `scripts/verify-course.mjs` recorrió las 210 slides a 1440×900, 1280×720 y 390×844; cero errores JS, solicitudes fallidas y overflow horizontal; sin scroll de proyección. Comprobó catálogo, pasos, índice/notas/guías, movimiento reducido, descargas/persistencia e interacciones. Ocho PDFs exportados con páginas correctas (28×7+14); capturas de catálogo, SQL, Gold y recuperación inspeccionadas. Artefactos en `/tmp/bigdata-plan3-curso/`.

`scripts/verify-resources.py` validó checksum/conteos del fixture, resultados Gold esperados, rúbrica100 y ejecutó las SELECT de employees contra una base reducida SQLite. Esto no equivale a una prueba en MariaDB real. Se revisó sintaxis estática GoogleSQL con sqlglot 30.29.0 en `/tmp/bigdata-sql-validation`, separando el DDL dinámico de EXECUTE IMMEDIATE; no ejecuta ni garantiza los scripts en BigQuery. Enlaces/IDs/recursos de los 20 HTML revisados, y diff sin errores de formato.

**Para abrir:** servidor desde raíz con `python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2`; URL `http://localhost:4183/`. La prueba detiene su servidor al terminar; volver a iniciarlo para revisar. No se alteró Firebase ni se publicaron sitios, crearon recursos, hicieron commits o push.

**Pendiente real:** ensayo GCP y MariaDB con identidad de alumno; región/cuotas/costos; conexión/acceso BI; modelo e interfaz GenAI; perfilado/procedencia/licencia de fuentes grandes y paquetes distintos por equipo. El fixture demuestra el mecanismo, no procesamiento masivo ni hallazgos sobre PROFECO. Próximo paso: revisión editorial del usuario y ensayo de laboratorios con los datos/cuentas reales.

## CP-006 — Revisión editorial de las primeras tres sesiones · 2026-11-05

**Petición:** superar estructura repetida y peso de texto del lote inicial; revisar intro, syllabus exclusivo de Especialidad y kit chema_id_kit.zip; inspirarse en el aula publicada y decks de León Palafox; producir S1–S3.

**Fuentes revisadas:** syllabus_especialidad.md preservado exacto, kit de voz/storytelling/visualización/presentaciones/tokens; decks.json del sitio publicado; clases HTML de León localizadas desde /courses/deep-learning/ porque el directorio indicado devuelve404. Se inspeccionó Introducción en Chromium. No se copió su código o identidad. Kit textual preservado en docs/rediseno-especialidad/identidad-chema; imagen firma y fuentes locales con OFL en presentaciones-v2/identidad.

**Decisiones:** audiencia decide antes del revelado, títulos con mensaje, una idea por pantalla, alternancia de composición y fondos, una atención cromática principal. Se mantiene SQL S2 como prerrequisito de Bronze S3/Silver S4, explicando la diferencia interna entre módulos y labs del syllabus. PROFECO guiado; dataset distinto por equipo; ML conceptual acotado, nada de Maestría. La implementación es propuesta para revisión, no aprobación final.

**Implementado:** S1 27 slides (dilema del arroz, unidad/fecha, escala y arquitectura, casos externos y entorno); S2 28 (grano, filtro, agrupación, vigencia, INNER/LEFT y labs Q1–Q6); S3 26 (origen, ETL/ELT, externa/nativa, esquema, acceso y lectura/costo). Total81 nuevas; curso207. Composiciones específicas, diagramas SVG/HTML progresivos, gráfica desde cero, preguntas con interacción manual, guion hablado con tiempos y pausas, PDFs16:9. Ficha H1 fuera del lienzo, persistente y descargable. Fuentes font locales para presentar sin red.

**Archivos:** editorial/guion.py fuente única de slides/notas S1–S3; editorial.css e interacciones.js; scripts/build-editorial.py. build.py preserva esos decks/notas/README y continúa generando guías desde JSON; se alinearon pasos Q1–Q6, nombres de archivos Bronze, etapa externa/materialización y evidencia de escala. S1 guía directa enlaza ficha-proyecto.html. Catálogo/manifest dinámicos para conteos nuevos. Se actualizaron AGENTS, plan, propuesta, guiones documentales, fuentes y README. No se cambió la narrativa de S4–S8.

**Verificación:** verify-editorial.mjs recorrió81 slides a1440×900,1280×720,390×844. Cero errores JS/requests, recortes, overflow, superposiciones con fuentes y fallos de contraste oscuro comprobados. Verificó revelado/retroceso/recarga, índice/notas/lab, selección de código, filtro2/4 filas, INNER1/LEFT2, LIMIT1/10, fade manual/movimiento reducido, ficha H1 persistente/descarga y guías. PDFs27/28/26 páginas confirmados, formato16:9; texto del diagrama Medallion presente al imprimir. Capturas inspeccionadas de apertura, gráfico, arquitectura, SQL, Bronze y móvil. Se corrigieron contraste heredado y colisión entre clases de layout y componentes. Un detector de vacío se ajustó porque no reconocía texto en diagramas/listas; el recorrido final pasa.

**Regresión:** verify-course.mjs ahora cubre S4–S8:126 slides, mismas tres resoluciones y prácticas; cero errores o desbordes. verify-resources.py conserva checksum,16/1/2/13,Gold150/160/54 y SQL común sobre fixture SQLite.21 HTML revisados: IDs únicos y referencias locales válidas. git diff --check pasa. Los seis archivos sucios previos mantienen sus conteos de diff; no hubo commit, push, deploy ni acciones cloud.

**Artefactos:** /tmp/bigdata-editorial/ contiene capturas, report.json, sesion-1/2/3-editorial.pdf y sesiones-01-03-editorial.zip. Regresión S4–S8 en /tmp/bigdata-plan3-curso/. Servidor de QA se detiene al terminar. Para revisar: `python3 -m http.server 4183 --bind 127.0.0.1 --directory presentaciones-v2`, abrir /especialidad-01/.

**Límites:** efectividad pedagógica pendiente de ensayo con audiencia y revisión del usuario. No se perfiló PROFECO ni se validaron consultas en GCP/MariaDB real. Los controles locales no demuestran costos, permisos ni escala. Las simulaciones están marcadas como ficticias/conceptuales y los casos atribuidos a sus publicadores.

## Plantilla para siguientes checkpoints

```text
CP-00N — Nombre y fecha
Objetivo:
Decisiones confirmadas / propuestas:
Archivos y cambios:
Verificación ejecutada y resultados:
Límites o bloqueos concretos:
Próximo paso:
```


## CP-007 — Sesión 4: Silver y gobierno · 2026-11-05

Petición: «genera slides 4». Implementadas27 slides con identidad y narrativa de las tres anteriores. Un precio0 abre el dilema; regla explícita, exclusión y cobertura conducen al cierre. Interacciones de precio, reconciliación16=13+2+1 y particiones. Caso Carrefour2024; GDPR/HIPAA como contexto, fuentes oficiales verificadas. SQL completo existente se conserva; guía sincronizada con seis pasos5/8/12/12/10/8 minutos y transferencia al dataset distinto de cada equipo.

Fuente: editorial/guion.py SESSIONS[4], silver.js y estilos específicos. build.py preserva ahora S1–S4; build-editorial genera esas cuatro; catálogo cuenta206. Guion documental actualizado en sesiones/04.md. HTML de S1–S3 comprobado idéntico al inicio. Recursos/SQL no modificados; validación local del fixture pasa, sin ejecución GCP.

QA en verify-editorial.mjs extendido a S4: recorrido de108 slides en proyector y móvil, interacciones y PDFs. Se corrigió el ancho de la tabla de reglas en móvil. Artefactos /tmp/bigdata-editorial/, PDF sesion-4-editorial.pdf. Se reutilizó servidor ya activo en4183; no se detiene porque no fue iniciado en este turno. Sin publicación, commit ni provisión cloud. Próximo paso: revisar sesión4 y después abordar Gold.


## CP-008 — Sesión5: Gold · 2026-11-05

Petición: «haz la5».27 slides con relato del subtotal54 frente a canastas completas150/160. Catálogo, grano, dimensiones/hechos, selección temporal, LEFT JOIN, cobertura, NULL, cardinalidad y diccionario KPI. Caso Mercado Libre contextual; vistas materializadas explicadas sin prometer compatibilidad de toda ventana.

Interacciones: elegibilidad de canasta y unión que conserva p4/p5 ausentes. Fuente editorial guion.py SESSIONS[5], gold.js; build general preserva S1–S5. Guía JSON alineada a seis pasos, script06_gold completo y control07 descargable. SQL original sin cambios. Plantillas y esquema propio dependen del paquete docente, sin imponer canastas a todos.

QA: verify-editorial extendido a135 slides, tres tamaños e interacciones S5; PDF en /tmp/bigdata-editorial/sesion-5-editorial.pdf. Recursos ficticios validados localmente. Servidor4183 preexistente reutilizado, no se detiene. No ejecución GCP, publicación ni commit. Próximo paso: revisión de Gold y después visualización S6.

## CP-009 — Sesión 6: visualización ejecutiva · 2026-11-05

Petición: «sigue», continuidad después de S5. Se rediseña S6 con 27 slides / 180 min: tensión del subtotal presentado como mejor compra, audiencia, jerarquía, barras desde cero, agregación, filtros, estados sin evidencia, acceso y costos. Caso Mercado Libre contextualizado. Laboratorio de seis pasos / 55 min y transferencia al dataset distinto de cada equipo.

Fuente: editorial/guion.py SESSIONS[6], bi.js y bi.css. Práctica independiente especialidad-06/practica.html generada desde el mismo tablero. Filtro Todas/A/B/C actualiza titular, menor costo completo y denominador; C conserva costo desconocido. Antes/después corrige la afirmación engañosa. Guía de BI distingue fuentes canastas/detalle y controles separados; no presupone sincronización automática. Título descriptivo o escenario bloqueado en BI, sin prometer automatización equivalente al prototipo local.

Build preserva decks editoriales S1–S6; genéricos S7–S8. Total 204 slides, 162 editoriales. Guion documental, catálogo, AGENTS, plan y fuentes actualizados. QA Chromium: 162 slides a 1440×900,1280×720,390×844, sin errores de consola/red ni recortes; interacciones S6 y práctica independiente pasan. Se corrigió el título largo del tablero para ganar espacio. Inspección visual de capturas; PDF S6 con 27 páginas en /tmp/bigdata-editorial/sesion-6-editorial.pdf. git diff --check limpio.

Servidor 4183 preexistente reutilizado. Sin ejecución GCP/BI real, sin publicar, commit ni push. Permisos desde una segunda identidad, equivalencia BI/SQL y perfilado de datos reales continúan pendientes. Próximo paso: revisión local de S6 y rediseño S7 GenAI/evidencia (ML conceptual máximo 10 min, sin entrenamiento).

## CP-010 — Sesión 7: GenAI y evidencia · 2026-11-05

Petición: «sigue», continuación después de S6. S7 rediseñada: 27 slides / 180 min. Apertura con memo docente que presenta subtotal de C como canasta completa; el grupo contrasta afirmaciones y reconstruye la recomendación. ML conceptual solo 15–25 min, sin entrenamiento. Caso Carrefour Marketing Studio atribuido a Google Cloud; ninguna cifra de beneficio ni afirmación de que sea RAG.

Fuentes: editorial/guion.py SESSIONS[7], ai.css, ai.js. Auditoría interactiva con cita real y tres veredictos: contradicha, sustentada y sin respaldo. Recuperación local por términos conservada en practica.html; F03 contiene el límite de inventario. Generación en servicio aprobado mediante transferencia humana; no API del sitio ni RAG automático. Laboratorio 55 min y transferencia 30 min al dataset distinto de cada equipo. Prompt completo incluye tratar documentos como datos y no seguir instrucciones embebidas; no promete protección absoluta.

Guía JSON actualizada: SQL 08_resumen_ejecutivo.sql, dos solicitudes planificadas, registro de salida literal y corregida, ruta Studio y contingencia docente. Documentación GCP consultada muestra Agent Studio donde el syllabus usa Vertex AI Studio: se conservan referencias y se exige ensayo de cuenta/modelo/permisos/crédito. No hay ejecución cloud. build.py preserva S1–S7; S8 sigue base. Total203, editoriales189. Plan, AGENTS, README, fuentes y guion documental S7 actualizados.

QA: Chromium recorre189 slides en1440×900,1280×720,390×844; sin errores de consola/red ni desbordamientos detectados. Pruebas de auditoría con tres veredictos y reinicio al cambiar afirmación; clic no avanza slide. Recuperación cobertura/inventario y pregunta sin coincidencias verificadas. Capturas de apertura y auditoría inspeccionadas; PDF de27 páginas /tmp/bigdata-editorial/sesion-7-editorial.pdf. git diff --check limpio. El primer intento encontró servidor4183 detenido; se inició uno nuevo (sesión72563), disponible para revisión. Sin commit, push, publicación ni provisión cloud.

Próximo paso: revisión local de S7 y rediseño S8, comité ejecutivo y defensa del proyecto, sin infraestructura nueva. Continúan pendientes ensayos reales de SQL/BI/modelo y preparación de datasets propios.

## CP-011 — Sección independiente de publicación · 2026-11-09

El usuario pide que el push publique el rediseño en /refactor_especialidad/ antes de crear una clase independiente. Se añade scripts/package-refactor.py y se configura workflow de Hosting para plan3. Build aislado desde HEAD más nuevas fuentes; quedan fuera los seis archivos modificados previamente del sitio antiguo y presentaciones/notebooks. El empaquetador conserva los1199 archivos del build principal y añade110 materiales públicos bajo el prefijo. app.js,index.html,decks.json del build coinciden byte a byte con producción consultada hoy. No se modifica Firestore.

Documentación en docs/rediseno-especialidad/publicacion.md. El workflow antiguo todavía existe en plan2: evitar pushes allí para que no retire la sección. Commit/push y verificación de Actions pendientes al escribir este corte. La clase independiente aún no tiene tema/alcance definido y no se ha comenzado.

Validación de prefijo: verify-hosting.mjs pasa para ocho decks, guías/recursos y prácticas S6/S7. La revisión detectó y corrigió la exclusión de .sh descargables. Los snapshots fuente y CSV conservan su formato original (incluidos espacios finales/CRLF); no se normalizaron para preservar contenido y hashes.

Publicación confirmada: push de plan3, commit0a56790. GitHub Actions42718560410 terminó success. URL https://bigdata-up.web.app/refactor_especialidad/ responde200; sesiones1/7, práctica7, SQL y reto SQL verificados. Después del despliegue index.html,app.js,decks.json conservan exactamente sus bytes anteriores. No se publicaron los cambios locales previos.

Clase independiente: usuario confirmó ejecutivos, BigQuery y Bronze/Silver/Gold,180 minutos. Antes de producir materiales pregunta si usar all_data.csv o actualizar QQP. Inventario:19706.44MB, última modificación2023-05-27; no prueba periodo ni esquema. Recomendación en discusión: conservar archivo histórico como Bronze y usar corte oficial reciente acotado/congelado para taller, con nueva entrega para enseñar actualización. No se ha descargado/perfilado el archivo grande ni creado el deck independiente.

## CP-012 — Clase emergente BigQuery / all_data · 2026-11-09

Usuario confirma all_data y orden BigQuery → Medallion → laboratorio → tarea deactualización, incluyendo propuestas dearquitectura. Se crea clase autónoma en presentaciones-v2/clase-bigquery,26 slides /180min: BigQuery30, arquitecturas20, Medallion20, pausa10, laboratorio80 y tarea20. No modifica el currículo de8 sesiones. Fuenteseditoriales guion.py, estilos.css e interacciones.js; generador scripts/build-clase-bigquery.py. Diagramas progresivos, comparación real, selector warehouse/lake+warehouse/lakehouse y demostración deLIMIT frente a particiones. Guía y tarea completas generadas; ocho archivosSQL, esquemaJSON y scripts bq.

Inspección real: DriveID1dLxKFxawXTTaqCDr9Y9YpYdWTpOhol42 medianteHTTPRange; archivo20663702126 bytes. Tres ventanas de2MiB (inicio,mitad,final),1500 filas completas de15 columnas porventana: muestra4500 filas conservada con manifiesto ySHA256. Fechas vistas2011/2014/2015, no cobertura global. CabecerascamelCase fechaRegistro/cadenaComercial/nombreComercial.3000 municipios con espacios finales. ParREFRESCO/SPRITE/BOTELLA2LT.NO RETORNABLE/TLALPAN/2014-03-19 en dos tiendas a15.10 y15.50MXN. No aleatoria ni representativa, sin descarga completa ni atribuir ahorro actual.

Diseño: datasets emergente_* separados del curso. Staging entrada reemplazable; Bronze con lote,fuente,fecha y firma; protección de repetición porlote bajo ejecución serial. Silver deduplica15campos exactos,normaliza,convierte y conserva rechazos. Partición mensual,clustering y filtro obligatorio. Copia plana temporal para benchmark. Gold porproducto/tienda/día conserva conflictos; nunca suma precios como ventas. BenchmarkA/B/C con resultados comparables, caché desactivada y registrojob/bytes. Limpieza explícita elimina solo tabla plana. SQL03/04 reconstruyen todo; tarea propone incremental, no se finge implementado. Ruta docente dearchivo completo usa GCS preparado, no20.7GB enCloud Shell.

Validación: verify-all-data-sample.py pasa hash/4500distintas/4500aceptadas/0rechazadas/0conflictos/parhistórico y repetición lógica local. sqlglot30.30.0 analiza los8SQL en dialectoBigQuery. NO ejecución en motorGCP; faltan carga, jobs y métricas reales. verify-clase-bigquery.mjs pasa26slides en1440×900,1280×720 y390×844, interacciones y links; sin errores ni recortes. Se corrigió desbordamiento móvil de texto de tarea. PDF26páginas en/tmp/bigdata-clase-bigquery/clase-bigquery.pdf.

Catálogo añade enlace fuera de las8sesiones. Workflow y package-refactor preparados para incluir clase-bigquery en siguientepush. Build aislado conserva1199archivos del sitio antiguo y empaqueta133archivos del refactor. Clase NO publicada ni commit/push realizado en este turno. Se conservan cambios previos ajenos sin tocar. Próximo: revisión de clase y ensayo docente en proyectoGCP antes de impartir/publicar.


## CP-013 — Simplificación del laboratorio emergente · 2026-11-09

Usuario solicita queries sencillas para audiencia poco técnica: Bronze as-it-is, creación Silver y Gold. Se reducen descargas a tres archivosSQL:10_bronze.sql muestra valores originales y ejemplosTRIM/SAFE_CAST en SELECT;20_silver.sql crea tabla limpia, tabla para revisar y conteo;30_gold.sql crea comparación de tienda y producto histórico. Laboratorio con tres pasos; docente prepara proyecto/datasets y puede cargar muestra de4500 filas. Se elimina del material del alumno la secuencia avanzada de8scripts, control serial de lotes, benchmarks con tabla duplicada y mantenimiento de bytes/job IDs. Optimización queda explicada en lenguaje ejecutivo: elegir columnas, filtrar fecha, estimar bytes y LIMIT afecta salida. Se simplifica tarea de actualización sin pedir implementarMERGE.

Build clase regenerado. Los3 archivos SQL pasan parser sqlglot30.30 en dialectoBigQuery; verify-clase-bigquery.mjs pasa26slides, tres tamaños, interacción y links. Muestra local sigue pasando4500 filas y comparación histórica. No motor GCP. Requiere revisar que README/guía generados no conserven referencias a scripts eliminados. Siguiente: publicar revisión simplificada con push plan3.
