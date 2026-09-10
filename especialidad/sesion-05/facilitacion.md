# Facilitación — Sesión 05: Cómo se ve un pipeline de datos real

> Guion de 3 horas: lab guiado en Colab + demo de dashboard. Es la sesión que
> cierra el ciclo completo (de dónde viene el dato → a dónde va) — dale al cierre
> con el dashboard el mismo peso que al ETL en sí.

## Antes de empezar (facilitador)

Prueba `recursos/etl-tipo-cambio/etl_tipo_cambio_colab.ipynb` de punta a punta
antes de la sesión — cualquier fricción de configuración (API keys, permisos)
la quieres resolver tú, no en vivo con el grupo esperando.

---

## Bloque 1 — Apertura y gancho (0:00–0:15)

**Talking point de apertura:**

> "ETL son las siglas de Extract, Transform, Load — y es, literalmente, el
> patrón detrás de casi cualquier sistema de datos que van a encontrar en su
> trabajo. Hoy lo van a ver correr de principio a fin, sin escribir Python
> desde cero, y vamos a terminar viendo a dónde va el dato: un dashboard real."

**Pregunta de apertura:**

> "Piensen en un reporte que reciben regularmente en su trabajo — ¿de dónde
> creen que salieron esos números, y qué tuvo que pasar entre que el dato
> 'nació' y que ustedes lo vieron en el reporte?"

---

## Bloque 2 — ETL, la teoría (0:15–1:00, 45 min)

### Extract, Transform, Load (20 min)
Recorre las tres etapas con el ejemplo real: una API pública de tipo de cambio
→ limpieza en Python → carga en MariaDB. Para cada etapa, pregunta: **"¿qué
podría salir mal aquí específicamente?"** (Extract: la API no responde;
Transform: un valor viene en formato inesperado; Load: la base de datos no
tiene espacio o permisos).

### La pregunta que casi nunca se hace (15 min)

> "¿Quién usa el dato al final, y para qué?" — plantéala como el hilo
> conductor de toda la sesión, no solo de la última parte.

### Por qué esto importa (10 min)

> "Es fácil construir un ETL técnicamente perfecto que nadie termina usando —
> el ejercicio de hoy cierra explícitamente con la respuesta visual a esa
> pregunta."

---

## Bloque 3 — Break (1:00–1:10, 10 min)

---

## Bloque 4 — Lab guiado (1:10–2:40, 90 min)

### Paso 1 — Correr el ETL en Colab (50 min)

En parejas, solo llenando la celda de configuración (no tocan el resto del
código):

```python
# etl_tipo_cambio_colab.ipynb — solo esta celda se edita
SIMBOLOS = ["MXN", "EUR"]
```

**Deberías ver:** el notebook corre extract → transform → load, terminando con
una confirmación de filas cargadas en MariaDB.

**Talking point mientras corre:** "Noten los encabezados de sección en el
notebook — extract, transform, load están marcados explícitamente. Sigan ese
flujo aunque no lean cada línea de código."

**Si falla en la etapa de Load:** confirmar la conexión a MariaDB
(`environment/mariadb-vscode-setup.md`) — es el punto de fricción más común de
este lab.

### Paso 2 — El dashboard, sin tocar código (30 min)

```python
# recursos/etl-cripto/ETL_Crypto_Dash_mejorado.ipynb — correr, sin modificar
create_dashboard(df_resultado)
```

**Talking point antes de correr:** "Este notebook es un ETL distinto —
enriquecimiento de datos de cripto — pero termina en algo que el de tipo de
cambio no muestra: un dashboard real. Corran esta celda y observen."

**Deberías ver:** una figura con gráficas de cambio % y noticias recientes.

### Paso 3 — Diagrama del flujo armado (10 min)

Cada pareja dibuja (a mano o en una herramienta simple) el flujo que acaban de
correr: origen → transformación → destino → consumo final.

---

## Bloque 5 — Cierre (2:40–3:00, 20 min)

**Entregable de hoy:** diagrama del flujo + captura del resultado, incluyendo
la captura del dashboard.

**Puente a la Sesión 6:**

> "Hoy vieron un pipeline completo de punta a punta. La próxima sesión vemos
> dónde 'vive' todo esto a mayor escala — data lakes, y por qué el orden
> importa tanto como el dato mismo."

---

## Notas de costo GCP

- Este lab corre en Colab (gratis) + MariaDB (instancia ya creada en sesiones
  previas) — sin costo adicional de cómputo GCP hoy. Buen momento para
  confirmar que la instancia de MariaDB no se dejó corriendo innecesariamente
  entre sesiones.
