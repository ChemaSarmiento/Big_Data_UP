-- Gold · desde qué aplicación se publica (top 8 del archivo; el resto se agrupa en «otras»).
CREATE OR REPLACE TABLE tweets_gold.aplicaciones_dia
PARTITION BY fecha AS
WITH top AS (
  SELECT aplicacion FROM tweets_silver.tweets GROUP BY aplicacion ORDER BY COUNT(*) DESC LIMIT 8
)
SELECT t.fecha,
       IF(t.aplicacion IN (SELECT aplicacion FROM top), t.aplicacion, 'otras') AS aplicacion,
       COUNT(*) AS tweets
FROM tweets_silver.tweets AS t
GROUP BY t.fecha, aplicacion;
