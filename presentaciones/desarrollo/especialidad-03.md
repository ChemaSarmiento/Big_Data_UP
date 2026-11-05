# Caso de apertura — una decisión con consecuencias

Caso real de este curso: alguien revisa las transacciones bancarias sospechosas de un solo día, pero la consulta recorre el histórico completo cada vez que se ejecuta. El resultado tiene menos de 50 filas y aun así factura como si hubiera leído millones. ¿Por qué `LIMIT 10` no garantiza una lectura barata?

**Antes de seguir:** pregúntale al grupo qué creen que está pasando — en voz alta, sin escribir nada.

---

# El mecanismo que necesitas entender

La respuesta al caso de apertura: `LIMIT 10` decide cuántas filas **se muestran al final**, no cuántas **se leen** para llegar ahí. BigQuery cobra por lo segundo, no por lo primero.

Mira estas dos tablas — mismos datos, mismo resultado, distinto trabajo:

| | `lab.sin_particion` (toda la tabla) | `lab.por_fecha` (particionada por día) |
|---|---|---|
| Filas en el resultado | 3 | 3 |
| Filas que tuvo que **leer** | 2,000,000 (todo el histórico) | 18,000 (solo el día pedido) |
| Bytes facturados (ejemplo) | ~140 MB | ~1.3 MB |

La pregunta nunca cambió. Lo que cambió es **cuánto tuvo que recorrer** para contestarla — eso es lo que ves en el estimador de bytes, no en las filas del resultado.

---

# Clustering en BigQuery

Clustering ordena físicamente las filas de una tabla según una o varias columnas que tú elijas (hasta 4), sin crear tablas separadas. Filas con valores parecidos en esa columna terminan en los mismos bloques de almacenamiento.

<div class="grid grid-cols-3 mt-4">
<div class="border rounded p-3"><div class="font-bold">bloque 1</div><div class="text-sm mt-1">from_account: ACC-001, ACC-002</div></div>
<div class="border rounded p-3" style="border-color:var(--accent);background:var(--wash)"><div class="font-bold">bloque 2</div><div class="text-sm mt-1">from_account: ACC-003, ACC-004</div></div>
<div class="border rounded p-3"><div class="font-bold">bloque 3</div><div class="text-sm mt-1">from_account: ACC-005, ACC-006</div></div>
</div>
<p class="text-sm mt-2"><code>WHERE from_account = 'ACC-003'</code> solo abre el bloque resaltado — no toca los demás.</p>
*(diagrama de ejemplo — se puede reemplazar por uno real de la consola)*

Útil cuando filtras seguido por una columna que **no** es la fecha — por ejemplo, investigar todo el historial de una cuenta marcada como sospechosa.

---

# Partitioning en BigQuery: el archivero con un cajón por día

Un archivero con miles de expedientes sueltos, sin orden → para encontrar los de un día, revisas **todo** el archivero. El mismo archivero, con **un cajón por día** → buscar ese día es abrir un solo cajón.

Eso es particionar: la tabla se organiza físicamente en pedazos — en `lab.por_fecha`, un pedazo por cada día de `timestamp`.

<div class="grid grid-cols-4 mt-4">
<div class="border rounded p-3 text-center">2025-01-01</div>
<div class="border rounded p-3 text-center" style="border-color:var(--accent);background:var(--wash)">2025-01-02</div>
<div class="border rounded p-3 text-center">2025-01-03</div>
<div class="border rounded p-3 text-center">...</div>
</div>
<p class="text-sm mt-2"><code>WHERE DATE(timestamp) = '2025-01-02'</code> solo abre el cajón resaltado.</p>
*(diagrama de ejemplo — se puede reemplazar por uno real de la consola)*

**El límite real:** particionar ayuda solo si filtras por la columna de partición. Filtrar por otra columna (`from_account`, por ejemplo) no usa el cajón — ahí entra el clustering del slide anterior. La combinación típica para este dataset: partición por fecha + clustering por cuenta.

---

# Laboratorio guiado — preparación y objetivo

Hoy trabajas sobre un dato real del curso: `bank_transactions.csv` (transacciones bancarias, ~7.5 GB), ya subido a Cloud Storage. Si tu proyecto final es del caso banca/riesgo, hoy es tu primer contacto real con ese mismo dataset.

**Lo que ya existe** (el equipo técnico lo preparó antes de clase, cargando el mismo CSV dos veces):
- `lab.sin_particion` — la tabla completa, sin ninguna organización especial.
- `lab.por_fecha` — exactamente los mismos datos, organizados en particiones por día (`PARTITION BY DATE(timestamp)`).

Mismas filas, misma información — solo cambia cómo están organizadas físicamente. Eso es lo que vas a comprobar.

**Antes de empezar:** en BigQuery, abre el explorador (panel izquierdo) → tu proyecto → el dataset `lab` → confirma que ves las dos tablas (`sin_particion`, `por_fecha`). Si no aparecen, avisa antes de seguir.

---

# Laboratorio · paso 1 — elige un día y mira el costo antes de correr

1. En el editor de BigQuery, pega esta consulta (cambia `MI_PROYECTO` por el tuyo):
```sql
SELECT COUNT(*) AS transacciones, SUM(amount) AS monto_total
FROM `MI_PROYECTO.lab.sin_particion`
WHERE DATE(timestamp) = '2025-01-15';
```
2. **Antes de dar clic en "Ejecutar"**, mira el número del estimador de bytes (esquina superior derecha) y anótalo.
3. Abre una pestaña nueva, pega la misma consulta pero cambia `sin_particion` por `por_fecha`. Mira el estimador otra vez, antes de ejecutar.

**Lo que deberías notar:** el número de la tabla particionada es mucho más chico, aunque la pregunta es idéntica.

---

# Laboratorio · paso 2 — ejecuta las dos y guarda la evidencia

1. Ejecuta las dos consultas del paso anterior (botón "Ejecutar" en cada pestaña).
2. Debajo de la tabla de resultados, busca la pestaña **"Detalles del job"**.
3. Anota, de cada una: bytes procesados, bytes facturados y duración.
4. Confirma que `transacciones` y `monto_total` son **idénticos** en ambas — si no coinciden, algo está mal con las tablas; avisa antes de seguir.

---

# Laboratorio · paso 3 — interpreta lo que acabas de ver

Con tus números del paso 2, completa en voz alta: "Para la misma pregunta, `lab.por_fecha` leyó ___ veces menos datos que `lab.sin_particion`."

Cambia la fecha del `WHERE` a otro día y repite el paso 1 — confirma que el patrón se mantiene, no fue casualidad de ese día.

---

# Laboratorio · paso 4 — construye tu evidencia visual

1. En una hoja de cálculo (o a mano), dibuja dos barras: bytes procesados de `sin_particion` y de `por_fecha`.
2. Título de la gráfica: tu conclusión en una frase.

**Lo que deberías ver** (si tu resultado se comporta como el mecanismo de hace unos slides):

<p class="text-sm font-bold mt-4">Bytes procesados</p>
<div class="space-y-4 mt-2">
<div><div class="text-sm">sin_particion</div><div class="rounded" style="background:var(--accent);width:100%;height:28px"></div><div class="text-xs mt-1">140 MB</div></div>
<div><div class="text-sm">por_fecha</div><div class="rounded" style="background:var(--accent);width:1%;min-width:6px;height:28px"></div><div class="text-xs mt-1">1.3 MB</div></div>
</div>

Si tus barras salen parecidas entre sí, algo no está funcionando — revisa el slide "Cuando el resultado no es el esperado" antes de entregar.

---

# Laboratorio · paso 5 — exploración visual, sin escribir código

1. Corre esta consulta sobre `lab.por_fecha`:
```sql
SELECT DATE(timestamp) AS dia, COUNT(*) AS transacciones_sospechosas
FROM `MI_PROYECTO.lab.por_fecha`
WHERE is_suspicious = true
GROUP BY dia
ORDER BY dia;
```
2. Clic en **"Explorar con Looker Studio"** desde los resultados de BigQuery.
3. Gráfico de líneas — eje X: `dia`, eje Y: `transacciones_sospechosas`.

Sin instalar nada, sin escribir Python — la misma ruta que usarías en el trabajo real para una primera mirada rápida a un dato nuevo.

---

# Laboratorio — ¿qué demuestra el resultado?

Entregar: las consultas usadas, la confirmación de que el resultado es igual en ambas tablas, tu comparación visual de bytes, y el gráfico de Looker Studio. La evidencia principal es el trabajo evitado para la misma pregunta, no una cifra de costo sin contexto.

**Discusión:** compara la evidencia con lo que el grupo dijo en el caso de apertura. Distingue lo observado de lo que todavía no puedes concluir.

---

# Cuando el resultado no es el esperado

No hay filas: revisa qué fechas existen realmente en la tabla (`SELECT MIN(timestamp), MAX(timestamp) FROM ...`). Los bytes no bajan: revisa que el `WHERE` filtre por `timestamp`/`DATE(timestamp)` — exactamente la columna de partición, no otra. Tiempo muy pequeño: puede que el job haya usado caché de resultados; vuelve a correr con un cambio en la consulta para comprobar.

**Regla de trabajo:** conserva la consulta, el cambio que hiciste y la evidencia del resultado inesperado. Cambia una sola cosa a la vez.

---

# Para profundizar después de clase

Extensión de 30–45 minutos: agrega clustering por `from_account` a `lab.por_fecha` y repite el paso 1 filtrando por una cuenta en vez de por fecha — compara el estimador de bytes de las tres combinaciones.

El ejercicio de clase usa una muestra acotada del dataset; no sustituye la evidencia de volumen real que exige el proyecto final. Detén procesos y recursos temporales al terminar.
