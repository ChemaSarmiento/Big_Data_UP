-- MariaDB / datacharmer test_db. Solo SELECT; la base la carga el docente.
-- '9999-01-01' significa vigente en el snapshot histórico, NO empleados de hoy.
-- La unidad salarial del ejemplo no se presume MXN.
USE employees;
SELECT 1 AS conexion;

-- Q1. ¿Qué departamentos existen? Grano: departamento.
SELECT dept_no, dept_name FROM departments ORDER BY dept_no;

-- Q2. ¿Qué empleados se contrataron entre 1990 y 1994?
-- Grano: persona identificada por emp_no; orden estable.
SELECT emp_no, first_name, last_name, hire_date
FROM employees
WHERE hire_date >= '1990-01-01' AND hire_date < '1995-01-01'
ORDER BY hire_date, emp_no LIMIT 20;

-- Q3. ¿Cuántas personas vigentes se asignan a cada departamento?
SELECT d.dept_no, d.dept_name, COUNT(DISTINCT de.emp_no) AS personas
FROM departments d
LEFT JOIN dept_emp de ON d.dept_no = de.dept_no AND de.to_date = '9999-01-01'
GROUP BY d.dept_no, d.dept_name ORDER BY personas DESC, d.dept_no;

-- Q4. ¿Qué departamentos tienen salario medio vigente >= 60000?
-- LEFT no es necesario aquí: buscamos solo asignaciones/salarios coincidentes.
SELECT d.dept_no, d.dept_name, COUNT(DISTINCT de.emp_no) AS personas,
       AVG(s.salary) AS salario_medio
FROM departments d
JOIN dept_emp de ON d.dept_no = de.dept_no AND de.to_date = '9999-01-01'
JOIN salaries s ON de.emp_no = s.emp_no AND s.to_date = '9999-01-01'
GROUP BY d.dept_no, d.dept_name
HAVING AVG(s.salary) >= 60000 ORDER BY salario_medio DESC, d.dept_no;

-- Q5. ¿Quién está asignado a qué departamento en el snapshot?
SELECT e.emp_no, e.first_name, e.last_name, d.dept_name
FROM employees e
JOIN dept_emp de ON e.emp_no = de.emp_no AND de.to_date = '9999-01-01'
JOIN departments d ON de.dept_no = d.dept_no
ORDER BY e.emp_no, d.dept_no LIMIT 20;

-- Q6. ¿Por qué el historial devuelve más filas que personas?
-- Acotar a una persona: no crear un join cartesiano masivo para demostrarlo.
SELECT e.emp_no, s.salary, s.from_date, s.to_date
FROM employees e JOIN salaries s ON e.emp_no = s.emp_no
WHERE e.emp_no = 10001 ORDER BY s.from_date;
SELECT e.emp_no, s.salary, s.from_date, s.to_date
FROM employees e JOIN salaries s ON e.emp_no = s.emp_no
WHERE e.emp_no = 10001 AND s.to_date = '9999-01-01'
ORDER BY s.from_date;
-- Controles: nombres no son llaves y MAX(salary) histórico no es salario vigente.
SELECT COUNT(*) AS filas, COUNT(DISTINCT emp_no) AS personas FROM employees;
SELECT emp_no, COUNT(*) AS salarios_vigentes
FROM salaries WHERE to_date = '9999-01-01'
GROUP BY emp_no HAVING COUNT(*) > 1;
