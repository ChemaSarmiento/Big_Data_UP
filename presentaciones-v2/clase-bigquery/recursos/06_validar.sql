SELECT * FROM emergente_silver.control;
SELECT COUNT(*) AS conflictos FROM emergente_gold.precio_tienda_dia WHERE precios_distintos>1;
SELECT COUNT(*) AS grupos_con_menos_de_dos_tiendas FROM emergente_gold.comparacion
WHERE tiendas_comparables<2;
-- Comprobar igualdad exacta A/B (debe devolver0 filas).
WITH a AS (
 SELECT tienda_id,establecimiento,MIN(precio_mxn) AS precio_mxn FROM emergente_silver.precios_plana
 WHERE fecha=DATE '2014-03-19' AND municipio='TLALPAN' AND estado='DISTRITO FEDERAL'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
 GROUP BY tienda_id,establecimiento
), b AS (
 SELECT tienda_id,establecimiento,MIN(precio_mxn) AS precio_mxn FROM emergente_silver.precios
 WHERE fecha=DATE '2014-03-19' AND municipio='TLALPAN' AND estado='DISTRITO FEDERAL'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
 GROUP BY tienda_id,establecimiento
)
SELECT 'solo_a' AS diferencia,* FROM (SELECT * FROM a EXCEPT DISTINCT SELECT * FROM b)
UNION ALL
SELECT 'solo_b',* FROM (SELECT * FROM b EXCEPT DISTINCT SELECT * FROM a);
