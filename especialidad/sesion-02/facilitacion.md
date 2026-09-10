# Facilitación — Sesión 02: Cómo funciona por dentro

> Guion de 3 horas: demo guiada, sin que el grupo escriba código. Hoy tú eres el
> que corre el notebook — el grupo observa, interactúa con parámetros simples, y
> construye intuición con analogías.

## Antes de empezar (facilitador)

Ten `recursos/spark/01_rdd_basico.ipynb` abierto y probado de antemano — si el
cluster real es pesado para una demo en vivo, prepara la muestra pequeña
(`head -n 1000 war_tweets.txt`) para que corra en segundos frente al grupo.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "Hoy no van a tocar código — van a ver, en vivo, cómo una computadora reparte
> un trabajo grande entre varias máquinas. Es la pieza que le da sentido a todo
> lo que vieron mencionado la sesión pasada como 'cómputo distribuido'."

**Pregunta de apertura:**

> "Si les pidiera contar cuántas veces aparece la palabra 'fraude' en 10,000
> documentos, ¿cómo lo organizarían si tuvieran un equipo de 10 personas
> ayudándoles?"

---

## Bloque 2 — Analogías (0:15–1:00, 45 min)

### Biblioteca repartida (15 min)
Cuenta la analogía completa de `teoria.md` — 100 bodegas, 3 copias de cada
libro. Pregunta: **"¿por qué 3 copias, y no solo 1 con mucho cuidado de que no
se pierda?"**

### El equipo de 10 personas (15 min)
Retoma la pregunta de apertura — ahora sí resuélvela con el grupo: dividir los
10,000 documentos entre 10 personas, cada una cuenta su porción, al final se
suman los resultados parciales. Esto **es** MapReduce, en español simple.

### Qué es un cluster (15 min)
Explica los dos roles (maestro/trabajadores) con la analogía del equipo:
alguien coordina quién hace qué y junta los resultados (maestro); el resto
hace el trabajo pesado (trabajadores).

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Demo en vivo (1:10–2:30, 80 min)

### Correr el notebook frente al grupo (40 min)

```python
# recursos/spark/01_rdd_basico.ipynb — correr celda por celda, narrando cada una
conteo = sc.textFile(RUTA).flatMap(...).map(...).reduceByKey(...)
conteo.take(10)
```

**Talking point mientras corre:** "Vean el tiempo que tarda. Ahora vamos a
cambiar un parámetro y correrlo de nuevo — quiero que vean el efecto, no que se
lo describa."

### Interactuar con parámetros simples (25 min)

Cambia el número de particiones o el tamaño de la muestra en vivo, y pide al
grupo que prediga qué va a pasar **antes** de correrlo:

```python
# Con más particiones (más "trabajadores" virtuales)
conteo_2 = sc.textFile(RUTA, minPartitions=20).flatMap(...).map(...).reduceByKey(...)
```

**Pregunta de predicción:** "¿esperan que sea más rápido, más lento, o igual?"

### Cuando una parte tarda mucho más (15 min)

Si tienes tiempo, muestra (o describe con el diagrama) el caso de skew — una
palabra que aparece muchísimo más que las demás y desbalancea el trabajo.
Menciónalo como concepto a reconocer, no a resolver: "esto tiene nombre —
skew — y en Maestría se resuelve a fondo; aquí solo necesitan reconocerlo si lo
oyen mencionar".

---

## Bloque 5 — Cierre (2:30–3:00, 30 min)

**Quiz corto de conceptos** (no formal, es diagnóstico): 3-4 preguntas orales
o de opción múltiple sobre cluster, paralelo, y las analogías de hoy.

**Puente a la Sesión 3:**

> "Hoy vieron cómputo distribuido en abstracto. La próxima sesión lo van a usar
> ustedes mismos, con SQL, sobre una tabla real de millones de filas — sin
> necesitar el cluster que hoy vimos correr."

---

## Notas de costo GCP

- Si el cluster real se usó para la demo, recuerda apagarlo al terminar la
  sesión — el grupo no lo va a tocar directamente, pero sigue siendo tu
  responsabilidad como facilitador.
