---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 03
## SQL para analítica a escala

Especialidad — Big Data

---

# Mismo SQL, otra escala

El SQL que ya practicaste (base pequeña, un servidor) es casi idéntico al de hoy (BigQuery, millones de filas).

Lo que cambia: **cómo piensas el costo y el tamaño.**

---

# BigQuery desde el navegador — tres zonas

1. El editor de consultas
2. El explorador de tablas y columnas
3. <span class="accent">El estimador de bytes — revísalo antes de correr</span>

---

# Cómo leer una consulta (en el orden real)

```
FROM     -- de qué tabla parto
WHERE    -- qué filas me quedo
GROUP BY -- cómo las agrupo
SELECT   -- qué muestro al final
```

Aunque `SELECT` se escribe primero, es lo último que sucede.

---

# Particionar: el archivero con un cajón por mes

Sin particionar → revisas el archivero completo para encontrar enero.

Particionado por mes → abres un solo cajón.

**Misma pregunta, mismo resultado — una fracción del costo.**

---

# Cómo se ve el costo de una consulta

BigQuery cobra por **datos leídos**, no por tiempo ni por filas devueltas.

- `SELECT *` cuesta como si necesitaras todo — aunque uses 2 de 30 columnas
- Filtrar por la columna de partición puede costar una fracción de lo mismo sin particionar

---

# Lab guiado

4-5 consultas sobre un dataset ya preparado (NYC Taxi, en BigQuery) — se completan, no se escriben desde cero.

**Entregable:** consultas completadas + una interpretación de una frase cada una + **una visualización** (Looker Studio, sin código).

---

# → Sesión 04

Introducción a Spark
