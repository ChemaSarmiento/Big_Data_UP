#!/usr/bin/env bash
set -euo pipefail
# En Cloud Shell, subir SOLO los dos archivos pequeños de la muestra.
# Ejecutar desde su carpeta. Sobrescribe exclusivamente el staging entrada.
: "${PROJECT_ID:?Define PROJECT_ID con el proyecto autorizado del taller}"
bq --project_id="$PROJECT_ID" --location=us-central1 load \
  --replace --source_format=CSV --skip_leading_rows=1 \
  --allow_quoted_newlines=true --max_bad_records=0 \
  emergente_bronze.entrada all_data_muestra.csv esquema-bronze.json
