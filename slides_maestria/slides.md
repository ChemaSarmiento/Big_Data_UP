---
theme: seriph
class: text-center
highlighter: shiki
transition: slide-left
mdc: true
title: "Big Data — Maestría en Ciencia de Datos"
info: |
  Índice de las 14 presentaciones del track de Maestría (00 + 01-13).
  Cada sesión es un deck independiente: sesion-00.md ... sesion-13.md
---

# Big Data
## Maestría en Ciencia de Datos

<div class="pt-6 text-sm opacity-60">
14 decks independientes — uno por sesión (sesion-00.md a sesion-13.md, 39h de clase)
</div>

---

# Índice

<div class="grid grid-cols-2 gap-x-8 gap-y-1 text-left text-sm">

- **00** — Prerequisito obligatorio
- **01** — Arquitecturas distribuidas
- **02** — SQL distribuido avanzado
- **03** — Spark Core I: Catalyst y shuffle
- **04** — Spark Core II: skew y diagnóstico
- **05** — Ingeniería de features a escala
- **06** — Entrenamiento distribuido
- **07** — Lakehouse I: formatos y medallion
- **08** — Lakehouse II: transacciones y versionado
- **09** — Streaming I: fundamentos y setup
- **10** — Streaming II: inferencia en tiempo real
- **11** — Model serving y monitoreo
- **12** — MLOps con Airflow
- **13** — Gobernanza, seguridad y capstone

</div>

<div class="mt-4 text-xs opacity-60">
Las Sesiones 3-4, 7-8, 9-10 y 11-12 son pares que antes eran una sola sesión sobrecargada — se dividieron para cubrir cada tema completo en 3 horas reales.
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
