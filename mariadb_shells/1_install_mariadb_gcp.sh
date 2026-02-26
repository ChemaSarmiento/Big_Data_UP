#!/bin/bash
# 1. Instalar MariaDB
sudo apt-get update
sudo apt-get install -y mariadb-server mariadb-client

# 2. Habilitar el servicio
sudo systemctl enable mariadb
sudo systemctl start mariadb

# 3. Configurar para acceso remoto (IMPORTANTE para Big Data)
# Cambia 127.0.0.1 por 0.0.0.0 para aceptar conexiones de cualquier IP
sudo sed -i 's/bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mariadb.conf.d/50-server.cnf
sudo systemctl restart mariadb