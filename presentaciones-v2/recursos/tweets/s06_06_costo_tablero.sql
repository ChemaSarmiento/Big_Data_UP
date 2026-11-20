-- Paso 6 · ¿Cuánto cuesta abrir tu tablero? Mira las consultas que lanzó en la última hora.
-- cache_hit = true significa que BigQuery reutilizó un resultado reciente y no leyó datos.
SELECT FORMAT_TIMESTAMP('%H:%M:%S', creation_time) AS hora,
       cache_hit,
       ROUND(total_bytes_billed / POW(1024, 2), 1) AS mib_facturados,
       ARRAY_TO_STRING(ARRAY(SELECT t.table_id FROM UNNEST(referenced_tables) AS t), ', ') AS tablas
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE job_type = 'QUERY'
  AND creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR)
ORDER BY creation_time DESC
LIMIT 10;
