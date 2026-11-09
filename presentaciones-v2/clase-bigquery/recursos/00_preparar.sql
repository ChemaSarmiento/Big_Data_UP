-- GoogleSQL. Proyecto de laboratorio seleccionado en la consola.
-- Nombres exclusivos del taller. No apuntar a datasets del curso o productivos.
-- Región propuesta: us-central1; cambiar coherentemente si la política exige otra.
-- Expiración de tablas nuevas:7 días. Conservar archivos originales fuera de BigQuery.
CREATE SCHEMA IF NOT EXISTS emergente_bronze
OPTIONS(location='us-central1', default_table_expiration_days=7);
CREATE SCHEMA IF NOT EXISTS emergente_silver
OPTIONS(location='us-central1', default_table_expiration_days=7);
CREATE SCHEMA IF NOT EXISTS emergente_gold
OPTIONS(location='us-central1', default_table_expiration_days=7);
CREATE TABLE IF NOT EXISTS emergente_bronze.entrada (
  producto STRING,
  presentacion STRING,
  marca STRING,
  categoria STRING,
  catalogo STRING,
  precio STRING,
  fechaRegistro STRING,
  cadenaComercial STRING,
  giro STRING,
  nombreComercial STRING,
  direccion STRING,
  estado STRING,
  municipio STRING,
  latitud STRING,
  longitud STRING
);
