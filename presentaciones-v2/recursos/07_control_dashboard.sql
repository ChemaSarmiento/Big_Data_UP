-- GoogleSQL: comprobar exactamente un escenario antes de interpretar el dashboard.
SELECT escenario, establecimiento, cobertura, costo_completo_mxn, subtotal_mxn
FROM curso_gold.canastas WHERE escenario='demo_2024-01-15'
ORDER BY elegible DESC, costo_completo_mxn, establecimiento;
SELECT establecimiento, producto, cantidad_envases, fecha_observada, importe_mxn
FROM curso_gold.detalle WHERE escenario='demo_2024-01-15' ORDER BY establecimiento,producto;
-- No sumar costos de distintas tiendas como si fueran una sola compra.
-- No sumar snapshots ni escenarios en tarjetas de total.
