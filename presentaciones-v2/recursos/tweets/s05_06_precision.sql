-- PASO 6 · ¿Las palabras clave miden el tema? Lee 5 tweets por tema (23 de marzo, inglés y español).
-- Lee solo un día de texto de Silver (≈ 0.1 GB). Clasifica cada fila tú mismo: acierto, dudoso o falso positivo.
WITH m AS (
  SELECT p.tema, p.palabra, t.idioma,
         REPLACE(SUBSTR(t.texto, 1, 150), '\n', ' ') AS texto,
         ROW_NUMBER() OVER (PARTITION BY p.tema ORDER BY FARM_FINGERPRINT(CAST(t.tweet_id AS STRING))) AS fila
  FROM tweets_silver.tweets AS t
  CROSS JOIN tweets_gold.temas_palabras AS p
  WHERE t.fecha = '2022-03-23' AND t.idioma IN ('en', 'es')
    AND REGEXP_CONTAINS(LOWER(t.texto), CONCAT(r'\b', p.palabra, r'\b'))
)
SELECT tema, palabra, idioma, texto
FROM m
WHERE fila <= 5
ORDER BY tema, fila;
