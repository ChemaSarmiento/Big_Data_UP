-- Paso 2 · Armar un contexto con TABLAS Gold: una línea numerada por tabla, con su nombre, filtro y base.
-- Cada línea lleva su etiqueta [T1]…[T6] para que el modelo pueda citarla y tú puedas auditarla.
WITH t1 AS (
  SELECT 1 AS o, FORMAT('[T1] tweets_gold.tema_dia · 2022-03-23 · inglés · base %d tweets: %s',
         ANY_VALUE(tweets_dia),
         STRING_AGG(FORMAT('%s %d (%.3f %%)', tema, tweets_tema, pct_del_dia), '; ' ORDER BY pct_del_dia DESC)) AS linea
  FROM tweets_gold.tema_dia
  WHERE fecha = DATE '2022-03-23' AND grupo_idioma = 'en'
),
t2 AS (
  SELECT 2, FORMAT('[T2] tweets_gold.hashtags_dia · 2022-03-23 · cinco hashtags con más tweets: %s',
         STRING_AGG(FORMAT('#%s %d (%.3f %%)', hashtag, tweets, pct_del_dia), '; ' ORDER BY tweets DESC))
  FROM (SELECT hashtag, tweets, pct_del_dia FROM tweets_gold.hashtags_dia
        WHERE fecha = DATE '2022-03-23' ORDER BY tweets DESC LIMIT 5)
),
t3 AS (
  SELECT 3, FORMAT('[T3] tweets_gold.autores_alcance · todo el archivo · segmento de seguidores: %s',
         STRING_AGG(FORMAT('%s → %.2f %% de los tweets y %.2f %% de los likes', segmento, pct_tweets, pct_likes), '; ' ORDER BY segmento))
  FROM tweets_gold.autores_alcance
),
t4 AS (
  SELECT 4, FORMAT('[T4] tweets_gold.conversacion_dia · 2022-03-23 · tipo de tweet: %s',
         STRING_AGG(FORMAT('%s %d tweets, mediana %d likes', tipo, tweets, mediana_likes), '; ' ORDER BY tweets DESC))
  FROM tweets_gold.conversacion_dia
  WHERE fecha = DATE '2022-03-23'
),
t5 AS (
  SELECT 5, FORMAT('[T5] tweets_gold.aplicaciones_dia · 2022-03-23 · tres aplicaciones con más tweets: %s',
         STRING_AGG(FORMAT('%s %d', aplicacion, tweets), '; ' ORDER BY tweets DESC))
  FROM (SELECT aplicacion, tweets FROM tweets_gold.aplicaciones_dia
        WHERE fecha = DATE '2022-03-23' AND aplicacion != 'otras' ORDER BY tweets DESC LIMIT 3)
),
t6 AS (
  SELECT 6, FORMAT('[T6] tweets_gold.actividad_hora · 2022-03-23 · tres horas UTC con más tweets: %s',
         STRING_AGG(FORMAT('%d:00 → %d', hora_utc, tweets), '; ' ORDER BY tweets DESC))
  FROM (SELECT hora_utc, SUM(tweets) AS tweets FROM tweets_gold.actividad_hora
        WHERE fecha = DATE '2022-03-23' GROUP BY hora_utc ORDER BY tweets DESC LIMIT 3)
)
SELECT STRING_AGG(linea, '\n' ORDER BY o) AS contexto
FROM (SELECT * FROM t1 UNION ALL SELECT * FROM t2 UNION ALL SELECT * FROM t3
      UNION ALL SELECT * FROM t4 UNION ALL SELECT * FROM t5 UNION ALL SELECT * FROM t6);
