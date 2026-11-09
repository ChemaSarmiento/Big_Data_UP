#!/usr/bin/env bash
# Solo lectura: no crea recursos ni modifica la configuración.
set -euo pipefail
gcloud config get project
