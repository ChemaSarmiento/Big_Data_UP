#!/bin/bash
DB_ROOT_PASSWORD="root"
APP_USER="big_data_user"
APP_PASS="Example123"

# 1. Crear Base de Datos y Usuario para la clase
sudo mysql -u root -p"$DB_ROOT_PASSWORD" -e "CREATE USER IF NOT EXISTS '$APP_USER'@'%' IDENTIFIED BY '$APP_PASS';"
sudo mysql -u root -p"$DB_ROOT_PASSWORD" -e "GRANT ALL PRIVILEGES ON *.* TO '$APP_USER'@'%';"
sudo mysql -u root -p"$DB_ROOT_PASSWORD" -e "FLUSH PRIVILEGES;"