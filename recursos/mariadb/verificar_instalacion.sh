#!/bin/bash
# verificar_instalacion.sh
# Corre esto desde Cloud Shell. Se conecta por SSH y revisa que MariaDB haya
# quedado instalado y escuchando correctamente.

set -euo pipefail

ZONE="us-central1-a"
INSTANCE_NAME="mariadb-curso"

echo "=== Últimas líneas del log de instalación ==="
gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --command="sudo tail -n 20 /var/log/mariadb_install.log"

echo
echo "=== ¿MariaDB está escuchando en 0.0.0.0:3306? ==="
gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --command="sudo ss -tulpn | grep 3306 || echo 'NO está escuchando -- revisar el log de arriba'"

echo
echo "=== Estado del servicio ==="
gcloud compute ssh "$INSTANCE_NAME" --zone="$ZONE" --command="sudo systemctl status mariadb --no-pager"
