-- Bronze muestra los valores como llegaron desde el CSV.
-- Carga previa: all_data_muestra.csv en emergente_bronze.entrada.
SELECT producto, presentacion, marca, precio, fechaRegistro, municipio
FROM emergente_bronze.entrada
WHERE producto='REFRESCO' AND marca='SPRITE' AND municipio LIKE 'TLALPAN%'
LIMIT 10;

-- La limpieza se muestra como una consulta; la tabla original no cambia.
SELECT municipio AS municipio_original, TRIM(municipio) AS municipio_limpio,
 precio AS precio_original, SAFE_CAST(precio AS NUMERIC) AS precio_numerico
FROM emergente_bronze.entrada
WHERE producto='REFRESCO' AND marca='SPRITE' AND TRIM(municipio)='TLALPAN'
LIMIT 5;

SELECT COUNT(*) AS filas_bronze FROM emergente_bronze.entrada;
-- Esperado con la muestra: 4500.
