# Managed Service for Apache Spark — creación de cluster

Reemplaza `MLOPS/` del repo original (que todavía usaba el nombre "Dataproc" en su
prosa y README — actualizado aquí). Los comandos `gcloud dataproc ...` **no cambiaron**;
solo el nombre comercial del producto.

## Qué cambió respecto al original

- Los comandos tenían hardcodeado el bucket del semestre anterior
  (`gs://big-data-lunes-20260223/...`) — se reemplazó por `$BUCKET_NAME`, una variable
  que cada quien define con su propio bucket. Un comando con un bucket ajeno hardcodeado
  simplemente falla para cualquiera que no sea el instructor original.
- Se agregó la nota de nombre "Managed Service for Apache Spark" (2026).
- `Instalacion_Cluster.pdf` y `hugging_face_deps.sh` se conservan tal cual — seguían
  siendo útiles y no tenían nada que corregir.

## A) Cluster estándar (Jupyter + Zeppelin, para las sesiones de Spark/Hive)

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export ZONE=us-central1-a
export CLUSTER_NAME=curso-cluster
export BUCKET_NAME=<tu-bucket>

gcloud dataproc clusters create $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --zone=$ZONE \
    --image-version=2.1-ubuntu20 \
    --master-machine-type=e2-highmem-2 \
    --master-boot-disk-size=50 \
    --num-workers=3 \
    --worker-machine-type=e2-standard-2 \
    --worker-boot-disk-size=100 \
    --no-address \
    --optional-components=JUPYTER,ZEPPELIN \
    --enable-component-gateway \
    --max-idle=1h \
    --max-age=3h \
    --scopes='https://www.googleapis.com/auth/cloud-platform' \
    --properties="dataproc:jupyter.notebook.gcs.dir=gs://$BUCKET_NAME/notebooks"
```

`--max-idle=1h --max-age=3h` es importante para el free tier: el cluster se autodestruye
si nadie lo usa por 1 hora, o a las 3 horas de vida sin importar el uso — evita que
alguien se olvide un cluster prendido durante el fin de semana.

## B) Cluster con soporte de Hugging Face (para la sesión de features/modelos)

Sube `hugging_face_deps.sh` a tu bucket primero:

```bash
gsutil cp hugging_face_deps.sh gs://$BUCKET_NAME/hugging_face_deps.sh

gcloud dataproc clusters create $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --zone=$ZONE \
    --image-version=2.1-ubuntu20 \
    --master-machine-type=n1-standard-2 \
    --master-boot-disk-size=50 \
    --num-workers=2 \
    --worker-machine-type=n1-standard-4 \
    --worker-boot-disk-size=100 \
    --initialization-actions=gs://$BUCKET_NAME/hugging_face_deps.sh \
    --metadata=PIP_PACKAGES="transformers datasets torch" \
    --enable-component-gateway \
    --max-idle=1h \
    --max-age=3h \
    --scopes='https://www.googleapis.com/auth/cloud-platform' \
    --properties="dataproc:jupyter.notebook.gcs.dir=gs://$BUCKET_NAME/notebooks"
```

Workers más pocos pero más poderosos (30 GB RAM) — necesario para cargar modelos tipo
BART/BERT en memoria.

## Revisar cuotas antes de crear un cluster

```bash
gcloud compute regions describe us-central1
```

## Ver también

- `recursos/mariadb/` — para la base de datos del curso (separada del cluster de Spark).
- `environment/gcp-setup.md` — presupuesto y servicios Always Free.
