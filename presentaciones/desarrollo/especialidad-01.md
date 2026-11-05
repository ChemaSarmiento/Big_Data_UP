# Caso de apertura — una decisión con consecuencias

Caso hipotético: un reporte de ventas de 50 MB tarda segundos; un flujo de fraude debe activar una revisión mientras llegan eventos. Ambos usan GCP. ¿Los dos necesitan la misma arquitectura?

**Antes de continuar:** escribe una hipótesis y qué evidencia podría hacerte cambiar de opinión.

---

# El mecanismo que necesitas entender

Big Data surge de restricciones de volumen, velocidad, variedad y confiabilidad frente al plazo y los recursos disponibles. Un tamaño por sí solo no decide el diseño. Cloud computing ofrece infraestructura y servicios bajo demanda; también aloja tareas pequeñas.

La pregunta útil es qué decisión debe ocurrir, con qué demora tolerable y qué trabajo impide cumplirla.

---

# Elegir bien exige reconocer el límite

Distribuir aporta capacidad, pero añade coordinación, transferencia y operación. Batch simplifica recuperación y reproducibilidad; streaming permite reaccionar antes a cambio de mantener estado continuo. La mejor arquitectura depende de la acción, no del prestigio de una tecnología.

---

# Predice el resultado antes de comprobarlo

Un CSV pequeño se consulta en una VM cloud. ¿Es automáticamente Big Data?

<div class="knowledge-check">
<button type="button" data-correct="false">Sí, por estar en GCP</button>
<button type="button" data-correct="true">No, falta justificar escala y restricciones</button>
<button type="button" data-correct="false">Sí, si usamos Python</button>
<p class="check-feedback" role="status" hidden data-explanation="Cloud describe cómo obtienes infraestructura. Big Data exige justificar restricciones de datos y procesamiento."></p>
</div>

---

# Laboratorio guiado — preparación y objetivo

Taller guiado con dos casos y una hoja de decisión. No requiere crear recursos. Trabajar en equipos; cada recomendación debe incluir una alternativa simple y una condición que la haría insuficiente.

**Organización:** concepto y práctica en la misma sesión. La instalación y descarga de datos se verifican antes; el ejercicio central ocupa 90 minutos. Las extensiones se realizan después. En las sesiones de casos, el bloque se trabaja como taller.

---

# Laboratorio · paso 1 — concretar la acción

Define consumidor, decisión y demora tolerable. Sustituye “tener un dashboard” por una acción: ajustar inventario, investigar alerta o asignar presupuesto.

---

# Laboratorio · paso 2 — dimensionar el problema

Registra tamaño por periodo, tasa de llegada, retención, fuentes y restricciones de calidad. Marca qué cifras son supuestos del caso y qué medirías en una organización real.

---

# Laboratorio · paso 3 — comparar tres opciones

Propón SQL en una máquina, batch distribuido y flujo de eventos. Para cada una indica beneficio, complejidad, costo y modo de recuperación. Descarta las que no cambian la decisión a tiempo.

---

# Laboratorio · paso 4 — defender la recomendación

Haz una ficha: decisión, arquitectura mínima, evidencia y límite. Otro equipo cambia una condición —por ejemplo latencia o volumen— y verifica si tu propuesta sigue siendo válida.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar ficha de una página. Una respuesta “no hace falta Big Data todavía” es válida si explicita escala, plazo y alternativa. No justifiques arquitectura solo por usar un servicio cloud.

**Discusión:** compara la evidencia con tu hipótesis inicial. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

El caso no tiene decisión: define quién actúa. Se mezclan unidades: distingue GB almacenados, eventos/s y tiempo de respuesta. No hay evidencia: presenta el supuesto como supuesto y diseña una medición.

**Regla de trabajo:** conserva la entrada, el cambio aplicado y la evidencia del fallo. Cambia una condición a la vez.

---

# Para profundizar después de clase

Extensión de 30–45 minutos: adaptar la ficha a una pregunta del proyecto final. Buscar fuente real, licencia, cobertura y limitaciones antes de diseñar todo el pipeline.

El ejercicio de clase usa una muestra acotada; no sustituye la evidencia de volumen real exigida por el proyecto final. Detén procesos y recursos temporales al terminar.

---

# Referencias — qué buscar en cada fuente

- [Crédito y límites de GCP](https://docs.cloud.google.com/free/docs/free-cloud-features).
- [El contexto da significado a los datos](https://www.storytellingwithdata.com/blog/2021/1/14/data-doesnt-speak-for-itself).

Contrasta la explicación con el comportamiento de tu ejecución. Las fuentes documentan el mecanismo; las cifras de rendimiento se obtienen del laboratorio, no se inventan.
