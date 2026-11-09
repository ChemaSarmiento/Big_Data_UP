#!/usr/bin/env bash
set -euo pipefail
# Ruta docente: objeto completo YA preparado en GCS, ubicación compatible.
# No descarga20.7GB a Cloud Shell. Sobrescribe exclusivamente entrada.
: "${PROJECT_ID:?Define PROJECT_ID con el proyecto autorizado}"
: "${SOURCE_URI:?Define SOURCE_URI con gs://bucket/ruta/all_data.csv}"
[[ "$SOURCE_URI" == gs://* ]] || { echo 'Se requiere URI gs://'; exit 1; }
bq --project_id="$PROJECT_ID" --location=us-central1 load \
  --replace --source_format=CSV --skip_leading_rows=1 \
  --allow_quoted_newlines=true --max_bad_records=0 \
  emergente_bronze.entrada "$SOURCE_URI" esquema-bronze.json
