# Facilitación — Sesión 13: Gobernanza, seguridad y capstone técnico

> Guion de 3 horas: teoría breve + presentaciones del capstone. A diferencia de
> las sesiones anteriores, hoy la mayoría del tiempo es de los estudiantes, no
> tuyo — tu rol cambia de instructor a moderador/evaluador.

## Antes de empezar (facilitador)

Ten la rúbrica de `PROGRAMA.md` Sección 5 impresa o proyectada, visible durante
todas las presentaciones — no la guardes para el final. Confirma el orden de
presentación y el cronómetro de 15 minutos por equipo **antes** de empezar.

---

## Bloque 1 — Apertura y teoría breve (0:00–0:45, 45 min)

**Talking point de apertura:**

> "Antes de que empiecen las presentaciones, media hora de teoría que conecta
> directo con lo que van a presentar: gobernanza no es burocracia — es lo que
> separa un proyecto de curso de algo que un banco real podría operar."

### IAM a nivel tabla (10 min)

Conecta con el Módulo 0 (IAM de proyecto) — hoy es más fino: dataset, columna,
fila. Pregunta: **"¿alguno de sus capstones maneja datos que ameritarían este
nivel de control?"**

### Data Catalog y linaje (10 min)

Pregunta rápida: **"¿podrían responder ahora mismo 'de dónde viene exactamente
este número' en su propio capstone, sin revisar el código?"** — es el problema
que el linaje resuelve, y una buena autoevaluación antes de presentar.

### Cumplimiento y FinOps (15 min)

Recorre las tres exigencias de banca (explicabilidad, trazabilidad,
retención/borrado) y el punto de FinOps: la puerta de calidad del DAG (Sesión
12) es, en el fondo, una decisión de costo disfrazada de decisión técnica.

### Transición a presentaciones (10 min)

Recuerda la rúbrica completa en voz alta frente al grupo — visualización,
pruebas, todas las etapas del pipeline — antes de que empiece la primera
presentación.

---

## Bloque 2 — Presentaciones del capstone (0:45–2:45, 120 min)

Con máx. 15 min por equipo, esto da espacio para ~7-8 equipos con margen de
transición. Ajusta según el tamaño real del grupo.

**Estructura sugerida por presentación (facilítala así, no la dejes libre):**
- 12 min: presentación del equipo
- 3 min: preguntas del grupo + retroalimentación tuya

**Talking points para dar retroalimentación consistente entre equipos (úsalos
como checklist mental durante cada una):**

- ¿La pregunta de negocio es específica, o es "analizamos los datos y
  encontramos cosas"? (la rúbrica exige lo primero)
- ¿Mostraron al menos una visualización de sus conclusiones, no solo una tabla
  de métricas?
- ¿Hay evidencia de pruebas — validación de calidad de datos, comparación
  antes/después de al menos una optimización?
- ¿El pipeline cubre las 5 etapas técnicas requeridas (ingesta, features,
  entrenamiento, serving, streaming/orquestación)?
- ¿Mostraron el código, aunque sea brevemente, o solo lo mencionaron?

**Pregunta que vale la pena hacer a cada equipo, si nadie más la hace:**

> "¿Qué harían distinto si tuvieran que llevar esto a producción real mañana?"

Es la pregunta que conecta todo el contenido de las Sesiones 11-13
(serving, monitoreo, gobernanza) con lo que acaban de presentar.

---

## Bloque 3 — Cierre del programa (2:45–3:00, 15 min)

**Talking point de cierre:**

> "Empezaron hace 13 sesiones con un cluster de MapReduce contando palabras.
> Terminan hoy con un pipeline completo de ingesta a serving, con monitoreo y
> orquestación automatizada. Eso no es una metáfora — es literalmente lo que
> demostraron hoy."

**Temas de profundización sugeridos, mencionar brevemente:**
- Delta Lake/Iceberg avanzado (más allá de lo visto en Sesión 7-8)
- Entrenamiento distribuido con GPUs
- Feature stores productivos (Feast, Vertex AI Feature Store)
- BigQuery ML

---

## Notas de costo GCP

- Recuerda al grupo, como cierre práctico: revisar `Billing → Reports` una
  última vez y apagar/borrar cualquier recurso de su capstone que no necesiten
  mantener vivo después del curso (clusters, endpoints, topics de Pub/Sub
  Lite) — el crédito de $300 no es indefinido.
