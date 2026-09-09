---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 07
## Datos en tiempo real

Especialidad — Big Data

---

# La pregunta que separa batch de tiempo real

**¿Alguien va a actuar distinto si la respuesta llega en segundos en vez de en horas?**

Si no — batch es más simple, más barato, y no pierde nada.

---

# Reporte mensual vs. fraude en el momento

| | Batch | Tiempo real |
|---|---|---|
| Cuándo se procesa | En bloques programados | Conforme llega, sin esperar |
| Ejemplo | Reporte de ventas mensual | Fraude detectado *mientras ocurre* |

---

# El costo de elegir tiempo real

| | Batch | Tiempo real |
|---|---|---|
| Infraestructura | Más barata — se apaga entre ventanas | Corriendo todo el tiempo |
| Desarrollo | Se corrige y se vuelve a correr | Diseñado para fallar sin perder ni duplicar datos |
| Cuándo se justifica | La mayoría de reportes | Fraude, alertas, precios dinámicos |

---

# El error común: elegir por prestigio, no por necesidad

<span class="accent">Construir streaming para un reporte que nadie mira hasta la mañana siguiente</span> = pagar toda la complejidad, sin ganar nada.

---

# Demo guiada

Un flujo de eventos simple. El grupo identifica: ¿en qué parte de mi negocio aplicaría esto?

**Entregable:** ninguno formal.

---

# → Sesión 08

Costos, gobernanza y cómo evaluar un proyecto de datos
