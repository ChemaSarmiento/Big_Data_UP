-- PASO 2 · Hashtags por día. Crea la tabla con 31_gold_hashtags_dia.sql (usa tweets_silver.hashtags).
-- Umbral del script: solo hashtags con al menos 25 tweets ese día.

-- 2.1 Los hashtags más usados el 23 de marzo.
SELECT hashtag, tweets, pct_del_dia
FROM tweets_gold.hashtags_dia
WHERE fecha = '2022-03-23'
ORDER BY tweets DESC
LIMIT 8;

-- 2.2 ¿Qué se pierde con el umbral? Compara Gold con la tabla Silver completa.
SELECT
  (SELECT COUNT(DISTINCT hashtag) FROM tweets_silver.hashtags) AS hashtags_en_silver,
  (SELECT COUNT(DISTINCT hashtag) FROM tweets_gold.hashtags_dia) AS hashtags_en_gold,
  (SELECT COUNT(*) FROM tweets_silver.hashtags)                  AS filas_silver,
  (SELECT SUM(tweets) FROM tweets_gold.hashtags_dia)             AS filas_cubiertas_en_gold;
-- Referencia: 223523 · 2261 · 3339839 · 2397514 (el umbral conserva 71.8 % de las menciones).

-- Ejercicio E2: hashtags del 27 de marzo que no llegaron al umbral el 17 (pista: NOT IN con subconsulta).
