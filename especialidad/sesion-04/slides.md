---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 04
## Introducción a Spark

Especialidad — Big Data

---

# ¿Qué hace Spark que SQL no hace?

BigQuery es excelente para filtros, agregaciones, joins.

Pero no cubre bien: lógica de negocio compleja, machine learning, combinar fuentes muy distintas en un mismo flujo.

<span class="accent">Spark: más flexible, a cambio de más líneas de código.</span>

---

# Tres palabras, nada más

- **DataFrame** — una tabla, como en BigQuery o Excel
- **Transformación** — describe qué quieres hacer (*no se ejecuta todavía*)
- **Acción** — dispara la ejecución real (`.show()`, `.count()`)

---

# Por qué un notebook "no hace nada" y de repente tarda

Spark solo *planea* con cada transformación.

Al llegar a una acción, ejecuta **todo el plan acumulado** de una vez — por eso esa celda parece tardar más.

---

# Lo que no vemos hoy, a propósito

*Shuffle*, optimización de planes de ejecución — eso es Maestría, un track técnico completo.

Con reconocer la palabra "shuffle" como "mover datos entre máquinas, y que cuesta", basta para este track.

---

# Lab guiado

Notebook "fill-in-the-blanks" — completar líneas de un pipeline ya armado sobre el catálogo de precios PROFECO.

**Entregable:** notebook completado.

---

# → Sesión 05

Cómo se ve un pipeline de datos real
