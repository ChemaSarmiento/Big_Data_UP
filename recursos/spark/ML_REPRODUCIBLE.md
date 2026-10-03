# Contrato S5–S6 → S10–S12

La misma entrada bancaria tiene `transaction_id`, `timestamp`, `amount`, `currency`, `is_suspicious`. Timestamp UTC, ID único, label binario, monto finito o ausente imputable; cadenas de monto no numéricas se rechazan. Los errores se diagnostican antes del entrenamiento, no se silencian. El script escribe conteos de nulos train/test en métricas.

## Ejecutar el baseline

Subir `04_pipeline_ml.py` y `ml_common.py` al bucket. Elegir fecha según la cobertura real del dataset, con ambas clases a cada lado, y **fijarla antes de evaluar**. No asumir que la fecha ilustrativa coincide con el archivo del Drive.

```bash
export MODEL_RUN=s6-baseline-01
export CUTOFF=<FECHA_ISO_DEL_DATASET>
gcloud dataproc jobs submit pyspark gs://$BUCKET_NAME/scripts/04_pipeline_ml.py \
  --cluster=curso-cluster --region=us-central1 \
  --py-files=gs://$BUCKET_NAME/scripts/ml_common.py -- \
  --input gs://$BUCKET_NAME/raw/bank_transactions/bank_transactions.csv \
  --output gs://$BUCKET_NAME/modelos/runs/$MODEL_RUN --cutoff "$CUTOFF"
```

En local: activar el entorno Python 3.11, Java 17 y `PYSPARK_PYTHON` apuntando al mismo intérprete que el driver; usar paths locales y `spark-submit --master local[2]`. El entorno del cluster ya proporciona GCS/Java compatibles.

## Artefactos del candidato

| Ruta bajo `modelos/runs/<RUN_ID>` | Uso |
|---|---|
| `pipeline/` | Hora derivada + transformaciones ajustadas con train + clasificador |
| `metrics.json` | ROC-AUC, PR-AUC, conteos/nulos, corte, entrada y URI del mismo candidato |
| `referencia.parquet/` | Muestra acotada de montos no nulos de train para investigar drift |
| `features/` (notebook S5) | Transformador de features sin clasificador |

`<RUN_ID>` no se comparte entre candidatos. El CLI baseline guarda un modelo logístico; la extensión del notebook compara otras opciones. Si se elige CV/GBT, guardar su pipeline completo y escribir sus propias métricas/referencia, no reutilizar las del baseline. Airflow toma únicamente el candidato de su ejecución.

## Selección y lectura de resultados

Se aprende imputación, categorías y escala solo sobre train. Para CV, envolver el **pipeline completo** para que se reajuste dentro de cada fold; no hacer CV sobre features aprendidas con todos los folds. CV aleatoria dentro de train no equivale a validación temporal; si el objetivo exige predecir futuro, añadir validación por bloques y reservar test final.

Una ROC-AUC alta no fija el umbral de negocio. Comparar PR-AUC con prevalencia, precisión/recall, costo de errores y un baseline. Los umbrales docentes del DAG necesitan justificación y no reemplazan evaluación de performance. Guardar una gráfica con unidades/contexto y conclusión, tiempos/condiciones de cómputo, costo observado y limitaciones de la etiqueta `is_suspicious`.
