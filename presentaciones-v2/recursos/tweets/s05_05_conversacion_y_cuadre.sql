-- PASO 5 · Conversación y cuadre entre tablas. Crea la tabla con 35_gold_conversacion.sql.

-- 5.1 Originales, respuestas y citas en todo el periodo.
SELECT tipo, SUM(tweets) AS tweets, SUM(likes) AS likes,
       ROUND(SUM(likes) / SUM(tweets), 2) AS likes_por_tweet
FROM tweets_gold.conversacion_dia
GROUP BY tipo
ORDER BY tweets DESC;

-- 5.2 Cuadre: las tablas Gold con grano por tweet deben sumar el mismo total que Silver.
SELECT
  (SELECT COUNT(*) FROM tweets_silver.tweets)          AS silver,
  (SELECT SUM(tweets) FROM tweets_gold.conversacion_dia) AS conversacion,
  (SELECT SUM(tweets) FROM tweets_gold.actividad_hora)   AS actividad,
  (SELECT SUM(tweets) FROM tweets_gold.aplicaciones_dia) AS aplicaciones;
-- Referencia: las cuatro columnas dicen 6798932. Si una difiere, el GROUP BY perdió o repitió filas.

-- Ejercicio E5: ¿qué día tuvo el mayor porcentaje de respuestas? (pista: SUM(IF(tipo='respuesta', tweets, 0)) / SUM(tweets)).
