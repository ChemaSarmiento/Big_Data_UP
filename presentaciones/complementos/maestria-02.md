# Dos cálculos de ventana necesitan dos etapas

Una ventana calcula sobre las filas de su etapa. Si otro cálculo depende de ese resultado, usa una subconsulta o CTE para separar las etapas.

```sql
WITH ranking AS (
  SELECT tipo_transaccion, monto,
    RANK() OVER (
      PARTITION BY tipo_transaccion ORDER BY monto DESC
    ) AS posicion
  FROM transacciones
)
SELECT tipo_transaccion, monto, posicion,
  COUNT(*) OVER (PARTITION BY tipo_transaccion) AS filas_del_tipo
FROM ranking
WHERE posicion <= 3;
```

**Antes de ejecutar:** ¿el conteo describe todo el grupo o solo las filas que quedaron después de filtrar? Explica el orden lógico.
