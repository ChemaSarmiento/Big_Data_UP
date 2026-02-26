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
    --master-machine-type n2-standard-2 \
    --master-boot-disk-size 100 \
    --num-workers 2 \
    --worker-machine-type n2-standard-2 \
    --worker-boot-disk-size 100 \
    --optional-components JUPYTER,ZEPPELIN \
    --enable-component-gateway \
    --scopes 'https://www.googleapis.com/auth/cloud-platform'
```

---
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

deberías de ver:

```

```

Si el servicio no está disponible, corre:

```
sudo tail -n 20 /var/log/mariadb_install.log
```

y verás que sucedió con la instalación, si sigue 