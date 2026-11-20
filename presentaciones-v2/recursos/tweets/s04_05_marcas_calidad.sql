-- Paso 5 · Marca, no borres. Cada regla es una columna verdadero/falso; tú decides después qué excluir.

-- 5.1 Cuántos tweets cae en cada regla y cuántos quedan al aplicarlas.
--     texto_repetido: el mismo texto exacto aparece 20 veces o más.
WITH marcadas AS (
  SELECT fecha = DATE '2022-03-16'                  AS dia_parcial,
         idioma = 'und'                             AS idioma_desconocido,
         COUNT(*) OVER (PARTITION BY texto) >= 20   AS texto_repetido,
         es_respuesta
  FROM tweets_silver.tweets
)
SELECT COUNT(*)                                                                         AS tweets,
       COUNTIF(dia_parcial)                                                             AS dia_parcial,
       COUNTIF(idioma_desconocido)                                                      AS idioma_desconocido,
       COUNTIF(texto_repetido)                                                          AS texto_repetido,
       COUNTIF(NOT (dia_parcial OR idioma_desconocido OR texto_repetido))               AS quedan_con_3_reglas,
       COUNTIF(NOT (dia_parcial OR idioma_desconocido OR texto_repetido OR es_respuesta)) AS quedan_sin_respuestas
FROM marcadas;

-- 5.2 Los textos que más se copian. El nombre del paso (por_texto) es distinto al de la columna (texto):
--     si el alias de SELECT se llamara igual que la columna, GROUP BY agruparía por el alias recortado.
WITH por_texto AS (
  SELECT texto, COUNT(*) AS copias, COUNT(DISTINCT usuario) AS cuentas
  FROM tweets_silver.tweets
  GROUP BY texto
)
SELECT SUBSTR(texto, 1, 40) AS inicio, copias, cuentas
FROM por_texto
ORDER BY copias DESC
LIMIT 4;

-- 5.3 Ubicación vacía e idioma sin determinar.
SELECT COUNTIF(ubicacion_usuario IS NULL OR TRIM(ubicacion_usuario) = '')                        AS sin_ubicacion,
       ROUND(100 * COUNTIF(ubicacion_usuario IS NULL OR TRIM(ubicacion_usuario) = '') / COUNT(*), 1) AS pct_sin_ubicacion,
       COUNTIF(idioma = 'und')                                                                   AS idioma_und
FROM tweets_silver.tweets;

-- 5.4 Likes: el promedio y la mediana cuentan historias distintas.
SELECT ROUND(AVG(likes), 2)                          AS promedio,
       APPROX_QUANTILES(likes, 100)[OFFSET(50)]      AS mediana,
       ROUND(100 * COUNTIF(likes = 0) / COUNT(*), 1) AS pct_con_cero_likes,
       COUNTIF(likes >= 1000)                        AS tweets_con_mil_o_mas,
       ROUND(100 * SUM(IF(likes >= 1000, likes, 0)) / SUM(likes), 1) AS pct_de_los_likes
FROM tweets_silver.tweets;
