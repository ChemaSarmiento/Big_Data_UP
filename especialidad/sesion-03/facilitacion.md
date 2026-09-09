# Facilitación — Sesión 03: SQL para analítica a escala

> Guion de 3 horas: talking points + lab guiado. Nada de código se escribe desde
> cero — se completa y se corre. El objetivo es que el grupo *sienta* la diferencia
> entre una base pequeña y 1,400+ millones de filas reales, no que memorice sintaxis.

## Antes de empezar (facilitador)

Verifica que el proyecto de GCP del grupo tenga acceso a datasets públicos de
BigQuery (viene por default, pero confírmalo con una consulta de prueba tú mismo
antes de la sesión):

```sql
SELECT COUNT(*) FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`;
```

Si esto corre para ti, corre para el grupo — no depende de ningún bucket propio.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Hoy vamos a consultar una tabla real de la Ciudad de Nueva York: **146 millones de
> viajes en taxi**, un año completo, con hora, ubicación, tarifa y propina de cada
> uno. Está pública, gratis, y la vamos a consultar en segundos — no porque el
> dataset sea pequeño, sino porque BigQuery está diseñado exactamente para esto."

**Pregunta de apertura (2 min en parejas):**

> "Si yo les preguntara 'a qué hora del día se dan más propinas altas en Nueva York',
> ¿cómo lo resolverían con las herramientas que ya conocen — Excel, por ejemplo?"

Deja que se den cuenta solos de que 146 millones de filas rompe Excel (límite real:
1,048,576 filas por hoja). **Ese es el gancho — no lo digas tú, que lo encuentren.**

**Ejemplo de actualidad:**

> "Este mismo tipo de análisis — patrones de movilidad urbana a partir de datos de
> transporte — es la base de cómo Uber y las ciudades inteligentes deciden dónde
> poner carriles exclusivos o ajustar precios dinámicos. El dataset que van a tocar
> hoy es del mismo tipo de dato que alimenta esas decisiones reales."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

Sigue `teoria.md` como contenido; aquí el cómo darlo en vivo.

### BigQuery desde la consola (10 min)

Comparte pantalla y navega en vivo — no lo describas, muéstralo:

1. Abre la consola de BigQuery
2. Busca `bigquery-public-data` en el explorador → `new_york_taxi_trips` →
   `tlc_yellow_trips_2015`
3. Señala el ícono de esquema (columnas) **antes** de escribir una sola consulta

**Talking point:** "Antes de escribir cualquier consulta, siempre miren el esquema
primero — adivinar nombres de columna es la forma #1 de perder tiempo."

### Cómo leer una consulta (10 min)

Escribe esta consulta vacía en el editor y pide al grupo que identifique cada
cláusula antes de correrla:

```sql
SELECT passenger_count, AVG(tip_amount) AS propina_promedio
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE trip_distance > 0
GROUP BY passenger_count
ORDER BY passenger_count;
```

**Pregunta:** "¿En qué orden se ejecuta esto realmente, aunque `SELECT` esté
primero?" (Respuesta: `FROM` → `WHERE` → `GROUP BY` → `SELECT` → `ORDER BY`.)

### Particionar: la demo que hace la teoría tangible (15 min)

**No te quedes en la analogía del archivero — muéstrala con números reales.** Corre
estas dos consultas en vivo, una tras otra, y que el grupo lea el estimador de bytes
antes de ejecutar cada una:

```sql
-- Consulta 1: sin filtro de fecha, sobre TODA la tabla de 2015
SELECT COUNT(*) FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE EXTRACT(MONTH FROM pickup_datetime) = 1;
```

```sql
-- Consulta 2: misma pregunta, pero sobre una tabla ya separada por año/mes
-- (las tablas tlc_yellow_trips_20XX YA están particionadas por año como tablas separadas)
SELECT COUNT(*) FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
TABLESAMPLE SYSTEM (1 PERCENT);
```

**Talking point mientras miran el estimador de bytes de cada una:**

> "Fíjense en la esquina superior derecha antes de darle correr. Ese número — no el
> tiempo que tarda — es lo que están a punto de pagar. Acostúmbrense a mirarlo
> siempre antes del botón de correr, no después."

### Costo de una consulta (10 min)

Corre esta y compárala en vivo contra una versión con `SELECT *`:

```sql
-- Cara: trae todas las columnas
SELECT * FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015` LIMIT 10;

-- Barata: solo las que necesitas
SELECT pickup_datetime, fare_amount FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015` LIMIT 10;
```

**Nota importante para ti:** el `LIMIT` no reduce el costo en BigQuery — sigue
escaneando las columnas pedidas de toda la tabla antes de recortar el resultado.
Es un error común asumir que `LIMIT 10` es barato. Acláralo explícitamente, es
una de las confusiones más comunes de quien viene de SQL tradicional.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Calentamiento — sql-practica (15 min)

Antes de ir a datos masivos, repasar sobre `test_db` (secciones 1-3 de
`recursos/sql-practica/employee_db_queries.sql`) — mismo tipo de pregunta, base
pequeña. Es la transición explícita del Módulo 0 a hoy.

### Consultas guiadas sobre NYC Taxi (60 min)

Completa cada `___` con el grupo — no las escribas tú, pide voluntarios que
propongan qué va en el espacio en blanco:

**1. Exploración — ¿cuántos viajes hay en enero de 2015?**
```sql
SELECT COUNT(*) AS total_viajes
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE EXTRACT(MONTH FROM ___) = ___;
```

**2. Filtro + agregación — ¿cuál es la tarifa promedio por número de pasajeros?**
```sql
SELECT passenger_count, ROUND(AVG(___), 2) AS tarifa_promedio
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE trip_distance > 0 AND fare_amount > 0
GROUP BY ___
ORDER BY ___;
```
**Deberías ver:** una fila por cada valor de `passenger_count` (0-9), con la tarifa
promedio subiendo levemente con más pasajeros. Si sale una fila con `passenger_count
= 0`, es un dato real "sucio" — buen momento para mencionar veracidad (Sesión 1).

**3. Patrón temporal — ¿a qué hora del día se paga más propina en promedio?**
```sql
SELECT EXTRACT(HOUR FROM pickup_datetime) AS hora_del_dia,
       ROUND(AVG(___), 2) AS propina_promedio
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
WHERE tip_amount > 0
GROUP BY ___
ORDER BY hora_del_dia;
```
**Deberías ver:** 24 filas. Pide al grupo que identifique la hora pico *antes* de
pasar a la visualización — que lo encuentren leyendo la tabla, no solo la gráfica.

**4. Comparación — ¿pago con tarjeta da más propina que pago en efectivo?**
```sql
SELECT
  CASE WHEN payment_type = '1' THEN 'Tarjeta' ELSE 'Efectivo/Otro' END AS metodo,
  ROUND(AVG(tip_amount), 2) AS propina_promedio,
  COUNT(*) AS num_viajes
FROM `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2015`
GROUP BY metodo;
```
**Talking point sobre el resultado:** casi toda la propina reportada va a estar en
"Tarjeta" — pregunta al grupo *por qué* antes de explicar (efectivo casi nunca se
reporta en el sistema del taxímetro, es una limitación real del dato, no del
análisis — conecta con "veracidad" de la Sesión 1).

### Visualización — Looker Studio (15 min)

Con la consulta 3 (propina por hora) ya corrida:

1. Clic en **"Explorar con Looker Studio"** desde los resultados de BigQuery
2. Elegir gráfico de barras — eje X: `hora_del_dia`, eje Y: `propina_promedio`
3. Sin escribir código — arrastrar y soltar

**Entregable de hoy:** las 4 consultas completadas + interpretación de una frase cada
una + esta visualización.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Pregunta de cierre:**

> "Volviendo a la pregunta de apertura — ¿cómo se sintió resolver esto sobre 146
> millones de filas comparado con lo que imaginaron al inicio con Excel?"

**Puente a la Sesión 4:**

> "Hoy le hicimos preguntas a un dato que ya estaba en una tabla lista. La próxima
> sesión vemos qué pasa cuando el dato *no* llega así de ordenado — ahí es donde
> entra Spark."

---

## Notas de costo GCP

- Los datasets `bigquery-public-data` **no cuentan contra el almacenamiento** del
  proyecto — solo contra la cuota de consulta (1TB/mes gratis, on-demand).
- `tlc_yellow_trips_2015` completa son ~26GB — una sola consulta con `SELECT *` sin
  filtro consume una fracción notable del 1TB mensual del grupo si cada persona la
  corre por separado. Recuérdalo antes del ejercicio de comparación `SELECT *`.
- Si el grupo es grande (15+), coordina que no todos corran las consultas más
  pesadas al mismo tiempo, más por cuota compartida de proyecto que por costo real.
