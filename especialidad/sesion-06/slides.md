---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
  .box { border-left: 4px solid #1d4ed8; padding: 0.5em 1em; background: rgba(29,78,216,0.05); }
---

# Sesión 06
## Data Lakes y gobierno del dato

Especialidad — Big Data (sin lab de código)

---

## Bodega vs. archivero organizado

Un data warehouse tradicional: un archivero, todo ya clasificado en carpetas
con etiqueta.

Un **data lake**: una bodega — se mete cualquier cosa sin clasificar de
entrada, porque no siempre sabes de antemano cómo vas a necesitar usarlo
después.

<div class="box">
Esto no es un defecto — clasificar de más antes de saber para qué se va a
usar el dato es, en sí mismo, una forma de sobre-ingeniería (Sesión 1).
</div>

---

## Medallion — tres capas de madurez

| Capa | Analogía | Contiene |
|---|---|---|
| 🟤 Bronze | La bodega tal cual llega el camión | Datos crudos, sin limpiar |
| ⚪ Silver | La bodega ya ordenada por categoría | Datos limpios, tipados |
| 🟡 Gold | El escaparate, listo para vender | Listo para un dashboard |

`recursos/etl-tipo-cambio/` implementa este patrón: `data/raw/` (bronze) →
`data/processed/` (silver) → MariaDB (gold).

---

## Por qué importa el gobierno del dato

**Sin control de acceso** → cualquiera modifica datos sensibles, sin registro
de quién lo hizo.

**Sin validación de calidad** → un error se propaga silenciosamente hasta el
dashboard que un ejecutivo usa para decidir.

**Sin linaje (origen documentado)** → cuando algo sale mal, nadie puede
rastrear de dónde vino el dato.

<div class="box">
El gobierno del dato se evalúa por sus <b>consecuencias</b>, no por su
configuración técnica.
</div>

---

# Actividad

## Caso de estudio

Una falla real por mal manejo de datos — costo de negocio, no técnico.

En equipos: ¿qué falló en términos de gobernanza (no de tecnología)? ¿Cómo se
habría evitado? No busquen el error de código — busquen el error de proceso.

---

## Entregable de hoy

Ninguno formal — la discusión en equipo es el ejercicio.

---

# → Sesión 07

Datos en tiempo real
