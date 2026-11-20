-- S8 · Control de una cifra: ¿qué porcentaje del 23 de marzo de 2022 (tweets en inglés) mencionó energía?
-- Cifra a auditar (tweets_gold.tema_dia): 10530 de 311363 = 3.382 %. Aquí se reconstruye desde Silver.
-- Lee solo la columna texto de UN día (fecha es la partición): ~100 MB, no los 2.45 GB de la tabla.

-- 1. Cifra publicada en Gold.
SELECT fecha, tweets_tema, tweets_dia, pct_del_dia
FROM tweets_gold.tema_dia
WHERE tema = 'energia' AND grupo_idioma = 'en' AND fecha = DATE '2022-03-23';

-- 2. La misma cifra reconstruida desde Silver con la misma regla (palabras de temas_palabras).
WITH dia AS (
  SELECT tweet_id, texto
  FROM tweets_silver.tweets
  WHERE fecha = DATE '2022-03-23' AND idioma = 'en'
)
SELECT (SELECT COUNT(*) FROM dia)                                      AS tweets_dia,
       COUNT(DISTINCT d.tweet_id)                                      AS tweets_tema,
       ROUND(100 * COUNT(DISTINCT d.tweet_id) / (SELECT COUNT(*) FROM dia), 3) AS pct_del_dia
FROM dia AS d
CROSS JOIN tweets_gold.temas_palabras AS p
WHERE p.tema = 'energia'
  AND REGEXP_CONTAINS(LOWER(d.texto), CONCAT(r'\b', p.palabra, r'\b'));

-- 3. Conciliación de bases: la suma de tweets_dia en Gold debe igualar las filas de Silver.
SELECT (SELECT COUNT(*) FROM tweets_silver.tweets) AS filas_silver,
       (SELECT SUM(base) FROM (SELECT ANY_VALUE(tweets_dia) AS base
                               FROM tweets_gold.tema_dia GROUP BY fecha, grupo_idioma)) AS base_en_gold;
