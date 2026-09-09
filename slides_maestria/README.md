# Slides de Maestría (Slidev)

Un deck de [Slidev](https://sli.dev) por sesión — `sesion-00.md` a `sesion-13.md`.
Se eligió Slidev para este track (y no Marp, que usa Especialidad) porque el
contenido técnico se apoya en diagramas Mermaid y bloques de código resaltado —
ver la comparación completa de herramientas en la conversación que originó esta
carpeta, o simplemente abrir cualquier deck para ver el patrón.

`slides.md` es el índice — no tiene contenido de sesión, solo enlaza a los 14 decks.

## Setup

```bash
npm install
```

## Correr un deck en modo presentación

```bash
npx slidev sesion-00.md --open
```

Atajos: flecha derecha / espacio para avanzar, `o` para vista de overview, `f`
para pantalla completa.

## Exportar

```bash
npx slidev export sesion-00.md              # PDF
npx slidev export sesion-00.md --format pptx  # PPTX
npx slidev export sesion-00.md --format png   # una imagen por slide
```

## Convención de cada deck

- **Título = la conclusión, no la categoría** ("Spark corrió 8x más rápido...", no "Comparación de rendimiento")
- **Un acento de color** (`text-blue-500`/`border-blue-500`) sobre fondo neutro — nunca una paleta de 6 colores compitiendo por atención
- **Diagramas Mermaid** para el mecanismo central de cada sesión (arquitectura, DAG, pipeline) — no texto describiendo lo que un diagrama muestra mejor
- **Código real**, tomado de `recursos/` — nunca pseudocódigo inventado para la slide
- Cierra siempre con un puente explícito a la siguiente sesión

Principios de diseño (Cole Nussbaumer Knaflic, *Storytelling with Data*): un color
de acento y el resto en gris, nunca pie charts ni 3D, etiqueta directa en vez de
leyenda aparte, y un arco narrativo por sesión (contexto → tensión → resolución).

## Por qué cada sesión es un archivo independiente, no un solo deck de 100+ slides

Cada `sesion-XX.md` se abre y exporta por separado — un facilitador no necesita
cargar las 10 sesiones para presentar una sola, y un cambio en la Sesión 6 no
arriesga romper el archivo de la Sesión 1. Todos comparten el mismo
`package.json`/tema, así que el estilo es consistente sin necesitar un proyecto
Node por sesión.
