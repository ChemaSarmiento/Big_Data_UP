# MariaDB en GCP + conexión remota desde VSCode

La creación de la instancia y la regla de firewall ya están automatizadas en
`recursos/mariadb/` — este documento cubre solo la parte de **conectar VSCode** una vez
que la instancia existe.

## 1. Crear la instancia (si no la has creado)

```bash
cd recursos/mariadb
./crear_firewall_y_instancia.sh
```

Esto crea la regla de firewall (`0.0.0.0/0` por default — ver la nota didáctica en
`recursos/mariadb/README.md`) y la instancia `mariadb-curso` con el tag `mariadb-server`
en un solo paso, con el usuario compartido de la clase ya creado
(`big_data_user` / `Example123`).

## 2. Conectar VSCode

Con el firewall abierto, no hace falta túnel — se conecta directo a la IP externa de la
instancia:

1. Instalar la extensión **SQLTools** + **SQLTools MySQL/MariaDB Driver**.
2. Nueva conexión: host = IP externa de la instancia
   (`gcloud compute instances describe mariadb-curso --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'`),
   puerto `3306`, usuario `big_data_user`, password `Example123`.
3. Probar con un `SELECT 1;` antes de correr cualquier script del curso.

> Si en algún momento recreas la instancia con un firewall más restringido
> (`./crear_firewall_y_instancia.sh 35.235.240.0/20`, rango de IAP), entonces sí necesitas
> un túnel:
> ```bash
> gcloud compute start-iap-tunnel mariadb-curso 3306 --local-host-port=localhost:3306 --zone=us-central1-a
> ```
> y conectar VSCode a `localhost:3306` en vez de a la IP externa.

## 3. Checklist

- [ ] Instancia creada (`recursos/mariadb/crear_firewall_y_instancia.sh`)
- [ ] `recursos/mariadb/verificar_instalacion.sh` corrido sin errores
- [ ] Conexión probada desde VSCode con un `SELECT 1;` (usuario `big_data_user`)
- [ ] Apagar la instancia (`gcloud compute instances stop mariadb-curso --zone=us-central1-a`) cuando no se use, para no gastar crédito
