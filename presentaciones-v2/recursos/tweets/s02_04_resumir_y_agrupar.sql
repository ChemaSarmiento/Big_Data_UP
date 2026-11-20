-- Paso 4 · Resume y agrupa.
-- Ejecuta el archivo completo con:
--   mysql -u big_data_user -pExample123 employees -t < s02_04_resumir_y_agrupar.sql

-- 4.1 Funciones de agregación sobre los salarios vigentes. Comprueba: 240124 filas, promedio 72012.
SELECT COUNT(*)       AS vigentes,
       MIN(salary)    AS minimo,
       MAX(salary)    AS maximo,
       ROUND(AVG(salary)) AS promedio,
       SUM(salary)    AS nomina
FROM salaries
WHERE to_date = '9999-01-01';

-- 4.2 El promedio de todo el historial no es el salario de hoy. Comprueba: 63811.
SELECT ROUND(AVG(salary)) AS promedio_del_historial FROM salaries;

-- 4.3 GROUP BY: cuántas personas hay de cada género. Comprueba: M 179973 y F 120051.
SELECT gender, COUNT(*) AS empleados
FROM employees
GROUP BY gender;

-- 4.4 Una función de fecha para agrupar: contrataciones por año.
SELECT YEAR(hire_date) AS anio, COUNT(*) AS contratados
FROM employees
GROUP BY YEAR(hire_date)
ORDER BY anio;

-- 4.5 HAVING filtra grupos; WHERE filtra filas. Comprueba: d005 61386, d004 53304 y d007 37701.
SELECT dept_no, COUNT(*) AS vigentes
FROM dept_emp
WHERE to_date = '9999-01-01'
GROUP BY dept_no
HAVING COUNT(*) > 30000
ORDER BY vigentes DESC;

-- 4.6 CASE: una regla de negocio convertida en columna (bandas de salario vigente).
SELECT CASE WHEN salary < 50000  THEN '1 · menos de 50 mil'
            WHEN salary < 70000  THEN '2 · 50 a 70 mil'
            WHEN salary < 100000 THEN '3 · 70 a 100 mil'
            ELSE                      '4 · 100 mil o más' END AS banda,
       COUNT(*) AS empleados
FROM salaries
WHERE to_date = '9999-01-01'
GROUP BY banda
ORDER BY banda;

-- Ejercicios:
-- E1 · ¿A cuánto asciende la nómina vigente y cuál es el salario máximo vigente? Comprueba: 17291866123 y 158220.
-- E2 · ¿En qué año se contrató a más personas y cuántas fueron? Comprueba: 1986 con 36150.
-- E3 · ¿Cuántas personas tienen hoy cada cargo (tabla titles)? Ordena de mayor a menor. Comprueba: Senior Engineer 85939 es el mayor.

-- Soluciones:
-- E1: SELECT SUM(salary) AS nomina, MAX(salary) AS maximo FROM salaries WHERE to_date = '9999-01-01';
-- E2: SELECT YEAR(hire_date) AS anio, COUNT(*) AS contratados FROM employees GROUP BY YEAR(hire_date) ORDER BY contratados DESC LIMIT 1;
-- E3: SELECT title, COUNT(*) AS vigentes FROM titles WHERE to_date = '9999-01-01' GROUP BY title ORDER BY vigentes DESC;
