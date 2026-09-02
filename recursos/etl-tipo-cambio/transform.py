"""
transform.py — Etapa de TRANSFORMACIÓN
Lee el JSON crudo más reciente de data/raw/, lo convierte a una tabla larga
(fecha, moneda_origen, moneda_destino, tasa), calcula columnas derivadas
y aplica validaciones básicas de calidad de datos. Esta es la capa "silver".
"""

import json
import sys
from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent / "data" / "processed"


def _archivo_crudo_mas_reciente() -> Path:
    archivos = sorted(RAW_DIR.glob("tipo_cambio_*.json"))
    if not archivos:
        raise FileNotFoundError(
            "[transform] No hay archivos en data/raw/. Corre extract.py primero."
        )
    return archivos[-1]


def cargar_crudo(ruta: Path) -> dict:
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def a_tabla_larga(datos: dict) -> pd.DataFrame:
    """
    El JSON de Frankfurter viene anidado como:
    {"base": "USD", "rates": {"2024-01-01": {"MXN": 17.05}, "2024-01-02": {...}, ...}}
    Esta función lo aplana a una fila por (fecha, moneda_destino).
    """
    moneda_base = datos["base"]
    filas = []
    for fecha_str, tasas_del_dia in datos["rates"].items():
        for moneda_destino, tasa in tasas_del_dia.items():
            filas.append({
                "fecha": fecha_str,
                "moneda_origen": moneda_base,
                "moneda_destino": moneda_destino,
                "tasa": tasa,
            })

    df = pd.DataFrame(filas)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values(["moneda_destino", "fecha"]).reset_index(drop=True)
    return df


def calcular_columnas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Variación diaria, variación %, y promedio móvil de 7 días -- por cada par de moneda."""
    df = df.copy()
    grupo = df.groupby("moneda_destino")["tasa"]

    df["variacion_diaria"] = grupo.diff()
    df["variacion_pct"] = grupo.pct_change() * 100
    df["promedio_movil_7d"] = grupo.transform(lambda s: s.rolling(window=7, min_periods=1).mean())

    return df


def validar_calidad(df: pd.DataFrame) -> None:
    """
    Chequeos de calidad de datos básicos. Si algo falla, se detiene el pipeline
    en vez de cargar datos sospechosos a la base -- este es el punto donde,
    en un pipeline real, se dispararía una alerta.
    """
    errores = []

    if df["tasa"].isnull().any():
        errores.append("Hay valores nulos en la columna 'tasa'.")

    if (df["tasa"] <= 0).any():
        errores.append("Hay tasas de cambio menores o iguales a cero.")

    duplicados = df.duplicated(subset=["fecha", "moneda_origen", "moneda_destino"]).sum()
    if duplicados > 0:
        errores.append(f"Hay {duplicados} filas duplicadas por (fecha, origen, destino).")

    # Umbral de variación diaria irreal para un tipo de cambio entre monedas mayores
    # (ajustar si se agregan monedas con volatilidad estructuralmente distinta).
    variacion_extrema = df["variacion_pct"].abs() > 15
    if variacion_extrema.any():
        errores.append(
            f"Hay {variacion_extrema.sum()} filas con variación diaria > 15%, "
            "revisar antes de cargar."
        )

    if errores:
        print("[transform] Validación de calidad FALLÓ:", file=sys.stderr)
        for e in errores:
            print(f"  - {e}", file=sys.stderr)
        raise ValueError("Los datos no pasaron la validación de calidad. Revisar antes de cargar.")


def guardar_procesado(df: pd.DataFrame) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    ruta = PROCESSED_DIR / "tipo_cambio_clean.csv"
    df.to_csv(ruta, index=False)
    return ruta


def main():
    ruta_cruda = _archivo_crudo_mas_reciente()
    print(f"[transform] Leyendo {ruta_cruda} ...")

    datos = cargar_crudo(ruta_cruda)
    df = a_tabla_larga(datos)
    df = calcular_columnas_derivadas(df)
    validar_calidad(df)

    ruta_salida = guardar_procesado(df)
    print(f"[transform] OK — {len(df)} filas transformadas y validadas -> {ruta_salida}")


if __name__ == "__main__":
    main()
