# Separar primero evita aprender del futuro

<figure data-infographic="sin-fuga"></figure>

El artefacto conserva lo aprendido en train. En CV se reajusta el pipeline dentro de cada fold.


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


---

# ROC-AUC no explica sola el costo de los errores

- Mostrar prevalencia y un baseline junto a PR-AUC.
- Elegir el umbral de decisión según precisión, recall y costo de falsos positivos/negativos.
- Mantener el test futuro reservado para la evaluación final.
- Comparar candidatos con el mismo corte, datos y condiciones de cómputo.

**Entregable:** una recomendación con métricas, limitaciones y costo; no solo «ganó el AUC más alto».