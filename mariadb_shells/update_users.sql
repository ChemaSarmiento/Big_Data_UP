CREATE USER 'big_data_user'@'%' IDENTIFIED BY 'Example123';
GRANT ALL PRIVILEGES ON *.* TO 'big_data_user';
FLUSH PRIVILEGES;
