"""
monitor_drift.py
Monitoreo de drift de datos: compara la distribución de `amount` entre el set de
entrenamiento (referencia) y un lote reciente de transacciones scoreadas por
07_streaming_scoring.py -- si el lote reciente se separó demasiado de la
referencia, el modelo puede estar viendo un tipo de transacción distinto al que
aprendió (ej. cambio de comportamiento por temporada, o un ataque nuevo).

Usa el Population Stability Index (PSI), el estándar de la industria para esto
(no requiere asumir una distribución particular, y da un número interpretable):
  PSI < 0.1  -> sin drift relevante
  0.1 - 0.25 -> drift moderado, vigilar
  > 0.25     -> drift significativo, considerar reentrenar

pip install pandas numpy

Correr:
  python monitor_drift.py \
      --referencia gs://<TU-BUCKET>/raw/bank_transactions/bank_transactions.csv \
      --lote_reciente gs://<TU-BUCKET>/streaming/scores \
      --columna amount
"""
import argparse

import numpy as np
import pandas as pd


def calcular_psi(referencia: pd.Series, actual: pd.Series, n_buckets: int = 10) -> float:
    limites = np.quantile(referencia, np.linspace(0, 1, n_buckets + 1))
    limites[0], limites[-1] = -np.inf, np.inf

    dist_referencia = pd.cut(referencia, limites).value_counts(normalize=True, sort=False)
    dist_actual = pd.cut(actual, limites).value_counts(normalize=True, sort=False)

    # Evita log(0) / división por 0 en buckets vacíos -- un bucket sin datos no
    # debería romper el cálculo, solo aportar 0 a ese bucket.
    epsilon = 1e-6
    dist_referencia = dist_referencia.clip(lower=epsilon)
    dist_actual = dist_actual.clip(lower=epsilon)

    psi_por_bucket = (dist_actual - dist_referencia) * np.log(dist_actual / dist_referencia)
    return float(psi_por_bucket.sum())


def interpretar(psi: float) -> str:
    if psi < 0.1:
        return "sin drift relevante"
    if psi < 0.25:
        return "drift moderado -- vigilar"
    return "drift significativo -- considerar reentrenar (dispara mlops_pipeline_dag.py manualmente)"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--referencia", required=True, help="CSV/Parquet usado para entrenar (Sesión 4/5)")
    parser.add_argument("--lote_reciente", required=True, help="Parquet de scores recientes (salida de 07_streaming_scoring.py)")
    parser.add_argument("--columna", default="amount")
    args = parser.parse_args()

    referencia = pd.read_csv(args.referencia, usecols=[args.columna])[args.columna]
    lote_reciente = pd.read_parquet(args.lote_reciente, columns=[args.columna])[args.columna]

    psi = calcular_psi(referencia, lote_reciente)
    print(f"=== PSI para '{args.columna}': {psi:.4f} -- {interpretar(psi)} ===")
