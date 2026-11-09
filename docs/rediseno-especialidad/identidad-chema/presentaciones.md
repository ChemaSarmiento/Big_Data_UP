# Presentaciones

Reglas de diapositivas y cómo aplicarlas en cada herramienta. La voz de los textos sale de `voz.md`; aquí está la parte visual y de construcción.

## Lienzo y composición

La proporción es 16:9, con margen exterior de 64 px a la escala del sistema (128 px en un lienzo de 1920 × 1080). El título va arriba a la izquierda, en Source Serif 4 600, de máximo dos líneas y redactado como afirmación de no más de doce palabras. Encima puede llevar una etiqueta corta en mayúsculas, en `label`, color `brand`, que nombre el tramo del mensaje. Cada diapositiva tiene una sola idea (la lógica de títulos y de gráficos está en `storytelling.md` y `visualizacion.md`), menos de veinticinco palabras y un solo elemento rojo. La fuente va abajo a la izquierda en `caption` y el número de página a la derecha.

La portada y el cierre usan fondo oscuro o `brand`, con la imagen firma en un lado. Los fondos alternan entre los dos temas del sistema; una diapositiva de enunciado en el tema oscuro, con la cifra grande en rojo, funciona como clímax.

## Color en gráficas

La serie principal va en `brand`, el contexto o la comparación en `ink-muted`, el dato destacado (uno solo) en `signal` y una tercera serie en `teal`. Los ejes, las rejillas y los marcos van en `line`, y las etiquetas en `caption`. No hay 3D ni degradados, y las leyendas se sustituyen por anotaciones directas cuando se puede. Las barras parten de cero, no hay más de cuatro colores por gráfica, y el color nunca dice algo solo: va acompañado de una etiqueta («mejora», «+4 pts»).

## Combinaciones de texto con contraste suficiente

Todas superan 4.5:1; las razones son aproximadas.

| Texto sobre fondo | Claro | Oscuro |
| --- | --- | --- |
| `ink` sobre `surface-100` | 14:1 | 16:1 |
| `ink-muted` sobre `surface-100` | 7:1 | 9:1 |
| `brand` sobre `surface-100` | 10:1 | 9:1 |
| `on-brand` sobre `brand` | 10:1 | 9:1 |
| `on-signal` sobre `signal` | 5:1 | 5:1 |
| `signal-ink` sobre `surface-100` | 6.2:1 | 8:1 |
| `teal` sobre `surface-100` | 6.6:1 | 10:1 |

Texto sobre un fondo rojo usa siempre `on-signal`; texto pequeño en color señal usa `signal-ink`, nunca `signal`.

## Cifras

Aproximaciones con `~`, múltiplos con `×`, diferencias de índices en «puntos». Las monedas llevan código (`MXN`, `USD`) y periodo. Los porcentajes no llevan decimales salvo que importen, y se usa el mismo número de decimales dentro de una tabla. La cifra protagonista va en `data-lg` y las de tabla en `data`, alineadas a la derecha.

## Notas del orador

Se escriben en la voz completa de Chema, no como resumen de la diapositiva. Marcan las pausas (`[pausa 3 s]`), la pregunta que se lanza a la sala antes de mostrar una cifra y la frase con la que se acepta un fallo. Nunca repiten el texto de la diapositiva.

## Por herramienta

**Slidev.** `assets/Kits/slidev/style.css` junto a `slides.md`, con las tres tipografías declaradas en el encabezado. `assets/Kits/slidev/ejemplo.md` trae portada, hallazgo, comparación y cierre, con notas en comentarios HTML.

**Marp.** `assets/Kits/marp/chema.css` como tema (`theme: chema`), con clases `dark`, `statement` y `cover`. `assets/Kits/marp/ejemplo.md` muestra el uso.

**HTML y CSS a mano.** `assets/CSS/chema-brand.css` con la clase `.cs-slide` para lienzos 16:9, tema claro y oscuro automático, y componentes para tarjetas, cifras y tablas.

**PowerPoint.** `assets/Kits/powerpoint/README.md` da los colores del tema por ranura, las tipografías con su sustituta segura, las medidas en pulgadas y las equivalencias de tamaño en puntos. La plantilla `chema-plantilla.pptx` va en el paquete descargable.

**Google Slides.** `assets/Kits/google-slides/README.md` explica cómo importar la plantilla `chema-plantilla.pptx` (mismo archivo que usa PowerPoint, en el formato de Google de 10 × 5.625 in) y trae un script de Apps Script que arma un deck desde un arreglo de diapositivas.

**Sitios y aplicaciones.** `assets/Kits/tailwind/theme.css` para Tailwind v4 y `assets/CSS/chema-brand.css` para HTML puro.
