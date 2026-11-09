-- 1. Crear Silver con nombres limpios y tipos útiles. Bronze queda intacta.
CREATE OR REPLACE TABLE emergente_silver.precios_limpios AS
SELECT TRIM(producto) AS producto, TRIM(presentacion) AS presentacion,
 TRIM(marca) AS marca, TRIM(categoria) AS categoria,
 SAFE_CAST(precio AS NUMERIC) AS precio_mxn,
 SAFE_CAST(fechaRegistro AS DATE) AS fecha,
 TRIM(cadenaComercial) AS cadena_comercial,
 TRIM(nombreComercial) AS establecimiento,
 TRIM(estado) AS estado, TRIM(municipio) AS municipio,
 SAFE_CAST(latitud AS FLOAT64) AS latitud,
 SAFE_CAST(longitud AS FLOAT64) AS longitud
FROM emergente_bronze.entrada;

-- 2. Separar los registros que requieren revisión.
CREATE OR REPLACE TABLE emergente_silver.precios_para_revisar AS
SELECT * FROM emergente_silver.precios_limpios
WHERE producto IS NULL OR marca IS NULL OR presentacion IS NULL
 OR precio_mxn IS NULL OR precio_mxn<=0 OR fecha IS NULL;

-- 3. Revisar el conteo. Con la muestra: 4500 Silver y 0 para revisar.
SELECT (SELECT COUNT(*) FROM emergente_bronze.entrada) AS bronze,
 (SELECT COUNT(*) FROM emergente_silver.precios_limpios) AS silver,
 (SELECT COUNT(*) FROM emergente_silver.precios_para_revisar) AS revisar;
