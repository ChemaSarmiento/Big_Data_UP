# Laboratorio de Big Data: Dataproc, Hive, Jupyter y Zeppelin

Este repositorio contiene la guía paso a paso para desplegar un entorno de análisis de datos a gran escala en Google Cloud Platform (GCP). El clúster está configurado para procesar archivos de más de 20GB de manera eficiente.

## Requisitos Previos

* Una cuenta activa en Google Cloud Platform.
* Un proyecto creado con la facturación habilitada.
---

Creación del Clúster desde Cloud Shell

Abre **Cloud Shell** y ejecuta los siguientes bloques de código.

### A) Definición de Variables
Configura el entorno según tu proyecto.

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export ZONE=us-central1-a
export CLUSTER_NAME=hive-learning-cluster
```



### B) Código para crear cluster en Cloud Shell
```bash 
gcloud dataproc clusters create $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --zone=$ZONE \
    --image-version=2.1-ubuntu20 \
    --master-machine-type=e2-highmem-2 \
    --master-boot-disk-size 50 \
    --num-workers=3 \
    --worker-machine-type=e2-standard-2 \
    --worker-boot-disk-size 100 \
	--no-address \
    --optional-components JUPYTER,ZEPPELIN \
    --enable-component-gateway \
    --scopes 'https://www.googleapis.com/auth/cloud-platform' \
    --properties 'dataproc:jupyter.notebook.gcs.dir=gs://big-data-lunes-20260223/notebooks'
```





---

#### Opciones adicionales:

El clúster será principalmente para procesamiento, podemos agregar las siguientes opciones:
```
   --max-idle=1h \
    --max-age=3h \
```
Para que tenga un tiempo de vida de 3 horas, y si nadie lo usa en 1 hora se borrará automáticamente. 

De igual forma, para persistir tus notebooks de Spark, podremos exportar la siguiente variable:

```
export BUCKET_NAME=mi-bucket-creado
```

y agregar la opción la creación del clúster para crear un folder dentro del bucket, donde siempre vivan los notebooks, si borras el clúster, los notebooks se mantienen.

```
--properties="dataproc:jupyter.notebook.gcs.dir=gs://$BUCKET_NAME/notebooks"
```

De forma completa, quedaría así:


```
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export ZONE=us-central1-a
export CLUSTER_NAME=hive-learning-cluster
export BUCKET_NAME=mi-bucket-creado

gcloud dataproc clusters create $CLUSTER_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --zone=$ZONE \
    --image-version=2.1-ubuntu20 \
    --master-machine-type=e2-highmem-2 \
    --master-boot-disk-size 50 \
    --num-workers=3 \
    --worker-machine-type=e2-standard-2 \
    --worker-boot-disk-size 100 \
	--no-address \
    --optional-components JUPYTER,ZEPPELIN \
    --enable-component-gateway \
    --max-idle=1h \
    --max-age=3h \
    --scopes 'https://www.googleapis.com/auth/cloud-platform' \
    --properties="dataproc:jupyter.notebook.gcs.dir=gs://$BUCKET_NAME/notebooks"
```

### B.1) Clúster listo para usar hugging-face

Primero, crear un .sh que subiremos a un bucket, debe tener el código que encontrarás en [este script](hugging_face_deps.sh), suponiendo que la ruta es gs://tubucket/hugging_face_deps.sh :

```
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
export ZONE=us-central1-a
export CLUSTER_NAME=hive-learning-cluster
export BUCKET_NAME=mi-bucket-creado

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

Nota que los workers son menos, pero mas poderosos, y también agregamos "initialization-actions", esto permite correr scripts para hacer instalaciones al crearse el cluster.

**Corrección (verificado contra la especificación oficial de GCP):** `n1-standard-4` tiene **15 GB de RAM** por worker (4 vCPU), no 30 GB — la cifra anterior estaba mal. Para modelos chicos (DistilBERT, ~300 MB cargado) sobra margen de sobra. Para BART-base (~560 MB) también alcanza. Para BART-large o para correr inferencia sobre el dataset completo sin muestrear, conviene subir a `n1-highmem-4` (26 GB) o acotar el volumen de texto procesado — no asumir que "cabe cualquier cosa" sin volver a calcular.

#### Pasar un token (Hugging Face u otro) al Jupyter de este cluster

**Forma por defecto, la que usa `PySpark_Recommenders_Steam.ipynb`:** pegar el token
directo en la variable `HF_TOKEN` de la celda de parámetros, igual que `BUCKET`. Es
explícito y no depende de nada del cluster. El costo: **este repo es público en
GitHub** — si haces commit/push del notebook después de correrlo con el token real
puesto, queda en el historial de git para siempre, aunque lo borres en un commit
posterior. La misma celda lo recuerda con un comentario; antes de guardar cualquier
cambio que vaya a Git, vuelve a dejar el placeholder (`<TU_TOKEN_DE_HUGGING_FACE>`).

**Alternativa que nunca toca el archivo** (la celda la detecta sola si el placeholder
sigue puesto): el Jupyter que levanta `--enable-component-gateway` corre como **servicio
administrado** (systemd) en el master, no como algo que tú arrancas a mano desde una
terminal — por eso un `export MI_VARIABLE=valor` por SSH no le llega al kernel de forma
confiable, y no lo documentamos como solución por esa razón. Lo que sí funciona,
verificado y ya usado en este mismo repo (`Synthetic_Data/deploy/gcp/run_pilot.py` lee su
propio token de servicio exactamente así): la **metadata de la instancia de GCE**.
Cualquier proceso en el master —sin importar cómo se haya lanzado— puede leerla vía
`http://metadata.google.internal/computeMetadata/v1/instance/attributes/<NOMBRE>`.

```
# Opción 1 — al crear el cluster, en el mismo --metadata que ya usa PIP_PACKAGES:
--metadata=PIP_PACKAGES="transformers datasets torch",HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Opción 2 — con el cluster ya creado, sin recrearlo (nombre del master: <CLUSTER_NAME>-m):
gcloud compute instances add-metadata $CLUSTER_NAME-m --zone=$ZONE \
    --metadata=HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```



**Nota** Revisa tus cuotas desde gcloud con el siguiente comando:

```
gcloud compute regions describe us-central1
```


### C) Crear una VM con MariaDB


```bash
# 1. Variables de entorno
export PROJECT_ID=$(gcloud config get-value project)
export ZONE=us-central1-a
export INSTANCE_NAME=mi-primer-base-de-datos

# 2. Creación de la Instancia
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=e2-small \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --tags=mariadb,http-server,https-server \
    --metadata=startup-script='#!/bin/bash
exec > /var/log/mariadb_install.log 2>&1
echo "--- Iniciando Instalación Automática ---"
apt-get update
apt-get install -y git

# Clonar repositorio
git clone https://github.com/ChemaSarmiento/Big_Data_UP.git /tmp/Big_Data_UP

# Ejecutar lógica de instalación
if [ -d "/tmp/Big_Data_UP/mariadb_shells" ]; then
    cd /tmp/Big_Data_UP/mariadb_shells
    chmod +x *.sh
    ./1_install_mariadb_gcp.sh
    ./2_config_security.sh
    ./3_setup_database.sh
fi
echo "--- Proceso Finalizado ---"'
```

### D) Crea tu regla de firewall (sólo 1 vez)

corre este código en tu cloud shell:

```
gcloud compute firewall-rules create allow-mariadb-access \
    --allow tcp:3306 \
    --target-tags=mariadb \
    --description="Permitir tráfico MariaDB puerto 3306"
```

## Revisa tu instalación

Entra por SSH a tu instancia recién creada, corre el siguiente código

```
sudo ss -tulpn | grep 3306
```

deberías de ver:

```
tcp   LISTEN  0  80  0.0.0.0:3306 ...
```

y el servicio de mariadb listo

```
$> sudo systemctl status mariadb
```

Si el servicio no está disponible, corre:

```
sudo tail -n 20 /var/log/mariadb_install.log
```

y verás que sucedió con la instalación.