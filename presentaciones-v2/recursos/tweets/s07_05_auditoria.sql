-- Paso 5 · Auditar. Cada afirmación del texto generado se comprueba con una consulta sobre Gold.
-- Veredictos posibles: sustentada, contradicha, sin respaldo (el dato no puede decidirlo).

-- A1 «La energía fue el tema con más presencia el 23 de marzo en inglés.»  → sustentada
SELECT tema, tweets_tema, pct_del_dia
FROM tweets_gold.tema_dia
WHERE fecha = DATE '2022-03-23' AND grupo_idioma = 'en'
ORDER BY pct_del_dia DESC;

-- A2 «Las sanciones pesaron más en español que en inglés.»  → contradicha
SELECT grupo_idioma, SUM(tweets_tema) AS tweets, SUM(tweets_dia) AS base,
       ROUND(100 * SUM(tweets_tema) / SUM(tweets_dia), 2) AS pct
FROM tweets_gold.tema_dia
WHERE tema = 'sanciones'
GROUP BY grupo_idioma
ORDER BY pct DESC;

-- A3 «La mayoría de los likes viene de cuentas con más de un millón de seguidores.»  → contradicha
SELECT segmento, pct_tweets, pct_likes
FROM tweets_gold.autores_alcance
ORDER BY segmento;

-- A4 «La mitad de los tweets son respuestas.»  → sustentada
SELECT tipo, SUM(tweets) AS tweets,
       ROUND(100 * SUM(tweets) / SUM(SUM(tweets)) OVER (), 1) AS pct
FROM tweets_gold.conversacion_dia
GROUP BY tipo
ORDER BY tweets DESC;

-- A5 «Las sanciones causaron el pico de energía del 23 de marzo.»  → sin respaldo
-- A6 «A la gente en Europa le preocupó más la energía.»  → sin respaldo
-- Ninguna tabla Gold trae causas ni país: el idioma no es el país y cuatro de cada diez autores no declara ubicación.
-- Lo que sí puedes comprobar sobre A6 es cuántos autores dejaron la ubicación vacía:
SELECT COUNTIF(ubicacion IS NULL) AS autores_sin_ubicacion, COUNT(*) AS autores,
       ROUND(100 * COUNTIF(ubicacion IS NULL) / COUNT(*), 1) AS pct
FROM tweets_silver.autores;
