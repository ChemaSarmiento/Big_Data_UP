-- GoogleSQL. Ejemplo ILUSTRATIVO de cinco envases, una tienda, misma ventana histórica.
-- Ejecutar después de 04_silver.sql. Reemplaza SOLO tablas curso_gold.
DECLARE inicio DATE DEFAULT DATE '2024-01-15';
DECLARE fin DATE DEFAULT DATE '2024-01-15';
DECLARE escenario_id STRING DEFAULT 'demo_2024-01-15';
CREATE SCHEMA IF NOT EXISTS curso_gold OPTIONS(location='us-central1');
CREATE OR REPLACE TABLE curso_gold.catalogo AS
SELECT p AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 1 AS cantidad_envases
FROM UNNEST(['p1','p2','p3','p4','p5']) p;
CREATE OR REPLACE TABLE curso_gold.precios_elegidos AS
SELECT s.* FROM curso_silver.observaciones s
JOIN curso_gold.catalogo c USING(producto, marca, presentacion)
WHERE s.fecha_observada BETWEEN inicio AND fin
QUALIFY ROW_NUMBER() OVER (
 PARTITION BY producto, marca, presentacion, establecimiento
 ORDER BY fecha_observada DESC, id DESC) = 1;
-- LEFT JOIN desde tienda x catálogo: no perder productos sin observación.
CREATE OR REPLACE TABLE curso_gold.detalle AS
SELECT escenario_id AS escenario, t.establecimiento, c.*,
 p.id, p.fecha_observada, p.precio_envase_mxn,
 p.precio_envase_mxn*c.cantidad_envases AS importe_mxn
FROM (SELECT DISTINCT establecimiento FROM curso_silver.observaciones) t
CROSS JOIN curso_gold.catalogo c
LEFT JOIN curso_gold.precios_elegidos p
 ON t.establecimiento=p.establecimiento AND c.producto=p.producto
 AND c.marca=p.marca AND c.presentacion=p.presentacion;
CREATE OR REPLACE TABLE curso_gold.canastas AS
SELECT escenario, establecimiento, COUNT(precio_envase_mxn) AS productos_encontrados,
 COUNT(*) AS productos_requeridos,
 SAFE_DIVIDE(COUNT(precio_envase_mxn),COUNT(*)) AS cobertura,
 SUM(importe_mxn) AS subtotal_mxn,
 IF(COUNT(precio_envase_mxn)=COUNT(*),SUM(importe_mxn),NULL) AS costo_completo_mxn,
 COUNT(precio_envase_mxn)=COUNT(*) AS elegible, inicio AS fecha_inicio, fin AS fecha_fin
FROM curso_gold.detalle GROUP BY escenario, establecimiento;
ASSERT (NOT EXISTS (
 SELECT 1 FROM curso_gold.precios_elegidos
 GROUP BY producto, marca, presentacion, establecimiento HAVING COUNT(*)>1
)) AS 'Fan-out antes de la agregacion';
SELECT * FROM curso_gold.canastas ORDER BY establecimiento;
-- A: 5/5, 150; B: 5/5, 160; C: 3/5, subtotal54, costo completo NULL.
-- Regla última observación no garantiza simultaneidad si se amplía la ventana.
