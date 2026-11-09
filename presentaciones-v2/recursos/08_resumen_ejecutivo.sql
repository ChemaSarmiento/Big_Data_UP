-- GoogleSQL. Exportar el resultado acotado, no la tabla cruda completa, para la práctica de IA.
SELECT escenario, establecimiento, productos_encontrados, productos_requeridos,
 cobertura, subtotal_mxn, costo_completo_mxn, elegible, fecha_inicio, fecha_fin
FROM curso_gold.canastas
WHERE escenario='demo_2024-01-15' ORDER BY establecimiento;
-- Fixture ilustrativo. El resultado no prueba disponibilidad actual ni ahorro real.
