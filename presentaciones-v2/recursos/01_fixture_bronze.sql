-- GoogleSQL. EJEMPLO ILUSTRATIVO, no filas del Drive ni prueba de escala.
-- Ejecutar en un proyecto de laboratorio. Reemplaza SOLO tablas curso_*.
-- Región propuesta us-central1: si la política exige otra, cambiarla en todo el flujo.
CREATE SCHEMA IF NOT EXISTS curso_bronze OPTIONS(location='us-central1');
CREATE SCHEMA IF NOT EXISTS curso_silver OPTIONS(location='us-central1');
CREATE SCHEMA IF NOT EXISTS curso_gold OPTIONS(location='us-central1');
CREATE OR REPLACE TABLE curso_bronze.observaciones_raw AS
SELECT * FROM UNNEST([
STRUCT('A1' AS id, 'p1' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '10' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('A2' AS id, 'p2' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '20' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('A3' AS id, 'p3' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '30' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('A4' AS id, 'p4' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '40' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('A5' AS id, 'p5' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '50' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('B1' AS id, 'p1' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'B' AS establecimiento, '2024-01-15' AS fecha_texto, '12' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('B2' AS id, 'p2' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'B' AS establecimiento, '2024-01-15' AS fecha_texto, '22' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('B3' AS id, 'p3' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'B' AS establecimiento, '2024-01-15' AS fecha_texto, '32' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('B4' AS id, 'p4' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'B' AS establecimiento, '2024-01-15' AS fecha_texto, '42' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('B5' AS id, 'p5' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'B' AS establecimiento, '2024-01-15' AS fecha_texto, '52' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('C1' AS id, 'p1' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'C' AS establecimiento, '2024-01-15' AS fecha_texto, '8' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('C2' AS id, 'p2' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'C' AS establecimiento, '2024-01-15' AS fecha_texto, '18' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('C3' AS id, 'p3' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'C' AS establecimiento, '2024-01-15' AS fecha_texto, '28' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('C4' AS id, 'p4' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'C' AS establecimiento, '2024-01-15' AS fecha_texto, '0' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('C5' AS id, 'p5' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'C' AS establecimiento, 'fecha-invalida' AS fecha_texto, '48' AS precio_texto, 'fixture-curso.csv' AS archivo_origen),
STRUCT('A1' AS id, 'p1' AS producto, 'Marca demo' AS marca, '1 envase' AS presentacion, 'A' AS establecimiento, '2024-01-15' AS fecha_texto, '10' AS precio_texto, 'fixture-curso.csv' AS archivo_origen)
]);
SELECT COUNT(*) AS filas FROM curso_bronze.observaciones_raw; -- 16 en el fixture
