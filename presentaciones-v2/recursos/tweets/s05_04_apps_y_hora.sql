-- PASO 4 · Aplicaciones y ritmo del día. Crea las tablas con 33_gold_aplicaciones_dia.sql y 34_gold_actividad_hora.sql.

-- 4.1 Desde qué aplicación se publica (todo el periodo).
SELECT aplicacion, SUM(tweets) AS tweets,
       ROUND(100 * SUM(tweets) / SUM(SUM(tweets)) OVER (), 1) AS pct
FROM tweets_gold.aplicaciones_dia
GROUP BY aplicacion
ORDER BY tweets DESC;

-- 4.2 Ritmo del día en días completos (17 a 27 de marzo), hora UTC.
SELECT hora_utc, SUM(tweets) AS tweets
FROM tweets_gold.actividad_hora
WHERE fecha BETWEEN '2022-03-17' AND '2022-03-27'
GROUP BY hora_utc
ORDER BY hora_utc;

-- 4.3 El día parcial se ve aquí: el 16 de marzo solo tiene horas 20 a 23.
SELECT hora_utc, SUM(tweets) AS tweets
FROM tweets_gold.actividad_hora
WHERE fecha = '2022-03-16'
GROUP BY hora_utc
ORDER BY hora_utc;

-- Ejercicio E4: ¿a qué hora UTC publica más cada grupo de idioma? (pista: GROUP BY grupo_idioma, hora_utc).
