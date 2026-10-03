# Un pipeline necesita un contrato entre etapas

| Etapa | Pregunta de control | Evidencia |
|---|---|---|
| Extracción | ¿Llegó la fuente esperada? | Fecha de extracción y cantidad de registros |
| Transformación | ¿Se conservaron las reglas del negocio? | Nulos, duplicados y filas rechazadas |
| Carga | ¿El consumidor recibió el resultado correcto? | Conteo de salida y consulta de verificación |

**Discusión:** si el proceso corre dos veces con la misma entrada, ¿duplica las ventas del dashboard? Define la regla antes de programar el pipeline.
