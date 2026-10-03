# Drift pide investigar antes de cambiar el modelo

<figure data-infographic="mlops"></figure>

Un candidato rechazado conserva el modelo servido. Justifica baseline, umbral y costo de la decisión.


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
