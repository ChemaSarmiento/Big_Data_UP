-- Paso 3 · Filtra y ordena.
-- Ejecuta el archivo completo con:
--   mysql -u big_data_user -pExample123 employees -t < s02_03_filtrar_y_ordenar.sql

-- 3.1 WHERE con AND: mujeres contratadas desde 1990. Comprueba: 53839.
SELECT COUNT(*) AS mujeres_desde_1990
FROM employees
WHERE gender = 'F' AND hire_date >= '1990-01-01';

-- 3.2 Los paréntesis cambian la respuesta. Comprueba: 869 y 722.
SELECT COUNT(*) AS sin_parentesis
FROM employees
WHERE gender = 'F' AND hire_date >= '1999-01-01' OR first_name = 'Georgi';

SELECT COUNT(*) AS con_parentesis
FROM employees
WHERE gender = 'F' AND (hire_date >= '1999-01-01' OR first_name = 'Georgi');

-- 3.3 IN, BETWEEN y LIKE. Comprueba: 709, 25610 y 186.
SELECT COUNT(*) AS in_tres_nombres FROM employees WHERE first_name IN ('Georgi', 'Bezalel', 'Parto');
SELECT COUNT(*) AS contratados_1990 FROM employees WHERE hire_date BETWEEN '1990-01-01' AND '1990-12-31';
SELECT COUNT(*) AS apellido_fac     FROM employees WHERE last_name LIKE 'Fac%';

-- 3.4 ORDER BY y LIMIT: los cinco salarios vigentes más altos (to_date = '9999-01-01' significa «hoy»).
SELECT emp_no, salary
FROM salaries
WHERE to_date = '9999-01-01'
ORDER BY salary DESC
LIMIT 5;

-- 3.5 Empates: varias personas entraron el primer día. Una segunda llave fija el orden.
SELECT emp_no, hire_date
FROM employees
ORDER BY hire_date, emp_no
LIMIT 5;

-- Ejercicios:
-- E1 · ¿Cuántas mujeres fueron contratadas durante 1995? Comprueba: 4795.
-- E2 · ¿Cuántos apellidos empiezan con «Pi»? Comprueba: 2331.
-- E3 · Muestra las 3 personas contratadas más recientemente (desempata por emp_no, de mayor a menor). Comprueba: 463807, 428377 y 499553.

-- Soluciones:
-- E1: SELECT COUNT(*) FROM employees WHERE gender = 'F' AND hire_date BETWEEN '1995-01-01' AND '1995-12-31';
-- E2: SELECT COUNT(*) FROM employees WHERE last_name LIKE 'Pi%';
-- E3: SELECT emp_no, first_name, last_name, hire_date FROM employees ORDER BY hire_date DESC, emp_no DESC LIMIT 3;
