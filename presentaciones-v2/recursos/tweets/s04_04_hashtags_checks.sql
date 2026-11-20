-- Paso 4 · Revisa la tabla hashtags (la creaste con 22_silver_hashtags.sql).

-- 4.1 Un tweet de una agencia de noticias: sus hashtags viven en un arreglo (una celda con tres valores).
SELECT tweet_id, usuario, hashtags
FROM tweets_silver.tweets
WHERE fecha = '2022-03-27' AND tweet_id = 1508054980313370628;

-- 4.2 El mismo tweet en la tabla hashtags: UNNEST lo convirtió en tres filas.
SELECT tweet_id, fecha, idioma, hashtag
FROM tweets_silver.hashtags
WHERE fecha = '2022-03-27' AND tweet_id = 1508054980313370628
ORDER BY hashtag;

-- 4.3 ¿Cuadra? DISTINCT quitó hashtags repetidos dentro de un mismo tweet.
SELECT SUM(ARRAY_LENGTH(hashtags))                      AS hashtags_en_arreglos,
       (SELECT COUNT(*) FROM tweets_silver.hashtags)    AS filas_en_la_tabla,
       COUNTIF(ARRAY_LENGTH(hashtags) > 0)              AS tweets_con_hashtag
FROM tweets_silver.tweets;

-- 4.4 Los ocho hashtags con más tweets.
SELECT hashtag, COUNT(*) AS tweets
FROM tweets_silver.hashtags
GROUP BY hashtag
ORDER BY tweets DESC
LIMIT 8;

-- 4.5 El grano al unir: cada tweet aparece una vez por hashtag. No sumes tweets sobre este resultado.
SELECT COUNT(*)                 AS filas_del_join,
       COUNT(DISTINCT t.tweet_id) AS tweets_distintos
FROM tweets_silver.tweets AS t
JOIN tweets_silver.hashtags AS h USING (tweet_id);
