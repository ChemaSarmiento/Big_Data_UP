-- Gold · hashtags por día. Umbral: solo hashtags con al menos 25 tweets ese día (definición editable).
CREATE OR REPLACE TABLE tweets_gold.hashtags_dia
PARTITION BY fecha AS
WITH por_dia AS (
  SELECT fecha, COUNT(*) AS tweets_dia FROM tweets_silver.tweets GROUP BY fecha
)
SELECT h.fecha, h.hashtag, COUNT(*) AS tweets, d.tweets_dia,
       ROUND(100 * COUNT(*) / d.tweets_dia, 3) AS pct_del_dia
FROM tweets_silver.hashtags AS h
JOIN por_dia AS d USING (fecha)
GROUP BY h.fecha, h.hashtag, d.tweets_dia
HAVING COUNT(*) >= 25;
