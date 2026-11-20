-- Gold · ritmo del día: tweets por hora UTC y grupo de idioma.
CREATE OR REPLACE TABLE tweets_gold.actividad_hora
PARTITION BY fecha AS
SELECT fecha,
       EXTRACT(HOUR FROM fecha_hora) AS hora_utc,
       IF(idioma IN ('en', 'es'), idioma, 'otro') AS grupo_idioma,
       COUNT(*) AS tweets
FROM tweets_silver.tweets
GROUP BY fecha, hora_utc, grupo_idioma;
