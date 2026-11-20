-- Gold · estructura de la conversación: originales, respuestas y citas por día, con likes típicos.
CREATE OR REPLACE TABLE tweets_gold.conversacion_dia
PARTITION BY fecha AS
SELECT fecha,
       CASE WHEN es_respuesta THEN 'respuesta'
            WHEN es_cita      THEN 'cita'
            ELSE                   'original' END AS tipo,
       COUNT(*) AS tweets,
       SUM(likes) AS likes,
       APPROX_QUANTILES(likes, 100)[OFFSET(50)] AS mediana_likes
FROM tweets_silver.tweets
GROUP BY fecha, tipo;
