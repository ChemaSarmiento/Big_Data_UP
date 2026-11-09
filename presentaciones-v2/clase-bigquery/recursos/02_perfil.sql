-- Seleccionar el lote que se desea inspeccionar. No extrapolar una muestra al total.
SELECT COUNT(*) AS filas,
 COUNT(DISTINCT fila_hash) AS distintas,
 MIN(SAFE_CAST(fechaRegistro AS DATETIME)) AS fecha_min,
 MAX(SAFE_CAST(fechaRegistro AS DATETIME)) AS fecha_max,
 COUNTIF(municipio != TRIM(municipio)) AS municipio_con_espacios,
 COUNTIF(SAFE_CAST(precio AS NUMERIC) IS NULL OR SAFE_CAST(precio AS NUMERIC)<=0) AS precio_invalido,
 COUNTIF(SAFE_CAST(fechaRegistro AS DATETIME) IS NULL) AS fecha_invalida
FROM emergente_bronze.observaciones
WHERE lote_id='all_data_muestra_v1';
SELECT producto, presentacion, marca, precio, fechaRegistro, nombreComercial, municipio
FROM emergente_bronze.observaciones
WHERE lote_id='all_data_muestra_v1' AND producto='REFRESCO' AND marca='SPRITE'
 AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
 AND DATE(SAFE_CAST(fechaRegistro AS DATETIME))=DATE '2014-03-19'
 AND TRIM(municipio)='TLALPAN';
