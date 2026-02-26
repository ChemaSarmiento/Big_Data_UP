# Despliegue de Instancia MariaDB (GCP Free Tier)

Esta guía detalla cómo crear una instancia compatible con la capa gratuita de Google Cloud, utilizando **Ubuntu** y automatizando la configuración de MariaDB mediante scripts de inicio.

## ⚙️ 1. Requisitos del Free Tier (Capa Gratuita)
Para que esta instancia no genere cargos, debe cumplir con:
* **Región:** `us-west1`, `us-central1` o `us-east1`.
* **Tipo de máquina:** `e2-micro` (2 vCPU, 1 GB RAM).
* **Disco:** Hasta 30 GB (Standard Persistent Disk).

## 🚀 2. Creación de la Instancia con Auto-Configuración

Ejecuta este comando en Cloud Shell. Utilizaremos el parámetro `--metadata-from-file` para que los scripts de tu repositorio se ejecuten al arrancar la máquina.

```bash
# Variables de entorno
export PROJECT_ID=$(gcloud config get-value project)
export ZONE=us-central1-a
export INSTANCE_NAME=mariadb-free-tier

# Creación de la instancia Ubuntu e2-micro
gcloud compute instances create $INSTANCE_NAME \
    --project=$PROJECT_ID \
    --zone=$ZONE \
    --machine-type=e2-micro \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=30GB \
    --boot-disk-type=pd-standard \
    --network-interface=network-tier=PREMIUM,subnet=default \
    --tags=mariadb-server \
    --metadata=startup-script='#!/bin/bash
        # Actualizar sistema e instalar Git
        apt-get update && apt-get install -y git
        
        # Clonar repositorio
        git clone [https://github.com/ChemaSarmiento/Big_Data_UP.git](https://github.com/ChemaSarmiento/Big_Data_UP.git) /tmp/Big_Data_UP
        cd /tmp/Big_Data_UP/mariadb_shells
        
        # Dar permisos y ejecutar scripts en orden
        chmod +x *.sh
        ./2_install_mariadb.sh
        ./3_setup_database.sh'
🛠️ 3. Ajuste de los Scripts (.sh) para Automatización
Para que los scripts 2_... y 3_... de tu Git funcionen sin intervención humana (modo desatendido) durante la creación, deben ajustarse de la siguiente manera:

Ajuste para el Script 2 (Instalación):
Asegúrate de que use el flag -y para no pedir confirmación:

Bash
# Dentro de 2_install_mariadb.sh
sudo apt-get install -y mariadb-server
Ajuste para el Script 3 (Configuración/SQL):
Como el Startup Script corre como root, para crear bases de datos o usuarios sin que pida contraseña interactivamente, usa este formato:

Bash
# Dentro de 3_setup_database.sh
mysql -e "CREATE DATABASE IF NOT EXISTS my_db;"
mysql -e "CREATE USER IF NOT EXISTS 'admin'@'%' IDENTIFIED BY 'tu_password';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'admin'@'%';"
mysql -e "FLUSH PRIVILEGES;"
🔒 4. Apertura del Firewall (Puerto 3306)
Para permitir que herramientas externas (como DBeaver o Sqoop desde Dataproc) se conecten:

Bash
gcloud compute firewall-rules create allow-mysql-remote \
    --allow tcp:3306 \
    --target-tags=mariadb-server \
    --description="Permitir acceso remoto a MariaDB"