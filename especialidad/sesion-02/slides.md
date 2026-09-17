---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
---

# Sesión 02
## Cómo funciona por dentro

Especialidad — Big Data (sin código)

---

## Una biblioteca, repartida en 100 bodegas

En vez de un edificio con todos los libros: 100 bodegas más pequeñas por la
ciudad, cada una con una parte de la colección — y cada libro con **3 copias**
guardadas en bodegas distintas, por si una se incendia.

<div class="box">
Eso es exactamente lo que hace Cloud Storage (o HDFS, su antecesor) con tus
datos: los parte y los reparte, con copias de seguridad automáticas.
</div>

---

## Contar palabras en 10,000 documentos

**Una persona, uno por uno** → lento.

**10 personas, 1,000 documentos cada una, al mismo tiempo, sumando resultados
parciales al final** → cómputo distribuido.

Es exactamente lo que hace un cluster de Spark cuando procesa un archivo de
20GB — dividir el trabajo entre varios trabajadores que avanzan a la vez.

---

## Un cluster: dos roles

- **Nodo maestro** — coordina, reparte el trabajo, junta resultados
- **Nodos trabajadores** — hacen el trabajo pesado, cada uno su porción

<div class="box">
Cuando alguien "crea un cluster" en GCP, literalmente está encendiendo varias
máquinas virtuales configuradas para trabajar juntas con estos dos roles.
</div>

---

## "Procesar en paralelo" no es magia

Dividir entre más máquinas ayuda **hasta cierto punto** — coordinar 100
máquinas para un archivo de 10MB cuesta más que el ahorro (como contratar 10
personas para leer un solo párrafo).

---

## Cuando una parte tarda mucho más que las demás

Un documento gigante entre 9,999 pequeños → ese trabajador se vuelve el
cuello de botella. Todos los demás terminan y esperan.

<div class="box">
Esto se llama <span class="accent">skew</span> — lo vas a escuchar mencionar,
no necesitas resolverlo hoy. Maestría lo resuelve a fondo en un módulo
completo.
</div>

---

# Demo en vivo

## `recursos/spark/01_rdd_basico.ipynb`

El facilitador corre un `reduceByKey` contando palabras sobre tweets reales —
sin que nadie escriba código. Es la versión en código de la analogía de los
10,000 documentos.

Si el cluster real es pesado para una demo en vivo, se usa una muestra pequeña
del archivo para que corra en segundos.

---

## Entregable de hoy

Ninguno formal — quiz corto de conceptos al cierre.

---

# → Sesión 03

SQL para analítica a escala
