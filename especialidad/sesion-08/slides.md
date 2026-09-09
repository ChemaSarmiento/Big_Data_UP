---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 08
## Costos, gobernanza y cómo evaluar un proyecto de datos

Especialidad — Big Data

---

# Tres formas en que la nube cobra

- **Por uso** — exactamente lo que consumes (impredecible si nadie vigila)
- **Por hora** — mientras algo está encendido, aunque esté ocioso
- **Por almacenamiento** — pequeño pero constante, indefinidamente

---

# Cinco preguntas que expone cualquier propuesta técnica

1. ¿Se apaga solo, o hay que apagarlo a mano?
2. ¿Hay alerta si el gasto se sale de lo esperado?
3. ¿El costo escala con el uso, o hay un fijo alto sin importar?
4. ¿Quién puede crear recursos nuevos, con qué límite?
5. ¿Qué tan dependientes somos de un solo proveedor?

---

# Framework de evaluación — cuatro dimensiones

| Dimensión | Pregunta central |
|---|---|
| Arquitectura | ¿Corresponde al problema real, o es sobre-ingeniería? |
| Costo | ¿Estimado mensual, y qué pasa si crece 10x? |
| Riesgo | ¿Qué pasa si algo falla? |
| Tiempo | ¿El cronograma incluye pruebas, o asume que todo funciona a la primera? |

---

# Un caso real: barato y rápido ≠ bien gobernado

La versión original de la base del curso exponía el puerto a internet completo, con contraseñas en el código.

<span class="accent">Ninguna de las cuatro preguntas de arriba lo habría dejado pasar.</span>

---

# Taller

Aplicar el framework a un caso ficticio, en equipos.

**Entregable:** framework aplicado al caso.

---

# → Sesión 09

Presentación del proyecto final
