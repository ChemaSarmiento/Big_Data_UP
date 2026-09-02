"""
load.py — Etapa de CARGA
Lee la tabla ya limpia de data/processed/ y la carga a MariaDB con un
upsert idempotente: volver a correr este script con el mismo rango de
fechas actualiza las filas existentes en vez de duplicarlas.
"""

import os
import sys
from pathlib import Path

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

PROCESSED_DIR = Path(__file__).parent / "data" / "processed"

load_dotenv(Path(__file__).parent / ".env")

SQL_UPSERT = """
    INSERT INTO tipo_cambio
        (fecha, moneda_origen, moneda_destino, tasa, variacion_diaria, variacion_pct, promedio_movil_7d)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        tasa = VALUES(tasa),
        variacion_diaria = VALUES(variacion_diaria),
        variacion_pct = VALUES(variacion_pct),
        promedio_movil_7d = VALUES(promedio_movil_7d)
"""


def _conectar():
    faltantes = [v for v in ("DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME") if not os.getenv(v)]
    if faltantes:
        print(f"[load] ERROR: faltan variables de entorno: {faltantes}. "
              f"¿Copiaste .env.example a .env?", file=sys.stderr)
        raise EnvironmentError(f"Variables de entorno faltantes: {faltantes}")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )


def _leer_procesado() -> pd.DataFrame:
    ruta = PROCESSED_DIR / "tipo_cambio_clean.csv"
    if not ruta.exists():
        raise FileNotFoundError(
            "[load] No existe data/processed/tipo_cambio_clean.csv. Corre transform.py primero."
        )
    df = pd.read_csv(ruta, parse_dates=["fecha"])
    # NaN de pandas no es válido para mysql-connector; se convierte a None
    df = df.where(pd.notnull(df), None)
    return df


def cargar_a_mariadb(df: pd.DataFrame) -> int:
    conexion = _conectar()
    cursor = conexion.cursor()

    filas = [
        (
            row.fecha.date(),
            row.moneda_origen,
            row.moneda_destino,
            float(row.tasa),
            float(row.variacion_diaria) if row.variacion_diaria is not None else None,
            float(row.variacion_pct) if row.variacion_pct is not None else None,
            float(row.promedio_movil_7d) if row.promedio_movil_7d is not None else None,
        )
        for row in df.itertuples(index=False)
    ]

    try:
        cursor.executemany(SQL_UPSERT, filas)
        conexion.commit()
        return cursor.rowcount
    except mysql.connector.Error as e:
        conexion.rollback()
        print(f"[load] ERROR al cargar a MariaDB, se hizo rollback: {e}", file=sys.stderr)
        raise
    finally:
        cursor.close()
        conexion.close()


def main():
    df = _leer_procesado()
    print(f"[load] Cargando {len(df)} filas a MariaDB ...")
    filas_afectadas = cargar_a_mariadb(df)
    print(f"[load] OK — {filas_afectadas} filas afectadas (inserts + updates)")


if __name__ == "__main__":
    main()
