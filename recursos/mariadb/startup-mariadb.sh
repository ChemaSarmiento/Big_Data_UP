#!/bin/bash
# startup-mariadb.sh
#
# Corre AUTOMÁTICAMENTE al arrancar la VM (vía --metadata-from-file=startup-script=...).
#
# NOTA DIDÁCTICA: el usuario y password de la clase son fijos y compartidos a propósito
# (big_data_user / Example123) para que todos los alumnos entren con la misma credencial
# sin fricción. Esto es intencional para un entorno de curso desechable, NO es una
# práctica que se deba replicar en un sistema con datos reales.

set -euo pipefail
exec > /var/log/mariadb_install.log 2>&1
echo "--- Iniciando instalación automática de MariaDB ---"

# --- Usuario y password de la clase (fijos y compartidos, ver nota arriba) ---
DB_APP_USER="big_data_user"
DB_APP_PASSWORD="Example123"

# --- El password de root sí se genera por instancia (no se comparte con los alumnos) ---
meta() {
  curl -s -H "Metadata-Flavor: Google" \
    "http://metadata.google.internal/computeMetadata/v1/instance/attributes/$1"
}
DB_ROOT_PASSWORD="$(meta db-root-password)"

if [[ -z "$DB_ROOT_PASSWORD" ]]; then
  echo "ERROR: falta db-root-password en la metadata de la instancia. Abortando." >&2
  exit 1
fi

# --- 1. Instalar MariaDB (modo no interactivo) ---
echo "Instalando mariadb-server..."
apt-get update
apt-get install -y mariadb-server

# --- 2. Habilitar acceso remoto (bind-address) ---
echo "Configurando bind-address = 0.0.0.0..."
sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf

systemctl restart mariadb
systemctl enable mariadb

# --- 3. Password de root + limpieza de accesos inseguros por default ---
echo "Configurando password de root y removiendo accesos anónimos..."
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';"
mysql -u root -p"${DB_ROOT_PASSWORD}" -e "DELETE FROM mysql.user WHERE User='';"
mysql -u root -p"${DB_ROOT_PASSWORD}" -e "DROP DATABASE IF EXISTS test;"
mysql -u root -p"${DB_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"

# --- 4. Usuario compartido de la clase ---
# El host queda en '%' (cualquier IP): junto con el firewall abierto a 0.0.0.0/0
# (ver crear_firewall_y_instancia.sh), cualquier alumno se conecta desde donde sea
# con la misma credencial, sin depender de túneles ni IPs fijas.
echo "Creando usuario compartido de la clase (${DB_APP_USER})..."
mysql -u root -p"${DB_ROOT_PASSWORD}" -e \
  "CREATE USER IF NOT EXISTS '${DB_APP_USER}'@'%' IDENTIFIED BY '${DB_APP_PASSWORD}';"
mysql -u root -p"${DB_ROOT_PASSWORD}" -e \
  "GRANT ALL PRIVILEGES ON *.* TO '${DB_APP_USER}'@'%';"
mysql -u root -p"${DB_ROOT_PASSWORD}" -e "FLUSH PRIVILEGES;"

echo "--- Instalación completa ---"
echo "Usuario de la clase: ${DB_APP_USER} / ${DB_APP_PASSWORD}"
