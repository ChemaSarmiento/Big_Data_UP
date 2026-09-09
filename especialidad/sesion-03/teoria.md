# Teoría — Sesión 03: SQL para analítica a escala

> Hoy conectas dos cosas: el SQL que ya practicaste en el Módulo 0 (base pequeña,
> un solo servidor) y BigQuery (millones de filas, distribuido). El SQL que escribes
> es casi idéntico — lo que cambia es cómo piensas sobre el costo y el tamaño.

## 1. BigQuery desde la consola web

No necesitas instalar nada. La consola web de BigQuery tiene tres zonas que vas a usar
hoy:

- **El editor de consultas** — donde escribes/completas SQL.
- **El explorador de esquema** (panel izquierdo) — para ver qué tablas y columnas
  existen antes de escribir la consulta, en vez de adivinar.
- **El estimador de bytes** (arriba a la derecha del editor, antes de correr) — te
  dice cuánto va a costar la consulta *antes* de ejecutarla. Revisarlo es un hábito
  que vale la pena adoptar desde tu primera consulta.

## 2. Cómo leer una consulta

Una consulta SQL, sin importar qué tan larga se vea, se lee siempre en el mismo orden
lógico (no en el orden en que está escrita):

```
FROM   -- de qué tabla parto
WHERE  -- qué filas me quedo
GROUP BY -- cómo las agrupo
SELECT -- qué columnas/cálculos muestro al final
```

Aunque `SELECT` se escribe primero, es lo último que "sucede" lógicamente. Leer una
consulta ajena de abajo hacia arriba (o al menos, ubicando primero el `FROM` y el
`WHERE`) suele ser más fácil que leerla de arriba hacia abajo.

## 3. Qué es "particionar" una tabla

**Analogía del archivero:** imagina un archivero con miles de expedientes sueltos, sin
ningún orden — para encontrar los expedientes de enero, tendrías que revisar el
archivero completo. Ahora imagina el mismo archivero, pero con un cajón por mes —
buscar "los expedientes de enero" significa abrir un solo cajón, no revisar todo.

Eso es particionar una tabla: la tabla se organiza físicamente en pedazos (típicamente
por fecha), y una consulta que filtra por esa columna solo toca el pedazo relevante,
no la tabla completa. Es la diferencia entre revisar un cajón y revisar el archivero
entero — y en BigQuery, esa diferencia se traduce directamente en menos costo y menos
tiempo de espera.

## 4. Cómo se ve el costo de una consulta

BigQuery cobra por la cantidad de datos que la consulta lee, no por cuánto tiempo
tarda en correr, ni por cuántas filas devuelve. Dos consecuencias prácticas:

- `SELECT *` (traer todas las columnas) cuesta como si necesitaras todas las columnas,
  aunque tu análisis solo use 2 de 30 — porque BigQuery guarda cada columna por
  separado y solo lee las que pides.
- Una consulta sobre una tabla particionada, filtrando por la columna de partición,
  puede costar una fracción de la misma consulta sobre una tabla sin particionar —
  aunque el resultado final sea idéntico.

Antes de correr cada consulta de hoy, revisa el estimador de bytes en la esquina
superior derecha del editor — es la forma más directa de conectar esta teoría con lo
que vas a ver en pantalla.

---

## Referencias

- [BigQuery — primeros pasos desde la consola (guía oficial)](https://cloud.google.com/bigquery/docs/quickstarts/query-public-dataset-console)
- [BigQuery — Introduction to Partitioned Tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery — Estimating query costs](https://cloud.google.com/bigquery/docs/estimate-costs)
