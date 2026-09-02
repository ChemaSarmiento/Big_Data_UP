"""
run_etl.py — Orquestador
Corre las 3 etapas (extract -> transform -> load) en orden, con logging
de tiempos. Si una etapa falla, se detiene el pipeline (no tiene sentido
cargar datos si la transformación falló).

Uso:
    python run_etl.py --base USD --symbols MXN --dias 90
"""

import argparse
import time
from datetime import date, timedelta

import extract
import load
import transform


def main():
    parser = argparse.ArgumentParser(description="Pipeline de ETL: tipo de cambio -> MariaDB")
    parser.add_argument("--base", default="USD")
    parser.add_argument("--symbols", default="MXN")
    parser.add_argument("--dias", type=int, default=90)
    args = parser.parse_args()

    monedas_destino = [m.strip().upper() for m in args.symbols.split(",")]
    fecha_fin = date.today()
    fecha_inicio = fecha_fin - timedelta(days=args.dias)

    inicio_total = time.time()

    print("=" * 60)
    print("ETAPA 1/3: EXTRACT")
    print("=" * 60)
    t0 = time.time()
    datos = extract.extraer_serie_historica(args.base.upper(), monedas_destino, fecha_inicio, fecha_fin)
    extract.guardar_crudo(datos, fecha_inicio, fecha_fin)
    print(f"[run_etl] Extract completado en {time.time() - t0:.1f}s")

    print("=" * 60)
    print("ETAPA 2/3: TRANSFORM")
    print("=" * 60)
    t0 = time.time()
    df = transform.a_tabla_larga(datos)
    df = transform.calcular_columnas_derivadas(df)
    transform.validar_calidad(df)
    transform.guardar_procesado(df)
    print(f"[run_etl] Transform completado en {time.time() - t0:.1f}s")

    print("=" * 60)
    print("ETAPA 3/3: LOAD")
    print("=" * 60)
    t0 = time.time()
    df_cargar = df.where(df.notnull(), None)
    filas_afectadas = load.cargar_a_mariadb(df_cargar)
    print(f"[run_etl] Load completado en {time.time() - t0:.1f}s "
          f"({filas_afectadas} filas afectadas)")

    print("=" * 60)
    print(f"PIPELINE COMPLETO en {time.time() - inicio_total:.1f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
