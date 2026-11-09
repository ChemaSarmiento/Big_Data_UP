-- GoogleSQL. Registrar bytes, caché y tiempo. En un fixture pequeño no prometer ahorro medible.
SELECT establecimiento, COUNT(*) AS observaciones
FROM curso_silver.observaciones
WHERE fecha_observada BETWEEN DATE '2024-01-01' AND DATE '2024-01-31'
GROUP BY establecimiento ORDER BY establecimiento; -- A=5, B=5, C=3
SELECT id, COUNT(*) AS repeticiones FROM curso_silver.observaciones
GROUP BY id HAVING COUNT(*) > 1; -- ninguna fila en el fixture
SELECT * FROM curso_silver.reporte_calidad;
