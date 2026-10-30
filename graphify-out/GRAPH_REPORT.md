# Graph Report - Florentino  (2026-10-29)

## Corpus Check
- 32 files · ~44,913 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 28 file(s) not represented in the graph (top: .tex 20, .puml 5, (none) 1)

## Summary
- 465 nodes · 1440 edges · 13 communities (12 shown, 1 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 264 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `980857f5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- conftest.py
- RolUsuario
- Acuerdos de trabajo · Equipo B
- Usuario
- models.py
- with
- portal.py
- schemas.py
- ordenes.py
- seguridad.py
- notificaciones.py
- Sistema de Órdenes de Servicio y Citas

## God Nodes (most connected - your core abstractions)
1. `Usuario` - 59 edges
2. `RolUsuario` - 53 edges
3. `OrdenServicio` - 37 edges
4. `Base` - 27 edges
5. `ReglaNegocioError` - 26 edges
6. `Cotizacion` - 20 edges
7. `abrir_orden()` - 19 edges
8. `NoEncontradoError` - 18 edges
9. `solicitar_codigo()` - 18 edges
10. `confirmar_codigo()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `listar_usuarios()` --uses--> `RolUsuario`  [INFERRED]
  backend/app/rutas/personal.py → backend/app/models.py
- `Sesion` --uses--> `RolUsuario`  [INFERRED]
  backend/app/schemas.py → backend/app/models.py
- `UsuarioNuevo` --uses--> `RolUsuario`  [INFERRED]
  backend/app/schemas.py → backend/app/models.py
- `UsuarioSalida` --uses--> `RolUsuario`  [INFERRED]
  backend/app/schemas.py → backend/app/models.py
- `requiere_rol()` --uses--> `RolUsuario`  [INFERRED]
  backend/app/seguridad.py → backend/app/models.py

## Import Cycles
- None detected.

## Communities (13 total, 1 thin omitted)

### Community 0 - "conftest.py"
Cohesion: 0.06
Nodes (39): Base, crear_motor(), get_db(), Bahia, Cita, Cliente, ClienteParticular, EstadoCita (+31 more)

### Community 1 - "RolUsuario"
Cohesion: 0.08
Nodes (42): Autorizacion, RolUsuario, huella(), verificar_huella(), codigo_cliente(), enlace_cliente(), Flujo, test_cpa28_cada_rol_solo_hace_lo_suyo() (+34 more)

### Community 2 - "Acuerdos de trabajo · Equipo B"
Cohesion: 0.18
Nodes (10): Acuerdos de trabajo · Equipo B, Commits, Comunicación, Código, Datos personales, Decisiones, Documentos, Incumplimiento (+2 more)

### Community 3 - "Usuario"
Cohesion: 0.12
Nodes (35): OrdenServicio, Pago, Usuario, detalle_orden(), resumen_orden(), abrir_orden(), actualizar_checklist(), asignar() (+27 more)

### Community 4 - "models.py"
Cohesion: 0.09
Nodes (25): Canal, Cotizacion, DetalleCotizacion, EstadoAutorizacion, EstadoBahia, EstadoCotizacion, EstadoOrden, Garantia (+17 more)

### Community 5 - "with"
Cohesion: 0.05
Nodes (42): run, name, runs-on, steps, PGPASSWORD, POSTGRES_DB, POSTGRES_PASSWORD, name (+34 more)

### Community 6 - "portal.py"
Cohesion: 0.10
Nodes (18): NoEncontradoError, ReglaNegocioError, ciclo_de_vida(), no_encontrado(), regla_violada(), salud(), TokenAcceso, acceso() (+10 more)

### Community 7 - "schemas.py"
Cohesion: 0.10
Nodes (34): NivelCombustible, Asignacion, AutorizacionSalida, BahiaSalida, Checklist, CitaSalida, ClienteNuevo, CodigoPresencial (+26 more)

### Community 8 - "ordenes.py"
Cohesion: 0.12
Nodes (19): AsignacionColaborador, ChecklistInspeccion, Diagnostico, Fotografia, HistorialEstado, RecepcionVehicular, ahora(), hoy() (+11 more)

### Community 9 - "seguridad.py"
Cohesion: 0.12
Nodes (11): _b64(), crear_sesion(), _firma(), hash_secreto(), leer_sesion(), nuevo_codigo_2fa(), nuevo_token_cliente(), requiere_rol() (+3 more)

### Community 10 - "notificaciones.py"
Cohesion: 0.38
Nodes (3): enviar(), Mensaje, ultimo_mensaje()

### Community 17 - "Sistema de Órdenes de Servicio y Citas"
Cohesion: 0.29
Nodes (6): Base de datos (PostgreSQL), Compilar el documento, Contenido del repositorio, Ejecutar el backend, Equipo, Sistema de Órdenes de Servicio y Citas

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `RolUsuario` connect `RolUsuario` to `conftest.py`, `Usuario`, `models.py`, `schemas.py`, `ordenes.py`, `seguridad.py`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Are the 47 inferred relationships involving `Usuario` (e.g. with `agenda()` and `agregar_vehiculo()`) actually correct?**
  _`Usuario` has 47 INFERRED edges - model-reasoned connections that need verification._
- **Should `conftest.py` be split into smaller, more focused modules?**
  _Cohesion score 0.059018367961457395 - nodes in this community are weakly interconnected._
- **Why does `Usuario` connect `Usuario` to `conftest.py`, `seguridad.py`, `models.py`, `ordenes.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `RolUsuario` (e.g. with `listar_usuarios()` and `Sesion`) actually correct?**
  _`RolUsuario` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Should `RolUsuario` be split into smaller, more focused modules?**
  _Cohesion score 0.08391608391608392 - nodes in this community are weakly interconnected._
- **Why does `ReglaNegocioError` connect `portal.py` to `conftest.py`, `ordenes.py`, `Usuario`, `models.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._