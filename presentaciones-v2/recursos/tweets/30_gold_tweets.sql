-- 1. Tabla pequeña de temas satélite. Es una definición editable, no un hecho del dato.
CREATE OR REPLACE TABLE tweets_gold.temas_palabras AS
SELECT * FROM UNNEST([
  STRUCT('energia' AS tema, 'oil' AS palabra), ('energia','gas'), ('energia','fuel'), ('energia','petrol'),
  ('energia','energy'), ('energia','petróleo'), ('energia','gasolina'), ('energia','combustible'), ('energia','energía'),
  ('alimentos','wheat'), ('alimentos','grain'), ('alimentos','food'), ('alimentos','fertilizer'),
  ('alimentos','trigo'), ('alimentos','cereal'), ('alimentos','alimentos'), ('alimentos','fertilizantes'),
  ('aviacion','airline'), ('aviacion','airlines'), ('aviacion','flights'), ('aviacion','airspace'),
  ('aviacion','aviation'), ('aviacion','aerolínea'), ('aviacion','vuelos'), ('aviacion','espacio aéreo'),
  ('sanciones','sanctions'), ('sanciones','sanction'), ('sanciones','sanciones'), ('sanciones','sanción'),
  ('cadena_suministro','supply chain'), ('cadena_suministro','shipping'), ('cadena_suministro','logistics'),
  ('cadena_suministro','cadena de suministro'), ('cadena_suministro','puerto'), ('cadena_suministro','logística'),
  ('mercados','inflation'), ('mercados','stock market'), ('mercados','markets'), ('mercados','inflación'),
  ('mercados','precios'), ('mercados','bolsa'), ('mercados','mercados')
]);

-- 2. Gold: un tweet cuenta una vez por tema, aunque use varias palabras del tema.
--    Grano: fecha + tema + grupo de idioma. pct_del_dia usa el total de tweets del mismo día e idioma.
CREATE OR REPLACE TABLE tweets_gold.tema_dia
PARTITION BY fecha AS
WITH por_tweet AS (
  SELECT t.fecha, p.tema,
         IF(t.idioma IN ('en', 'es'), t.idioma, 'otro') AS grupo_idioma,
         t.tweet_id, t.likes
  FROM tweets_silver.tweets AS t
  CROSS JOIN tweets_gold.temas_palabras AS p
  WHERE REGEXP_CONTAINS(LOWER(t.texto), CONCAT(r'\b', p.palabra, r'\b'))
  GROUP BY t.fecha, p.tema, grupo_idioma, t.tweet_id, t.likes
),
dia AS (
  SELECT fecha, IF(idioma IN ('en', 'es'), idioma, 'otro') AS grupo_idioma, COUNT(*) AS tweets_dia
  FROM tweets_silver.tweets
  GROUP BY fecha, grupo_idioma
)
SELECT m.fecha, m.tema, m.grupo_idioma,
       COUNT(*) AS tweets_tema, SUM(m.likes) AS likes_tema,
       ANY_VALUE(d.tweets_dia) AS tweets_dia,
       ROUND(100 * COUNT(*) / ANY_VALUE(d.tweets_dia), 3) AS pct_del_dia
FROM por_tweet AS m
JOIN dia AS d USING (fecha, grupo_idioma)
GROUP BY m.fecha, m.tema, m.grupo_idioma;
