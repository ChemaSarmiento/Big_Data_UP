-- Paso 2 · Mira la base: tablas, columnas y filas.
-- Dentro de la VM:  mysql -u big_data_user -pExample123 employees
-- Pega cada sentencia (termina en punto y coma) o ejecuta el archivo completo con:
--   mysql -u big_data_user -pExample123 employees -t < s02_02_mirar_la_base.sql

-- 2.1 ¿Qué tablas hay? (dos de ellas, current_dept_emp y dept_emp_latest_date, son vistas)
SHOW TABLES;

-- 2.2 ¿Qué columnas tiene employees y de qué tipo?
DESCRIBE employees;

-- 2.3 Las primeras cinco filas. Sin ORDER BY, el orden que ves no está garantizado.
SELECT * FROM employees LIMIT 5;

-- 2.4 ¿Cuántas filas hay? Comprueba: 300024.
SELECT COUNT(*) AS empleados FROM employees;

-- 2.5 SELECT con columnas elegidas, un alias y una expresión.
SELECT emp_no,
       CONCAT(first_name, ' ', last_name) AS nombre,
       hire_date AS contratado
FROM employees
LIMIT 3;

-- Ejercicios (intenta cada uno antes de leer su solución al final):
-- E1 · ¿Qué columnas tiene la tabla salaries?
-- E2 · Lista los departamentos (dept_no y dept_name) en orden alfabético por nombre. Debes ver 9 filas.
-- E3 · Muestra nombre completo y fecha de contratación de 5 empleados.

-- Soluciones:
-- E1: DESCRIBE salaries;
-- E2: SELECT dept_no, dept_name FROM departments ORDER BY dept_name;
-- E3: SELECT CONCAT(first_name, ' ', last_name) AS nombre, hire_date FROM employees LIMIT 5;
