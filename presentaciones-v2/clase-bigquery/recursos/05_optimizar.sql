-- Ejecutar CADA SELECT por separado. Misma pregunta y resultados; distinta organización física.
-- Desactivar caché en configuración de consulta para la comparación.
-- Anotar bytes procesados/facturados, cache_hit, tiempo y job_id reales. No inventar porcentajes.
-- A: tabla plana, columnas necesarias y filtros lógicos.
SELECT tienda_id, establecimiento, MIN(precio_mxn) AS precio_mxn
FROM emergente_silver.precios_plana
WHERE fecha=DATE '2014-03-19' AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
GROUP BY tienda_id,establecimiento ORDER BY tienda_id;
-- B: misma consulta en tabla particionada por mes y agrupada por columnas de filtro.
SELECT tienda_id, establecimiento, MIN(precio_mxn) AS precio_mxn
FROM emergente_silver.precios
WHERE fecha=DATE '2014-03-19' AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
GROUP BY tienda_id,establecimiento ORDER BY tienda_id;
-- C: consumir Gold pequeña ya calculada (requiere pagar/mantener su construcción).
SELECT tienda_id,establecimiento,precio_comparable_mxn AS precio_mxn
FROM emergente_gold.precio_tienda_dia
WHERE fecha=DATE '2014-03-19' AND estado='DISTRITO FEDERAL' AND municipio='TLALPAN'
 AND producto='REFRESCO' AND marca='SPRITE' AND presentacion='BOTELLA 2 LT. NO RETORNABLE'
ORDER BY tienda_id;
-- A/B usan MIN; compararlos con C solo cuando no hay conflicto de precios para esa selección.
-- LIMIT limita filas devueltas; no es un límite de bytes leídos.
-- Con4500 filas, mínimos de facturación y bloques pequeños pueden ocultar la mejora.
