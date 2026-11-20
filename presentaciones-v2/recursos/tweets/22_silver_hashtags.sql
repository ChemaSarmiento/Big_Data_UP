-- Silver 3 · hashtags: una fila por tweet y hashtag. UNNEST convierte el arreglo en filas.
-- DISTINCT evita contar dos veces un hashtag repetido dentro del mismo tweet.
CREATE OR REPLACE TABLE tweets_silver.hashtags
PARTITION BY fecha AS
SELECT DISTINCT t.tweet_id, t.fecha, t.idioma, h AS hashtag
FROM tweets_silver.tweets AS t, UNNEST(t.hashtags) AS h
WHERE h != '';
