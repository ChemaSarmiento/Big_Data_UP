-- 1. Gold: precio por tienda para un producto, presentación y fecha.
-- direccion entra al grano: dos tiendas con el mismo nombre comercial en
-- el mismo municipio no se mezclan en una sola fila.
-- estado_precio queda lista para cuando SÍ haya más de un precio en el
-- mismo grupo -- MIN() por sí solo elige el menor en silencio y no avisa.
CREATE OR REPLACE TABLE emergente_gold.precio_sprite_tlalpan AS
SELECT fecha, estado, municipio, producto, marca, presentacion,
 cadena_comercial, establecimiento, direccion, MIN(precio_mxn) AS precio_mxn,
 COUNT(*) AS observaciones,
 CASE WHEN COUNT(*) > 1 AND MIN(precio_mxn) <> MAX(precio_mxn)
      THEN 'conflicto' ELSE 'único' END AS estado_precio
FROM emergente_silver.precios_limpios
WHERE fecha=DATE '2014-03-19' AND producto='REFRESCO' AND marca='SPRITE'
 AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
 AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
GROUP BY fecha, estado, municipio, producto, marca, presentacion,
 cadena_comercial, establecimiento, direccion;

-- 2. Observado: dos tiendas (direcciones distintas), cada una con un solo
-- precio -- ambas 'único'. 15.10 y 15.50 MXN.
SELECT establecimiento, direccion, precio_mxn, observaciones, estado_precio
FROM emergente_gold.precio_sprite_tlalpan ORDER BY precio_mxn;
-- Evidencia histórica. No prueba existencia ni precio actual.

-- 3. Qué podríamos revisar: ¿cuántos conflictos hay en TODA la muestra
-- observada, no solo en el caso de Sprite/Tlalpan que armamos arriba?
SELECT
 COUNTIF(precios_distintos > 1) AS grupos_en_conflicto,
 COUNT(*) AS grupos_totales
FROM (
 SELECT producto, marca, presentacion, fecha, estado, municipio,
  cadena_comercial, establecimiento, direccion,
  COUNT(DISTINCT precio_mxn) AS precios_distintos
 FROM emergente_silver.precios_limpios
 GROUP BY producto, marca, presentacion, fecha, estado, municipio,
  cadena_comercial, establecimiento, direccion
);
-- En lo observado: 0 de 4500 grupos en conflicto. No asumas que el
-- archivo completo se comporta igual -- aquí sí vale la pena repetir
-- esta consulta cuando se cargue.

-- 4. Qué podríamos revisar: ¿el agregado perdió o duplicó filas al
-- agrupar? El total de observaciones en Gold debe ser igual al número
-- de filas de Silver que de verdad cumplen el mismo filtro.
SELECT
 (SELECT SUM(observaciones) FROM emergente_gold.precio_sprite_tlalpan) AS suma_en_gold,
 (SELECT COUNT(*) FROM emergente_silver.precios_limpios
  WHERE fecha=DATE '2014-03-19' AND producto='REFRESCO' AND marca='SPRITE'
   AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
   AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN') AS filas_en_silver;
-- Deben coincidir (2 y 2). Si no coinciden, el GROUP BY perdió o
-- duplicó algo -- no lo asumas, compáralo cada vez.
