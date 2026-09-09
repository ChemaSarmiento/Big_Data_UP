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

# Sesión 01
## Big Data para decisiones de negocio

Especialidad — Big Data

---

# Un banco pregunta dos cosas muy distintas

**"¿Cuántas transacciones tuvo cada sucursal el mes pasado?"**
→ Una consulta SQL de toda la vida.

**"¿Qué transacción, entre millones, es fraude *ahora mismo*?"**
→ <span class="accent">Ahí sí se justifica Big Data.</span>

---

## Las 5 V's — el marco para distinguir uno de otro

| V | Pregunta |
|---|---|
| Volumen | ¿GB, TB, o PB? |
| Velocidad | ¿Cada cuánto llega, y qué tan rápido hay que responder? |
| Variedad | ¿Un formato, o texto + imágenes + logs mezclados? |
| Veracidad | ¿Qué tan sucio es el dato? |
| **Valor** | ¿Vale la pena el esfuerzo? |

---

## La V que más se olvida: Valor

Procesar 20TB de logs que nadie va a usar para nada **es** Big Data — mal aplicado.

La pregunta nunca es "¿tenemos muchos datos?"

Es: **¿el problema requiere procesar todo eso junto, rápido, de formas que una hoja de cálculo no puede?**

---

## El error más caro: sobre-ingeniería

Montar un cluster para un problema que un `SELECT` resuelve en 3 segundos.

---

## El mapa del ecosistema — hoy solo el mapa completo

| Categoría | Resuelve |
|---|---|
| Storage | Dónde viven los datos |
| Cómputo distribuido | Procesar en paralelo |
| Bases analíticas | Responder SQL a escala (Sesión 3) |
| Streaming | Datos que llegan sin parar (Sesión 7) |
| Orquestación | Coordinar los pasos de un pipeline |

---

# Actividad

2-3 casos reales — el grupo decide: ¿inversión justificada, o sobre-ingeniería?

**Entregable:** ficha de 1 página con un caso propio de tu industria.

---

# → Sesión 02

Cómo funciona por dentro (sin código pesado)
