# Revisión curricular — rama plan2

## Perfiles y estructura

Especialidad: perfil mixto de negocio, riesgo, producto y análisis; decisiones, lectura crítica de evidencia y ETL guiado. Maestría: perfil técnico de ciencia de datos; implementación, validación temporal, rendimiento y operación de un prototipo. Son perfiles inferidos del material, no requisitos institucionales confirmados. Los programas incorporan hitos y resultados observables dentro de las 27 y 39 horas existentes.

## Fallas corregidas

| Hallazgo | Resultado |
|---|---|
| Confusión entre free tier y prueba | Ruta US$300/90 días, presupuesto ilustrativo, recursos temporales y cierre explícito |
| Pub/Sub Lite retirado | Pub/Sub estándar, puente durable a GCS y file stream; ACK posterior al almacenamiento y deduplicación |
| Data Catalog retirado | Referencia actualizada a Knowledge Catalog |
| Features aprendidas sobre todos los datos | Corte temporal antes de fit; pipeline completo ajustado con train |
| Entrenamiento y Airflow con contratos distintos | Esquema bancario común, artefactos por run y validación de la URI del candidato |
| Jinja y errores HTTP sin garantías claras | Campos renderizados, token de recarga y errores propagados |
| Drift descrito como automatización completa | Reporte revisado, trigger explícito y nueva puerta ROC/PR-AUC |
| Dataset bancario inferior a 15 GB | Advertencia y fuentes reales relevantes; no inflar mediante duplicación |
| Entregables y visualización poco guiados | Plantillas, hitos, ejercicios y ocho infográficos propios |

## Storytelling y visualización

Siguiendo principios de Cole Nussbaumer Knaflic: audiencia y decisión explícitas, títulos que expresan una conclusión, contexto y unidades, reducción de ruido, jerarquía por posición y énfasis con un color. Los valores ilustrativos se identifican como tales. Animación escalonada para conducir la explicación, navegación por clic/teclado y respeto a movimiento reducido. Los SVG son editables y originales; los PNG previos se conservan.

Referencias: [el “so what”](https://www.storytellingwithdata.com/blog/2017/3/22/so-what), [los datos necesitan contexto](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

## Fuentes técnicas

- [Prueba y free tier de GCP](https://docs.cloud.google.com/free/docs/free-cloud-features): elegibilidad, crédito y cuotas.
- [Budgets](https://docs.cloud.google.com/billing/docs/how-to/budgets): las alertas no detienen automáticamente el gasto.
- [Retiro de Pub/Sub Lite](https://docs.cloud.google.com/pubsub/lite/docs/release-notes).
- [Retiro de Data Catalog](https://docs.cloud.google.com/knowledge-catalog/docs/deprecations).
- [Structured Streaming 3.5](https://spark.apache.org/docs/3.5.3/structured-streaming-programming-guide.html).
- [Airflow: recursos recomendados](https://airflow.apache.org/docs/apache-airflow/2.11.0/installation/prerequisites.html).

## Validación y límites

Build: 25 presentaciones, 350 diapositivas. Chromium revisa catálogo, navegación, móvil, las 350 diapositivas, 14 diagramas Mermaid y ocho SVG: sin errores de ejecución, imágenes rotas ni desbordamiento detectado en las vistas probadas.

Cuatro pruebas locales cubren entrenamiento/guardado/carga con Spark 3.5.3 y Java 17, streaming con ventanas y deduplicación, API/recarga, PSI y persistencia del puente. Airflow 2.11 valida importación, serialización, plantillas, ramas, métricas del run y fallas HTTP. Los casos GCS/HTTP usan dobles de prueba; no sustituyen integración cloud.

No se han creado recursos GCP ni realizado una corrida end-to-end en cloud. El presupuesto es una asignación docente, no una cotización ni garantía de que todos los proyectos cabrán. Antes de clase verificar cuotas, permisos, conectividad y la descarga de dependencias del cluster. El serving y Airflow standalone son prototipos docentes, no una arquitectura de producción.
