-- Gold: precio por tienda para un producto, presentación y fecha.
CREATE OR REPLACE TABLE emergente_gold.precio_sprite_tlalpan AS
SELECT fecha, estado, municipio, producto, marca, presentacion,
 cadena_comercial, establecimiento, MIN(precio_mxn) AS precio_mxn,
 COUNT(*) AS observaciones
FROM emergente_silver.precios_limpios
WHERE fecha=DATE '2014-03-19' AND producto='REFRESCO' AND marca='SPRITE'
 AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
 AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
GROUP BY fecha, estado, municipio, producto, marca, presentacion,
 cadena_comercial, establecimiento;

-- Muestra: dos tiendas observadas; 15.10 y 15.50 MXN.
SELECT establecimiento, precio_mxn, observaciones
FROM emergente_gold.precio_sprite_tlalpan ORDER BY precio_mxn;
-- Evidencia histórica. No prueba existencia ni precio actual.
