-- Elegir periodo compatible. Estos parámetros cubren la muestra, no certifican el archivo completo.
DECLARE inicio DATE DEFAULT DATE '2011-01-01';
DECLARE fin DATE DEFAULT DATE '2015-12-31';
CREATE OR REPLACE TABLE emergente_gold.precio_tienda_dia AS
SELECT fecha,estado,municipio,producto_id,producto,marca,presentacion,
 tienda_id,establecimiento,direccion,COUNT(*) AS observaciones,
 COUNT(DISTINCT precio_mxn) AS precios_distintos,
 MIN(precio_mxn) AS precio_min_mxn,MAX(precio_mxn) AS precio_max_mxn,
 IF(COUNT(DISTINCT precio_mxn)=1,MIN(precio_mxn),NULL) AS precio_comparable_mxn
FROM emergente_silver.precios
WHERE fecha BETWEEN inicio AND fin
GROUP BY fecha,estado,municipio,producto_id,producto,marca,presentacion,tienda_id,establecimiento,direccion;
CREATE OR REPLACE TABLE emergente_gold.comparacion AS
SELECT fecha,estado,municipio,producto_id,producto,marca,presentacion,
 COUNT(*) AS tiendas_observadas,
 COUNTIF(precio_comparable_mxn IS NOT NULL) AS tiendas_comparables,
 COUNTIF(precio_comparable_mxn IS NULL) AS tiendas_con_conflicto,
 MIN(precio_comparable_mxn) AS menor_precio_mxn,
 MAX(precio_comparable_mxn) AS mayor_precio_mxn,
 MAX(precio_comparable_mxn)-MIN(precio_comparable_mxn) AS diferencia_mxn
FROM emergente_gold.precio_tienda_dia
GROUP BY fecha,estado,municipio,producto_id,producto,marca,presentacion;
SELECT * FROM emergente_gold.comparacion
WHERE fecha=DATE '2014-03-19' AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE';
-- Muestra:2 tiendas comparables,15.10 y15.50 MXN; diferencia0.40 MXN.
-- Esto no mide ahorro actual ni disponibilidad. La muestra no cubre todas las tiendas.
-- S/M es marca no especificada: no basta para afirmar equivalencia comercial.
