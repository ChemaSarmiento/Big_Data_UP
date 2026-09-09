# Teoría — Sesión 00: Nivelación

> Este documento es el material de lectura/estudio antes de la Sesión 1. No se evalúa
> formalmente (ver `PROGRAMA.md`), pero sin esto la Sesión 1 va a sentirse confusa —
> vocabulario técnico que se usa sin explicar.

## 1. Linux esencial

No vas a administrar servidores. Vas a necesitar lo mínimo para no bloquearte cuando
un facilitador comparta pantalla o cuando sigas una guía paso a paso.

**La idea central:** una terminal es un explorador de archivos, pero en vez de hacer
doble clic para moverte entre carpetas, escribes el nombre del comando. No hay nada
"mágico" en esto — cada comando de terminal tiene un equivalente exacto en el explorador
gráfico que ya conoces:

| Lo que haces con el mouse | El comando equivalente | Qué hace |
|---|---|---|
| Abrir una carpeta | `cd nombre-carpeta` | Cambiar de directorio (*change directory*) |
| Ver qué hay en una carpeta | `ls` | Listar (*list*) el contenido |
| Ver "dónde estoy" | `pwd` | Imprimir el directorio actual (*print working directory*) |
| Crear una carpeta nueva | `mkdir nombre` | Crear directorio (*make directory*) |

Eso es prácticamente todo lo que necesitas reconocer para la Sesión 1. Si en algún
momento un comando se ve más largo (con `--flags` o `/rutas/con/slashes`), no memorices
la sintaxis — el objetivo de este track es que reconozcas qué está pasando, no que
lo escribas de memoria.

**Referencia:** [The Linux Command Line (guía gratuita, cap. 1-3 alcanzan)](https://linuxcommand.org/tlcl.php).

## 2. Python esencial

Tres ideas, nada más:

- **Una variable** es una etiqueta con un valor pegado — `precio = 25.9` guarda el
  número 25.9 bajo el nombre `precio`, para poder usarlo después sin reescribirlo.
- **Un notebook** (Jupyter/Colab) es un documento donde el texto explicativo y el
  código conviven en celdas separadas — corres una celda a la vez y ves el resultado
  justo debajo, no todo el programa de un jalón como en una hoja de cálculo con macros.
- **Correr una celda** es `Shift + Enter` (o el botón ▶). El orden en que corres las
  celdas importa — si una celda usa una variable que otra celda de más abajo todavía
  no ha creado, va a fallar. Es el error más común de alguien nuevo en notebooks, y no
  es un error tuyo: es cómo funciona la herramienta.

**Referencia:** [Google Colab — introducción oficial (10 min, interactiva)](https://colab.research.google.com/notebooks/intro.ipynb).

## 3. SQL esencial

SQL es el idioma con el que casi cualquier base de datos del mundo responde preguntas.
Tres palabras cubren el 80% de lo que vas a leer en este curso:

- **`SELECT`** — qué columnas quiero ver. `SELECT nombre, salario FROM empleados`
  significa "muéstrame las columnas nombre y salario de la tabla empleados".
- **`WHERE`** — con qué condición filtro filas. `WHERE salario > 50000` significa
  "solo las filas donde el salario sea mayor a 50,000".
- **`GROUP BY`** — cómo agrupo para resumir. `GROUP BY departamento` significa
  "trata cada departamento como un solo grupo" — típicamente se combina con una
  función como `COUNT()` o `AVG()`: "cuántos empleados hay por departamento" o
  "salario promedio por departamento".

Puesto junto:

```sql
SELECT departamento, AVG(salario) AS salario_promedio
FROM empleados
WHERE activo = 1
GROUP BY departamento;
```

Se lee de corrido: "de la tabla empleados, quédate solo con los activos, agrúpalos por
departamento, y muéstrame el salario promedio de cada grupo". Practica exactamente esto
en `recursos/sql-practica/employee_db_queries.sql` (secciones 1-2) — no hace falta
escribir SQL nuevo, solo correr y leer lo que cada consulta responde.

**Referencia:** [SQLBolt — lecciones interactivas 1-4 (gratis, sin registro)](https://sqlbolt.com/).

## 4. Acceso a la consola web de GCP

No vas a instalar nada en tu computadora. Todo el curso corre desde el navegador, en
la consola web de Google Cloud. Los pasos 1-3 de
[`environment/gcp-setup.md`](../../environment/gcp-setup.md) (cuenta, proyecto, alerta
de presupuesto) son los únicos que te tocan en este track — el resto de ese documento
(instalar `gcloud` localmente) es para el track de Maestría.

**Un detalle importante que sí te toca:** configura la alerta de presupuesto (paso 3)
antes de tocar cualquier otra cosa. Google Cloud da $300 USD de crédito por 90 días,
pero si algo queda corriendo sin que nadie lo apague, se puede consumir ese crédito
rápido — la alerta te avisa por correo antes de que eso pase.

---

## Mirando hacia adelante

Con esto ya tienes vocabulario suficiente para la Sesión 1. No necesitas practicar
más SQL o Python ahora mismo — en la Sesión 3 y 4 vas a volver a estas mismas ideas,
pero ya aplicadas a datos reales y a escala.

## Referencias

- [The Linux Command Line](https://linuxcommand.org/tlcl.php) — guía gratuita
- [Google Colab — introducción oficial](https://colab.research.google.com/notebooks/intro.ipynb)
- [SQLBolt](https://sqlbolt.com/) — lecciones interactivas de SQL
- [Google Cloud Free Tier](https://cloud.google.com/free) — documentación oficial del crédito de $300 USD
