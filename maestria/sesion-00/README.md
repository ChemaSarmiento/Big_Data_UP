# Sesión 00 — Prerequisito obligatorio (Linux, Python, SQL, GCP)

> Programa completo (evaluación, notas de facilitación): [`PROGRAMA.md`](../PROGRAMA.md)
> Teoría con explicaciones y referencias: [`teoria.md`](teoria.md)

## Índice
1. Linux: terminal avanzada, SSH, gestión de procesos, permisos
2. Python: repaso rápido, estructuras de datos, comprehensions, manejo de excepciones
3. SQL: JOINs complejos, window functions, CTEs
4. GCP: crear proyecto, `gcloud` CLI, IAM básico
5. Checkpoint de admisión (quiz + mini-ejercicio) antes de la Sesión 1

## Checkpoint de admisión
Quiz corto + mini-ejercicio de SQL y Python. Quien no lo pasa recibe material de refuerzo antes de la Sesión 1 — el ritmo desde el día 1 no deja espacio para nivelar en clase.

## Entregable
Checkpoint aprobado + proyecto de GCP configurado (ver `environment/gcp-setup.md`, checklist de la Sección 5).

## Ejemplo / material de apoyo
`recursos/sql-practica/employee_db_queries.sql` — progresión SELECT → agregaciones → joins → subconsultas sobre la base de datos de empleados (`test_db`). Es el mismo tipo de pregunta que se hará en SQL distribuido (Sesión 2), pero sobre una base pequeña de un solo nodo.

## Mirando hacia el proyecto final
El curso usa `bank_transactions.csv` como dataset transversal en las Sesiones 2-13 (detección de fraude), pero el capstone técnico (Sesión 13) puede construirse sobre ese mismo dataset o sobre uno propio del catálogo real — revisa [`recursos/datasets/README.md`](../../recursos/datasets/README.md) desde ahora, sobre todo si quieres un caso de negocio distinto a fraude bancario (retail/PROFECO, ciberseguridad, texto masivo). El requisito del proyecto final es ≥15GB (pueden combinarse varios archivos del catálogo) — vale la pena reservar mentalmente una opción desde esta sesión para no decidirlo apurado en la Sesión 5.

## Recursos vinculados
- [`recursos/sql-practica/`](../../recursos/sql-practica/) — SQL de nivelación
- [`environment/gcp-setup.md`](../../environment/gcp-setup.md) — setup de GCP
- [`recursos/datasets/README.md`](../../recursos/datasets/README.md) — catálogo de datasets reales (≥15GB)

## Slides
- **Deck nuevo:** [`slides_maestria/sesion-00.md`](../../slides_maestria/sesion-00.md) (Slidev) — `npx slidev sesion-00.md --open` desde `slides_maestria/`
- `slides/04_python_fasttrack.pptx`
- `slides/05_sql_fasttrack.pptx`

## Checklist de la sesión
- [ ] Contenido revisado
- [ ] Actividad completada
- [ ] Entregable subido (si aplica)
