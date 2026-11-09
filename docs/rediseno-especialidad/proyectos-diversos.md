# Proyecto integrador · un dataset distinto por equipo

**Decisión del usuario, 2026-11-05:** el proyecto final no utilizará los mismos datos para todos. **PROFECO queda como caso guiado**, no como proyecto final obligatorio. El alcance actual es exclusivamente Especialidad.

## Dos recorridos coordinados

- **Práctica guiada:** `employees` para SQL y PROFECO para el flujo Bronze → Silver → Gold → dashboard → memo. Permite aprender el mecanismo con apoyo común.
- **Proyecto propio:** cada equipo trabaja con una fuente/dataset distinto, una pregunta propia y KPIs pertinentes. Demuestra que puede transferir lo aprendido, no copiar una canasta.

Se reserva la franja de **130–160 min** de S1–S7 para el proyecto propio, usando plantillas y SQL docente adaptado por dataset. La ruta base cabe en clase: elegir datos no implica programar un pipeline desde cero. El laboratorio común produce una evidencia de práctica; el hito evaluado pertenece al dataset del equipo. No exigir dos proyectos completos paralelos.

## Selección y preparación

En S1 se elige una opción provisional; antes de terminar S2 se acuerda fuente/pregunta y se comprueba viabilidad. El docente prepara previamente un catálogo pequeño de paquetes ya perfilados, con muestra, fuente grande cuando proceda, esquema, reglas y consultas de base. El equipo puede proponer otro dataset si cumple las mismas condiciones y no desplaza la preparación técnica al alumnado ejecutivo.

Registrar por equipo: ID, integrantes, fuente raíz, archivo/versión/checksum, pregunta, grano, periodo, volumen real, permisos de uso y estado de acceso. Un CSV y su versión Parquet **son el mismo origen** a efectos de asignación. Cambiar región o filtrar el mismo archivo no basta para afirmar diversidad de fuentes. Evitar duplicar el dataset principal entre equipos; si no alcanzan las opciones validadas, ampliar el catálogo antes de asignar.

## Candidatos existentes, todavía sujetos a perfilado

Estos nombres existen en el inventario del curso; la columna de decisión es una **propuesta**, no un hallazgo ni una garantía de esquema/licencia. Las posibilidades definitivas dependen del contrato real. El origen público del enlace no prueba permiso para cualquier reutilización.

| Paquete candidato | Decisión posible | KPI candidato | Verificación necesaria |
|---|---|---|---|
| PROFECO, `all_data.csv` | Comparar una compra histórica | Costo/cobertura de canasta | A lo sumo un equipo podría elegirlo; preferir otro origen para evaluar transferencia más clara |
| Biblioteca, `Checkouts_by_Title_20250207.csv` | Priorizar recursos de colección por uso observado | Préstamos, cambio por periodo, participación por formato | Comprobar grano y campo de conteo; no equiparar filas con préstamos ni uso con demanda insatisfecha |
| Videojuegos, `steam_reviews.csv` | Priorizar revisión de comentarios o soporte | Proporción recomendada, volumen de reseñas por juego/periodo | Denominador, sesgo de selección y campos disponibles; no inferir ventas o usuarios totales |
| Ciudad, `carpetas_investigacion.csv` | Priorizar revisión operativa de registros por zona/periodo | Conteos y completitud temporal/geográfica | Expediente vs. hecho/persona, cobertura y posibles datos identificables; no inferir riesgo poblacional sin denominadores |
| Finanzas, `bank_transactions.csv` | Priorizar revisión de señales en transacciones de ejemplo | Monto por moneda, frecuencia y señales documentadas | Procedencia/sintético, moneda, grano y significado de etiqueta; no entrenar modelo ni llamar fraude a una señal |
| Catálogo/recomendación, `animes.csv` + `profiles.csv` + `reviews.csv` | Comparar cobertura y patrones de valoración | Cobertura, conteo de valoraciones y promedio con tamaño de muestra | Llaves, cardinalidad, escala de valoración y privacidad; no construir recomendador de ML |

No asignar de entrada logs personales, correos o tweets sensibles para compensar falta de opciones. Ampliar con fuentes abiertas apropiadas si el número de equipos excede el catálogo validado; no está cerrado el reparto sin conocer tamaño de grupo. Cada equipo comparte evidencia agregada, no datos personales crudos.

## Lo común es el contrato de entrega

| Hito | Evidencia del dataset propio |
|---|---|
| H1 · S1 | Audiencia, decisión, fuente candidata y mapa inicial |
| H2 · S2 | Fuente distinta registrada, grano/llaves y tres preguntas consultables; las seis consultas `employees` son práctica guiada |
| H3 · S3 | Fuente/manifiesto, Bronze consultable y alcance de volumen comprobado |
| H4 · S4 | Dos o más reglas relevantes, Silver, rechazados/reconciliación y gobierno |
| H5 · S5 | Gold con 3–5 KPIs propios, fórmulas/unidades/denominadores y control de doble conteo |
| H6 · S6 | Dashboard, controles de interpretación/acceso y recomendación basada en el dato |
| H7 · S7 | Memo asistido por GenAI y comprobación de afirmaciones; evidencia de recuperación si se muestra el patrón RAG |
| H8 · S8 | Documento de arquitectura/gobierno, SQL, dashboard, evidencia y defensa |

El documento distingue la arquitectura objetivo (incluida evolución posible a lakehouse) de lo que se ejecutó en GCS/BigQuery. Ningún equipo tiene que desplegar un lakehouse completo, entrenar un modelo ni escribir Python.

## Evaluación comparable sin KPIs idénticos

Conservar la rúbrica propuesta de 100 puntos del plan: pregunta/valor 20, arquitectura/gobierno 20, SQL/calidad/KPIs 25, comunicación/dashboard 20, evaluación de GenAI 10 y reproducibilidad/costo 5. Se evalúa si el KPI es válido para **su** decisión, no si coincide con los precios del ejemplo. No se asignan puntos a entrenamiento, precisión predictiva, algoritmos o métricas de ML.

La capacidad de GenAI para responder sobre el dataset no demuestra corrección: se exige un registro de afirmaciones y fuentes, con abstención cuando falte evidencia. Si no hay acceso a la interfaz, usar una respuesta docente sobre el paquete del equipo y señalar que no se ejecutó por el alumno.

**Recuperación:** cada paquete tendrá un punto de restauración Bronze/Silver/Gold para evitar que un problema anterior impida practicar el siguiente tema. Usarlo se registra; el equipo explica qué parte ejecutó. Las plantillas de código y las salidas esperadas se validan por paquete antes de distribuirse.
