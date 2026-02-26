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