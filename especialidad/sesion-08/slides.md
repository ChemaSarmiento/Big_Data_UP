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

# Sesión 08
## Costos, gobernanza y cómo evaluar un proyecto de datos

Especialidad — Big Data

---

## Tres formas en que la nube cobra

- **Por uso** — exactamente lo que consumes (impredecible si nadie vigila)
- **Por hora** — mientras algo está encendido, aunque esté ocioso
- **Por almacenamiento** — pequeño pero constante, indefinidamente

<div class="box">
El cluster que crearon en Maestría cobra por hora mientras está prendido —
por eso se insiste tanto en apagarlo.
</div>

---

## Cinco preguntas que expone cualquier propuesta técnica

1. ¿Se apaga solo, o hay que apagarlo a mano?
2. ¿Hay alerta si el gasto se sale de lo esperado?
3. ¿El costo escala con el uso, o hay un fijo alto sin importar?
4. ¿Quién puede crear recursos nuevos, con qué límite?
5. ¿Qué tan dependientes somos de un solo proveedor?

<div class="box">
Ninguna requiere conocimiento técnico — cualquier perfil de negocio puede
hacerlas.
</div>

---

## Framework de evaluación — cuatro dimensiones

| Dimensión | Pregunta central |
|---|---|
| Arquitectura | ¿Corresponde al problema real, o es sobre-ingeniería? |
| Costo | ¿Estimado mensual, y qué pasa si crece 10x? |
| Riesgo | ¿Qué pasa si algo falla? |
| Tiempo | ¿El cronograma incluye pruebas, o asume que todo funciona a la primera? |

---

## Un caso real: barato y rápido ≠ bien gobernado

La versión original de la base del curso exponía el puerto a internet
completo, con contraseñas en el código.

<div class="box">
Ninguna de las cuatro preguntas de arriba lo habría dejado pasar. "Barato y
rápido" y "bien gobernado" no siempre son lo mismo.
</div>

---

# Taller

## Aplicar el framework

En equipos, aplicar las 4 dimensiones a un caso ficticio.

Cada equipo debe producir una recomendación clara: **¿aprobarían la propuesta
tal cual, con condiciones, o la rechazarían?** — defendida con las 4
dimensiones, no con una opinión general.

---

## Entregable de hoy

Framework aplicado al caso ficticio.

---

# → Sesión 09

Presentación del proyecto final
