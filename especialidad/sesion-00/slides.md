---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
  table { font-size: 0.85em; }
---

# Sesión 00
## Nivelación

Especialidad — Big Data

---

## Nadie necesita salir de aquí sabiendo programar

El objetivo de hoy: que cuando en las próximas sesiones veas una terminal o
una consulta SQL en pantalla, **reconozcas qué está pasando** — no que lo
escribas tú.

- Terminal — lo mínimo para no bloquearte
- Python — variables, notebooks, correr una celda
- SQL — leer una consulta, no escribirla desde cero
- GCP — acceso desde el navegador, sin instalar nada

<div class="box">
Si ya has usado una hoja de cálculo con fórmulas y tablas dinámicas, ya
conoces el 80% de lo que viene hoy — solo con otro nombre.
</div>

---

## Una terminal es un explorador de archivos con teclado

| Con el mouse | En terminal |
|---|---|
| Abrir una carpeta | `cd nombre-carpeta` |
| Ver el contenido | `ls` |
| Ver dónde estás | `pwd` |
| Crear una carpeta | `mkdir nombre` |

No hay nada mágico — cada comando de terminal tiene su equivalente exacto en
el explorador gráfico que ya conoces.

---

## Un notebook: texto y código en el mismo documento

- Una celda a la vez, `Shift + Enter` para correrla
- El resultado aparece justo debajo, no todo el programa de golpe

<div class="box">
<span class="accent">El error más común no es tuyo:</span> si una celda usa una
variable que otra de más abajo todavía no creó, va a fallar. El orden en que
corres las celdas importa — es cómo funciona la herramienta, no un error de
quien la usa por primera vez.
</div>

---

## Tres palabras cubren el 80% del SQL que vas a leer

```sql
SELECT departamento, AVG(salario) AS promedio
FROM empleados
WHERE activo = 1
GROUP BY departamento;
```

**SELECT** qué columnas muestro · **WHERE** con qué condición filtro ·
**GROUP BY** cómo agrupo para resumir

Se lee de corrido: *"de la tabla empleados, quédate con los activos,
agrúpalos por departamento, muéstrame el salario promedio de cada grupo."*

---

## GCP: todo desde el navegador

1. Crear cuenta (crédito de $300 USD / 90 días)
2. Crear un proyecto
3. <span class="accent">Configurar alerta de presupuesto</span> — antes de tocar
   cualquier otra cosa

No vas a instalar nada en tu computadora — todo el curso corre desde el
navegador.

<div class="box">
El crédito de $300 se puede consumir rápido si algo queda corriendo sin que
nadie lo apague. La alerta te avisa por correo antes de que eso pase.
</div>

---

# Práctica guiada

## SQL de nivelación

`recursos/sql-practica/employee_db_queries.sql` — secciones 1-2, en parejas.
No escribes SQL nuevo hoy: corres consultas ya hechas y dices, en una frase,
qué responde cada una.

Es exactamente lo que vas a hacer en la Sesión 3, sobre datos reales.

---

## Mirando hacia el proyecto final

No hay que decidir hoy, pero conviene tenerlo en mente desde la primera
sesión: el proyecto final pide una pregunta de negocio específica respondida
con datos reales (≥15GB, procesamiento y visualizaciones).

`recursos/datasets/README.md` (Sección 5) sugiere una asignación por sector —
retail, banca/riesgo, ciberseguridad.

`recursos/proyecto-ejemplo/` desarrolla un proyecto completo de principio a
fin (detección de alzas de precio, datos reales de PROFECO) como referencia
de a qué se debería parecer el tuyo.

---

# → Sesión 01

Big Data para decisiones de negocio
