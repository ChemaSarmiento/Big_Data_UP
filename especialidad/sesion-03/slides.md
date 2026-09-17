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

## Particionar: el archivero con un cajón por mes

Un archivero con miles de expedientes sueltos, sin orden → para encontrar los
de enero, revisas **todo** el archivero.

El mismo archivero, con **un cajón por mes** → buscar enero es abrir un solo
cajón.

<div class="box">
Eso es particionar una tabla: se organiza físicamente en pedazos (típicamente
por fecha). Una consulta que filtra por esa columna solo toca el pedazo
relevante — misma pregunta, misma respuesta, una fracción del costo.
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

# Lab guiado
## El dataset de hoy: NYC Taxi, 146 millones de viajes reales

`bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015` — público,
gratis, consultable ahora mismo. Mismo tipo de dato que alimenta decisiones
reales de movilidad urbana (Uber, ciudades inteligentes).

<div class="box">
Antes de cada consulta de hoy: mira el estimador de bytes en la esquina
superior derecha, no el botón de correr.
</div>

---

## Paso 1 — Calentamiento con SQL ya conocido

`recursos/sql-practica/employee_db_queries.sql`, secciones 1-2 — mismo tipo de
pregunta que ya viste en el Módulo 0, sobre una base pequeña, antes de saltar a
millones de filas.

---

## Paso 2 — Completa la consulta: ¿cuántos viajes hubo en enero?

```sql
SELECT COUNT(*) AS total_viajes
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE EXTRACT(MONTH FROM ___) = ___;
```

<div class="box">
Completa los espacios con tu pareja antes de correrla — no hace falta escribir
SQL nuevo desde cero, solo decidir qué va en cada espacio.
</div>

---

## Paso 3 — Tarifa promedio por número de pasajeros

```sql
SELECT passenger_count, ROUND(AVG(___), 2) AS tarifa_promedio
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE trip_distance > 0 AND fare_amount > 0
GROUP BY ___
ORDER BY ___;
```

**Deberías ver:** una fila por cada valor de `passenger_count` (0-9). Si sale
una fila con `passenger_count = 0`, es un dato real "sucio" — la veracidad de
la Sesión 1, en vivo.

---

## Paso 4 — ¿A qué hora se paga más propina?

```sql
SELECT EXTRACT(HOUR FROM pickup_datetime) AS hora_del_dia,
       ROUND(AVG(tip_amount), 2) AS propina_promedio
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE tip_amount > 0
GROUP BY hora_del_dia
ORDER BY hora_del_dia;
```

**Deberías ver:** 24 filas — identifica la hora pico leyendo la tabla, antes de
pasar a la gráfica.

---

## Paso 5 — Visualización, sin escribir código

1. Corre la consulta del Paso 4
2. Clic en **"Explorar con Looker Studio"** desde los resultados de BigQuery
3. Gráfico de barras — eje X: `hora_del_dia`, eje Y: `propina_promedio`

<div class="box">
Sin instalar nada, sin Python — es la ruta que un perfil de negocio usaría en
el trabajo real.
</div>

---

## Entregable de hoy

- Las 4 consultas completadas
- Una interpretación de una frase por consulta ("¿qué responde esto?")
- La visualización de Looker Studio

---

# → Sesión 04

Introducción a Spark
