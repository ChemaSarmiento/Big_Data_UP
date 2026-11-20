-- Silver: una fila por tweet, con tipos reales. Bronze no se modifica.
-- Cuesta un escaneo completo de Bronze (~23.7 GB facturables); ejecútalo una vez.
CREATE OR REPLACE TABLE tweets_silver.tweets
PARTITION BY fecha
CLUSTER BY idioma AS
SELECT
  SAFE_CAST(JSON_VALUE(value, '$.id') AS INT64)                  AS tweet_id,
  SAFE_CAST(JSON_VALUE(value, '$.date') AS TIMESTAMP)            AS fecha_hora,
  DATE(SAFE_CAST(JSON_VALUE(value, '$.date') AS TIMESTAMP))      AS fecha,
  JSON_VALUE(value, '$.lang')                                    AS idioma,
  JSON_VALUE(value, '$.content')                                 AS texto,
  JSON_VALUE(value, '$.url')                                     AS url,
  JSON_VALUE(value, '$.user.username')                           AS usuario,
  SAFE_CAST(JSON_VALUE(value, '$.user.verified') AS BOOL)        AS usuario_verificado,
  SAFE_CAST(JSON_VALUE(value, '$.user.followersCount') AS INT64) AS seguidores,
  JSON_VALUE(value, '$.user.location')                           AS ubicacion_usuario,
  SAFE_CAST(JSON_VALUE(value, '$.likeCount') AS INT64)           AS likes,
  SAFE_CAST(JSON_VALUE(value, '$.retweetCount') AS INT64)        AS retuits,
  SAFE_CAST(JSON_VALUE(value, '$.replyCount') AS INT64)          AS respuestas,
  SAFE_CAST(JSON_VALUE(value, '$.quoteCount') AS INT64)          AS citas,
  JSON_VALUE(value, '$.inReplyToTweetId') IS NOT NULL            AS es_respuesta,
  JSON_VALUE(value, '$.quotedTweet.id') IS NOT NULL              AS es_cita,
  ARRAY(SELECT LOWER(h) FROM UNNEST(JSON_VALUE_ARRAY(value, '$.hashtags')) AS h) AS hashtags,
  JSON_VALUE(value, '$.sourceLabel')                             AS aplicacion
FROM tweets_bronze.entrada;
