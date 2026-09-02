-- =====================================================================
-- employee_db_queries.sql
-- Rescatado y limpiado de sql_and_me/employee_db_queries.sql del repo original.
-- Dataset: "test_db", la base de datos de empleados de ejemplo más usada para
-- practicar SQL -- oficial, pública y mantenida: https://github.com/datacharmer/test_db
-- =====================================================================

-- --- Preparación (correr una sola vez) ---
-- git clone https://github.com/datacharmer/test_db.git
-- cd test_db/
-- mysql -u <tu_usuario> -p < employees.sql

-- =====================================================================
-- Progresión: SELECT básico -> agregaciones -> joins -> subconsultas
-- =====================================================================

-- --- 1. Exploración básica ---
SELECT * FROM departments;
SELECT * FROM titles LIMIT 15;
SELECT DISTINCT title FROM titles;

-- --- 2. Conteos y agregaciones ---
SELECT COUNT(*) FROM departments;
SELECT COUNT(*) FROM dept_manager;
SELECT COUNT(DISTINCT CONCAT(first_name, last_name)) FROM employees;

-- --- 3. Joins explícitos (ANSI), preferidos sobre la sintaxis de coma del original ---
SELECT e.*, s.salary, s.to_date
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
ORDER BY e.emp_no, s.to_date
LIMIT 10;

-- Un empleado específico, su historial salarial completo
SELECT e.emp_no, s.salary, s.from_date, s.to_date
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
WHERE e.emp_no = 10001
ORDER BY s.to_date;

-- --- 4. Agregaciones con GROUP BY sobre joins ---
-- Salario máximo por empleado
SELECT e.emp_no, MAX(s.salary) AS salario_max
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
GROUP BY e.emp_no
LIMIT 20;

-- Estadísticas de salario por título
SELECT t.title,
       MAX(s.salary) AS max_salario,
       MIN(s.salary) AS min_salario,
       AVG(s.salary) AS prom_salario,
       STD(s.salary)  AS desviacion_salario
FROM employees e
JOIN salaries s ON e.emp_no = s.emp_no
JOIN titles t   ON e.emp_no = t.emp_no
GROUP BY t.title;

-- --- 5. Subconsultas: empleados que han tenido más de 2 títulos distintos ---
SELECT COUNT(*) FROM (
    SELECT e.emp_no, COUNT(*) AS num_titulos
    FROM employees e
    JOIN titles t ON e.emp_no = t.emp_no
    GROUP BY e.emp_no
    HAVING COUNT(*) > 2
) titulos_por_empleado;

-- --- 6. Nombres de gerentes por departamento ---
SELECT d.dept_name, CONCAT(e.first_name, ' ', e.last_name) AS gerente
FROM departments d
JOIN dept_manager dm ON d.dept_no = dm.dept_no
JOIN employees e     ON dm.emp_no = e.emp_no;

-- --- 7. Nombres duplicados (mismo first_name + last_name, más de una persona) ---
SELECT CONCAT(first_name, ' ', last_name) AS nombre_completo, COUNT(*) AS repeticiones
FROM employees
GROUP BY CONCAT(first_name, last_name)
HAVING COUNT(*) > 2;
