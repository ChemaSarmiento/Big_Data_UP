#!/bin/bash

# 1. Obtener nombre de la instancia actual
hname=$(hostname)
echo "Instancia actual: $hname"

# 2. Obtener el ID del Proyecto (forma más segura)
project=$(gcloud config get-value project)
echo "Proyecto detectado: $project"

# 3. Obtener la zona de la instancia actual
# Usamos --format="value(zone)" para obtener solo el nombre de la zona
zone=$(gcloud compute instances list --filter="name:($hname)" --format="value(zone)")
echo "Zona detectada: $zone"

# 4. Crear la regla de Firewall
# Nota: Se usa la red 'default'. Asegúrate de que tu instancia esté en esa red.
echo "Creando regla de firewall para MariaDB..."
gcloud compute firewall-rules create allow-mariadb \
    --project="$project" \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:3306 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=mariadb-server

# 5. Agregar el tag a la instancia actual para que la regla le aplique
echo "Asignando tag de red a la instancia..."
gcloud compute instances add-tags "$hname" \
    --zone "$zone" \
    --tags=mariadb-server
