# Teoría — Sesión 09: Presentación del proyecto final

> No hay contenido técnico nuevo hoy — esta página es una guía de cómo estructurar el
> documento y la presentación para que el esfuerzo técnico de las 8 sesiones
> anteriores se entienda y convenza, no solo "se muestre".

## 1. Por qué la estructura del documento no es arbitraria

Las seis secciones que pide `PROGRAMA.md` (Sección 5) no son un formalismo — cada una
responde a una pregunta que un tomador de decisiones real va a hacer, en el orden en
que la va a hacer:

| Sección | La pregunta que responde |
|---|---|
| Resumen ejecutivo | "¿Vale la pena que siga leyendo esto?" (30 segundos, sin jerga) |
| Visión general | "¿Qué es esto, exactamente, y qué NO hace?" |
| Revisión y uso de datos | "¿Puedo confiar en el dato detrás de esta conclusión?" |
| Proceso de desarrollo | "¿Cómo se construyó, y con qué?" |
| Resultados y conclusiones | "¿Qué encontraron, y cómo lo sé sin tener que revisar el código?" |
| A quién beneficia / costo-riesgo | "¿Y ahora qué? ¿Vale la pena invertir en esto?" |

Un error común es escribir el documento en el orden en que se hizo el trabajo (primero
lo técnico, al final el resumen) — eso invierte la prioridad de quien lo lee. Escribe
el resumen ejecutivo *al final*, cuando ya sabes exactamente qué vas a decir, pero
ponlo *primero* en el documento.

## 2. Cómo presentar sin perder al público en 15 minutos

Tres principios, todos derivados de las notas de facilitación de este track a lo
largo del curso:

- **Una visualización vale más que una tabla de números** — literalmente el criterio
  de evaluación lo exige (ver `PROGRAMA.md`, Sección 5). Si tu conclusión central no
  se puede mostrar en una gráfica, probablemente todavía no está lo suficientemente
  clara ni para ti mismo.
- **Empieza con la pregunta de negocio, no con la herramienta** — "usamos BigQuery y
  Looker Studio" es información de proceso, no el gancho de la presentación. El gancho
  es la pregunta que resolviste y para quién importa.
- **El código se muestra, no se explica línea por línea** — el criterio pide mostrarlo
  ("el código utilizado también se debe entregar o mostrar"), no que la audiencia lo
  entienda a detalle en 15 minutos. Una captura de pantalla del notebook completado, o
  un enlace, cumple el requisito sin consumir tiempo de presentación en explicar
  sintaxis.

---

## Referencias

- `PROGRAMA.md` (Sección 5) — criterios completos y tabla de pesos de evaluación
- [Google — Effective data storytelling: A guide](https://cloud.google.com/blog/products/data-analytics/effective-data-storytelling-a-guide) — principios generales de cómo presentar hallazgos de datos a una audiencia no técnica
