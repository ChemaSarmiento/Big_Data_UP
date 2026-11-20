-- Paso 3 · Valida las dos gráficas de «dentro del tema» para un día elegido.
-- 3a. Los 8 hashtags con más tweets el 23 de marzo.
SELECT hashtag, tweets, pct_del_dia
FROM tweets_gold.hashtags_dia
WHERE fecha = DATE '2022-03-23'
ORDER BY tweets DESC
LIMIT 8;

-- 3b. Desde qué aplicación se publicó ese día.
SELECT aplicacion, tweets
FROM tweets_gold.aplicaciones_dia
WHERE fecha = DATE '2022-03-23'
ORDER BY tweets DESC;
