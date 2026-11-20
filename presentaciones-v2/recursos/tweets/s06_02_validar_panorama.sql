-- Paso 2 · Valida la serie del panorama antes de dibujarla.
-- El porcentaje correcto es SUMA de tweets del tema dividida entre SUMA de tweets del día
-- (no promedies pct_del_dia: cada idioma tiene una base distinta).
SELECT fecha,
       SUM(tweets_tema) AS tweets_tema,
       SUM(tweets_dia)  AS tweets_dia,
       ROUND(100 * SUM(tweets_tema) / SUM(tweets_dia), 3) AS pct_ponderado
FROM tweets_gold.tema_dia
WHERE tema = 'energia'
GROUP BY fecha
ORDER BY fecha;
