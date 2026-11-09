-- GoogleSQL. Subir precios-ilustrativos.csv al bucket del equipo ANTES de ejecutar.
-- Cambiar SOLO uri por el objeto real. Este esquema es del FIXTURE, no all_data.csv.
DECLARE uri STRING DEFAULT 'REEMPLAZAR_POR_URI_GS_DEL_CSV_ILUSTRATIVO';
ASSERT (STARTS_WITH(uri, 'gs://')) AS 'Reemplaza uri por el objeto del fixture subido a GCS';
CREATE SCHEMA IF NOT EXISTS curso_bronze OPTIONS(location='us-central1');
EXECUTE IMMEDIATE FORMAT("""
CREATE OR REPLACE EXTERNAL TABLE curso_bronze.observaciones_externas (
 id STRING, producto STRING, marca STRING, presentacion STRING,
 establecimiento STRING, fecha_texto STRING, precio_texto STRING, archivo_origen STRING
) OPTIONS (format='CSV', uris=[%T], skip_leading_rows=1)
""", uri);
-- Fuente y dataset deben tener ubicación compatible.
SELECT id, producto, establecimiento, fecha_texto, precio_texto
FROM curso_bronze.observaciones_externas ORDER BY id LIMIT 10;
-- Materializar copia de trabajo del fixture para S4/S5; conserva el CSV original.
CREATE OR REPLACE TABLE curso_bronze.observaciones_raw AS
SELECT * FROM curso_bronze.observaciones_externas;
SELECT COUNT(*) AS filas FROM curso_bronze.observaciones_raw; -- 16 en el fixture
