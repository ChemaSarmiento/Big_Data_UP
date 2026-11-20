-- Bronze = el archivo tal como llegó: una columna `value` con el JSON crudo de cada tweet.
-- La carga se hace una vez, desde Cloud Shell, con tu propio bucket (la carga a BigQuery no cuesta):
--   bq --location=US mk --dataset tweets_bronze
--   bq --location=US load --replace --source_format=CSV \
--      --field_delimiter='þ' --quote='' --max_bad_records=0 \
--      tweets_bronze.entrada "gs://TU_BUCKET/war_tweets.txt" value:STRING
-- Por qué así: el archivo es JSON Lines (un JSON por línea). Si usas un separador que nunca aparece
-- en el texto y desactivas las comillas, cada línea completa cae en una sola columna sin alterarse.

-- 1. Cuántas filas llegaron. COUNT(*) no lee columnas: el estimador debe decir 0 bytes.
SELECT COUNT(*) AS tweets FROM tweets_bronze.entrada;

-- 2. Mirar un registro crudo. Cuesta una lectura completa de `value`, así que lee el estimador antes de ejecutar.
SELECT value FROM tweets_bronze.entrada LIMIT 1;
