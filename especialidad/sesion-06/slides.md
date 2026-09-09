---
marp: true
theme: default
paginate: true
style: |
  section { font-family: 'Helvetica Neue', Arial, sans-serif; }
  h1, h2 { color: #1d4ed8; }
  .accent { color: #1d4ed8; font-weight: bold; }
---

# Sesión 06
## Data Lakes y gobierno del dato

Especialidad — Big Data (sin lab de código)

---

# Bodega vs. archivero organizado

Un data warehouse tradicional: un archivero, todo ya clasificado.

Un **data lake**: una bodega — se mete cualquier cosa sin clasificar de entrada, porque no siempre sabes cómo vas a necesitarlo después.

---

# Medallion — tres capas de madurez

| Capa | Analogía | Contiene |
|---|---|---|
| 🟤 Bronze | La bodega tal cual llega el camión | Datos crudos, sin limpiar |
| ⚪ Silver | La bodega ya ordenada | Datos limpios, tipados |
| 🟡 Gold | El escaparate | Listo para un dashboard |

---

# Por qué importa el gobierno del dato

**Sin control de acceso** → cualquiera modifica datos sensibles, sin registro.

**Sin validación de calidad** → un error se propaga silenciosamente hasta el dashboard ejecutivo.

**Sin linaje** → cuando algo sale mal, nadie puede rastrear de dónde vino.

---

# El gobierno se evalúa por sus consecuencias

No por su configuración técnica — por lo que pasa cuando algo falla.

---

# Actividad

Caso de estudio de una falla real por mal manejo de datos — costo de negocio, no técnico. Discusión en grupo.

**Entregable:** ninguno formal.

---

# → Sesión 07

Datos en tiempo real
