-- Paso 6 · De la pregunta de negocio a la consulta.
-- Ejecuta el archivo completo con:
--   mysql -u big_data_user -pExample123 employees -t < s02_06_de_la_pregunta_a_la_consulta.sql
-- Regla: escribe primero la pregunta, luego las piezas (qué columnas, de qué tabla, qué filas, qué grupos),
-- y solo al final la consulta.

-- 6.1 Subconsulta escalar: ¿cuántas personas ganan hoy más que el promedio de hoy? Comprueba: 107706.
SELECT COUNT(*) AS arriba_del_promedio
FROM salaries
WHERE to_date = '9999-01-01'
  AND salary > (SELECT AVG(salary) FROM salaries WHERE to_date = '9999-01-01');

-- 6.2 Subconsulta con IN: nombres de personas que han sido gerentes (24 en total; aquí cinco).
SELECT first_name, last_name
FROM employees
WHERE emp_no IN (SELECT emp_no FROM dept_manager)
ORDER BY last_name
LIMIT 5;

-- 6.3 Pregunta A: ¿cuántas personas trabajan hoy en la empresa? Comprueba: 240124 (y no 300024).
SELECT COUNT(DISTINCT emp_no) AS trabajan_hoy
FROM dept_emp
WHERE to_date = '9999-01-01';

-- 6.4 Pregunta B: ¿qué departamentos tienen más de 30,000 personas hoy? (nombre, no código)
SELECT d.dept_name, COUNT(*) AS vigentes
FROM dept_emp AS de
JOIN departments AS d ON d.dept_no = de.dept_no
WHERE de.to_date = '9999-01-01'
GROUP BY d.dept_name
HAVING COUNT(*) > 30000
ORDER BY vigentes DESC;

-- 6.5 Pregunta C: ¿hay diferencia de salario vigente promedio entre géneros? Comprueba: M 72045 y F 71964.
--     Qué NO demuestra: que el pago sea justo o injusto; la consulta no mira puesto, antigüedad ni historia.
SELECT e.gender, COUNT(*) AS vigentes, ROUND(AVG(s.salary)) AS salario_promedio
FROM employees AS e
JOIN salaries AS s ON s.emp_no = e.emp_no AND s.to_date = '9999-01-01'
GROUP BY e.gender;

-- 6.6 Hasta dónde llega el dato. Comprueba: última contratación 2000-01-28 y último cambio de salario 2002-08-01.
SELECT (SELECT MAX(hire_date)  FROM employees) AS ultima_contratacion,
       (SELECT MAX(from_date)  FROM salaries)  AS ultimo_cambio_de_salario;

-- Ejercicios:
-- E1 · Escribe la pregunta, las piezas y la consulta: ¿cuántas personas tienen hoy el cargo «Senior Staff»? Comprueba: 82024.
-- E2 · ¿Qué departamento tiene el salario vigente promedio más alto? (puedes reutilizar el paso 5, E2) Comprueba: Sales.
-- E3 · ¿Qué porcentaje de las personas contratadas antes de 1990 sigue trabajando hoy? (usa el paso 5, E3) Comprueba: 80.0.

-- Soluciones:
-- E1: SELECT COUNT(*) FROM titles WHERE title = 'Senior Staff' AND to_date = '9999-01-01';   -- 82024
-- E2: (reutiliza 5.E2) el primero de la lista: Sales, 88853
-- E3: SELECT ROUND(100 * COUNT(DISTINCT CASE WHEN de.to_date = '9999-01-01' THEN e.emp_no END) / COUNT(DISTINCT e.emp_no), 1) AS pct_siguen
--     FROM employees AS e JOIN dept_emp AS de ON de.emp_no = e.emp_no WHERE e.hire_date < '1990-01-01';   -- 80.0
