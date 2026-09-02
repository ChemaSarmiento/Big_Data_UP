#!/bin/bash
# crear_firewall_y_instancia.sh
#
# Corre esto desde Cloud Shell (NO desde dentro de la instancia). Una sola invocación
# deja la firewall Y la instancia listas, con MariaDB instalándose automáticamente vía
# startup-script (usuario compartido de la clase: big_data_user / Example123).
#
# NOTA DIDÁCTICA: el firewall se abre a 0.0.0.0/0 (todo internet) a propósito, para que
# cualquier alumno se conecte sin túneles ni configuración de IP. Es una decisión
# deliberada para un entorno de curso desechable y sin datos reales — nunca uses este
# patrón (puerto de base de datos abierto a internet + credenciales compartidas) en un
# sistema con datos de verdad.
#
# Uso:
#   ./crear_firewall_y_instancia.sh [rango_origen_firewall]
#
#   Sin argumentos: usa 0.0.0.0/0 (todo internet) — el default de este curso.
#   Con un argumento (ej. 35.235.240.0/20 para IAP, o tu-ip/32): restringe el origen,
#   por si en algún momento quieres una versión menos expuesta del mismo ejercicio.

set -euo pipefail

PROJECT_ID=$(gcloud config get-value project)
ZONE="us-central1-a"
INSTANCE_NAME="mariadb-curso"
FIREWALL_RULE_NAME="allow-mariadb-curso"
NETWORK_TAG="mariadb-server"

RANGO_ORIGEN="${1:-0.0.0.0/0}"
if [[ "$RANGO_ORIGEN" == "0.0.0.0/0" ]]; then
  echo "Firewall abierto a todo internet (0.0.0.0/0) -- ejemplo didáctico, sin datos reales."
fi

echo "=== 1/3: Regla de firewall ==="
if gcloud compute firewall-rules describe "$FIREWALL_RULE_NAME" >/dev/null 2>&1; then
  echo "La regla '$FIREWALL_RULE_NAME' ya existe, no se recrea."
else
  gcloud compute firewall-rules create "$FIREWALL_RULE_NAME" \
    --project="$PROJECT_ID" \
    --direction=INGRESS \
    --priority=1000 \
    --network=default \
    --action=ALLOW \
    --rules=tcp:3306 \
    --source-ranges="$RANGO_ORIGEN" \
    --target-tags="$NETWORK_TAG" \
    --description="Acceso a MariaDB del curso (ejemplo didáctico), restringido a ${RANGO_ORIGEN}"
  echo "Regla creada, origen permitido: $RANGO_ORIGEN"
fi

echo "=== 2/3: Password de root (no se comparte con los alumnos) ==="
DB_ROOT_PASSWORD=$(openssl rand -base64 18)

echo "=== 3/3: Crear la instancia (firewall + tag ya están listos) ==="
gcloud compute instances create "$INSTANCE_NAME" \
  --project="$PROJECT_ID" \
  --zone="$ZONE" \
  --machine-type=e2-micro \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --tags="$NETWORK_TAG" \
  --metadata-from-file=startup-script=startup-mariadb.sh \
  --metadata=db-root-password="$DB_ROOT_PASSWORD"

cat << EOF

=== Instancia creada ===
Usuario y password de la clase (fijos, compartidos entre todos los alumnos):

  DB_HOST     = (ver 'gcloud compute instances describe ${INSTANCE_NAME} --zone=${ZONE}')
  DB_APP_USER = big_data_user
  DB_PASSWORD = Example123

La instalación tarda ~1-2 minutos en terminar. Verifica con:
  ./verificar_instalacion.sh
EOF
