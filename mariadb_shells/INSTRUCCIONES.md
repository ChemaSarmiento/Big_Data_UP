```sh
1. clonar git
2. Encontrar archivo [instalar_mariadb_easy.sh]
3. Dar permisos de ejecucion= "chmod +x instalar_mariadb_easy.sh"
4. Ejecutar usando "sudo ./instalar_mariadb_easy.sh"
5. Seguir instrucciones, para 'root' password dar enter (dado que es la primera vez) y despues settear uno nuevo, en este caso 'Example123', todo lo demas 'YES' o 'y'
6. Probar que el servicio este funcionando= "sudo systemctl status mariadb"
7. Encontrar el archivo [crear_usuario.sh] y darle permisos de ejecucion= "chmod +x crear_usuario.sh"
8. Ejecutar usando "sudo ./crear_usuario.sh"
8. Probar la conexion, "mysql -u big_data_user -p"
9. Salir de la base de datos con "quit" 
10. Encontrar el archivo [modificar_configuracion.sh], darle permisos de ejecucion: "chmod +x modificar_configuracion.sh"
11. Ejecutar usando "sudo ./modificar_configuracion.sh"
12. Encontrar el archivo [crear_regla_vpc.sh]
13. Dar permisos de ejecucion = "chmod +x crear_regla_vpc.sh]
14. Ejecutar usando "sudo ./crear_regla_vpc.sh"
15. Reiniciar instancia usando sudo reboot
16. Volverse a conectar, el servidor de base de datos ya aceptara conexiones remotas y se podra usar con sqoop.
```
