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


---

# La pregunta determina el gráfico

| Pregunta | Visual recomendado | Control de lectura |
|---|---|---|
| ¿Cuál es mayor? | Barras ordenadas | Origen cero y etiquetas directas |
| ¿Cómo cambia? | Línea temporal | Intervalos, unidades y cobertura |
| ¿Cómo se distribuye? | Histograma | Buckets y muestra explícitos |
| ¿Qué se relaciona? | Dispersión | No confundir relación con causalidad |

**Ejercicio:** toma un resultado del lab. Escribe primero la conclusión; después elige el gráfico que la demuestra.

---

# Destacar una conclusión reduce el esfuerzo de lectura

- Un título con hallazgo: «La partición redujo los bytes leídos»; agregar la magnitud solo cuando exista medición.
- Contexto neutral y un acento para lo relevante; el color comunica una razón.
- Etiquetas junto al dato, unidades y una nota con fuente/condiciones.
- Eliminar bordes, leyendas redundantes y decimales que no ayudan a decidir.

**Evitar:** gráficos 3D, escalas engañosas y flechas que afirmen causalidad sin evidencia. La elección no depende de una prohibición universal de un tipo de gráfico.
