sudo apt-get update
sudo apt install mariadb-server
sudo systemctl status mariadb (“buscar por enabled o active”)
sudo mysql_secure_installation

mysql -u root -p
sudo mysql -uroot -pexample123




CREATE USER ‘sqoop_user’@’%’ IDENTIFIED BY ‘Example123’;
MariaDB> GRANT ALL PRIVILEGES ON *.* TO ‘sqoop_user’;
FLUSH PRIVILEGES



modificar el archivo /etc/mysql/my.cnf, agregar las siguientes lineas al final:
[mysqld]
skip-networking=0
skip-bind-address


modificar el archivo /etc/mysql/mariadb.conf.d/50-server.cnf 
comentar la siguiente línea:
#bind-address 	= 127.0.0.1
