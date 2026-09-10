# Facilitación — Sesión 06: Data Lakes y gobierno del dato

> Guion de 3 horas: charla + caso de estudio, sin lab de código. Es una sesión
> puramente conceptual — el peso está en la discusión, no en la demo.

## Antes de empezar (facilitador)

Prepara (o adapta) un caso real de falla por mal manejo de datos — con costo de
negocio medible, no técnico. Si tienes uno del sector del grupo, mejor que uno
genérico.

---

## Bloque 1 — Apertura y gancho (0:00–0:20)

**Talking point de apertura:**

> "Hoy no vamos a tocar una sola línea de código. Vamos a hablar de algo que
> cuesta más caro cuando sale mal que casi cualquier decisión técnica: cómo se
> organiza y quién controla el acceso a los datos de una organización."

**Pregunta de apertura:**

> "¿Alguno ha vivido, en su trabajo, un caso donde nadie sabía quién era
> responsable de un dato, o de dónde había salido un número que apareció en un
> reporte importante?"

---

## Bloque 2 — Data lake y medallion (0:20–1:00, 40 min)

### Bodega vs. archivero (15 min)
Cuenta la analogía completa — un archivero (todo clasificado de entrada) vs.
una bodega (se guarda tal cual llega, se clasifica después). Pregunta: **"¿por
qué querría alguien *no* clasificar de entrada?"** (porque estructurar de más
antes de saber para qué se va a usar el dato es, en sí mismo, sobre-ingeniería
— conecta con la Sesión 1).

### Medallion (25 min)
Recorre bronze/silver/gold con la tabla de `teoria.md`. Muestra (sin correr
código) las carpetas `data/raw/` y `data/processed/` de
`recursos/etl-tipo-cambio/` — que vean físicamente cómo cambia un archivo de
una carpeta a otra.

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Por qué importa el gobierno del dato (1:10–2:00, 50 min)

Recorre los tres escenarios de `teoria.md` (sin control de acceso, sin
validación de calidad, sin linaje) con una pregunta abierta cada uno:

> "Sin control de acceso — ¿qué tan grave sería en su organización que
> cualquiera pudiera modificar datos financieros sin dejar registro?"

> "Sin validación de calidad — ¿han visto un error 'chiquito' propagarse hasta
> un reporte ejecutivo?"

> "Sin linaje — si algo sale mal, ¿podrían hoy mismo rastrear de dónde vino un
> número específico en su organización?"

---

## Bloque 5 — Caso de estudio (2:00–2:50, 50 min)

Presenta el caso real preparado — costo de negocio, no técnico. En equipos,
discutir: ¿qué falló en términos de gobernanza (no de tecnología)? ¿Cómo se
habría evitado?

**Talking point antes de abrir la discusión:**

> "No busquen el error de código — busquen el error de proceso: ¿quién debió
> haber revisado esto, y por qué no pasó?"

Cada equipo comparte su conclusión en 2 minutos al resto del grupo.

---

## Bloque 6 — Cierre (2:50–3:00, 10 min)

**Sin entregable formal hoy** — cierra con una síntesis breve de los tres
escenarios de gobernanza vistos.

**Puente a la Sesión 7:**

> "Hasta ahora todo lo que vimos asumía que los datos ya estaban esperando
> quietos. La próxima sesión vemos qué cambia cuando los datos no paran de
> llegar."

---

## Notas de costo GCP

- No aplica — sesión sin cómputo.
