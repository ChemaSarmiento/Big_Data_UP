# Especialidad · propuesta de slides y laboratorios

**Versión 0.4 · 2026-11-05 · rama plan3.** Ocho sesiones implementadas para revisión local, **203 slides**. Tras revisar el primer lote, el usuario pidió reducir repetición visual y aplicar su kit de storytelling/identidad. **S1–S7 se reescribieron con 27, 28, 26, 27, 27, 27 y 27 slides; S8 conservan su versión base.**

La [propuesta editorial S1–S7](docs/rediseno-especialidad/propuesta-editorial-s01-s03.md) y el [syllabus específico de Especialidad](docs/rediseno-especialidad/syllabus-especialidad-fuente.md) son las referencias vigentes para ese corte. [Índice local](presentaciones-v2/index.html) · [Uso y límites](presentaciones-v2/README.md). El [plan general](PLAN_ESPECIALIDAD.md) conserva alcance y entregables. Las guías extensas acompañan a la proyección; los labs cloud siguen pendientes de ensayo real.

**Actualización del usuario:** PROFECO es el ejemplo guiado; **cada equipo usa un dataset distinto en el proyecto final**. La práctica de ML no forma parte de Especialidad. Su presencia en el syllabus se cubre con 10 minutos conceptuales, sin entrenamiento ni entregable predictivo. Ver el [contrato de proyectos diversos](docs/rediseno-especialidad/proyectos-diversos.md).

## Recorrido de 24 horas

| Sesión y guion | Teoría que se debe comprender | Laboratorio y resultado |
|---|---|---|
| [1. Una compra merece evidencia](docs/rediseno-especialidad/sesiones/01.md) | Big Data, distribución, cloud, OLTP/OLAP, warehouse/lake/lakehouse y mapa Medallion | Proyecto, crédito verificado, presupuesto, bucket y ficha de decisión |
| [2. SQL para preguntas precisas](docs/rediseno-especialidad/sesiones/02.md) | Tablas, llaves, grano, filtros, agregaciones, joins y vigencias | Seis consultas guiadas en `employees`/MariaDB y diagnóstico de doble conteo |
| [3. Bronze: conservar y consultar](docs/rediseno-especialidad/sesiones/03.md) | ETL/ELT, esquemas, tablas externas, cómputo separado y escala | Bronze en GCS/BigQuery, manifiesto y evidencia de consulta de fuente grande |
| [4. Silver: datos comparables y gobernados](docs/rediseno-especialidad/sesiones/04.md) | Calidad, tipos, duplicados, privacidad, permisos, retención y partición | Silver, rechazados, reconciliación y matriz de gobierno |
| [5. Gold: una canasta defendible](docs/rediseno-especialidad/sesiones/05.md) | Modelo analítico, joins, selección temporal, KPIs y costos | Gold con costo/cobertura por establecimiento y validación manual |
| [6. Del dashboard a la acción](docs/rediseno-especialidad/sesiones/06.md) | Comunicación visual, filtros, agregaciones y consumo de datos | Dashboard interactivo y recomendación con alcance histórico |
| [7. GenAI y evidencia bajo evaluación](docs/rediseno-especialidad/sesiones/07.md) | Predicción vs. generación, LLM, recuperación, citas y errores | Memo con evidencia, demo de recuperación y auditoría de afirmaciones |
| [8. Comité de decisión](docs/rediseno-especialidad/sesiones/08.md) | Defensa de valor, arquitectura, evidencia, costo y riesgo | Proyecto integrado, defensa y cierre de recursos |

## Correspondencia explícita con el syllabus

| Contenido de Especialidad en el syllabus | Dónde se enseña y comprueba |
|---|---|
| Cloud y aprovisionamiento | S1: proyecto/billing/bucket; operación y cierre reaparecen en cada lab |
| Warehouse → lake → lakehouse | S1: comparación visual y diseño objetivo; S3/S5: distinguir implementación docente de capacidades de lakehouse |
| Casos banca, retail, salud y logística | S1: tarjetas HSBC/Mercado Libre/Mayo Clinic/UPS Capital; retomados en S3–S7 según la pregunta |
| ETL vs. ELT | S3: dos recorridos del mismo archivo; alumno justifica su ruta |
| Medallion | Mapa desde S1, Bronze S3, Silver S4, Gold S5, rastreo S8 |
| Calidad, gobierno, seguridad, compliance, privacidad | S4 explícita, con decisiones de acceso/retención; S6 distribución del dashboard; S7 uso del LLM |
| SQL esencial, filtros, agregaciones y joins | S2 completa con `employees`; transferencia y práctica BigQuery en S3–S5 |
| Motores distribuidos/BigQuery | S1 modelo conceptual; S3 lectura a escala; S4–S5 particiones y bytes |
| ML para decisión de negocio | S7: 10 min para distinguir predicción/generación y responsabilidad; sin laboratorio, código, entrenamiento ni entregable de ML |
| LLM/GenAI y RAG | S7: generación, recuperación visible, evaluación de evidencia y abstención |
| Visualización ejecutiva | S6: Looker Studio como herramienta del syllabus, con KPIs específicos de precios |
| Documento de arquitectura/gobierno, SQL y dashboard | Hitos H1–H7 ensamblados y defendidos en S8; anexo IA complementario |

Se modifica la **secuencia de laboratorios** del syllabus, no sus objetivos: SQL se adelanta de S4 a S2 y Bronze/Silver se desplazan a S3/S4. Se conserva S5 Gold, S6 visualización, S7 GenAI y S8 defensa. No se agrega una novena sesión de nivelación.

La práctica **guiada** de ventas/clientes del syllabus se adapta a **precios observados PROFECO**, por elección del usuario. «Ventas», «ticket» y «usuarios activos» pasan a costo de canasta, cobertura, diferencias entre alternativas comparables y calidad. Las funciones de ventana y vistas materializadas no serán requisitos de programación del ejecutivo: se suministra SQL comentado y se usa CTAS/vista lógica en la ruta base.

## Ritmo y carga de trabajo

En S1–S7 se mantiene la agenda de **180 minutos**. La numeración de la tabla siguiente describe S4–S7; para S1–S7 usar sus guiones vigentes, cuya extensión sigue el relato:

| Minutos | Slides orientativas | Uso |
|---|---|---|
| 0–15 | 01–03 | Dilema, recuperación de lo anterior y resultado del día |
| 15–45 | 04–11 | Teoría visual con ejemplos y preguntas; unos 3–4 min por pantalla |
| 45–65 | 12–15 | Caso, demostración y decisión de transferencia |
| 65–75 | 16 | Pausa |
| 75–130 | 17–23 | Laboratorio: entrada y seis pasos guiados |
| 130–160 | 24–26 | Aplicación al proyecto, validación entre pares y corrección |
| 160–180 | 27–28 | Hito, comprensión y cierre de costos/recursos |

Un laboratorio usa **55 minutos**: 5 + 8 + 12 + 12 + 10 + 8. La producción debe ensayar esos tiempos; son una asignación pedagógica, no tiempos cloud garantizados. Los ejemplos/listas extensas van a la guía. La franja de aplicación de 30 minutos se reserva al dataset propio del equipo, con plantillas y puntos de restauración ya preparados. Los pasos de las tablas describen la práctica común; no hay que duplicar todo el laboratorio ni programar otra solución desde cero. Los hitos evaluados corresponden al proyecto propio, según el contrato de proyectos diversos. No se exige trabajo adicional fuera de las 24 h para completar la ruta base.

## Contrato del ejemplo guiado PROFECO

Antes de escribir el SQL final se debe perfilar `all_data.csv`: columnas, tipos, fechas, origen, permisos de uso, identidad de producto/establecimiento y duplicados. Los siguientes son **nombres lógicos propuestos**, no encabezados verificados:

- Bronze: `profeco_bronze.observaciones_raw`, manifiesto con URI, tamaño, checksum, fecha de ingesta y conteos comprobados.
- Silver: `profeco_silver.observaciones`, `rechazadas` y `reporte_calidad`; campos canónicos como `id_producto`, `id_establecimiento`, `fecha_observada`, `precio_envase_mxn` y procedencia.
- Catálogo docente de cinco productos: identidad aprobada, marca/presentación exacta y `cantidad_envases` entera. Evitar conversiones de unidad dudosas; si se comparan unidades normalizadas, mantener visible la presentación comprable.
- Gold: `profeco_gold.precios_elegidos` (una fila por producto/establecimiento/escenario) y `canastas` (una fila por establecimiento/escenario). La selección usa una ventana histórica común y una regla determinista documentada, propuesta: última observación válida dentro de esa ventana. Cada producto conserva su fecha; no fingir simultaneidad.
- La ventana final se elige según cobertura real. Si ningún establecimiento tiene los cinco productos, el resultado puede ser «no hay una alternativa completa»; no inventar precios ni cambiar silenciosamente la canasta.
- Cobertura = productos requeridos encontrados / cinco. Costo = suma de precio por envase × cantidad de envases, visible como **subtotal** si falta algún producto. Rankings de canasta completa solo entre alternativas elegibles.
- Los snapshots de escenarios no se suman entre sí. El dashboard obliga a elegir un escenario y mantiene el grano de `canastas`.

`employees` es un puente didáctico independiente: no se une con PROFECO. Las cifras de salario son datos de ejemplo y su unidad no se presupone MXN. «Actual» significa la vigencia del snapshot del dataset; no la plantilla laboral de hoy.

## Qué recibe el alumno y qué prepara el docente

Cada sesión completa tendrá una fuente de slides, guía HTML imprimible, notas de facilitación, archivos descargables y fuentes. Cada paso de laboratorio especificará ubicación de interfaz, acción, código exacto por motor, salida comprobable, error/recuperación, evidencia y cierre. No se publicará SQL con nombres inventados presentándolo como probado.

El docente prepara cuentas/accesos de respaldo, MariaDB con `employees`, una muestra reproducible y una fuente grande en GCS, y plantillas de Silver/Gold. Los alumnos interpretan y ejecutan cambios acotados: no administran clústeres ni programan Python. Para la transferencia de 30 minutos, el docente entrega un paquete distinto por equipo, con esquema y consultas base comprobados. No se obliga a todos a reutilizar la canasta o los KPIs de PROFECO. El montaje docente forma parte de la producción del curso, no de una sesión extra obligatoria.

## Casos, teoría y extensiones

Las fichas usarán las [fuentes registradas](docs/rediseno-especialidad/fuentes.md), diagramas propios y beneficios atribuidos al publicador. HSBC y Mayo Clinic amplían los sectores del syllabus; son arquitectura y contexto, no pruebas de rentabilidad de nuestro proyecto. GDPR/HIPAA se tratan como referencias para reconocer contexto y responsabilidades, sin presentar precios públicos como datos clínicos ni dar por cumplida una norma por usar cloud.

**Fuera de la ruta obligatoria:** Spark/Python, streaming implementado, modelos entrenados, embeddings masivos, Iceberg/Delta, orquestación y tuning. Las ampliaciones conceptuales o SQL avanzado van a material posterior, sin añadir tareas para aprobar Especialidad.

## Cómo producir a partir de estos guiones

1. Conservar el piloto como referencia; convertirlo en componentes compartidos sin romper su ruta.
2. Producir S1–S2 completas con diagramas y códigos verificados de preparación/SQL.
3. Cerrar contrato real de datos; generar la muestra y salidas esperadas antes de producir S3–S5.
4. Crear dashboard y evidencia de ejecución; después escribir gráficas y conclusiones de S6.
5. Ensayar modelo/interfaz/costo y corpus de evidencia; después capturar S7 y preparar contingencias.
6. Ensayar el recorrido completo, preparar S8, verificar pantallas, impresión y guías. Desplegar solo cuando se solicite.

El kit posterior y la revisión editorial sustituyen la repetición visual del primer lote. No se toma como aprobación automática de ponderaciones, mínimo de volumen o cantidad de equipos. El siguiente resultado de producción recomendado es **S1 completa**, seguida de S2; estos guiones permiten revisar contenido antes de codificar los ocho decks.
