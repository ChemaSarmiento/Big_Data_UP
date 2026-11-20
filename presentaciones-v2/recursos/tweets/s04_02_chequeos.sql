-- Paso 2 · ¿Silver cuadra con Bronze? Cuatro comprobaciones baratas.

-- 2.1 Filas de Bronze y de Silver. COUNT(*) no lee columnas: el estimador debe decir 0 bytes.
SELECT (SELECT COUNT(*) FROM tweets_bronze.entrada) AS bronze,
       (SELECT COUNT(*) FROM tweets_silver.tweets)  AS silver;

-- 2.2 ¿Hay ids repetidos o vacíos? Solo lee dos columnas.
SELECT COUNT(*)                     AS filas,
       COUNT(DISTINCT tweet_id)     AS ids_distintos,
       COUNTIF(tweet_id IS NULL)    AS sin_id,
       COUNTIF(fecha_hora IS NULL)  AS sin_fecha
FROM tweets_silver.tweets;

-- 2.3 ¿Qué periodo cubre y cuántos tweets hay por día?
SELECT fecha, COUNT(*) AS tweets
FROM tweets_silver.tweets
GROUP BY fecha
ORDER BY fecha;

-- 2.4 ¿Qué tipo tiene cada columna? Son metadatos: no leen datos de la tabla.
SELECT column_name, data_type
FROM tweets_silver.INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'tweets'
ORDER BY ordinal_position;
