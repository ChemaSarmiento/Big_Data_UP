# Catalyst decide el plan; Tungsten reduce su costo

| Capa | Decisión | Evidencia para buscar |
|---|---|---|
| Catalyst | Reescribir y optimizar el plan | Filtros y columnas leídos, estrategia de join |
| Tungsten | Ejecutar con menos trabajo de CPU y memoria | Generación de código en el plan físico |

- **Column pruning:** leer únicamente las columnas necesarias.
- **Predicate pushdown:** acercar los filtros a la lectura cuando la fuente lo permite.
- **Whole-stage code generation:** combinar operadores compatibles en código generado.

**Compruébalo:** compara `df.explain("formatted")` antes y después de seleccionar columnas y filtrar. La mejora se demuestra con el plan y una medición.


---

# Repartir por clave puede concentrar el trabajo

<figure data-infographic="shuffle"></figure>

Ejemplo ilustrativo, no medición real. Contrasta la duración por task y los bytes de shuffle antes de optimizar.