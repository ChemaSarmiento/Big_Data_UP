-- Paso 1 · ¿Existen tus tablas Gold y cuánto pesan? Usa metadatos: el estimador debe decir 0 bytes.
SELECT table_id AS tabla, row_count AS filas, size_bytes AS bytes
FROM tweets_gold.__TABLES__
ORDER BY table_id;
