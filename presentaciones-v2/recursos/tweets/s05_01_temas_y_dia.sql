-- PASO 1 · Gold de temas. Antes de ejecutar, crea las tablas con 30_gold_tweets.sql (temas_palabras + tema_dia).
-- Requiere tweets_silver.tweets (sesión anterior). Lee solo la columna `texto` de Silver (≈ 1.2 GB).

-- 1.1 ¿Cuántos pares tweet–tema hay? Un tweet cuenta una vez por tema, pero puede estar en varios temas.
SELECT SUM(tweets_tema) AS pares_tweet_tema FROM tweets_gold.tema_dia;
-- Referencia: 342484 pares. Tweets distintos con algún tema: 314527.

-- 1.2 Una fila de Gold explicada: energía en inglés, día por día.
SELECT fecha, tweets_tema, tweets_dia, pct_del_dia
FROM tweets_gold.tema_dia
WHERE tema = 'energia' AND grupo_idioma = 'en'
ORDER BY fecha;

-- 1.3 Control del denominador: tweets_dia, sumado una vez por día e idioma, debe dar el total de Silver.
SELECT SUM(tweets_dia) AS base_total
FROM (SELECT fecha, grupo_idioma, ANY_VALUE(tweets_dia) AS tweets_dia
      FROM tweets_gold.tema_dia GROUP BY fecha, grupo_idioma);
-- Referencia: 6798932.

-- Ejercicio E1: ¿qué porcentaje de los tweets en español habla de sanciones en todo el periodo?
-- Pista: SUM(tweets_tema) / SUM(tweets_dia) filtrando tema y grupo_idioma. (Respuesta de referencia: 0.91 %).
