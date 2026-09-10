# Facilitación — Sesión 02: SQL distribuido avanzado

> Guion de 3 horas: talking points + lab guiado. Sin cluster hoy — todo corre en
> BigQuery desde el navegador. Aprovecha eso para un ritmo más rápido que la
> Sesión 1.

## Antes de empezar (facilitador)

Verifica acceso a `bigquery-public-data.new_york_taxi_trips` y a
`carpetas_investigacion` (Hive) antes de la sesión — ambos deben responder sin
configuración adicional.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "BigQuery no es 'una base de datos grande' — está diseñado desde cero para
> escalar horizontalmente, basado en un sistema interno de Google llamado
> Dremel. Hoy vamos a entender ese diseño lo suficiente para escribir consultas
> que cuesten una fracción de lo que costarían sin pensar en ello."

**Pregunta de apertura:**

> "¿Alguna vez han corrido una consulta que tardó mucho más de lo esperado, sin
> saber por qué? Guarden esa experiencia — hoy vamos a tener el vocabulario para
> diagnosticarla."

**Ejemplo de actualidad:**

> "Empresas como Spotify o Shopify corren miles de consultas analíticas diarias
> sobre BigQuery a esta escala — la diferencia entre una consulta bien y mal
> diseñada ahí no es de segundos, es de miles de dólares al mes."

---

## Bloque 2 — Teoría (0:15–1:00, 45 min)

### Motor de ejecución columnar (15 min)

> "Si les pidiera el promedio de una sola columna de una tabla de 50 columnas,
> ¿cuánto de la tabla creen que hay que leer?"

Deja que asuman "toda la fila" antes de explicar columnar storage — el contraste
es lo que hace memorable el concepto.

### Particionamiento y clustering (15 min)

Demo en vivo con las dos consultas de `teoria.md` — correr ambas, mostrar el
estimador de bytes de cada una **antes** de ejecutar. El contraste visual (una
consulta estima 50GB, la otra 2GB) vale más que la explicación.

### Costo: on-demand vs. capacity (10 min)

Pregunta directa: **"¿Cuál de los dos modelos conviene para este curso, con
1TB/mes gratis?"** (respuesta: on-demand, porque el uso es esporádico — no
justifica reservar slots).

### Window functions anidadas y CTEs recursivas (5 min)

Solo plantea el patrón — se practica en el lab.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Rediseñar una tabla mal particionada (40 min)

Sobre `recursos/hive/hive-queries.sql` Sección 3: correr 3.1 (sin particionar) y
3.2/3.3 (particionada) sobre Carpetas de investigación FGJ CDMX, comparando
tiempo real.

```sql
-- 3.1: escanea toda la tabla
SELECT delito, COUNT(*) FROM carpetas_investigacion_sin_particion
WHERE anio = 2024 GROUP BY delito;

-- 3.2: solo la partición de 2024
SELECT delito, COUNT(*) FROM carpetas_investigacion_particionada
WHERE anio = 2024 GROUP BY delito;
```

**Deberías ver:** el mismo resultado, con una diferencia notable en bytes
procesados (visible en el job de BigQuery/Hive). Pide a cada pareja que anote
el número exacto antes de seguir — es la base del "reporte antes/después" del
entregable.

### Paso 2 — Window functions y CTEs recursivas (35 min)

Completar en vivo, con el grupo dictando qué va en cada espacio (mismo estilo
que Especialidad, pero sin el nivel de guía — aquí escriben ellos):

```sql
SELECT sucursal, tipo_transaccion, monto,
       RANK() OVER (PARTITION BY tipo_transaccion ORDER BY monto DESC) AS ranking
FROM transacciones;
```

Después, la CTE recursiva de `teoria.md` (cadena de referidos) — es la parte
más nueva para la mayoría, dale los 15 minutos completos.

### Paso 3 — La gráfica del entregable (15 min)

```python
import matplotlib.pyplot as plt
plt.bar(["Sin particionar", "Particionada"], [bytes_sin, bytes_con])
plt.ylabel("Bytes escaneados")
plt.show()
```

**Deberías ver:** una diferencia visual clara. Si los números salen parecidos,
revisar que la consulta 3.1 realmente no esté usando la columna de partición en
el `WHERE` — error común de copiar/pegar mal la consulta base.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** reporte de optimización antes/después + la gráfica de
barras + las consultas de window functions/CTEs completadas.

**Puente a la Sesión 3:**

> "Hoy optimizamos consultas SQL. La próxima sesión hacemos lo mismo pero para
> Spark — el mismo principio (leer menos, mover menos datos) aplicado a un
> motor distinto."

---

## Notas de costo GCP

- Esta sesión no usa cluster — todo el costo es de consultas BigQuery, dentro
  del 1TB/mes gratis. Aun así, recuérdales revisar el estimador de bytes antes
  de cada consulta — es el hábito que están construyendo, no solo el resultado
  de hoy.
