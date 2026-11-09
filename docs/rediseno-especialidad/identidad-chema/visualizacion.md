# Visualización de datos

La parte visual del storytelling con datos, con el enfoque de Cole Nussbaumer Knaflic y los principios de la Gestalt que ella usa para explicar por qué un gráfico limpio se entiende más rápido. Son descripciones propias de sus ideas, aplicadas a los tokens de esta identidad. La estructura del relato está en `storytelling.md`.

## Elegir el visual

Con una o dos cifras, el visual más eficaz es el texto: el número grande y una frase. Una tabla sirve cuando se consultan valores exactos, con el dato clave resaltado y el resto tenue; un mapa de calor es una tabla con color. Para relaciones entre dos variables, la dispersión. Para el tiempo continuo, las líneas, y para comparar dos momentos, la gráfica de pendiente. Para categorías, las barras, horizontales si los nombres son largos, siempre desde cero. Para contribuciones que suman y restan, la cascada. Las barras apiladas se usan con cuidado, porque solo la primera serie se compara bien.

Se evitan el pastel y la dona, porque el ojo compara mal ángulos y áreas; los efectos 3D, que distorsionan; y el eje secundario, que confunde (mejor dos gráficos alineados). La diapositiva culpable de la presentación de ejemplo usa un pastel de catorce rebanadas a propósito, como mal ejemplo.

## Quitar el desorden

Cada elemento que no informa añade carga cognitiva. El procedimiento es partir de la gráfica por defecto y quitar: el borde alrededor de la gráfica, las rejillas (o dejarlas muy tenues), los marcadores de datos, los decimales y las marcas de eje que sobran, y la leyenda, que se sustituye por etiquetas pegadas a los datos. Después, color consistente (la misma serie con el mismo color en todo el material), elementos alineados y espacio en blanco que deje respirar.

## Principios de la Gestalt

| Principio | Qué dice | Cómo se usa aquí |
| --- | --- | --- |
| Proximidad | Lo que está cerca se percibe como grupo | La etiqueta va pegada a su barra o cifra; los grupos se separan con espacio, no con líneas |
| Similitud | Lo que se parece (color, forma) se percibe como de la misma categoría | Una serie siempre del mismo color; el gris para el contexto y un solo acento para el dato clave |
| Cercamiento | Lo que está dentro de un borde o fondo se percibe como grupo | Una tarjeta en `surface-200` agrupa un dato y su nota; se usa poco, porque los marcos pesan |
| Cierre | El ojo completa las formas incompletas | Un gráfico sin borde ni caja se percibe cerrado; se eliminan los marcos innecesarios |
| Continuidad | El ojo sigue líneas y alineaciones | Todo se alinea al margen izquierdo; una línea o un borde común guía la lectura |
| Conexión | Lo que está unido por una línea se percibe como grupo, con más fuerza que por similitud | Las líneas de una serie temporal unen sus puntos; los conectores unen pasos de un proceso |

La alineación, el espacio en blanco y el contraste completan el conjunto: lo que no se alinea parece accidental, lo que no tiene aire se lee como ruido y lo que importa debe contrastar con lo que no.

## Dirigir la atención

Los atributos preatentivos, que el cerebro procesa antes de pensar, son el color, el tamaño, la posición y el énfasis tipográfico (negrita, cursiva, subrayado). Se usan con intención y con parquedad: si todo destaca, nada destaca. La receta de esta identidad es el gris para todo el contexto y un solo acento rojo (`signal`) para el dato que importa. Se hace la prueba de entrecerrar los ojos: lo primero que se distingue debe ser lo que la audiencia tiene que ver. La lectura empieza arriba a la izquierda, así que ahí van la conclusión y los elementos de orden.

El texto también es un visual. El título dice la conclusión, la cifra clave va en negrita y las anotaciones se pegan al dato. Un gráfico sin una frase que diga qué mirar deja el trabajo al público.

## Pensar como diseñador

Knaflic ordena el criterio de diseño en ideas que se aplican a cada pieza. Las affordances son las pistas que dicen cómo leer algo: se resalta lo importante, se eliminan las distracciones y se crea una jerarquía visual clara. La accesibilidad es que cualquiera lo entienda: texto legible, contraste suficiente, color que nunca dice algo solo. La estética es que un material cuidado gana la confianza de la audiencia, y se logra con limpieza, no con adornos. La aceptación es que el público debe aceptar el diseño: se conoce su cultura y se adapta el estilo a ella.

## Especificación con esta identidad

| Elemento del gráfico | Token |
| --- | --- |
| Serie principal o dato neutral | `brand` |
| Contexto y comparación | `ink-muted` |
| El dato que importa (uno solo) | `signal` |
| Tercera serie | `teal` |
| Ejes, rejillas (tenues) y marcos | `line` |
| Etiquetas y anotaciones | `caption` en `ink-muted`; la cifra clave en `data` o `data-lg` |
| Fondo de tarjeta de un dato | `surface-200` con borde de 1 px en `line` |

Las barras parten de cero, tienen más ancho que los huecos entre ellas y llevan el valor pegado al final. No hay más de cuatro colores por gráfico. El color nunca dice algo solo: el dato en rojo lleva una etiqueta («mejora», «+4 pts»). En un lienzo de 1920 × 1080 el texto de los ejes no baja de 24 px; en PowerPoint y Google Slides, de 10 pt.
