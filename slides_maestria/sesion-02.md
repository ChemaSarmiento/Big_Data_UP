---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Sesión 02 — SQL distribuido avanzado"
info: |
  Maestría en Ciencia de Datos — Big Data
  Sesión 02: BigQuery, particionamiento, costo, window functions
---

# Sesión 02
## SQL distribuido avanzado

<div class="pt-6 text-sm opacity-60">
No es "SQL más complejo" — es entender qué pasa adentro para no optimizar a ciegas
</div>

---

# BigQuery no es "una base de datos grande"

Está diseñado desde cero para escalar horizontalmente (arquitectura Dremel).
Tres decisiones de diseño explican su comportamiento:

<v-clicks>

- **Almacenamiento columnar** — cada columna se guarda por separado
- **Separación de storage y cómputo** — puedes escalar cómputo sin mover datos
- **Ejecución en árbol** — miles de "hojas" procesan en paralelo, resultados se agregan hacia arriba

</v-clicks>

<div class="grid grid-cols-2 gap-6 mt-4">
<div>
<div class="text-sm font-bold opacity-70 mb-2">Tradicional (por fila)</div>
<div class="p-3 border rounded bg-gray-500/10 text-sm">id, nombre, monto, fecha...</div>
</div>
<div>
<div class="text-sm font-bold opacity-70 mb-2">BigQuery (columnar)</div>
<div class="flex gap-2">
<div class="p-3 border rounded bg-yellow-500/10 text-sm">id</div>
<div class="p-3 border rounded bg-yellow-500/10 text-sm">nombre</div>
<div class="p-3 border rounded bg-yellow-500/10 text-sm">monto</div>
<div class="p-3 border rounded bg-yellow-500/10 text-sm">fecha</div>
</div>
</div>
</div>

<div v-click class="mt-4 text-xl">
<code>SELECT *</code> cuesta como si necesitaras todas las columnas — aunque uses 3 de 50
</div>

---

# Particionamiento: el archivero con un cajón por mes

<v-clicks>

- Sin partición: `WHERE fecha = '2026-01-01'` escanea **toda** la tabla
- Con partición por fecha: solo abre el cajón de ese día
- **Clustering** (hasta 4 columnas): ordena físicamente *dentro* de cada partición — salta bloques enteros sin necesitar partición separada

</v-clicks>

<div v-click class="mt-8 p-4 border-l-4 border-blue-500">
recursos/hive/hive-queries.sql Sección 3 — compara el tiempo real, sin particionar (3.1) vs particionada (3.2/3.3), sobre datos de la FGJ CDMX
</div>

---

# Dos formas de pagar, y confundirlas sale caro

| Modelo | Se cobra por | Conviene si... |
|---|---|---|
| **On-demand** | TB escaneados | Uso esporádico (este curso) |
| **Capacity-based** | Slots reservados | Uso constante y predecible |

<div v-click class="mt-8 text-blue-500 font-bold">
Cada byte de más (por un SELECT * innecesario) sale directo de tu presupuesto mensual de 1TB
</div>

<div v-click class="mt-4 text-sm opacity-70">
El estimador de bytes de la consola te dice el costo ANTES de ejecutar — hábito a construir desde hoy
</div>

---

# Window functions anidadas + CTEs recursivos

```sql {1-8|10-18}
-- Window function: ranking dentro de cada grupo
SELECT sucursal, tipo_transaccion, monto,
       RANK() OVER (
         PARTITION BY tipo_transaccion
         ORDER BY monto DESC
       ) AS ranking
FROM transacciones;

-- CTE recursiva: jerarquía sin profundidad fija
WITH RECURSIVE cadena_referidos AS (
  SELECT cliente_id, referido_por, 1 AS nivel
  FROM clientes WHERE referido_por IS NULL
  UNION ALL
  SELECT c.cliente_id, c.referido_por, cr.nivel + 1
  FROM clientes c
  JOIN cadena_referidos cr ON c.referido_por = cr.cliente_id
)
SELECT * FROM cadena_referidos ORDER BY nivel;
```

<div class="mt-2 text-sm opacity-70">
Una CTE recursiva se define en términos de sí misma: un caso base + un paso que se repite hasta que no quedan más filas
</div>

---
layout: center
class: text-center
---

# Lab de hoy

Sobre datos reales de Carpetas de investigación de la FGJ CDMX

---

# Paso 1 — Rediseñar una tabla mal particionada

```sql
-- 3.1: escanea toda la tabla
SELECT delito, COUNT(*) FROM carpetas_investigacion_sin_particion
WHERE anio = 2024 GROUP BY delito;

-- 3.2: solo la partición de 2024
SELECT delito, COUNT(*) FROM carpetas_investigacion_particionada
WHERE anio = 2024 GROUP BY delito;
```

<div class="mt-6 p-3 border-l-4 border-blue-500 text-sm text-left">
<b>Deberías ver:</b> el mismo resultado, con una diferencia notable en bytes
procesados. Anota el número exacto de cada una — es la base del reporte.
</div>

---

# Paso 2 — Completar window functions y CTEs

Mismo estilo de las diapositivas anteriores, pero ahora las escribes tú —
sobre `transacciones`, con el ranking por tipo de transacción, y la cadena de
referidos completa.

---

# Paso 3 — La gráfica del entregable

```python
import matplotlib.pyplot as plt
plt.bar(["Sin particionar", "Particionada"], [bytes_sin, bytes_con])
plt.ylabel("Bytes escaneados")
plt.show()
```

<div class="mt-6 p-4 border-l-4 border-blue-500 font-bold">
Entregable: reporte antes/después + la gráfica de barras + las consultas de window functions/CTEs completadas
</div>

---
layout: center
class: text-center
---

# → Sesión 03

Spark Core avanzado I — Catalyst, tipos de shuffle, y cómo leer un plan de ejecución
