-- Paso 3 · Revisa la tabla autores (la creaste con 21_silver_autores.sql).

-- 3.1 Un autor con varios tweets, del más reciente al más antiguo.
--     orden = 1 es el que se queda en autores. Mira cómo cambia seguidores.
SELECT tweet_id, fecha_hora, seguidores,
       ROW_NUMBER() OVER (PARTITION BY usuario ORDER BY fecha_hora DESC) AS orden
FROM tweets_silver.tweets
WHERE usuario = 'skift'
ORDER BY fecha_hora DESC;

-- 3.2 Lo que quedó de ese autor: una sola fila.
SELECT * FROM tweets_silver.autores WHERE usuario = 'skift';

-- 3.3 ¿Cuadra? Una fila por autor y todos los tweets contados una vez.
SELECT COUNT(*)                  AS autores,
       COUNT(DISTINCT usuario)   AS usuarios_distintos,
       SUM(tweets_en_archivo)    AS tweets_sumados
FROM tweets_silver.autores;

-- 3.4 CTE: WITH le pone nombre a un paso intermedio para poder resumirlo otra vez.
--     Primero cuenta tweets por autor; después cuenta autores por tramo.
WITH tweets_por_autor AS (
  SELECT usuario, COUNT(*) AS tweets
  FROM tweets_silver.tweets
  GROUP BY usuario
)
SELECT CASE WHEN tweets = 1  THEN '1'
            WHEN tweets = 2  THEN '2'
            WHEN tweets <= 5 THEN '3 a 5'
            WHEN tweets <= 20 THEN '6 a 20'
            ELSE 'más de 20' END AS tweets_publicados,
       MIN(tweets)   AS orden,
       COUNT(*)      AS autores,
       SUM(tweets)   AS tweets_totales
FROM tweets_por_autor
GROUP BY tweets_publicados
ORDER BY orden;
