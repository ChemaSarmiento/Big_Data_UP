-- GoogleSQL. Requiere 01_fixture_bronze.sql o 02_bronze_externa.sql.
SELECT COUNT(*) AS filas, COUNT(DISTINCT id) AS identificadores
FROM curso_bronze.observaciones_raw; -- fixture: 16 / 15
SELECT establecimiento, COUNT(*) AS registros
FROM curso_bronze.observaciones_raw GROUP BY establecimiento ORDER BY establecimiento;
SELECT id, producto, fecha_texto, precio_texto FROM curso_bronze.observaciones_raw
WHERE establecimiento='C' ORDER BY id;
-- LIMIT no es control general de bytes leídos. Guardar job ID/bytes/cache hit de cada ejecución.
