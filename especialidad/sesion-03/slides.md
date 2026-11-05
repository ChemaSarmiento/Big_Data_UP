---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
  table { font-size: 0.8em; }
---

# Sesión 03
## SQL para analítica a escala

Especialidad — Big Data

---

## Mismo SQL, otra escala

El SQL que ya practicaste en el Módulo 0 (base pequeña, un solo servidor) es
**casi idéntico** al que vas a usar hoy en BigQuery (millones de filas,
distribuido).

Lo que cambia no es la sintaxis — es **cómo piensas el costo y el tamaño** del
dato que estás consultando.

---

## BigQuery desde el navegador — tres zonas

<div class="box">
<strong>[CAPTURA PENDIENTE]</strong> consola de BigQuery con las tres zonas marcadas — chema agrega el screenshot real aquí.
</div>

1. **El editor de consultas** — donde escribes/completas SQL
2. **El explorador de esquema** (panel izquierdo) — columnas y tipos de cada
   tabla, revísalo *antes* de escribir la consulta
3. <span class="accent">El estimador de bytes</span> — arriba a la derecha,
   antes de correr: te dice cuánto va a costar la consulta antes de ejecutarla

<div class="box">
Adivinar nombres de columna sin mirar el esquema primero es la forma #1 de
perder tiempo en una consulta.
</div>

---

## Cómo leer una consulta (en el orden real)

```
FROM     -- de qué tabla parto
WHERE    -- qué filas me quedo
GROUP BY -- cómo las agrupo
SELECT   -- qué muestro al final
ORDER BY -- en qué orden lo muestro
```

Aunque `SELECT` se escribe primero, es **lo último que sucede lógicamente**.
Leer de abajo hacia arriba (o ubicar primero `FROM`/`WHERE`) suele ser más
fácil que leer de arriba hacia abajo.

---

## Lo mismo, pero aplicado — tabla chiquita de 4 filas

| from_account | amount | is_suspicious |
|---|---|---|
| ACC-001 | 500 | false |
| ACC-002 | 12000 | true |
| ACC-001 | 300 | false |
| ACC-003 | 8000 | true |

Consulta: `SELECT from_account, SUM(amount) FROM t WHERE is_suspicious = true GROUP BY from_account`

1. **FROM** t → partimos de las 4 filas.
2. **WHERE** is_suspicious = true → quedan 2 filas (ACC-002, ACC-003).
3. **GROUP BY** from_account → cada cuenta ya es su propio grupo.
4. **SELECT** → `ACC-002: 12000`, `ACC-003: 8000`.

<div class="box">
Mismo orden que el slide anterior — aquí lo ves aplicado, no solo descrito.
</div>

---

## Cómo se ve el costo de una consulta

BigQuery cobra por **datos leídos**, no por tiempo de ejecución ni por filas
devueltas. Dos trampas comunes:

- `SELECT *` cuesta como si necesitaras **todas** las columnas — aunque tu
  análisis solo use 2 de 30 (BigQuery guarda cada columna por separado y solo
  lee las que pides)
- <span class="accent">`LIMIT 10` NO reduce el costo</span> — sigue escaneando
  las columnas pedidas de **toda** la tabla antes de recortar el resultado

---

# → Sesión 04

Introducción a Spark
