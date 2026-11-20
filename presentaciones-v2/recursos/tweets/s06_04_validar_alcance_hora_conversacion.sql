-- Paso 4 · Valida las tres gráficas de «quién, cuándo y cómo».
-- 4a. Quién concentra los tweets y quién concentra los likes.
SELECT segmento, autores, tweets, pct_tweets, pct_likes
FROM tweets_gold.autores_alcance
ORDER BY segmento;

-- 4b. Ritmo del 23 de marzo: la hora UTC con más y con menos tweets por idioma.
SELECT grupo_idioma,
       ARRAY_AGG(hora_utc ORDER BY tweets DESC LIMIT 1)[OFFSET(0)] AS hora_pico,
       MAX(tweets) AS tweets_pico,
       ARRAY_AGG(hora_utc ORDER BY tweets ASC LIMIT 1)[OFFSET(0)]  AS hora_valle,
       MIN(tweets) AS tweets_valle
FROM tweets_gold.actividad_hora
WHERE fecha = DATE '2022-03-23'
GROUP BY grupo_idioma
ORDER BY grupo_idioma;

-- 4c. Cómo se reparte la conversación el 27 de marzo.
SELECT tipo, tweets,
       ROUND(100 * tweets / SUM(tweets) OVER (), 1) AS pct,
       mediana_likes
FROM tweets_gold.conversacion_dia
WHERE fecha = DATE '2022-03-27'
ORDER BY tweets DESC;
