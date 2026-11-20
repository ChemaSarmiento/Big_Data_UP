-- Paso 5 · Une tablas con JOIN.
-- Ejecuta el archivo completo con:
--   mysql -u big_data_user -pExample123 employees -t < s02_05_unir_tablas.sql

-- 5.1 Tres tablas unidas por sus llaves: empleado → departamento → nombre del departamento.
SELECT e.emp_no, e.first_name, e.last_name, d.dept_name, de.from_date, de.to_date
FROM employees AS e
JOIN dept_emp AS de ON de.emp_no = e.emp_no
JOIN departments AS d ON d.dept_no = de.dept_no
WHERE e.emp_no IN (10001, 10010)
ORDER BY e.emp_no, de.from_date;

-- 5.2 INNER JOIN solo conserva a quien tiene pareja. Comprueba: 24 personas son gerentes.
SELECT COUNT(*) AS con_pareja
FROM employees AS e
JOIN dept_manager AS m ON m.emp_no = e.emp_no;

-- 5.3 LEFT JOIN conserva todas las filas de la izquierda y pone NULL donde no hay pareja.
--     Comprueba: 300024 filas, 24 con gerencia y 300000 sin gerencia.
SELECT COUNT(*) AS filas,
       COUNT(m.emp_no) AS con_gerencia,
       COUNT(*) - COUNT(m.emp_no) AS sin_gerencia
FROM employees AS e
LEFT JOIN dept_manager AS m ON m.emp_no = e.emp_no;

SELECT e.emp_no, e.first_name, e.last_name, m.dept_no
FROM employees AS e
LEFT JOIN dept_manager AS m ON m.emp_no = e.emp_no
WHERE e.emp_no IN (10001, 10002, 10003, 110022, 110039, 110085)
ORDER BY e.emp_no;

-- 5.4 Un JOIN puede multiplicar filas. Una persona con 17 salarios se vuelve 17 filas.
--     Comprueba: 2844047 filas (no 300024) y promedio 63811 (no 72012).
SELECT COUNT(*) AS filas, ROUND(AVG(s.salary)) AS promedio
FROM employees AS e
JOIN salaries AS s ON s.emp_no = e.emp_no;

-- 5.5 Unir solo lo vigente evita la multiplicación. Comprueba: 240124 filas y promedio 72012.
SELECT COUNT(*) AS filas, ROUND(AVG(s.salary)) AS promedio_vigente
FROM employees AS e
JOIN salaries AS s ON s.emp_no = e.emp_no AND s.to_date = '9999-01-01';

-- 5.6 Un JOIN sin condición cruza todo con todo. Comprueba: 2700216 filas (300024 × 9).
SELECT COUNT(*) AS cruce FROM employees CROSS JOIN departments;

-- Ejercicios:
-- E1 · ¿Cuántas personas trabajan hoy en cada departamento? (usa dept_emp, departments y to_date = '9999-01-01') Comprueba: Development 61386 es el mayor.
-- E2 · ¿Cuál es el salario vigente promedio por departamento? Ordena de mayor a menor. Comprueba: Sales 88853 es el mayor.
-- E3 · ¿Cuántas personas contratadas antes de 1990 siguen trabajando hoy? Comprueba: 131779.

-- Soluciones:
-- E1: SELECT d.dept_name, COUNT(*) AS vigentes FROM dept_emp AS de JOIN departments AS d ON d.dept_no = de.dept_no WHERE de.to_date = '9999-01-01' GROUP BY d.dept_name ORDER BY vigentes DESC;
-- E2: SELECT d.dept_name, ROUND(AVG(s.salary)) AS salario_promedio FROM dept_emp AS de JOIN departments AS d ON d.dept_no = de.dept_no JOIN salaries AS s ON s.emp_no = de.emp_no AND s.to_date = '9999-01-01' WHERE de.to_date = '9999-01-01' GROUP BY d.dept_name ORDER BY salario_promedio DESC;
-- E3: SELECT COUNT(*) FROM employees AS e JOIN dept_emp AS de ON de.emp_no = e.emp_no WHERE de.to_date = '9999-01-01' AND e.hire_date < '1990-01-01';
