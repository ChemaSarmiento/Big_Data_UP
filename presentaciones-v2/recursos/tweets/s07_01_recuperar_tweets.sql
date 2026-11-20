-- Paso 1 · Recuperar. Los 5 tweets en inglés con más likes que mencionan energía el 23 de marzo de 2022.
-- Filtra por fecha (partición) y por idioma (cluster) antes de ordenar: así lees una fracción de la tabla.
SELECT likes, url, SUBSTR(texto, 1, 230) AS texto
FROM tweets_silver.tweets
WHERE fecha = DATE '2022-03-23'
  AND idioma = 'en'
  AND REGEXP_CONTAINS(LOWER(texto), r'\b(oil|gas|fuel|petrol|energy)\b')
ORDER BY likes DESC
LIMIT 5;

-- Lo mismo, pero armado como UN solo texto numerado, listo para copiar en el prompt.
SELECT STRING_AGG(FORMAT('[%d] (%d likes) %s %s', n, likes, url, texto), '\n' ORDER BY n) AS contexto
FROM (
  SELECT ROW_NUMBER() OVER (ORDER BY likes DESC) AS n, likes, url,
         REPLACE(SUBSTR(texto, 1, 230), '\n', ' ') AS texto
  FROM tweets_silver.tweets
  WHERE fecha = DATE '2022-03-23'
    AND idioma = 'en'
    AND REGEXP_CONTAINS(LOWER(texto), r'\b(oil|gas|fuel|petrol|energy)\b')
  ORDER BY likes DESC
  LIMIT 5
);
