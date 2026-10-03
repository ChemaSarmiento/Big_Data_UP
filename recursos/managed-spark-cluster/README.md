# Cluster docente temporal — crédito GCP US$300

La configuración usa Spark 3.5 de la imagen `2.2-debian12`, con dos workers. Ver [presupuesto, permisos y limpieza](../../environment/gcp-setup.md). Las VMs, discos y tarifa de Spark consumen crédito desde la creación hasta la eliminación. Estimar costo y revisar cuota **antes** de ejecutar.

```bash
export PROJECT_ID=<PROJECT_ID>
export BUCKET_NAME=<BUCKET_UNICO>
export CLUSTER_NAME=curso-cluster
gcloud dataproc clusters create "$CLUSTER_NAME" \
    --project="$PROJECT_ID" --region=us-central1 --zone=us-central1-a \
    --image-version=2.2-debian12 \
    --master-machine-type=e2-standard-2 --master-boot-disk-size=50 \
    --num-workers=2 --worker-machine-type=e2-standard-2 --worker-boot-disk-size=50 \
    --no-address --optional-components=JUPYTER --enable-component-gateway \
    --max-idle=20m --max-age=3h \
    --scopes=https://www.googleapis.com/auth/cloud-platform
```

Este perfil tiene 3 VMs y 150 GB de discos configurados, además del bucket. No es un cluster gratuito. Verificar Private Google Access en la subred y permisos de la cuenta de servicio para leer/escribir el bucket. Para cargar paquetes externos en un cluster sin IP pública, preparar salida con Cloud NAT (con su costo) o artefactos accesibles desde el bucket; no asumir acceso a Maven/PyPI.

## Labs de ML y streaming

```bash
gcloud storage cp recursos/spark/04_pipeline_ml.py recursos/spark/ml_common.py gs://$BUCKET_NAME/scripts/
gcloud storage cp recursos/streaming/stream_common.py recursos/streaming/07a_streaming_conteo.py recursos/streaming/07_streaming_scoring.py gs://$BUCKET_NAME/scripts/
```

Ejecutar `gcloud dataproc jobs submit pyspark` con `--py-files=gs://.../ml_common.py` o `stream_common.py`, según el lab. Ver los comandos completos en sus READMEs. Estos labs usan librerías ya incluidas en el cluster y no necesitan el conector retirado de Pub/Sub Lite.

## Lakehouse S7–8

Recrear el cluster con las propiedades de [Iceberg](../lakehouse-iceberg/README.md), runtime `iceberg-spark-runtime-3.5_2.12:1.6.1` y extensión SQL. Resolver/almacenar el JAR antes del lab si se opera sin salida a Internet. No mezclar una imagen Spark 3.3 con un runtime para Spark 3.5.

## Cierre obligatorio

```bash
gcloud dataproc clusters delete "$CLUSTER_NAME" --region=us-central1
```

Confirmar eliminación en la consola y revisar el saldo. Guardar checkpoints/modelos en GCS; `/tmp` del cluster desaparece. `Instalacion_Cluster.pdf` y `hugging_face_deps.sh` son referencias históricas, no la receta obligatoria actual. Hugging Face/GPU queda como panorama opcional: no es necesario para los entregables de MLlib.
