-- Ejecutar tras cargar la muestra o el CSV completo en entrada.
-- Bronze conserva valores y duplicados del lote; entrada es el área de carga reemplazable.
-- Ejecución serial en proyecto dedicado: no protege contra dos escritores concurrentes.
DECLARE lote STRING DEFAULT 'all_data_muestra_v1';
DECLARE fuente STRING DEFAULT 'drive:1dLxKFxawXTTaqCDr9Y9YpYdWTpOhol42; muestra 4500 filas';
CREATE TABLE IF NOT EXISTS emergente_bronze.observaciones AS
SELECT e.*, CAST(NULL AS STRING) AS lote_id,
 CAST(NULL AS STRING) AS fuente_uri, CURRENT_TIMESTAMP() AS ingestado_en,
 TO_HEX(SHA256(TO_JSON_STRING(e))) AS fila_hash
FROM emergente_bronze.entrada e WHERE FALSE;
ASSERT (SELECT COUNT(*) > 0 FROM emergente_bronze.entrada) AS 'entrada está vacía';
ASSERT (SELECT COUNT(*) = 0 FROM emergente_bronze.observaciones WHERE lote_id=lote)
 AS 'Lote ya cargado: no lo repitas. Para otro archivo usa otro ID y su fuente.';
INSERT INTO emergente_bronze.observaciones
SELECT e.*, lote, fuente, CURRENT_TIMESTAMP(), TO_HEX(SHA256(TO_JSON_STRING(e)))
FROM emergente_bronze.entrada e;
SELECT lote_id, COUNT(*) AS filas, COUNT(DISTINCT fila_hash) AS filas_distintas
FROM emergente_bronze.observaciones GROUP BY lote_id;
