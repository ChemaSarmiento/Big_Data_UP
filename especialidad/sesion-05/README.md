# Sesión 05 — Cómo se ve un pipeline de datos real

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)
> Guion de 3 horas (talking points + lab paso a paso): [`facilitacion.md`](facilitacion.md)

## Índice
1. Qué es un ETL
2. De dónde vienen los datos, a dónde van, quién los consume al final (dashboard, modelo, reporte)

## Lab guiado
Armar un flujo simple con una herramienta low-code/no-code o notebook muy asistido, con apoyo técnico 1:1.

## Entregable
Diagrama del flujo armado + captura del resultado, incluyendo la captura del dashboard final (ver abajo) — cierra el ciclo completo: de dónde vienen los datos → a dónde van → **qué se ve al final**.

## Ejemplo / material de apoyo
`recursos/etl-tipo-cambio/etl_tipo_cambio_colab.ipynb` — correrlo en Colab sin tocar el código (solo llenar la celda de configuración) es exactamente el nivel de este track: el grupo ve extract → transform → load funcionando de principio a fin sin escribir Python desde cero. Para cerrar el flujo con "quién consume el dato al final", correr (sin modificar) la celda `create_dashboard()` de `recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb` — mismo patrón E-T-L, pero termina en un dashboard real en vez de solo una tabla en MariaDB, que es justo la pregunta que abre esta sesión ("a dónde van los datos, quién los consume al final").

## Recursos vinculados
- [`recursos/etl-tipo-cambio/etl_tipo_cambio_colab.ipynb`](../../recursos/etl-tipo-cambio/etl_tipo_cambio_colab.ipynb)
- [`recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb`](../../recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb) — celda `create_dashboard()`, para mostrar el consumo final del dato

## Slides
- **Deck nuevo:** [`slides.md`](slides.md) (Marp)

**Cómo presentar** (desde esta carpeta):
```bash
npx @marp-team/marp-cli slides.md -o slides.html   # exporta y abre slides.html en el navegador
```
Pantalla completa: F11 en el navegador. Flechas ←/→ para navegar entre slides.
Alternativa en PDF (modo presentación del lector): `npx @marp-team/marp-cli slides.md -o slides.pdf`.

Material de apoyo (pptx original):
- `slides/02_fuentes_y_manejo.pptx`
- `slides/06_grandes_bases_de_datos.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
