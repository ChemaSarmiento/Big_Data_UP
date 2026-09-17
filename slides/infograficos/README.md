# Infográficos nuevos — Introducción a Big Data

## También viven como PNG en intro-big-data/

Estas 4 slides también están insertadas como imagen, tal cual, dentro del
deck compartido `intro-big-data/slides.md` (slides "Las 5 V's de Big Data",
"On-Premise vs. Cloud Computing", "¿Y qué hay en la nube?" y "Anatomía de un
producto de datos") — los PNG viven en `intro-big-data/public/infograficos/`.
Como este entorno no tiene LibreOffice para rasterizar el `.pptx` directo,
`render_html.js` reconstruye cada infográfico como HTML/CSS a partir de los
mismos datos (posiciones, colores, texto, íconos) que originalmente generaron
el `.pptx`, reusando `icon_helper.js` para los íconos (react-icons + sharp).
Para regenerar los PNG tras un cambio de contenido:

```
npm install                      # en esta carpeta — react, react-dom, react-icons, sharp
node render_html.js              # escribe ./html/*.html
# luego, con playwright-chromium instalado (ya está en intro-big-data/):
node -e "
const { chromium } = require('playwright-chromium');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
  for (const f of ['5vs','onprem_vs_cloud','que_hay_en_la_nube','producto_de_datos']) {
    await page.goto('file://' + __dirname + '/html/' + f + '.html');
    await page.screenshot({ path: '../../intro-big-data/public/infograficos/' + f + '.png' });
  }
  await browser.close();
})();
" # ejecutar desde intro-big-data/ para que resuelva playwright-chromium
```

Si el contenido del `.pptx` cambia, actualiza los datos correspondientes en
`render_html.js` para que ambas versiones (pptx e imagen embebida) no
diverjan.

## Las 4 slides .pptx originales

Cuatro slides construidas para cerrar huecos reales encontrados al revisar
`01_introduccion.pptx`, `02_fuentes_y_manejo.pptx` y
`03_casos_de_uso_arquitectura.pptx` — slides con solo texto o completamente
vacías, y dos ejemplos con capturas de pantalla que ya se ven viejas. Cada
archivo es un `.pptx` de una sola slide, listo para copiar/pegar en el
archivo original (clic derecho en el panel de slides de PowerPoint →
"Reutilizar diapositivas", o copiar/pegar directo entre ventanas — conserva
mejor el formato que reescribir a mano).

## Qué reemplaza cada uno

| Archivo | Va en... | Slide(s) que reemplaza | Por qué |
|---|---|---|---|
| `infografico_5vs.pptx` | `01_introduccion.pptx` | Slide 8 ("Las V's") | Estaba completamente vacía — sin texto, sin imagen, sin notas |
| `infografico_onprem_vs_cloud.pptx` | `03_casos_de_uso_arquitectura.pptx` | Slides 18-19 | Dos slides seguidas de puro texto, sin un solo elemento visual |
| `infografico_que_hay_en_la_nube.pptx` | `03_casos_de_uso_arquitectura.pptx` | Slide 22 | Tabla completa en texto, sin imagen — y actualiza "Google Data Proc" a **Managed Service for Apache Spark** (nombre 2026, mismo cambio ya aplicado en el resto del repo del curso) |
| `infografico_producto_de_datos.pptx` | `02_fuentes_y_manejo.pptx` | Slide 37 ("Ejemplos: Custom Trading") | La captura de pantalla tiene fecha congelada (dic 2021 - ene 2022) — reemplazada por un diagrama conceptual que no caduca, y que conecta los 5 ejemplos de las slides 33-37 (Netflix, Spotify, Maps, FICO, Trading) en un solo patrón |

## Otros hallazgos de la revisión (no requieren infográfico nuevo)

- **`01_introduccion.pptx`, slide 11** ("¿Cuántos datos hay en el mundo?"): el
  texto de la slide (181 ZB para fin de 2025) y la imagen insertada (edición
  12 de Domo, que cita 149 ZB/2024 y 394 ZB/2028) citan años distintos — no
  están mal, pero no cuentan la misma historia. Verificado con Statista/IDC:
  181 ZB en 2025 es correcto; 2026 proyecta ~221-240 ZB. Alinear el texto de
  la slide con la misma edición de Domo que ya usan, o actualizar ambos al
  mismo año.
- **`01_introduccion.pptx`, slide 16** ("Un buen ejemplo…", screenshot de Our
  World in Data): es una captura de un sitio vivo — el conteo de gráficas y
  el artículo destacado se ven obviamente viejos en cuanto alguien compare
  contra el sitio real. Sugerencia: tomar una captura nueva antes de cada uso,
  o reemplazar por una cifra fija y verificable ("más de 13,000 gráficas de
  acceso abierto") que no depende de una captura de pantalla.
- **`02_fuentes_y_manejo.pptx`, slide 21** (arquitectura de Data Lake en GCP):
  usa **Cloud Datalab** y **Cloud ML Engine** — ambos deprecados hace años en
  favor de Vertex AI Workbench (que a su vez ya tiene sus propias notas de
  deprecación desde enero 2025). Dos capas de obsolescencia — necesita
  reemplazo completo del diagrama, no un parche de nombres. No se construyó
  aquí por alcance (es un diagrama de arquitectura completo, no un
  infográfico conceptual) — si se quiere, es el siguiente candidato natural.
- **`02_fuentes_y_manejo.pptx`, slide 17**: typo — "Data Warehouse (DH)"
  debería decir "(DW)".
- **Slides 33-34** (Netflix, Spotify): son capturas de UI personalizadas (una
  playlist y una lista específicas) — no explican el mecanismo, solo
  muestran el resultado. `infografico_producto_de_datos.pptx` ya las conecta
  conceptualmente; si se quiere, podrían quedar como capturas de apoyo
  "secundarias" en vez de la explicación principal.

## Fuentes usadas (verificadas, no inventadas)

- **5 V's:** definición base de Gartner (Volumen, Velocidad, Variedad),
  ampliada con Veracidad y Valor — ya son las 5 que el resto de la sesión
  (slides 9-14 de `01_introduccion.pptx`) desarrolla una por una.
- **Estadísticas de volumen de datos:** [Statista — Volume of data/information created, captured, copied, and consumed worldwide](https://www.statista.com/statistics/871513/worldwide-data-created/), verificado vía búsqueda — 181 ZB en 2025, proyección de ~221-240 ZB para 2026.
- **Deprecación de Cloud Datalab / Cloud ML Engine:** confirmado vía documentación de Google Cloud — Vertex AI Workbench es el reemplazo recomendado, con sus propias notas de deprecación desde enero 2025.
- **"Producto de datos":** [Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly Media](https://www.oreilly.com/library/view/data-mesh/9781492092384/) — la referencia que formalizó el término en la industria, con desarrollo activo en 2025 (Nextdata OS, la empresa que la propia autora fundó para llevarlo a producto).

## Cómo se construyeron

Con `pptxgenjs` (el mismo motor que usa el skill de PowerPoint de este
entorno) — iconos vectoriales reales (react-icons, no capturas de pantalla),
paleta de un solo color de acento sobre fondo neutro, siguiendo la misma
disciplina de diseño de Nussbaumer Knaflic que ya se usó en
`slides_maestria/` y en los `slides.md` de Especialidad. Cada slide se validó
estructuralmente (`validate.py` del skill) y se verificó por script que
ningún elemento se saliera del área de la diapositiva — este entorno no tiene
LibreOffice instalado, así que no hubo render visual de control; si algo se
ve apretado al abrirlo en PowerPoint, es la primera revisión pendiente.
