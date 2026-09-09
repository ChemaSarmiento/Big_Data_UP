# Teoría — Sesión 00: Prerequisito obligatorio (Linux, Python, SQL, GCP)

> Este Módulo 0 se evalúa con un checkpoint corto antes de la Sesión 1 (ver
> `PROGRAMA.md`). El ritmo desde el día uno es alto — no hay tiempo de clase para
> nivelar estos cuatro temas, así que este documento asume que ya programas en
> Python y conoces SQL básico, y profundiza justo donde el curso lo va a exigir.

## 1. Linux: terminal avanzada, SSH, procesos, permisos

En Maestría vas a operar clusters remotos (Dataproc), no solo correr notebooks
locales. Lo que hace la diferencia entre "seguir atorado" y "diagnosticar rápido":

- **SSH** (`ssh usuario@host`) es cómo abres una terminal *dentro* de una máquina
  remota — el cluster de Spark vive en GCP, no en tu laptop, y SSH es el túnel para
  operarlo como si estuviera enfrente de ti. `gcloud compute ssh <instancia>` hace
  esto automáticamente autenticado contra tu proyecto de GCP.
- **Gestión de procesos** (`ps aux`, `top`, `kill <pid>`): un cluster de Spark corre
  procesos JVM que pueden quedarse colgados o consumir memoria. Saber listar procesos
  y matarlos por PID es la diferencia entre reiniciar el cluster completo (caro, en
  tiempo y en crédito de GCP) y matar un solo proceso zombie.
- **Permisos** (`chmod`, `chown`, el triplete `rwx` para dueño/grupo/otros): relevante
  en cuanto subas scripts de inicialización a un cluster (`hugging_face_deps.sh` en
  `recursos/managed-spark-cluster/`) — un script sin permiso de ejecución (`chmod +x`)
  falla en el arranque del cluster de forma silenciosa y difícil de diagnosticar si
  no sabes qué buscar.

**Referencia:** [SSH: The Secure Shell, cap. 1-2](https://www.snailbook.com/) · [gcloud compute ssh — documentación oficial](https://cloud.google.com/sdk/gcloud/reference/compute/ssh).

## 2. Python: estructuras de datos, comprehensions, excepciones

PySpark expone una API que se siente como Python normal, pero corre distribuido —
entender bien las estructuras de datos nativas de Python evita errores sutiles al
traducir lógica a Spark:

- **List/dict comprehensions** — `[x**2 for x in rango]` es el equivalente Python de
  un `map()`, y es literalmente el mismo patrón mental que usarás en
  `df.select(F.col("x") ** 2)` en Spark: transformar cada elemento sin un loop
  explícito.
- **Manejo de excepciones** (`try/except`) — importa porque un job de Spark que falla
  a la mitad de un dataset de 20GB no te da un traceback claro de "qué fila lo rompió"
  sin que tú hayas instrumentado el manejo de errores en el `Imputer`/parsing.
  `recursos/spark/05_data_cleansing.ipynb` es exactamente ese caso: datos "sucios" que
  rompen si no se anticipan (`\N` como nulo no estándar, columnas sin encabezado).

**Referencia:** [Python Data Structures — docs oficiales](https://docs.python.org/3/tutorial/datastructures.html) · [Errors and Exceptions — docs oficiales](https://docs.python.org/3/tutorial/errors.html).

## 3. SQL: JOINs complejos, window functions, CTEs

Esto es directamente lo que vas a escribir en la Sesión 2 (BigQuery) y en Hive
(`recursos/hive/hive-queries.sql`), así que vale la pena tenerlo sólido antes:

- **JOINs complejos** — no solo `INNER JOIN`, sino entender cuándo un `LEFT JOIN`
  cambia el resultado (filas que no tienen match del lado derecho se conservan con
  `NULL`) y por qué eso importa para no perder datos silenciosamente en un pipeline.
- **Window functions** — `RANK() OVER (PARTITION BY x ORDER BY y)` calcula un valor
  *por fila*, pero mirando un grupo de filas relacionadas, sin colapsarlas como haría
  un `GROUP BY`. Es la herramienta central de `recursos/spark/03_spark_sql.ipynb`
  (ranking de transacciones sospechosas) — practica ese notebook si esta idea no es
  automática todavía.
- **CTEs recursivos** (`WITH RECURSIVE`) — para jerarquías (ej. un árbol de
  categorías, o de reportes-directos en una organización) que un JOIN plano no puede
  resolver en un solo paso. Menos común en el día a día del curso, pero aparece en la
  Sesión 2 de Maestría (BigQuery) como parte de la profundización de SQL distribuido.

**Referencia:** [PostgreSQL — Window Functions (la explicación más clara que existe, aplica a BigQuery/Hive igual)](https://www.postgresql.org/docs/current/tutorial-window.html) · [BigQuery — Recursive CTEs](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#recursive_cte).

## 4. GCP: proyecto, `gcloud` CLI, IAM básico

A diferencia de Especialidad, aquí sí instalas y usas el SDK de Google Cloud
localmente — ver `environment/gcp-setup.md` completo (no solo los primeros 3 pasos).

- **`gcloud config set project <ID>`** — todo comando de `gcloud` opera sobre "el
  proyecto activo"; olvidar configurarlo es la causa #1 de "¿por qué mi cluster no
  aparece?" (se creó en otro proyecto sin que te dieras cuenta).
- **IAM básico** — quién puede hacer qué. Roles como `roles/dataproc.editor` o
  `roles/storage.objectViewer` son granulares a propósito: en la Sesión 13
  (Gobernanza) vas a ver por qué "darle a todos rol de Owner" es exactamente el tipo
  de decisión que un pipeline de datos regulado (banca, salud) no se puede permitir.

**Referencia:** [gcloud CLI — guía de inicio rápido](https://cloud.google.com/sdk/docs/quickstart) · [IAM — conceptos básicos](https://cloud.google.com/iam/docs/overview).

---

## Checkpoint de admisión

El quiz + mini-ejercicio de la Sesión 00 (ver `PROGRAMA.md`) cubre exactamente estos
cuatro bloques. Si algo de esta página no fue automático al leerlo, practica
`recursos/sql-practica/employee_db_queries.sql` completo (no solo las primeras
secciones, a diferencia de Especialidad) antes del checkpoint.

## Referencias

- [SSH: The Secure Shell](https://www.snailbook.com/)
- [gcloud compute ssh](https://cloud.google.com/sdk/gcloud/reference/compute/ssh)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Errors and Exceptions (Python)](https://docs.python.org/3/tutorial/errors.html)
- [PostgreSQL — Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [BigQuery — Recursive CTEs](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax#recursive_cte)
- [gcloud CLI — guía de inicio rápido](https://cloud.google.com/sdk/docs/quickstart)
- [IAM — conceptos básicos](https://cloud.google.com/iam/docs/overview)
