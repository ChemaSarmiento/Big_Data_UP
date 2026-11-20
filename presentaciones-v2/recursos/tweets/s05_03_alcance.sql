-- PASO 3 · Alcance de los autores. Crea la tabla con 32_gold_autores_alcance.sql (une Silver tweets y autores).

-- 3.1 La tabla completa: cada fila es un segmento por seguidores del autor.
SELECT segmento, autores, tweets, likes, pct_tweets, pct_likes
FROM tweets_gold.autores_alcance
ORDER BY segmento;

-- 3.2 ¿Quiénes escriben mucho? Distribución de tweets por autor (tabla Silver autores).
SELECT
  COUNTIF(tweets_en_archivo = 1)                 AS un_tweet,
  COUNTIF(tweets_en_archivo BETWEEN 2 AND 5)     AS de_2_a_5,
  COUNTIF(tweets_en_archivo BETWEEN 6 AND 50)    AS de_6_a_50,
  COUNTIF(tweets_en_archivo > 50)                AS mas_de_50,
  COUNT(*)                                       AS autores
FROM tweets_silver.autores;
-- Referencia: 1091593 · 554547 · 214017 · 11917 · 1872074.

-- Ejercicio E3: ¿qué segmento aporta más likes por tweet? (pista: likes / tweets en 3.1).
