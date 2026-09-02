# SQL de práctica — base de datos de empleados

Reemplaza `sql_and_me/` del repo original. Usa **test_db**
(https://github.com/datacharmer/test_db), la base de datos de ejemplo de empleados más
usada para practicar SQL — pública, oficial, y sigue mantenida.

## Qué cambió respecto al original

- `employee_db_queries.sql` tenía algunas consultas con errores reales (una condición
  encadenada sin sentido tipo `a.x = b.y = c.z`, y un `JOIN` implícito por coma sin
  condición que generaba un producto cartesiano) — probablemente notas de exploración
  del instructor, no ejemplos para la clase. Se limpiaron y se dejó solo lo que corre
  correctamente.
- Los joins con sintaxis de coma (`FROM a, b WHERE a.id = b.id`) se reescribieron como
  `JOIN ... ON ...` explícito — es el estándar que se enseña en el resto del curso
  (`recursos/hive/`, `recursos/etl-tipo-cambio/`), así que aquí conviene ser consistente.
- Se agregó `install_config_mariadb.sh` del original **no** — ese script era otra tercera
  variante de instalación de MariaDB, ya cubierta por `recursos/mariadb/`.

## Uso

```bash
git clone https://github.com/datacharmer/test_db.git
cd test_db/
mysql -u <tu_usuario> -p < employees.sql
mysql -u <tu_usuario> -p employees < ../recursos/sql-practica/employee_db_queries.sql
```

Buen punto de entrada para el Módulo 0 de nivelación (ambos tracks) antes de pasar a
SQL distribuido (BigQuery/Hive) — mismo tipo de preguntas, pero sobre una base pequeña
y de un solo nodo.
