"""
extract.py — Etapa de EXTRACCIÓN
Llama a la API pública de Frankfurter (tipos de cambio históricos, sin necesidad
de API key) y guarda la respuesta cruda en data/raw/ tal cual llega, sin transformar
nada todavía. Esta es la capa "bronze": el dato tal como lo entregó la fuente.
"""

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

import requests

BASE_URL = "https://api.frankfurter.app"
RAW_DIR = Path(__file__).parent / "data" / "raw"


def extraer_serie_historica(moneda_base: str, monedas_destino: list[str],
                             fecha_inicio: date, fecha_fin: date) -> dict:
    """
    Llama al endpoint de series de tiempo de Frankfurter:
    GET /{fecha_inicio}..{fecha_fin}?from={base}&to={destino1,destino2,...}
    Devuelve el JSON crudo tal como lo entrega la API.
    """
    simbolos = ",".join(monedas_destino)
    url = f"{BASE_URL}/{fecha_inicio.isoformat()}..{fecha_fin.isoformat()}"
    params = {"from": moneda_base, "to": simbolos}

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[extract] ERROR al llamar a la API: {e}", file=sys.stderr)
        print("[extract] Si el problema persiste, revisar si el endpoint "
              "cambió a https://api.frankfurter.dev/v1/ (ver README.md)", file=sys.stderr)
        raise

    datos = resp.json()
    if "rates" not in datos or not datos["rates"]:
        raise ValueError(
            f"[extract] La API respondió sin datos para el rango "
            f"{fecha_inicio}..{fecha_fin}. Respuesta: {datos}"
        )
    return datos


def guardar_crudo(datos: dict, fecha_inicio: date, fecha_fin: date) -> Path:
    """Guarda el JSON crudo, sin modificar, con nombre trazable al rango de fechas."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    nombre_archivo = f"tipo_cambio_{fecha_inicio.isoformat()}_{fecha_fin.isoformat()}.json"
    ruta = RAW_DIR / nombre_archivo
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return ruta


def main():
    parser = argparse.ArgumentParser(description="Extraer tipo de cambio histórico (capa bronze)")
    parser.add_argument("--base", default="USD", help="Moneda base (default: USD)")
    parser.add_argument("--symbols", default="MXN", help="Monedas destino separadas por coma (default: MXN)")
    parser.add_argument("--dias", type=int, default=90, help="Cuántos días hacia atrás extraer (default: 90)")
    args = parser.parse_args()

    monedas_destino = [m.strip().upper() for m in args.symbols.split(",")]
    fecha_fin = date.today()
    fecha_inicio = fecha_fin - timedelta(days=args.dias)

    print(f"[extract] Extrayendo {args.base} -> {monedas_destino} "
          f"de {fecha_inicio} a {fecha_fin} ...")

    datos = extraer_serie_historica(args.base.upper(), monedas_destino, fecha_inicio, fecha_fin)
    ruta = guardar_crudo(datos, fecha_inicio, fecha_fin)

    num_fechas = len(datos.get("rates", {}))
    print(f"[extract] OK — {num_fechas} fechas guardadas en {ruta}")


if __name__ == "__main__":
    main()
