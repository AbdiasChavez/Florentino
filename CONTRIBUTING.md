# Acuerdos de trabajo · Equipo B

Este archivo resume cómo trabajamos. La sección 2.1 del Documento de Ingeniería lo cita.

## Comunicación

- **Canal del equipo:** _por confirmar_ (para lo urgente).
- **GitHub** (issues y Pull Requests) para todo lo técnico: requisitos, código, documentos y revisiones.
- **Tiempo máximo de respuesta:** 24 horas en días hábiles.

## Reuniones

- **Daily:** breve, de lunes a viernes, presencial o por mensaje (qué hice, qué haré, qué me bloquea).
- **Eventos de Scrum:** Planning al inicio de cada sprint de dos semanas; Review y Retrospectiva al cierre.

## Decisiones

Se toman por consenso. Si no se logra:

- el **Product Owner** decide sobre alcance y prioridad del backlog;
- el **Scrum Master** decide sobre el proceso.

## Ramas y Pull Requests

- `main` está protegida: solo se integra mediante Pull Request.
- Hay una rama por rol de Scrum: `rol/product-owner`, `rol/scrum-master`, `rol/qa-lead` y `rol/developers`.
  Cada rol trabaja en la suya y la integra a `main` con un merge sin fast-forward (`git merge --no-ff`),
  para que quede visible qué integró cada rol.
- Todo Pull Request necesita **al menos una revisión de otro integrante** y la CI en verde antes de integrarse.
- Antes de abrir un PR, revisa que no haya datos personales reales, contraseñas ni llaves.

## Commits

- Formato **`Rol: mensaje`**, en español y en presente:
  `Developers: implementa recepción con checklist (HU-01)`, `QA Lead: agrega pruebas de cotización (CPA-10)`.
- Roles válidos: `Product Owner`, `Scrum Master`, `QA Lead`, `Developers`.
- Con referencia a la historia, el caso de prueba o la sección del documento cuando aplique.

## Documentos

- El Documento de Ingeniería está en LaTeX en `docs/documento/`, **un archivo por sección** en
  `docs/documento/secciones/`. Cada rol edita sus secciones y git fusiona los cambios. Ya no se usa `.docx`.
- Compila con `pdflatex -interaction=nonstopmode IS1-Fase1-EquipoB.tex` (dos veces) y revisa el `.log`
  si hay errores. El PDF entregable va en `docs/entregas/IS1-Fase1-EquipoB-v<versión>.pdf`.
- Los diagramas se guardan con su archivo fuente (PlantUML, draw.io o Mermaid) junto a la imagen.
- Una figura que todavía no existe se deja con `\figurapendiente{número}{título}{qué debe mostrar}{ruta}`:
  sale en rojo con su descripción hasta que alguien la reemplace por `\figura{...}`.

## Código

- Backend en `backend/`. Las reglas de negocio (RN-xx) van en `app/servicios/`, nunca en las rutas.
- Toda regla o permiso nuevo lleva su prueba en `backend/tests/` con el ID del caso (`test_cpaNN_...`).
- Las credenciales van en `backend/.env`, que no se sube. Usa `backend/.env.example` como plantilla.

## Datos personales

Solo datos ficticios en desarrollo, pruebas y demostraciones (LFPDPPP). Nunca se suben correos, teléfonos
ni datos reales de clientes o del equipo al repositorio.

## Incumplimiento

Se registra en la retrospectiva. A la segunda falta en el mismo sprint, el Scrum Master lo informa al profesor.
