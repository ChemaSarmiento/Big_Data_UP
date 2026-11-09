-- GoogleSQL. Ejecutar completo después de Bronze. Reemplaza SOLO tablas curso_silver.
CREATE SCHEMA IF NOT EXISTS curso_silver OPTIONS(location='us-central1');
-- Política del fixture: retirar solo copias exactamente iguales, conservar la evidencia cruda.
CREATE TEMP TABLE unicas AS SELECT DISTINCT * FROM curso_bronze.observaciones_raw;
CREATE TEMP TABLE tipadas AS
SELECT *, UPPER(TRIM(establecimiento)) AS tienda,
 SAFE_CAST(fecha_texto AS DATE) AS fecha_observada,
 SAFE_CAST(precio_texto AS NUMERIC) AS precio_envase_mxn
FROM unicas;
CREATE TEMP TABLE clasificadas AS
SELECT *, CASE
 WHEN fecha_observada IS NULL THEN 'fecha_invalida'
 WHEN precio_envase_mxn IS NULL OR precio_envase_mxn <= 0 THEN 'precio_invalido'
 WHEN producto IS NULL OR TRIM(producto)='' OR tienda IS NULL OR tienda='' THEN 'identidad_incompleta'
 ELSE NULL END AS motivo
FROM tipadas;
CREATE OR REPLACE TABLE curso_silver.observaciones
PARTITION BY fecha_observada AS
SELECT id, producto, marca, presentacion, tienda AS establecimiento,
 fecha_observada, precio_envase_mxn, archivo_origen
FROM clasificadas WHERE motivo IS NULL;
CREATE OR REPLACE TABLE curso_silver.rechazadas AS
SELECT * FROM clasificadas WHERE motivo IS NOT NULL;
CREATE OR REPLACE TABLE curso_silver.reporte_calidad AS
SELECT (SELECT COUNT(*) FROM curso_bronze.observaciones_raw) AS entrada,
 (SELECT COUNT(*) FROM unicas) AS unicas,
 (SELECT COUNT(*) FROM curso_bronze.observaciones_raw)-(SELECT COUNT(*) FROM unicas) AS duplicados,
 (SELECT COUNT(*) FROM curso_silver.observaciones) AS aceptadas,
 (SELECT COUNT(*) FROM curso_silver.rechazadas) AS rechazadas;
ASSERT (SELECT entrada = duplicados + aceptadas + rechazadas FROM curso_silver.reporte_calidad)
 AS 'Hay filas sin reconciliar';
SELECT * FROM curso_silver.reporte_calidad; -- fixture: 16 / 15 / 1 / 13 / 2
SELECT id, motivo FROM curso_silver.rechazadas ORDER BY id; -- C4 precio, C5 fecha
