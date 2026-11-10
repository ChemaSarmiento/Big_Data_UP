-- 1. Crear Silver con nombres limpios y tipos útiles. Bronze queda intacta.
-- direccion se conserva: sin ella, dos tiendas distintas con el mismo
-- nombre comercial en el mismo municipio se verían como una sola en Gold.
CREATE OR REPLACE TABLE emergente_silver.precios_limpios AS
SELECT TRIM(producto) AS producto, TRIM(presentacion) AS presentacion,
 TRIM(marca) AS marca, TRIM(categoria) AS categoria,
 SAFE_CAST(precio AS NUMERIC) AS precio_mxn,
 SAFE_CAST(fechaRegistro AS DATE) AS fecha,
 TRIM(cadenaComercial) AS cadena_comercial,
 TRIM(nombreComercial) AS establecimiento,
 TRIM(direccion) AS direccion,
 TRIM(estado) AS estado, TRIM(municipio) AS municipio,
 SAFE_CAST(latitud AS FLOAT64) AS latitud,
 SAFE_CAST(longitud AS FLOAT64) AS longitud
FROM emergente_bronze.entrada;

-- 2. Separar los registros que requieren revisión.
CREATE OR REPLACE TABLE emergente_silver.precios_para_revisar AS
SELECT * FROM emergente_silver.precios_limpios
WHERE producto IS NULL OR marca IS NULL OR presentacion IS NULL
 OR precio_mxn IS NULL OR precio_mxn<=0 OR fecha IS NULL;

-- 3. Revisar el conteo. En lo observado: 4500 en Silver y 0 para revisar.
SELECT (SELECT COUNT(*) FROM emergente_bronze.entrada) AS bronze,
 (SELECT COUNT(*) FROM emergente_silver.precios_limpios) AS silver,
 (SELECT COUNT(*) FROM emergente_silver.precios_para_revisar) AS revisar;

-- 4. Qué podríamos revisar: filas que, ya limpias, quedan idénticas en
-- todos sus campos. TRIM/SAFE_CAST no las detecta -- solo agrupar sí.
-- Si aparecieran, un conteo posterior (por ejemplo, Gold) se duplicaría
-- sin que nada lo avise.
SELECT producto, marca, presentacion, precio_mxn, fecha, establecimiento,
 direccion, COUNT(*) AS veces_repetida
FROM emergente_silver.precios_limpios
GROUP BY producto, marca, presentacion, precio_mxn, fecha, establecimiento, direccion
HAVING COUNT(*) > 1;
-- Vacío en lo observado: no encontramos filas idénticas repetidas aquí.

-- 5. Qué podríamos revisar: POR QUÉ se rechazó cada fila, no solo cuántas.
-- Un solo conteo (bloque 3) no distingue si el problema es el precio, la
-- fecha o un campo de texto vacío -- este desglose sí.
SELECT
 COUNTIF(producto IS NULL) AS sin_producto,
 COUNTIF(marca IS NULL) AS sin_marca,
 COUNTIF(presentacion IS NULL) AS sin_presentacion,
 COUNTIF(precio_mxn IS NULL) AS precio_no_convertible,
 COUNTIF(precio_mxn IS NOT NULL AND precio_mxn<=0) AS precio_no_positivo,
 COUNTIF(fecha IS NULL) AS fecha_no_convertible
FROM emergente_silver.precios_limpios;
-- En lo observado: todo en cero. Si algo sube, aquí está el motivo exacto,
-- no solo el total.

-- 6. Qué podríamos revisar: ¿el periodo que creemos tener es el que
-- de verdad hay? Bronze no lo dice; aquí sí se puede comprobar.
SELECT MIN(fecha) AS fecha_minima, MAX(fecha) AS fecha_maxima
FROM emergente_silver.precios_limpios;
-- En lo observado: 2011-01-10 a 2015-12-09 -- tres años sin continuidad,
-- no una serie diaria completa. No asumas cobertura entre esas fechas.

-- 7. Qué podríamos revisar: ¿un precio aceptado es creíble para ESE
-- producto, no solo distinto de cero? all_data mezcla categorías de
-- precio muy distinto (refrescos vs. televisores) -- un límite fijo
-- sin categoría marca como "sospechoso" algo que es real.
SELECT categoria, MIN(precio_mxn) AS precio_minimo, MAX(precio_mxn) AS precio_maximo,
 COUNT(*) AS filas
FROM emergente_silver.precios_limpios
GROUP BY categoria
ORDER BY precio_maximo DESC
LIMIT 5;
-- En lo observado: los precios más altos (hasta 13497) son televisores,
-- lavadoras y refrigeradores reales -- no errores de captura. Un filtro
-- "precio > 10000" sin categoría los marcaría como sospechosos por error.
