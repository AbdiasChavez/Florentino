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
- Cada integrante trabaja en `rama/<NOMBRE>` (por ejemplo, `rama/DULCE`).
- Todo Pull Request necesita **al menos una revisión de otro integrante** antes de integrarse.
- Antes de abrir un PR, revisa que no haya datos personales reales, contraseñas ni llaves.

## Commits

- En español y en presente: «Agrega…», «Corrige…», «Redacta…».
- Con referencia a la historia o al issue cuando aplique: `Agrega checklist de recepción (HU-01)`.

## Documentos

- Los entregables van en `docs/entregas/` con el nombre `IS1-Fase1-EquipoB-v<versión>.docx` y `.pdf`.
- Los diagramas se guardan con su archivo fuente (PlantUML, draw.io o Mermaid) junto a la imagen.
- El `.docx` es binario y git no puede fusionarlo: **solo una persona integra los cambios en cada entrega**.
  Los demás entregan su sección en un archivo aparte (o en Markdown en `docs/`) para que esa persona la integre.

## Datos personales

Solo datos ficticios en desarrollo, pruebas y demostraciones (LFPDPPP). Nunca se suben correos, teléfonos
ni datos reales de clientes o del equipo al repositorio.

## Incumplimiento

Se registra en la retrospectiva. A la segunda falta en el mismo sprint, el Scrum Master lo informa al profesor.
