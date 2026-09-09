---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  table { font-size: 0.85em; }
---

# Sesión 00
## Nivelación

Especialidad — Big Data

---

## Cuatro cosas, ninguna se evalúa hoy

- Terminal — lo mínimo para no bloquearte
- Python — variables, notebooks, correr una celda
- SQL — leer una consulta, no escribirla desde cero
- GCP — acceso desde el navegador, sin instalar nada

---

## Una terminal es un explorador de archivos con teclado

| Con el mouse | En terminal |
|---|---|
| Abrir una carpeta | `cd nombre-carpeta` |
| Ver el contenido | `ls` |
| Ver dónde estás | `pwd` |

*No hay nada mágico — cada comando tiene su equivalente gráfico.*

---

## Un notebook: texto y código en el mismo documento

- Una celda a la vez, `Shift + Enter` para correrla
- El resultado aparece justo debajo

<span class="accent">El error más común no es tuyo:</span> si una celda usa una variable que otra de más abajo todavía no creó, va a fallar.

---

## Tres palabras cubren el 80% del SQL que vas a leer

```
SELECT departamento, AVG(salario) AS promedio
FROM empleados
WHERE activo = 1
GROUP BY departamento;
```

**SELECT** qué muestro · **WHERE** qué filtro · **GROUP BY** cómo agrupo

---

## Practica con datos reales, sin escribir nada nuevo

`recursos/sql-practica/employee_db_queries.sql` — secciones 1-2

Se leen y se corren. El objetivo es reconocer qué responde cada consulta.

---

## GCP: todo desde el navegador

1. Crear cuenta (crédito de $300 USD / 90 días)
2. Crear un proyecto
3. **Configurar alerta de presupuesto** — antes de tocar cualquier otra cosa

---

# Mirando hacia el proyecto final

El catálogo de datasets reales (`recursos/datasets/`) ya sugiere una asignación por sector — retail, banca, ciberseguridad.

No hay que decidir hoy. Sí conviene empezar a pensarlo.

---

# → Sesión 01

Big Data para decisiones de negocio
