-- =====================================================================
-- hive-queries.sql
-- Progresión: crear tabla particionada -> filtros simples -> joins -> window functions
-- Dataset de referencia: ver recursos/datasets/README.md
-- =====================================================================

-- =====================================================================
-- SECCIÓN 1: Definición de la tabla externa
-- =====================================================================

CREATE DATABASE IF NOT EXISTS curso_bigdata;
USE curso_bigdata;

-- Se particiona por `sucursal` porque es la columna por la que más se filtra en las
-- consultas analíticas del curso (evita escanear todo el dataset en cada query).
-- Se usa formato Parquet (no CSV/texto) porque es columnar: las agregaciones que
-- siguen solo leen las columnas que necesitan, no la fila completa.
CREATE EXTERNAL TABLE IF NOT EXISTS transacciones (
    id_transaccion  BIGINT,
    fecha           DATE,
    tipo_transaccion STRING,
    monto           DOUBLE,
    cliente_id      STRING,
    es_fraude       INT
)
PARTITIONED BY (sucursal STRING)
STORED AS PARQUET
LOCATION 'gs://<TU-BUCKET>/curso-bigdata/transacciones/';

-- Después de cargar archivos directamente en el path de cada partición en Cloud
-- Storage, hay que avisarle a Hive que existen (si no, las queries no las ven):
MSCK REPAIR TABLE transacciones;

-- =====================================================================
-- SECCIÓN 2: Consultas de ejemplo (progresión sugerida)
-- =====================================================================

-- --- 2.1 Filtro simple sobre la columna de partición (rápido: solo lee esa partición) ---
SELECT tipo_transaccion, COUNT(*) AS num_transacciones
FROM transacciones
WHERE sucursal = 'sucursal_norte'
GROUP BY tipo_transaccion;

-- --- 2.2 Filtro sobre columna que NO es partición (más lento: escanea todas las particiones) ---
-- Se deja a propósito para que el grupo compare el tiempo de ejecución vs. 2.1
SELECT sucursal, COUNT(*) AS num_transacciones
FROM transacciones
WHERE monto > 5000
GROUP BY sucursal;

-- --- 2.3 Join con una segunda tabla (ej. catálogo de clientes) ---
CREATE EXTERNAL TABLE IF NOT EXISTS clientes (
    cliente_id  STRING,
    segmento    STRING,
    antiguedad_meses INT
)
STORED AS PARQUET
LOCATION 'gs://<TU-BUCKET>/curso-bigdata/clientes/';

SELECT c.segmento,
       COUNT(*) AS num_transacciones,
       SUM(t.monto) AS monto_total
FROM transacciones t
JOIN clientes c ON t.cliente_id = c.cliente_id
GROUP BY c.segmento
ORDER BY monto_total DESC;

-- --- 2.4 Window function: top 3 transacciones por monto en cada sucursal ---
-- Este es el mismo patrón que se usa en 03_spark_sql.py — a propósito, para que
-- el grupo vea que el SQL analítico es prácticamente idéntico entre Hive y Spark SQL.
SELECT sucursal, id_transaccion, monto, ranking
FROM (
    SELECT sucursal, id_transaccion, monto,
           RANK() OVER (PARTITION BY sucursal ORDER BY monto DESC) AS ranking
    FROM transacciones
) rankeado
WHERE ranking <= 3;

-- --- 2.5 Tasa de fraude por segmento de cliente (conecta con el pipeline de ML de Spark) ---
SELECT c.segmento,
       AVG(t.es_fraude) AS tasa_fraude,
       COUNT(*) AS num_transacciones
FROM transacciones t
JOIN clientes c ON t.cliente_id = c.cliente_id
GROUP BY c.segmento
ORDER BY tasa_fraude DESC;

-- =====================================================================
-- SECCIÓN 3: Caso real del curso — Carpetas de investigación (CDMX)
-- Rescatado y corregido de hive_commands_updated.sql del repo original
-- (ese archivo era en realidad Markdown con la extensión equivocada).
-- Dataset oficial y vivo: https://datos.cdmx.gob.mx/dataset/carpetas-de-investigacion-fgj-de-la-ciudad-de-mexico
-- Se actualiza mensualmente -- no depende del bucket del curso de un semestre anterior.
-- =====================================================================

-- --- 3.1 Tabla externa sobre el CSV descargado del portal de datos abiertos ---
CREATE EXTERNAL TABLE IF NOT EXISTS carpetas_investigacion (
    id                    INT,
    ao_hechos             INT,
    mes_hechos            STRING,
    fecha_hechos          TIMESTAMP,
    delito                STRING,
    categoria_delito      STRING,
    fiscalia              STRING,
    agencia               STRING,
    unidad_investigacion  STRING,
    colonia_hechos        STRING,
    alcaldia_hechos       STRING,
    fecha_inicio          TIMESTAMP,
    mes_inicio            STRING,
    ao_inicio             INT,
    longitud              FLOAT,
    latitud               FLOAT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION 'gs://<TU-BUCKET>/carpetas_investigacion/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- --- 3.2 Versión particionada (Parquet), para comparar rendimiento contra la de arriba ---
-- Nota de diseño: se particiona por año/mes porque es exactamente como se pregunta en
-- clase ("¿cuántos delitos de tipo X hubo en marzo de 2024?") -- coincide con el patrón
-- de acceso real, que es la razón correcta para elegir una columna de partición.
CREATE EXTERNAL TABLE IF NOT EXISTS carpetas_investigacion_particionada (
    id                   INT,
    delito               STRING,
    categoria_delito     STRING,
    fiscalia             STRING,
    agencia              STRING,
    colonia_hechos       STRING,
    alcaldia_hechos      STRING,
    longitud             FLOAT,
    latitud              FLOAT
)
PARTITIONED BY (anio INT, mes INT)
STORED AS PARQUET;

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

INSERT INTO carpetas_investigacion_particionada
PARTITION (anio, mes)
SELECT id, delito, categoria_delito, fiscalia, agencia, colonia_hechos, alcaldia_hechos,
       longitud, latitud, ao_hechos AS anio, MONTH(fecha_hechos) AS mes
FROM carpetas_investigacion;

-- --- 3.3 Pregunta analítica real: top delitos por alcaldía en un periodo dado ---
-- Al filtrar por anio/mes sobre la tabla particionada, Hive solo lee esas particiones
-- (partition pruning) -- comparar el tiempo contra la misma consulta sobre 3.1.
SELECT alcaldia_hechos, categoria_delito, COUNT(*) AS total
FROM carpetas_investigacion_particionada
WHERE anio = 2025 AND mes = 6
GROUP BY alcaldia_hechos, categoria_delito
ORDER BY total DESC
LIMIT 20;

-- --- 3.4 Bucketing: distribuir por alcaldía para optimizar JOINs y muestreo ---
-- (30 buckets es el valor que se validaba en el lab original: se espera ver exactamente
-- 30 archivos de salida en la carpeta de la tabla en Cloud Storage al terminar la carga)
CREATE EXTERNAL TABLE IF NOT EXISTS carpetas_investigacion_bucketed (
    id                   INT,
    delito               STRING,
    categoria_delito     STRING,
    colonia_hechos       STRING,
    alcaldia_hechos      STRING,
    fecha_hechos         TIMESTAMP
)
CLUSTERED BY (alcaldia_hechos) SORTED BY (fecha_hechos) INTO 30 BUCKETS
STORED AS PARQUET
LOCATION 'gs://<TU-BUCKET>/carpetas_investigacion_bucketed/';

SET hive.enforce.bucketing = true;

INSERT INTO carpetas_investigacion_bucketed
SELECT id, delito, categoria_delito, colonia_hechos, alcaldia_hechos, fecha_hechos
FROM carpetas_investigacion;
