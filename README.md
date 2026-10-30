# Sistema de Órdenes de Servicio y Citas

Proyecto de Ingeniería de Software I (IDSSI-27) · Universidad del Istmo, Campus Ixtepec · Equipo B.

Cliente: Servicio Automotriz Hermanos Ruiz, S.A. de C.V. El sistema digitaliza el ciclo de atención del
taller: citas, recepción del vehículo con checklist y fotografías, diagnóstico y asignación de bahía,
cotización con autorización del cliente por código 2FA, refacciones, cobro y entrega.

El avance detallado, paso a paso y por rol, está en [`Avances.txt`](Avances.txt).

## Contenido del repositorio

| Ruta | Contenido |
|---|---|
| `backend/` | API REST (Python, FastAPI) del flujo núcleo y sus pruebas automatizadas |
| `db/schema.sql` | Esquema de la base de datos (PostgreSQL), derivado del diagrama de clases v4 |
| `docs/documento/` | Documento de Ingeniería del Proyecto en LaTeX, un archivo por sección |
| `docs/entregas/` | PDF de cada entrega (`IS1-Fase1-EquipoB-v<versión>.pdf`) |
| `docs/propuesta/` | Propuesta de Solución Tecnológica (LaTeX) |
| `docs/03-vision/`, `docs/06-analisis/` | Fuentes de los diagramas (PlantUML) e imágenes del diagrama de clases |
| `.github/workflows/ci.yml` | Integración continua: pruebas, esquema en PostgreSQL y compilación del documento |
| `CONTRIBUTING.md` | Acuerdos de trabajo del equipo |

## Ejecutar el backend

Requiere Python 3.12 o superior.

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate            # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
cp .env.example .env              # el .env no se sube; sin cambios usa SQLite local
python -m app.semilla --demo      # 4 bahías, un usuario por rol y clientes FICTICIOS
uvicorn app.main:app --reload     # documentación interactiva: http://localhost:8000/docs
python -m pytest                  # 35 pruebas
```

La contraseña de los usuarios de demostración se toma de `SEED_PASSWORD` o se genera e imprime una vez.

## Base de datos (PostgreSQL)

Requiere PostgreSQL 14 o superior.

```bash
createdb taller
psql -d taller -f db/schema.sql
```

Después pon en `backend/.env`: `DATABASE_URL=postgresql+psycopg://USUARIO:CONTRASENA@localhost:5432/taller`.

## Compilar el documento

```bash
cd docs/documento
pdflatex -interaction=nonstopmode IS1-Fase1-EquipoB.tex   # dos veces, por el índice
```

Las figuras que todavía no existen aparecen en rojo con su descripción y la ruta de su archivo fuente.

## Equipo

| Integrante | GitHub | Rol |
|---|---|---|
| Abdías Daniel Chávez Cruz | AbdiasChavez | Product Owner, Developer |
| Ángel Yael Avendaño Guzmán | AyagDan | Scrum Master, Developer |
| Dulce María Estudillo Rosado | DulceRosado | Developer |
| Isis Alhelí González Maldonado | IsisAlheliGonzalezMaldonado | Developer |
| Isis Yamilet Meléndez Hernández | IsisMelendezHernandez | Developer |

El rol de QA Lead está por asignar.
