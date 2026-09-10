# Facilitación — Sesión 04: Introducción a Spark

> Guion de 3 horas: notebook "fill-in-the-blanks", guiado paso a paso. Es la
> primera vez que el grupo toca Spark directamente — mantén el nivel acotado
> (completar, no escribir desde cero) todo el tiempo.

## Antes de empezar (facilitador)

Prepara la versión simplificada de `recursos/spark/02_dataframes.ipynb`: quita
las celdas de `.explain()` y el guardado en Parquet particionado (eso es
Maestría) — deja solo lectura + `filter` + `groupBy` + `show()`.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "BigQuery, que usaron la sesión pasada, es excelente para preguntas que se
> expresan en SQL. Hoy vemos qué pasa cuando la pregunta es más compleja de lo
> que SQL resuelve bien — ahí es donde entra Spark."

**Pregunta de apertura:**

> "¿Se les ocurre algo que sea difícil de expresar como una sola consulta SQL,
> aunque sepan exactamente qué información necesitan?"

---

## Bloque 2 — Vocabulario mínimo (0:15–1:00, 45 min)

### DataFrame, transformación, acción (25 min)

Las tres palabras del día, con ejemplos concretos. Dale tiempo especial a la
distinción transformación/acción — es la más confusa la primera vez:

> "Una transformación es como escribir una receta — no cocinas nada todavía.
> Una acción es cuando efectivamente prendes la estufa. Pueden escribir 10
> transformaciones seguidas y Spark no ha tocado un solo dato hasta que llega
> la acción."

### Por qué no vemos shuffle/optimización hoy (10 min)

Sé explícito sobre el límite: "Eso es un track completo en Maestría. Aquí, con
saber que la palabra 'shuffle' existe y que es una operación costosa, ya
pueden participar en una conversación técnica sin bloquearse."

### Demo del "notebook que tarda de repente" (10 min)

Muestra en vivo: varias celdas de transformación que corren "instantáneo",
seguidas de un `.show()` que sí tarda. Pregunta: **"¿por qué creen que pasó
esto?"**

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Completar el notebook simplificado (75 min)

En parejas, completando los espacios en blanco de la versión simplificada de
`02_dataframes.ipynb` sobre el catálogo de precios PROFECO:

```python
df_filtrado = df.filter(F.col("categoria") == ___)
resumen = df_filtrado.groupBy(___).count()
resumen.show()
```

**Deberías ver:** cada pareja completando progresivamente — circula
activamente, este es el momento de mayor bloqueo técnico del track.

**Errores comunes:**
| Error | Causa | Solución |
|---|---|---|
| `NameError` en `F` | Falta el import de `functions as F` | Confirmar que la celda de imports corrió primero |
| `.show()` no imprime nada | El filtro no coincide con ningún valor real | Revisar mayúsculas/minúsculas del valor filtrado |

### Verificación en pareja (15 min)

Cada pareja explica a otra pareja, en una frase, qué hace su notebook
completado — es más valioso que tú lo confirmes tú mismo.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** notebook completado.

**Puente a la Sesión 5:**

> "Hoy procesaron datos ya limpios y listos. La próxima sesión vemos de dónde
> vienen esos datos antes de estar listos — el ciclo completo de un ETL real."

---

## Notas de costo GCP

- Si el notebook corre en un cluster compartido por el grupo, recuerda
  apagarlo al final — es fácil que quede prendido si varias parejas terminan
  en momentos distintos.
