-- Gold · concentración por tamaño de audiencia del autor (segmentos por seguidores).
CREATE OR REPLACE TABLE tweets_gold.autores_alcance AS
WITH base AS (
  SELECT t.tweet_id, t.likes, a.usuario,
         CASE WHEN a.seguidores < 1000      THEN '1 · menos de 1 mil'
              WHEN a.seguidores < 10000     THEN '2 · 1 mil a 10 mil'
              WHEN a.seguidores < 100000    THEN '3 · 10 mil a 100 mil'
              WHEN a.seguidores < 1000000   THEN '4 · 100 mil a 1 millón'
              ELSE                               '5 · más de 1 millón' END AS segmento
  FROM tweets_silver.tweets AS t
  JOIN tweets_silver.autores AS a USING (usuario)
)
SELECT segmento,
       COUNT(DISTINCT usuario) AS autores,
       COUNT(*)                AS tweets,
       SUM(likes)              AS likes,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_tweets,
       ROUND(100 * SUM(likes) / SUM(SUM(likes)) OVER (), 2) AS pct_likes
FROM base
GROUP BY segmento;
