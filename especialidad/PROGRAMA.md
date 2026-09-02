# Programa: Big Data — Track Especialidad
### 9 sesiones · 3 horas/semana · 27 horas totales · Entorno: GCP (free tier)

**Perfil de entrada:** perfiles diversos (negocio, producto, riesgo, actuaría, ingeniería no-software, etc.) que buscan especializarse. El interés es principalmente **ejecutivo/estratégico**: entender qué es posible, cuándo tiene sentido invertir en Big Data, cómo se ve un proyecto de datos por dentro y cómo evaluarlo — no formar ingenieros de datos.

**Diferencia clave vs. el track de Maestría:** aquí sí hay código y bases de datos (no se puede entender Big Data sin tocarlo), pero **siempre guiado y acotado**: notebooks para completar, no para escribir desde cero; demos en vivo con participación interactiva; menos tiempo de tuning y optimización profunda, más tiempo de "para qué sirve esto y cuándo lo uso". El entregable final es una **propuesta de arquitectura con caso de negocio**, no un pipeline productivo.

---

## 1. Objetivo del programa

Al terminar, el participante podrá:
- Hablar el mismo idioma que un equipo de datos (vocabulario, arquitectura, límites técnicos reales).
- Identificar cuándo un problema de negocio **sí** justifica una solución de Big Data y cuándo es sobre-ingeniería.
- Leer y modificar consultas SQL sobre datos a gran escala (BigQuery).
- Ejecutar y ajustar un notebook guiado de procesamiento distribuido (Spark) sin necesidad de escribirlo desde cero.
- Evaluar propuestas técnicas de su equipo: hacer las preguntas correctas sobre costo, arquitectura y riesgo.
- Presentar una propuesta de arquitectura de datos con caso de negocio justificado.

---

## 2. Módulo 0 — Nivelación (asíncrono, antes de la Sesión 1)

Aquí sí es puramente introductorio y no se evalúa — el objetivo es que nadie llegue en blanco a la Sesión 1, no filtrar acceso.

| Bloque | Contenido |
|---|---|
| Linux esencial | Qué es una terminal, comandos básicos de navegación (con analogías a un explorador de archivos) |
| Python esencial | Qué es una variable, un notebook, cómo correr una celda — lo mínimo para no bloquearse en los labs guiados |
| SQL esencial | `SELECT/WHERE/GROUP BY` — lo suficiente para leer una consulta y entender qué responde |
| Entorno del curso | Acceso a la consola web de GCP (sin necesidad de instalar nada localmente) |

---

## 3. Mapa general de las 9 sesiones

| # | Tema central | Formato dominante |
|---|---|---|
| 1 | Big Data para decisiones de negocio: panorama y casos de uso | Charla + casos |
| 2 | Cómo funciona por dentro (sin escribir código pesado) | Demo guiada |
| 3 | SQL para analítica a escala | Lab guiado (BigQuery) |
| 4 | Introducción a Spark: qué hace y para qué sirve | Notebook guiado |
| 5 | Cómo se ve un pipeline de datos real | Lab guiado (low-code) |
| 6 | Data Lakes y gobierno del dato, explicado para negocio | Charla + caso de mal manejo de datos |
| 7 | Datos en tiempo real: casos de uso y decisiones | Demo guiada |
| 8 | Costos, gobernanza y cómo evaluar un proyecto de datos | Taller (framework de decisión) |
| 9 | Presentación de propuestas | Presentaciones |

---

## 4. Detalle sesión por sesión

### Sesión 1 — Big Data para decisiones de negocio
- **Contenido:** las 5 V's explicadas con ejemplos de industria (banca, retail, salud), cuándo *sí* se necesita Big Data y cuándo un Excel/base de datos tradicional basta, panorama del ecosistema (storage, cómputo, streaming, orquestación) a nivel de mapa, no de detalle técnico.
- **Actividad:** análisis de 2-3 casos reales — el grupo decide si el caso justificaba una inversión en Big Data o fue sobre-ingeniería.
- **Entregable:** ficha de 1 página con un caso propio de su industria (¿aplica Big Data o no, y por qué?).

### Sesión 2 — Cómo funciona por dentro
- **Contenido:** almacenamiento y cómputo distribuido explicado con analogías (bibliotecas, equipos de trabajo dividiendo tareas), qué es un cluster, qué es "procesar en paralelo".
- **Actividad:** demo en vivo — el facilitador corre un job distribuido y el grupo interactúa (cambia parámetros simples, observa el efecto en tiempo/recursos).
- **Entregable:** ninguno formal; quiz corto de conceptos.

### Sesión 3 — SQL para analítica a escala
- **Contenido:** BigQuery desde la consola web, cómo leer una consulta, qué es "particionar" una tabla (analogía de archivero), cómo se ve el costo de una consulta.
- **Lab guiado:** completar y ejecutar 4-5 consultas sobre un dataset ya preparado (no se escribe SQL desde cero, se modifica).
- **Entregable:** las consultas completadas + interpretación en una frase de qué responde cada una.

### Sesión 4 — Introducción a Spark
- **Contenido:** qué problema resuelve Spark que SQL no resuelve, vocabulario mínimo (DataFrame, transformación, acción) sin entrar a shuffle/optimización.
- **Lab guiado:** notebook "fill-in-the-blanks" — completar líneas específicas de un pipeline ya armado y observar el resultado.
- **Entregable:** notebook completado.

### Sesión 5 — Cómo se ve un pipeline de datos real
- **Contenido:** qué es un ETL, de dónde vienen los datos, a dónde van, quién los consume al final (dashboard, modelo, reporte).
- **Lab guiado:** armar un flujo simple con una herramienta low-code/no-code o notebook muy asistido, con apoyo técnico 1:1.
- **Entregable:** diagrama del flujo armado + captura del resultado.

### Sesión 6 — Data Lakes y gobierno del dato
- **Contenido:** qué es un data lake explicado para negocio (bodega vs archivero organizado), arquitectura medallion en términos simples (datos crudos → limpios → listos para usar), por qué el gobierno del dato importa.
- **Actividad:** caso de estudio de una falla real por mal manejo de datos (costo de negocio, no técnico) y discusión en grupo.
- **Entregable:** ninguno formal.

### Sesión 7 — Datos en tiempo real
- **Contenido:** diferencia entre batch y tiempo real explicada con ejemplos (reporte mensual vs detección de fraude en el momento), qué trade-offs implica (costo, complejidad) optar por tiempo real.
- **Actividad:** demo guiada de un flujo de eventos simple, el grupo identifica en qué parte de su negocio aplicaría.
- **Entregable:** ninguno formal.

### Sesión 8 — Costos, gobernanza y cómo evaluar un proyecto de datos
- **Contenido:** cómo se cobra la nube (por uso, por hora, por almacenamiento), qué preguntas hacer para evitar sorpresas de costo, framework simple para evaluar una propuesta técnica de su equipo (arquitectura, costo, riesgo, tiempo).
- **Taller:** aplicar el framework a un caso ficticio en equipos.
- **Entregable:** framework aplicado al caso ficticio.

### Sesión 9 — Presentación de propuestas
- **Actividad principal:** cada participante o equipo presenta una **propuesta de arquitectura con caso de negocio** (10 min c/u) para un problema real de su área: qué se necesita, por qué, costo aproximado y riesgos.
- **Cierre:** retroalimentación cruzada, mapa de siguientes pasos (para quien quiera profundizar técnicamente, mención del track de Maestría).

---

## 5. Evaluación

| Componente | Peso |
|---|---|
| Entregables guiados (Sesiones 1, 3, 4, 5, 8) | 40% |
| Participación en discusiones y casos | 20% |
| Propuesta final (arquitectura + caso de negocio + presentación) | 40% |

**Criterios de la propuesta final:** debe identificar (1) el problema de negocio y por qué justifica Big Data, (2) un esquema de arquitectura a nivel conceptual (qué componentes, no necesariamente código), (3) una estimación de costo/beneficio, y (4) riesgos y consideraciones de gobernanza. No se evalúa código productivo.

---

## 6. Notas de facilitación

- El error más común en este track es que el facilitador "se emocione" y profundice en código — hay que resistir la tentación y mantener el nivel ejecutivo; quien quiera más profundidad, se le puede dirigir al track de Maestría.
- Los labs guiados funcionan mejor con apoyo técnico circulando en la sala (o breakout rooms con soporte), porque el grupo es heterogéneo y algunos se bloquean más rápido que otros.
- Priorizar ejemplos y casos del sector de los participantes (si el grupo es mayormente de banca/finanzas, usar esos casos) — aquí el enganche es la relevancia al negocio, no la elegancia técnica.
