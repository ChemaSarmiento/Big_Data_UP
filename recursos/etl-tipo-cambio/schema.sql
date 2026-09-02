-- schema.sql
-- Tabla destino del ejercicio de ETL. La llave primaria compuesta
-- (fecha, moneda_origen, moneda_destino) es lo que hace posible el
-- upsert idempotente en load.py: si se vuelve a cargar la misma fecha,
-- se actualiza en vez de duplicarse.

CREATE TABLE IF NOT EXISTS tipo_cambio (
    fecha               DATE            NOT NULL,
    moneda_origen       VARCHAR(3)      NOT NULL,
    moneda_destino      VARCHAR(3)      NOT NULL,
    tasa                DECIMAL(14,6)   NOT NULL,
    variacion_diaria    DECIMAL(14,6)   NULL,
    variacion_pct       DECIMAL(8,4)    NULL,
    promedio_movil_7d   DECIMAL(14,6)   NULL,
    cargado_en          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (fecha, moneda_origen, moneda_destino)
) ENGINE=InnoDB;
