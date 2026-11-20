#!/bin/bash
# Paso 1 · Entra a tu VM y carga la base employees.
# Parte A: en Cloud Shell. Si cambiaste el nombre o la zona de la VM en la sesión 1, usa los tuyos.
gcloud compute ssh mariadb-curso --zone=us-central1-a

# Parte B: ya dentro de la VM (el prompt cambia a tu_usuario@mariadb-curso).
git clone --depth 1 https://github.com/datacharmer/test_db.git
cd test_db
time mysql -u big_data_user -pExample123 -t < employees.sql

# Comprobación: cuenta las filas de cada tabla.
mysql -u big_data_user -pExample123 employees -t -e "
SELECT (SELECT COUNT(*) FROM employees)    AS empleados,
       (SELECT COUNT(*) FROM departments)  AS departamentos,
       (SELECT COUNT(*) FROM dept_emp)     AS dept_emp,
       (SELECT COUNT(*) FROM dept_manager) AS dept_manager,
       (SELECT COUNT(*) FROM titles)       AS titles,
       (SELECT COUNT(*) FROM salaries)     AS salaries;"
