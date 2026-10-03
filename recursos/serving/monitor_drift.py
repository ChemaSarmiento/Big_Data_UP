"""PSI sobre muestras acotadas; produce un reporte para el DAG, no una orden automática."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd


def calcular_psi(referencia, actual, n_buckets=10):
    if n_buckets < 2:
        raise ValueError("Se necesitan al menos dos buckets")
    reference = pd.to_numeric(pd.Series(referencia), errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    recent = pd.to_numeric(pd.Series(actual), errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if reference.empty or recent.empty:
        raise ValueError("PSI necesita dos muestras no vacías con valores finitos")
    # Repeated quantiles are common with discrete/constant amounts.
    limits = np.unique(np.quantile(reference, np.linspace(0, 1, n_buckets + 1)))
    if len(limits) == 1:
        value = limits[0]; width = max(abs(value) * 0.01, 1.0)
        limits = np.array([-np.inf, value - width, value + width, np.inf])
    else:
        limits[0], limits[-1] = -np.inf, np.inf
    ref_counts = np.histogram(reference, bins=limits)[0].astype(float) + 1e-6
    actual_counts = np.histogram(recent, bins=limits)[0].astype(float) + 1e-6
    expected, observed = ref_counts / ref_counts.sum(), actual_counts / actual_counts.sum()
    return float(np.sum((observed - expected) * np.log(observed / expected)))


def interpretar(psi):
    if psi < 0.1: return "sin cambio relevante bajo esta regla docente"
    if psi < 0.25: return "vigilar e investigar"
    return "investigar drift; evaluar candidato antes de desplegar"


def read_sample(uri, column, max_rows):
    # Monitoring gets bounded Parquet samples, never the multi-GB raw CSV.
    if uri.lower().endswith('.csv'):
        return pd.read_csv(uri, usecols=[column], nrows=max_rows)[column]
    frame = pd.read_parquet(uri, columns=[column])
    if len(frame) > max_rows:
        raise ValueError("El Parquet de monitoreo debe ser una muestra acotada, no el stream completo")
    return frame[column]


def report(reference_uri, recent_uri, column="amount", max_rows=100_000, threshold=0.25):
    reference, recent = read_sample(reference_uri, column, max_rows), read_sample(recent_uri, column, max_rows)
    psi = calcular_psi(reference, recent)
    return {"psi": psi, "threshold": threshold, "investigate": psi >= threshold, "interpretation": interpretar(psi),
            "column": column, "reference": reference_uri, "recent": recent_uri,
            "reference_rows": len(reference), "recent_rows": len(recent), "max_rows": max_rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--referencia", required=True)
    parser.add_argument("--lote-reciente", "--lote_reciente", dest="recent", required=True)
    parser.add_argument("--columna", default="amount")
    parser.add_argument("--salida", required=True, help="Archivo JSON local para revisar o pasar al DAG")
    args = parser.parse_args()
    result = report(args.referencia, args.recent, args.columna)
    Path(args.salida).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__": main()
