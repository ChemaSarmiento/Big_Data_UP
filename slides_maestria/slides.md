---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Big Data — Maestría en Ciencia de Datos"
info: |
  Índice de las 10 presentaciones del track de Maestría.
  Cada sesión es un deck independiente: sesion-00.md ... sesion-09.md
---

# Big Data
## Maestría en Ciencia de Datos

<div class="pt-6 text-sm opacity-60">
10 decks independientes — uno por sesión (sesion-00.md a sesion-09.md)
</div>

---

# Índice

<div class="grid grid-cols-2 gap-x-8 gap-y-2 text-left text-sm">

- **00** — Prerequisito obligatorio
- **01** — Arquitecturas distribuidas
- **02** — SQL distribuido avanzado
- **03** — Spark Core avanzado
- **04** — Ingeniería de features a escala
- **05** — Entrenamiento distribuido
- **06** — Data Lakes / Lakehouse
- **07** — Streaming e inferencia en tiempo real
- **08** — Model serving, monitoreo y MLOps
- **09** — Gobernanza, seguridad y capstone

</div>

---
layout: center
class: text-center
---

# Cómo correr un deck

```bash
npm install
npx slidev sesion-0X.md --open
```

Exportar a PDF/PPTX: `npx slidev export sesion-0X.md`

Ver `README.md` de esta carpeta para más detalle.
