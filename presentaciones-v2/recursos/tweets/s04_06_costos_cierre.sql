-- Paso 6 · Cuánto cuesta leer lo mismo de cuatro maneras, y el cuadre final.
-- No ejecutes 6.1 a 6.4 todavía: selecciona cada una y lee el estimador de bytes del editor.

-- 6.1 Una columna, toda la tabla.
SELECT texto FROM tweets_silver.tweets;

-- 6.2 Una columna, un solo día (la tabla está particionada por fecha).
SELECT texto FROM tweets_silver.tweets WHERE fecha = '2022-03-23';

-- 6.3 Una columna, un día y un idioma (la tabla está agrupada por idioma).
--     Esta sí ejecútala: abre «Información del trabajo» y compara los bytes procesados con el estimador.
SELECT texto FROM tweets_silver.tweets WHERE fecha = '2022-03-23' AND idioma = 'es';

-- 6.4 Todas las columnas, toda la tabla.
SELECT * FROM tweets_silver.tweets;

-- 6.5 Cuadre final de las tres tablas Silver. COUNT(*) sobre tablas no lee columnas; los DISTINCT sí.
SELECT (SELECT COUNT(*) FROM tweets_bronze.entrada)                    AS bronze,
       (SELECT COUNT(*) FROM tweets_silver.tweets)                     AS tweets,
       (SELECT COUNT(DISTINCT tweet_id) FROM tweets_silver.hashtags)   AS tweets_con_hashtag,
       (SELECT COUNT(*) FROM tweets_silver.autores)                    AS autores,
       (SELECT SUM(tweets_en_archivo) FROM tweets_silver.autores)      AS tweets_sumados_por_autor,
       (SELECT COUNT(*) FROM tweets_silver.hashtags)                   AS filas_hashtags;
