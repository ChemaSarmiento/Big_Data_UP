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

# Sesión 07
## Datos en tiempo real

Especialidad — Big Data

---

## La pregunta que separa batch de tiempo real

<div class="box" style="font-size:1.2em; text-align:center;">
¿Alguien va a actuar distinto si la respuesta llega en segundos en vez de en horas?
</div>

Si no — batch es más simple, más barato, y no pierde nada.

---

## Reporte mensual vs. fraude en el momento

| | Batch | Tiempo real |
|---|---|---|
| Cuándo se procesa | En bloques programados | Conforme llega, sin esperar |
| Ejemplo | Reporte de ventas mensual | Fraude detectado *mientras ocurre* |

---

## El costo de elegir tiempo real

| | Batch | Tiempo real |
|---|---|---|
| Infraestructura | Más barata — se apaga entre ventanas | Corriendo todo el tiempo |
| Desarrollo | Se corrige y se vuelve a correr | Diseñado para no perder ni duplicar datos mientras sigue corriendo |
| Cuándo se justifica | La mayoría de reportes | Fraude, alertas, precios dinámicos |

---

## El error común: elegir por prestigio, no por necesidad

<div class="box">
Construir streaming para un reporte que nadie mira hasta la mañana siguiente
= pagar toda la complejidad de la tabla anterior, sin ganar nada.
</div>

Es el mismo error de sobre-ingeniería de la Sesión 1, con otro disfraz.

---

# Demo guiada

## Un flujo de eventos simple

El facilitador corre un flujo en vivo — narra cada evento conforme llega:
"esto está pasando ahora mismo, no es un archivo que ya estaba esperando".

---

## Discusión: ¿dónde aplicaría en tu negocio?

En equipos: identifica un proceso de tu propia área que hoy es batch y evalúa
— ¿tiene sentido volverlo tiempo real?

<div class="box">
No busques "sí, esto sería genial en tiempo real" — busca honestamente si el
costo se justifica. La respuesta correcta muchas veces es "no, batch está bien".
</div>

---

## Entregable de hoy

Ninguno formal — la puesta en común de equipos es donde más valor se genera.

---

# → Sesión 08

Costos, gobernanza y cómo evaluar un proyecto de datos
