# Introducción a Big Data (Slidev)

Sesión compartida — base para Especialidad y Maestría, antes de la Sesión 1
de cualquiera de los dos tracks. Qué es Big Data, las 5 V's, tipos y
persistencia de datos, el pipeline de dato crudo a decisión, y Cloud vs.
On-Premise. Vive fuera de `especialidad/` y `maestria/` porque el contenido
es idéntico para ambos.

Incluye, embebidos como imagen, los 4 infográficos de
[`slides/infograficos/`](../slides/infograficos/) (Las 5 V's, On-Premise vs.
Cloud, ¿Y qué hay en la nube?, Anatomía de un producto de datos).

## Setup

```bash
npm install
```

## Cómo presentar

```bash
npx slidev slides.md --open
```

Abre un servidor local en modo presentación. Flechas/espacio para avanzar
(incluye los `v-click`), `f` pantalla completa, `o` vista de overview.

## Exportar

```bash
npx slidev export slides.md               # PDF
npx slidev export slides.md --format pptx  # PPTX
npx slidev export slides.md --format png   # una imagen por slide
```

## Regenerar los infográficos embebidos

Si cambia el contenido de un `.pptx` en `slides/infograficos/`, los PNG en
`public/infograficos/` no se actualizan solos — ver
[`slides/infograficos/README.md`](../slides/infograficos/README.md) para el
paso a paso (`render_html.js` + captura con Playwright).
