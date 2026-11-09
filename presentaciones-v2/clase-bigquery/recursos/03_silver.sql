-- Reconstrucción completa, reproducible: primera ruta docente, no actualización incremental.
-- Con el archivo entero, ensayar costo y duración antes de clase.
CREATE TEMP FUNCTION limpia(s STRING) AS (NULLIF(REGEXP_REPLACE(UPPER(TRIM(s)), r'\s+', ' '), ''));
CREATE TEMP TABLE unicas AS
SELECT * FROM emergente_bronze.observaciones
QUALIFY ROW_NUMBER() OVER(PARTITION BY fila_hash ORDER BY ingestado_en,lote_id)=1;
CREATE TEMP TABLE tipadas AS
SELECT fila_hash,lote_id,fuente_uri, producto AS producto_original,
 limpia(producto) AS producto, limpia(presentacion) AS presentacion,
 limpia(marca) AS marca, limpia(categoria) AS categoria, limpia(catalogo) AS catalogo,
 SAFE_CAST(precio AS NUMERIC) AS precio_mxn,
 SAFE_CAST(fechaRegistro AS DATETIME) AS fecha_hora_local,
 DATE(SAFE_CAST(fechaRegistro AS DATETIME)) AS fecha,
 limpia(cadenaComercial) AS cadena, limpia(nombreComercial) AS establecimiento,
 limpia(giro) AS giro, limpia(direccion) AS direccion,
 limpia(estado) AS estado, limpia(municipio) AS municipio,
 SAFE_CAST(latitud AS FLOAT64) AS latitud, SAFE_CAST(longitud AS FLOAT64) AS longitud
FROM unicas;
CREATE TEMP TABLE clasificadas AS
SELECT *, CASE
 WHEN fecha IS NULL THEN 'fecha_invalida'
 WHEN precio_mxn IS NULL OR precio_mxn<=0 THEN 'precio_invalido'
 WHEN producto IS NULL OR marca IS NULL OR presentacion IS NULL THEN 'producto_incompleto'
 WHEN establecimiento IS NULL OR direccion IS NULL OR estado IS NULL OR municipio IS NULL THEN 'tienda_incompleta'
 ELSE NULL END AS motivo
FROM tipadas;
CREATE OR REPLACE TABLE emergente_silver.rechazadas AS
SELECT * FROM clasificadas WHERE motivo IS NOT NULL;
CREATE OR REPLACE TABLE emergente_silver.precios
PARTITION BY DATE_TRUNC(fecha, MONTH)
CLUSTER BY estado,municipio,producto,marca
OPTIONS(require_partition_filter=true) AS
SELECT * EXCEPT(motivo),
 TO_HEX(SHA256(TO_JSON_STRING(STRUCT(producto,marca,presentacion)))) AS producto_id,
 TO_HEX(SHA256(TO_JSON_STRING(STRUCT(cadena,establecimiento,direccion,estado,municipio)))) AS tienda_id
FROM clasificadas WHERE motivo IS NULL;
-- Línea base de rendimiento SOLO para taller: misma Silver, sin partición ni clustering.
-- Duplica almacenamiento temporalmente. Expira en7 días; retirar al terminar comparación.
CREATE OR REPLACE TABLE emergente_silver.precios_plana AS
SELECT * EXCEPT(motivo),
 TO_HEX(SHA256(TO_JSON_STRING(STRUCT(producto,marca,presentacion)))) AS producto_id,
 TO_HEX(SHA256(TO_JSON_STRING(STRUCT(cadena,establecimiento,direccion,estado,municipio)))) AS tienda_id
FROM clasificadas WHERE motivo IS NULL;
CREATE OR REPLACE TABLE emergente_silver.control AS
SELECT (SELECT COUNT(*) FROM emergente_bronze.observaciones) AS entrada,
 (SELECT COUNT(*) FROM unicas) AS distintas,
 (SELECT COUNT(*) FROM emergente_bronze.observaciones)-(SELECT COUNT(*) FROM unicas) AS duplicadas_exactas,
 COUNTIF(motivo IS NULL) AS aceptadas,COUNTIF(motivo IS NOT NULL) AS rechazadas
FROM clasificadas;
ASSERT (SELECT entrada=duplicadas_exactas+aceptadas+rechazadas FROM emergente_silver.control)
 AS 'La reconciliación no cierra';
SELECT * FROM emergente_silver.control;
-- Los IDs son claves derivadas, no códigos oficiales de producto/tienda.
-- No fusionar automáticamente DISTRITO FEDERAL/CDMX ni presentaciones diferentes.
-- La fecha es local sin zona informada; no asumir UTC.
