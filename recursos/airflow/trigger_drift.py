"""Disparador explícito desde un reporte PSI revisado, sin credenciales GCP."""
import argparse
import json
import subprocess
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", required=True)
    parser.add_argument("--run-id", required=True, help="ID único de la investigación: drift-YYYYMMDD-HHMM")
    args = parser.parse_args()
    report = json.loads(Path(args.report).read_text())
    if not report["investigate"]:
        print("Sin trigger: PSI bajo el umbral del reporte"); return
    config = {"reason": "drift", "psi": report["psi"], "threshold": report["threshold"], "report": args.report}
    subprocess.run(["airflow", "dags", "trigger", "mlops_fraude_bank_transactions", "--run-id", args.run_id,
                    "--conf", json.dumps(config)], check=True)


if __name__ == "__main__": main()
