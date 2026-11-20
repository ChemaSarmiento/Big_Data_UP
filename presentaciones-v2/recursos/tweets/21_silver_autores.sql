-- Silver 2 · autores: una fila por autor (grano distinto al de tweets).
-- Un autor aparece en muchos tweets; nos quedamos con su dato más reciente.
CREATE OR REPLACE TABLE tweets_silver.autores AS
WITH ordenados AS (
  SELECT usuario, usuario_verificado, seguidores,
         NULLIF(TRIM(ubicacion_usuario), '') AS ubicacion,
         ROW_NUMBER() OVER (PARTITION BY usuario ORDER BY fecha_hora DESC) AS orden,
         COUNT(*)     OVER (PARTITION BY usuario)                          AS tweets_en_archivo
  FROM tweets_silver.tweets
)
SELECT usuario, usuario_verificado, seguidores, ubicacion, tweets_en_archivo
FROM ordenados
WHERE orden = 1;
