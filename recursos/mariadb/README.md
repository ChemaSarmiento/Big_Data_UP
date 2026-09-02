# MariaDB en GCP — instancia + firewall en un solo paso

Reemplaza `mariadb_shells/` del repo original. Ese folder tenía **dos flujos
redundantes y con nombres de archivo inconsistentes entre sí y con lo que
describían los 3 README** (`MLOPS/README.md`, `MLOPS/Instancia_MariaDB.md` e
`INSTRUCCIONES.md` se referían a scripts con nombres ligeramente distintos a
los que de verdad existen en el repo). Aquí queda un solo flujo, consistente
con lo que documenta este mismo README.

## Qué cambió respecto al original

| Antes | Ahora | Por qué |
|---|---|---|
| La regla de firewall se creaba en un paso aparte, manual, después de la instancia (o desde *dentro* de la instancia con permisos elevados en `4_crear_regla_vpc.sh`) | `crear_firewall_y_instancia.sh` crea ambas cosas en una sola invocación, firewall primero | Es lo que pediste: que crear la instancia también deje lista la regla de VPC. Además, que la propia instancia pueda modificar reglas de firewall de red es más superficie de ataque de la necesaria — mejor que lo haga el operador desde Cloud Shell. |
| `source-ranges=0.0.0.0/0` (puerto 3306 abierto a todo internet) | Sigue siendo `0.0.0.0/0` por decisión explícita — ver nota abajo | A petición: ejemplo didáctico, todos los alumnos entran igual sin configurar túneles ni IPs. El script acepta un rango distinto como argumento si en algún momento se quiere una versión más restringida del mismo ejercicio. |
| `APP_USER="big_data_user"`, `APP_PASS="Example123"` escritos en texto plano en el repo | Siguen siendo fijos y compartidos (mismos valores) por decisión explícita — ver nota abajo | A petición: todos los alumnos comparten la misma credencial. El password de `root` sí se sigue generando por instancia (no se comparte, y no hace falta que los alumnos lo sepan). |
| `1_instalar_mariadb_easy.sh` (flujo manual interactivo) + `1_install_mariadb_gcp.sh` (flujo automático) — dos formas distintas de instalar, con pasos que se pisan (`3_modificar_configuracion.sh`/`conf_mod.txt` vs. el `sed` de bind-address en el otro script) | Un solo `startup-mariadb.sh`, no interactivo, sin duplicación | Dos caminos para lo mismo es el tipo de cosa que se desincroniza con el tiempo — de hecho ya se había desincronizado (por eso los 3 README no concuerdan entre sí). |

> **Nota didáctica:** el firewall público y las credenciales compartidas son una
> decisión deliberada para este entorno de curso, desechable y sin datos reales —
> no es un descuido. Si en algún momento el mismo repo se usa con datos reales o
> fuera de un entorno de clase, lo primero que hay que revertir es esto: correr
> `./crear_firewall_y_instancia.sh 35.235.240.0/20` (rango de IAP) y cambiar el
> usuario/password fijos en `startup-mariadb.sh` por credenciales generadas.

## Archivos

- `crear_firewall_y_instancia.sh` — correr desde **Cloud Shell**. Crea la regla de firewall (si no existe, `0.0.0.0/0` por default) y luego la instancia.
- `startup-mariadb.sh` — corre automáticamente dentro de la VM al arrancar (vía `--metadata-from-file`). Instala MariaDB, habilita acceso remoto y crea el usuario compartido de la clase (`big_data_user` / `Example123`, fijos en este archivo).
- `verificar_instalacion.sh` — correr desde Cloud Shell después de crear la instancia, para confirmar que MariaDB quedó escuchando correctamente.

## Uso

```bash
cd recursos/mariadb
chmod +x *.sh

# Default del curso: firewall abierto a todo internet, usuario/password compartidos
./crear_firewall_y_instancia.sh

# Si en algún momento quieres la versión restringida (mismo ejercicio, menos expuesto):
./crear_firewall_y_instancia.sh 35.235.240.0/20   # rango de IAP

# Espera ~1-2 min y verifica:
./verificar_instalacion.sh
```

Credenciales de la clase (fijas): `big_data_user` / `Example123`. Con el firewall en
`0.0.0.0/0`, cualquier alumno se conecta directo a la IP externa de la instancia, puerto
`3306`, sin túnel — ver `environment/mariadb-vscode-setup.md` para el detalle de conexión
desde VSCode (el paso del túnel IAP ahí se vuelve opcional, no obligatorio, con este
firewall).

## Qué se descartó del repo original (y por qué)

- `1_instalar_mariadb_easy.sh`, `2_crear_usuario.sh`, `update_users.sql`,
  `3_modificar_configuracion.sh`, `conf_mod.txt`, `4_crear_regla_vpc.sh` —
  superados por el flujo consolidado de arriba.
- `sql_and_me/install_config_mariadb.sh` — mismo caso: otra tercera variante de
  instalación de MariaDB. `sql_and_me/employee_db_queries.sql` sí se conserva
  (ver `recursos/hive/` y este mismo folder, es contenido de ejercicios, no de
  infraestructura).
