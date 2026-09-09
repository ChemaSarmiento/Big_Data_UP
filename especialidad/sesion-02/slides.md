---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 02
## Cómo funciona por dentro

Especialidad — Big Data (sin código)

---

# Una biblioteca, repartida en 100 bodegas

En vez de un edificio con todos los libros: 100 bodegas más pequeñas por la ciudad — y cada libro con 3 copias, por si una bodega se incendia.

<span class="accent">Eso es almacenamiento distribuido.</span>

---

# Contar palabras en 10,000 documentos

**Una persona, uno por uno** → lento.

**10 personas, 1,000 documentos cada una, al mismo tiempo, sumando al final** → cómputo distribuido.

---

# Un cluster: dos roles

- **Nodo maestro** — coordina, reparte el trabajo, junta resultados
- **Nodos trabajadores** — hacen el trabajo pesado, cada uno su porción

Crear un cluster en GCP = encender varias máquinas configuradas para trabajar juntas.

---

# "Procesar en paralelo" no es magia

Dividir entre más máquinas ayuda **hasta cierto punto** — coordinar 100 máquinas para un archivo de 10MB cuesta más que el ahorro.

---

# Cuando una parte tarda mucho más que las demás

Un documento gigante entre 9,999 pequeños → ese trabajador se vuelve el cuello de botella. Todos los demás esperan.

Esto se llama **skew** — lo vas a escuchar mencionar, no necesitas resolverlo hoy.

---

# Demo en vivo

El facilitador corre un job real sobre tweets — contar palabras, sin que nadie escriba código.

**Entregable:** ninguno formal — quiz corto de conceptos.

---

# → Sesión 03

SQL para analítica a escala
