#!/bin/bash
# 1_install_mariadb.sh

echo "Instalando MariaDB Server..."
apt-get update
apt-get install -y mariadb-server

echo "Configurando acceso remoto (bind-address)..."
# Esta línea busca el bind-address y lo cambia a 0.0.0.0
sudo sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf

echo "Reiniciando MariaDB para aplicar cambios..."
sudo systemctl restart mariadb

echo "Habilitando MariaDB en el arranque..."
sudo systemctl enable mariadb