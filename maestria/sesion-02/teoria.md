# Teoría — Sesión 02: SQL distribuido avanzado

> El objetivo de esta sesión no es "escribir SQL más complejo" — es entender qué pasa
> *adentro* de BigQuery cuando corres una consulta, para poder diseñar tablas y
> escribir queries que cuesten menos y respondan más rápido, en vez de optimizar a
> ciegas.

## 1. Motor de ejecución de BigQuery

BigQuery no es "una base de datos grande" — es un motor de consultas distribuido
diseñado desde cero para escalar horizontalmente (arquitectura Dremel, el sistema
interno de Google en el que se basa). Tres decisiones de diseño que explican su
comportamiento:

- **Almacenamiento columnar.** En vez de guardar cada fila completa junta (como una
  base de datos transaccional tradicional), BigQuery guarda cada columna por separado.
  Si tu consulta solo necesita 3 de 50 columnas, BigQuery físicamente solo lee esas 3
  — no toca las otras 47. Esto es la razón #1 por la que `SELECT *` es mala práctica
  aquí: cuesta y tarda como si necesitaras todas las columnas, aunque tu análisis solo
  use unas cuantas.
- **Separación de almacenamiento y cómputo.** Los datos viven en Colossus (el sistema
  de archivos distribuido de Google); el cómputo lo hacen miles de máquinas
  temporalmente asignadas a tu consulta. Puedes escalar cómputo sin mover datos.
- **Ejecución en árbol (tree architecture).** Una consulta se reparte hacia miles de
  "hojas" que procesan en paralelo, y los resultados se agregan hacia arriba en
  varios niveles — no es un solo nivel de map/reduce, es un árbol de agregación.

## 2. Particionamiento y clustering

Dos técnicas complementarias para que BigQuery escanee menos datos de los que tiene:

- **Particionamiento:** divide una tabla en segmentos físicos según una columna
  (típicamente fecha). `WHERE fecha = '2026-01-01'` sobre una tabla particionada por
  fecha solo escanea la partición de ese día — no toda la tabla. Sin partición, esa
  misma consulta escanea *todo* el historial para filtrar después, ya tarde.
- **Clustering:** dentro de cada partición, ordena físicamente los datos según hasta 4
  columnas. Si filtras frecuentemente por `cliente_id` además de por fecha, clusterizar
  por `cliente_id` hace que BigQuery pueda saltarse bloques enteros de datos que no
  contienen ese cliente, sin necesitar una partición separada por cliente (que sería
  poco práctico con millones de clientes distintos).

`recursos/hive/hive-queries.sql` Sección 3 demuestra el mismo principio en Hive (no
BigQuery, pero la lógica de partition pruning es idéntica) sobre datos reales de
carpetas de investigación de la FGJ CDMX — comparar el tiempo de la consulta sin
particionar (3.1) contra la particionada (3.2/3.3) hace tangible la diferencia antes
de aplicarlo en BigQuery.

## 3. Costo: bytes escaneados vs. slots reservados

BigQuery tiene dos modelos de precio, y confundirlos lleva a sorpresas de facturación:

| Modelo | Cómo se cobra | Cuándo conviene |
|---|---|---|
| **On-demand** (bytes escaneados) | Por TB de datos que la consulta realmente lee (columnar + partition pruning reducen esto) | Uso esporádico, cargas de trabajo impredecibles |
| **Capacity-based** (slots reservados) | Por unidades de cómputo (slots) reservadas por adelantado, sin importar cuántos bytes se escaneen | Uso constante y predecible — puede ser más barato a volumen alto |

Para este curso (free tier, 1TB de consultas/mes), estás en el modelo on-demand — cada
byte escaneado de más (por un `SELECT *` innecesario, o una tabla sin particionar)
consume directamente ese presupuesto mensual. `EXPLAIN` o el estimador de bytes de la
consola (antes de correr la consulta) te dice el costo *antes* de ejecutar — hábito
que vale la pena adoptar desde ahora.

## 4. Window functions anidadas y CTEs recursivos

Ya viste window functions básicas en el Módulo 0. Aquí la complejidad sube en dos
direcciones:

- **Anidadas:** una window function que usa el resultado de otra. Por ejemplo, calcular
  un ranking (`RANK() OVER (...)`) y luego, sobre ese ranking, calcular un promedio
  móvil de los primeros N — requiere una subconsulta o CTE porque no puedes anidar
  window functions directamente en la misma cláusula `SELECT`.
- **CTEs recursivos** (`WITH RECURSIVE`): para resolver jerarquías que no tienen un
  número fijo de niveles — por ejemplo, una cadena de referidos donde cada cliente
  refirió a otro, sin límite de profundidad. Una CTE recursiva se define en términos
  de sí misma: un caso base (el primer nivel) + un paso que se repite hasta que no
  quedan más filas que agregar.

```sql
-- Ejemplo: cadena de referidos (jerarquía sin profundidad fija)
WITH RECURSIVE cadena_referidos AS (
  SELECT cliente_id, referido_por, 1 AS nivel
  FROM clientes
  WHERE referido_por IS NULL  -- caso base: los que no fueron referidos por nadie

  UNION ALL

  SELECT c.cliente_id, c.referido_por, cr.nivel + 1
  FROM clientes c
  JOIN cadena_referidos cr ON c.referido_por = cr.cliente_id
)
SELECT * FROM cadena_referidos ORDER BY nivel;
```

---

## Referencias

- [BigQuery — Query Execution Explained (docs oficiales, arquitectura Dremel)](https://cloud.google.com/bigquery/docs/query-overview)
- [BigQuery — Introduction to Partitioned Tables](https://cloud.google.com/bigquery/docs/partitioned-tables)
- [BigQuery — Introduction to Clustered Tables](https://cloud.google.com/bigquery/docs/clustered-tables)
- [BigQuery — On-demand vs. capacity pricing](https://cloud.google.com/bigquery/pricing)
- [BigQuery — Recursive CTEs (standard SQL)](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#recursive_cte)
- [Melnik et al. — Dremel: Interactive Analysis of Web-Scale Datasets (el paper detrás de BigQuery)](https://research.google/pubs/dremel-interactive-analysis-of-web-scale-datasets-2/)
