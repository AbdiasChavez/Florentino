<!-- converted from IS1_Fase1_EquipoB_Documento_Ingenieria-v0.1.docx -->

Universidad del Istmo · Campus Ixtepec
Ingeniería en Desarrollo de Software y Sistemas Inteligentes
Ingeniería de Software I (IDSSI-27) · Quinto semestre
Machote: Documento de Ingeniería del Proyecto – Fase 1
Sistema de Órdenes de Servicio y Citas · Servicio Automotriz Hermanos Ruiz, S.A. de C.V.
Equipo:  B (5 integrantes
Cliente: Servicio Automotriz Hermanos Ruiz
Producto: Sistema de Órdenes de Servicio y Citas
Versión del documento: v0.1· Fecha: 22/10/2026

Contenido
0. Cómo usar este machote
Portada
1. Información general del proyecto
2. Gestión del proyecto con Scrum
3. Visión y viabilidad del producto
4. Especificación de requisitos de software (SRS)
5. Plan de pruebas y trazabilidad
6. Modelos de análisis
7. Arquitectura y diseño
8. Diseño de la interfaz de usuario
9. Implementación del Release v0.1.0
10. Reporte final de pruebas e incidencias
11. Paquete de transferencia a la Fase 2
12. Retrospectiva del proyecto y contribución individual
13. Referencias
Anexos
Lista de verificación antes de entregar

# 0. Cómo usar este machote
Este documento es la plantilla del Documento de Ingeniería del Proyecto – Fase 1 que cada equipo entrega al profesor para su evaluación. Reúne en un solo archivo lo que el equipo produce durante los sprints 0 a 6 y que se encuentra en la carpeta docs/ del repositorio.
## 0.1 Reglas de uso
Conserven la numeración y el orden de las secciones. Si una sección no aplica, déjenla con la leyenda "No aplica" y una justificación de una línea.
Los recuadros grises marcados como "Instrucción" explican qué debe contener cada sección. Bórrenlos antes de entregar.
El texto gris entre corchetes, como [Escriba aquí…], es un marcador: reemplácenlo por contenido propio.
Las filas de ejemplo en las tablas solo muestran el formato; sustitúyanlas por los datos de su proyecto.
Los diagramas se insertan como imágenes legibles y su archivo fuente (draw.io, PlantUML o Mermaid) queda en el repositorio. Cada diagrama lleva número, título y ruta de su fuente: Figura 4.2. Máquina de estados de Pedido. Fuente: docs/04-analisis/estados/pedido.puml.
Cuando el contenido sea muy extenso (por ejemplo, las 35 historias de usuario o los 25 casos de prueba), el documento incluye la tabla resumen y el detalle completo puede quedar en un anexo o en el repositorio, con su enlace.
## 0.2 Entrega acumulativa
El documento crece sprint a sprint. En cada Sprint Review se entrega la versión vigente con las secciones correspondientes completas; el profesor evalúa solo las secciones del corte, pero puede pedir corregir las anteriores.
| Corte | Versión del documento | Secciones que deben estar completas | Evaluación en la que cuenta |
| --- | --- | --- | --- |
| Review 0 (sem. 5) | v0.1 | Portada, 1, 2.1– 2.4, 3 | Parcial 1 |
| Review 1 (sem. 7) | v0.2 | + 4.1– 4.5 (borrador), 4.6, 4.7 | Parcial 1 |
| Review 2 (sem. 9) | v1.0 (SRS firmado) | + 4 completa, 5.1–5.3, 2.5 | Parcial 2 |
| Review 3 (sem. 11) | v1.1 | + 6 | Parcial 3 |
| Review 4 (sem. 13) | v1.2 | + 7.1–7.5, 9.1–9.3 | Parcial 3 |
| Review 5 (sem. 15) | v1.3 | + 7.6–7.8, 8, 9.4 | Ordinaria |
| Demo final (sem. 16) | v2.0 (final de la Fase 1) | Todo el documento, incluidas 10, 11, 12, 13 y anexos | Ordinaria |

## 0.3 Formato de entrega
Archivos: este documento en Word (.docx) y en PDF, en docs/entregas/ del repositorio, y la liga del PDF en la minuta de la Review.
Nombre del archivo: IS1-Fase1-Equipo<A|B>-v<versión>.pdf, por ejemplo IS1-Fase1-EquipoA-v1.0.pdf.
Formato: carta, márgenes de 2.5 cm, fuente de 11 puntos, encabezados numerados, numeración de páginas, figuras y tablas numeradas.
Citas y referencias: formato APA 7. Toda norma, libro o dato de terceros se cita; las referencias deben ser verificables.
Uso de IA: se declara en la sección 2.6. Cualquier integrante debe poder explicar cualquier parte del documento.
Si la versión del documento no coincide con lo que hay en el repositorio y en el tablero, el profesor toma como válido el repositorio.

# Portada
| Campo | Dato |
| --- | --- |
| Asignatura | Ingeniería de Software I (IDSSI-27) |
| Documento | Documento de Ingeniería del Proyecto – Fase 1 |
| Equipo | B (5 integrantes) |
| Cliente | Servicio Automotriz Hermanos Ruiz |
| Nombre del producto | Sistema de Órdenes de Servicio y Citas |
| Versión del documento | v0.1 |
| Fecha | 22/10/2026 |
| Repositorio | https://github.com/AyagDan/SistemaDeServiciosYCitas |

## Control de versiones
| Versión | Fecha | Autor(es) | Descripción del cambio | Revisó |
| --- | --- | --- | --- | --- |
| v0.1 | 22/10/2026 | Isis Yamilet Meléndez Hernández | Integración del avance al machote oficial del profesor. | Ángel Yael Avendaño Guzmán |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## Aprobación del cliente
No aplica
Esta sección no aplica para la versión v0.1 (Parcial 1) debido a que los hitos de firma formal del SRS y del Release v0.1.0 se evalúan y registran en la Review 2 y en la Demo Final, respectivamente.

| Hito | Resultado (aceptado / aceptado con observaciones / rechazado) | Observaciones | Firma del cliente | Fecha |
| --- | --- | --- | --- | --- |
| SRS v1.0 (Review 2) |  |  |  |  |
| Release v0.1.0 (Demo final) |  |  |  |  |


# 1. Información general del proyecto
## 1.1 Integrantes y roles
| Nombre completo | Matrícula | Usuario GitHub | Rol(es) y sprints | Áreas principales de contribución |
| --- | --- | --- | --- | --- |
| Abdías Daniel Chávez Cruz | 0224170024 | adcc.wrh@gmail.com | Product Owner (S0–S6) Developer | [Requisitos, relación con el cliente…] |
| Ángel Yael Avendaño Guzmán | 0224170023 |  | Scrum master Developer |  |
| Dulce María Estudillo Rosado | 022470028 | rosadomar.qx@gmail.com | Product manager |  |
| Isis Alhelí González Maldonado |  | alhelig24@gmail.com |  |  |
| Isis Yamilet Meléndez Hernández | 0224170037 | isisyamiletmelendezher@gmail.com |  |  |

## 1.2 Enlaces del proyecto
| Recurso | Enlace |
| --- | --- |
| Repositorio | [URL] |
| Tablero (GitHub Projects / Jira) | [URL] |
| Prototipo de UI (Figma / Penpot) | [URL] |
| Ambiente de pruebas (staging) | [URL] (desde el Sprint 4) |
| Release v0.1.0 | [URL de GitHub Releases] |
| Canal de comunicación del equipo | [Nombre del canal] |

## 1.3 Resumen ejecutivo
Instrucción: Máximo media página, escrita para el cliente y sin jerga técnica: qué problema se resuelve, qué se entregó en la Fase 1, qué queda para la Fase 2 y cuál es el estado del producto. Esta sección se reescribe en cada versión.
[Escriba aquí el resumen ejecutivo.]

# 2. Gestión del proyecto con Scrum
## 2.1 Acuerdos de trabajo
Instrucción: Resumen de CONTRIBUTING.md: horarios y canal de comunicación, tiempo máximo de respuesta, cómo se toman las decisiones, convenciones de ramas y commits, y consecuencias por incumplimiento.
[Escriba aquí los acuerdos de trabajo.]
## 2.2 Definición de Listo (DoR) y Definición de Terminado (DoD)
Instrucción: Partan de la versión base del documento "Cronograma y entregables por sprint". Pueden hacerla más exigente, nunca más laxa. Registren los cambios por sprint.
| Definición de Listo | Definición de Terminado |
| --- | --- |
| ~ [Criterios] | ~ [Criterios] |

## 2.3 Resumen de sprints
Instrucción: Un renglón por sprint terminado. La velocidad es los puntos de historia terminados según la DoD, no los iniciados. Agreguen al final la gráfica de velocidad y, si la usan, la de quemado (burndown).
| Sprint | Fechas | Objetivo del sprint | ¿Se cumplió? (sí / parcial / no) | Puntos comprometidos | Puntos terminados |
| --- | --- | --- | --- | --- | --- |
| S0 |  |  |  | — | — |
| S1 |  |  |  |  |  |
| S2 |  |  |  |  |  |
| S3 |  |  |  |  |  |
| S4 |  |  |  |  |  |
| S5 |  |  |  |  |  |
| S6 |  |  |  |  |  |

### Evidencia de los eventos
Instrucción: Por sprint, la ruta a la minuta de la Review, a la retrospectiva y a los registros del Daily en el repositorio. Para cada retrospectiva, anoten las acciones de mejora y si se aplicaron en el siguiente sprint.
| Sprint | Minuta de Review | Retrospectiva | Acciones de mejora acordadas | ¿Se aplicaron? |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## 2.4 Registro de riesgos
Instrucción: Mínimo 8 riesgos desde el Sprint 0, actualizados en cada sprint. Probabilidad e impacto: alta / media / baja. Respuesta: evitar, mitigar, transferir o aceptar.
| ID | Riesgo | Probabilidad | Impacto | Respuesta y responsable | Estado |
| --- | --- | --- | --- | --- | --- |
| R-01 | Un integrante abandona el curso a mitad del semestre | Media | Alto | Mitigar: conocimiento compartido mediante revisión cruzada de PR; responsable: SM | Abierto |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 2.5 Solicitudes de cambio
Instrucción: Registren todas las solicitudes de cambio del cliente, ya sea que se acepten o no. Lo que se evalúa es el análisis de impacto y la negociación, no aceptar todo.
| ID / issue | Fecha | Solicitud del cliente | Impacto (requisitos, modelos, pruebas, esfuerzo) | Decisión y justificación | Release |
| --- | --- | --- | --- | --- | --- |
| SC-01 / #[n] |  |  |  | [Aceptada / rechazada / pospuesta a Fase 2] | [v0.1.0 / Fase 2] |
|  |  |  |  |  |  |

## 2.6 Declaración de uso de inteligencia artificial
Instrucción: Indiquen qué herramientas usaron, para qué partes y cómo verificaron el resultado. También se declara no usar IA. Nunca se ingresan datos personales reales.
| Herramienta | Sección o artefacto | Para qué se usó | Cómo se verificó | Responsable |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |


# 3. Visión y viabilidad del producto
## 3.1 Problema y contexto del cliente
Instrucción: Describan el negocio y el problema con las palabras del cliente, apoyándose en las entrevistas (citen la minuta). No copien el anteproyecto: deben aparecer hallazgos que solo se obtuvieron mediante preguntas.
[Escriba aquí el problema y su contexto.]
## 3.2 Objetivos del producto e indicadores
| Objetivo | Indicador | Situación actual | Meta | Cómo se medirá |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## 3.3 Alcance
| Dentro del alcance de la Fase 1 | Dentro del alcance de la Fase 2 | Fuera de alcance |
| --- | --- | --- |
| ~ [Lista] | ~ [Lista] | ~ [Lista] |

## 3.4 Stakeholders
| Stakeholder | Rol en el negocio | Interés en el sistema | Poder / interés | Estrategia de participación |
| --- | --- | --- | --- | --- |
| Dueños del taller | Propietarios; deciden la inversión y aprueban el proyecto. | Reducir disputas por cobros, cuidar la rentabilidad y la reputación, y no pagar licencias. | Alto poder – alto interés | Gestionar de cerca mediante entrevistas y revisiones de avance en cada entrega, validación de requisitos y aprobación formal del alcance. |
| Gerente | Supervisa la operación y autoriza entregas a crédito a flotillas. | Consultar tableros de control, controlar saldos y autorizar créditos con respaldo. | Alto poder – alto interés | Gestionar de cerca mediante sesiones de definición de reglas de crédito y de reportes, y pruebas de aceptación de su flujo. |
| Recepcionista | Registra ingresos, confirma citas y atiende a clientes. | Reducir llamadas de seguimiento y tener el registro de recepción y fotografías en un solo lugar. | Bajo poder – alto interés | Mantener informada e involucrada, participando en las pruebas de usabilidad, capacitación y retroalimentación continua. |
| Jefe de mecánicos | Centraliza diagnóstico, cotización y asignación de bahías en la tableta. | Flujos cortos, botones grandes y operación sin conexión. | Alto poder – alto interés | Gestionar de cerca los prototipos en el entrono real (tableta, pruebas con manos sucias) y ajustes por iteración. |
| Mecánicos de bahía y de apoyo | Realizan reparaciones, inspecciones y cubrimientos de turnos. | Recibir órdenes claras y enfocarse en el trabajo físico | Bajo poder – alto interés | Mantener informado con capacitaciones breves y un canal para reportar dificultades. |
| Encargado de almacén | Controla requisiciones, proveedores, costos e inventario de consumibles. | Directorio de proveedores, registro de costos y fechas, y tickets de compra por orden | Bajo poder – alto interés | Mantener informado e involucrado mediante entrevistas sobre su flujo de compras y pruebas del módulo M6. |
| Clientes particulares | Dueños de autos, motocicletas y vehículos. | Ver el estado de su vehículo, autorizar presupuestos y recibir un cobro transparente | Bajo poder – alto interés | Mantener informado con las pruebas de usabilidad con algunos clientes y alguna encuesta breve de satisfacción al finalizar el servicio. |
| Clientes de flotillas empresariales | Empresas con vehículos que pueden recibir entrega a crédito. | Condiciones de crédito claras y seguimiento de varios vehículos | Poder medio – interés medio | Mantener satisfechos al definir con el gerente las reglas del crédito y validar el flujo con un representante. |
| Equipo de desarrollo | Diseñan, construyen y prueban la plataforma. | Entregar un sistema que cumpla los requisitos y la norma ISO/IEC 25010 | Alto poder – alto interés | Gestionar de cerca con reuniones periódicas, control de versiones y revisiones internas de calidad. |
| Docente evaluador | Revisa el documento y el producto en curso. | Que el proyecto cumpla los criterios y entregas del curso | Alto poder – alto interés | Mantener satisfecho entregando a tiempo, pidiendo asesoría en los avances y pidiendo aclaraciones de dudas. |

## 3.5 Proceso actual (as-is)


Figura 1. Diagrama de actividades del proceso actual de atención del taller, con los problemas identificados en cada etapa. Elaboración propia.

El diagrama de actividades muestra el proceso actual de atención del taller antes de implementar la solución tecnológica. Se organiza en cuatro carriles (cliente, recepcionista, mecánico y registro manual) y recorre el flujo completo: solicitud de cita, recepción del vehículo, diagnóstico, cotización, autorización, reparación, entrega y archivo del historial. Los recuadros rojos señalan los problemas detectados en cada etapa, como el riesgo de errores en el registro de citas, los datos incompletos en las órdenes en papel, la información dispersa e ilegible, las demoras en la cotización manual, el exceso de llamadas y un historial difícil de consultar.
## 3.6 Estudio de viabilidad
Instrucción: Cada tipo de viabilidad con evidencia y una conclusión. La legal debe considerar la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (DOF 20-03-2025): qué datos personales se tratarán, para qué finalidades y con qué medidas de seguridad.
| Tipo | Análisis y evidencia | Conclusión (viable / viable con condiciones / no viable) |
| --- | --- | --- |
| Técnica |  |  |
| Económica |  |  |
| Operativa |  |  |
| Legal |  |  |
| De calendario |  |  |

Conclusión general: [Escriba aquí si el proyecto es viable y bajo qué condiciones.]

# 4. Especificación de requisitos de software (SRS)
Instrucción: Estructura adaptada de ISO/IEC/IEEE 29148:2018. El SRS es lo que el cliente firma en la Review 2. Cada requisito tiene un identificador único que se utiliza para la trazabilidad.
## 4.1 Propósito, alcance y audiencia del SRS
[Escriba aquí.]
## 4.2 Glosario del dominio
Instrucción: Mínimo 25 términos (Equipo A) o 20 términos (Equipo B), con los nombres que usa el cliente. Los nombres de las clases del dominio (sección 6) deben salir de aquí.
| Término | Definición | Sinónimos que usa el cliente |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |

## 4.3 Descripción general
### 4.3.1 Usuarios y sus características
El sistema será utilizado por distintos perfiles dentro de la estructura operativa del negocio y la parte gerencial del taller mecánico, además de los clientes finales del negocio. La siguiente tabla detalla las características, nivel técnico y contexto de uso:
| Tipo de usuario | Tareas principales | Experiencia tecnológica | Dispositivo y contexto de uso |
| --- | --- | --- | --- |
| Recepcionista | Registro de clientes/vehículos, check-in con fotos, apertura de órdenes, confirmación de citas web, cobranza y entrega. | Media: Manejo fluido de navegación web, correo electrónico y paquetes de oficina. | Computadora de escritorio en mostrador de recepción. Entorno de oficina con teclado/mouse. |
| Jefe de Mecánicos (Líder Técnico) | Diagnóstico técnico, elaboración de cotizaciones, asignación de bahías/mecánicos, requisición de refacciones y sellado final. | Baja–Media: Familiarizado con smartphones personales; poca experiencia con sistemas de gestión. | Tabletas táctiles exclusivas de taller (1 o 2 dispositivos). Entorno con ruido, polvo y manipulación con manos sucias/grasosas. |
| Mecánico en Bahía | Ejecución de reparaciones físicas, notificación de hallazgos adicionales o solicitud de refacciones al Jefe de Mecánicos. | Baja: Uso de teléfonos inteligentes para uso personal cotidiano. | Sin dispositivo asignado directo; interactúa a través del Jefe de Mecánicos para evitar deterioro de hardware |
| Encargado de Almacén | Atender solicitudes de piezas, consultar directorio de proveedores locales, registrar compras/tickets e historial de insumos. | Baja–Media: Uso básico de computadora para consulta de inventarios. | Computadora de escritorio o terminal dedicada en el área de almacén/refacciones. |
| Gerente (Dueño) | Monitoreo del Dashboard de KPIs (ocupación, ingresos), aprobación de entregas a crédito a flotillas y excepciones. | Media: Manejo de smartphones y computadoras para administración del negocio. | Laptop personal o dispositivo móvil (smartphone/tableta) con acceso remoto/local |
| Cliente | Solicitud de citas en línea, seguimiento en vivo del servicio y aprobación/rechazo de cotizaciones mediante código 2FA. | Variable (Baja a Alta): Desde usuarios sin conocimientos técnicos hasta usuarios avanzados. | Dispositivo móvil personal (iOS/Android) vía navegador web progresivo (PWA) sin instalar aplicaciones. |

### 4.3.2 Restricciones, supuestos y dependencias
- Restricciones:
- Presupuesto y Licenciamiento: El desarrollo debe realizarse estrictamente con herramientas, lenguajes y frameworks de código abierto (Open Source como Python y FastAPI), garantizando cero costos de licencias o rentas de software.
- Infraestructura Física: El taller cuenta únicamente con 4 bahías de trabajo físicas (capacidad estricta de 1 vehículo por bahía) y un estacionamiento con capacidad máxima de 5 vehículos en espera.
- Dispositivos Hardware: La captura digital en taller se limita a máximo 2 tabletas táctiles centralizadas por el Jefe de Mecánicos para proteger la inversión y evitar daños.
- Alcance del Vehículo: La plataforma atenderá exclusivamente vehículos ligeros (automóviles particulares, motocicletas y camionetas), excluyendo maquinaria pesada o industrial.
- Supuestos:
- Se asume que el taller mantiene activa una conexión de red local (Wi-Fi) para la sincronización entre computadoras de mostrador y tabletas de taller en condiciones normales.
- Se asume que los clientes cuentan con un número telefónico celular o correo electrónico capaz de recibir enlaces web y códigos de verificación de 6 dígitos (2FA).
- Se asume que los datos ingresados durante la fase de desarrollo y pruebas son 100% ficticios para dar cumplimiento a la Ley Federal de Protección de Datos Personales.
- Dependencias:
- Infraestructura Eléctrica y Red: Operación dependiente de baterías en laptops/tabletas y arquitectura Local-First / PWA (Service Workers e IndexedDB) para permitir la captura de datos offline durante cortes de luz o fallas de internet.
- Proveedores Externos de Comunicación: Dependencia del servicio de envío de correos/mensajes para la entrega puntual de tokens de acceso y códigos 2FA al cliente.
- Disponibilidad de Refaccionarias Locales: La adquisición de piezas fuera de stock depende del directorio de proveedores locales e historial de compras del almacén.

## 4.4 Requisitos funcionales
| ID | Requisito funcional | Módulo | Prioridad (MoSCoW) | Historias relacionadas |
| --- | --- | --- | --- | --- |
| RF-01 | El sistema deberá permitir autenticar mediante credenciales seguras al personal del taller según su rol (Gerente, Recepcionista, Mecánico y Encargado de Almacén). | M1 – Autenticación y Seguridad | Must | HU-01, HU-02 |
| RF-02.1 | El sistema deberá permitir al cliente consultar el estado de su vehículo y autorizar cotizaciones mediante un enlace web seguro enviado por correo o mensaje, sin instalar aplicaciones. | M1 – Autenticación y Seguridad | Must |  |
| RF-02.2 | El sistema deberá de expirar el enlace del cliente de manera automática una vez que el vehículo sea entregado y saldado. | M1 – Autenticación y Seguridad | Should |  |
| RF-02.3 | El sistema deberá de permitir enviar el enlace del cliente también por mensaje. | M1 – Autenticación y Seguridad | Could |  |
| RF-03.1 | El sistema deberá registrar, buscar y actualizar la información de clientes y vehículos (placas, marca, modelo, año y VIN (opcional)). | M3 – Recepción E Historial Inicial | Must |  |
| RF-03.2 | El sistema deberá mantener el historial de servicios de cada vehículo, con fotografías de recepción, diagnósticos técnicos y garantías aplicables (30 días en mano de obra). | M7 – Portal del Cliente, Cobro y Gerencia | Should |  |
| RF-04 | El sistema deberá registrar en la recepción el kilometraje, el nivel de combustible y un checklist de carrocería, y exigir fotografías digitales del estado inicial de la unidad. | M3 – Recepción E Historial Inicial | Must |  |
| RF-05 | El sistema deberá permitir abrir órdenes de servicio asociadas a una de las 4 bahías y a un mecánico responsable, controlando los estados operativos del taller. | M5 – Taller, Bahías y Expediente Técnico | Must |  |
| RF-06 | El sistema deberá generar cotizaciones desglosadas (mano de obra y refacciones/insumos) con vigencia de 5 días naturales y requerir firma digital validada con un código enviado al correo del cliente, de forma remota o presencial. | M4 Cotización y Contratos 2FA | Must |  |
| RF-07 | El sistema deberá bloquear el avance del trabajo y exigir una nueva autorización con verificación cuando los trabajos adicionales incrementen el monto inicial en más de 10 %. | M4 Cotización y Contratos 2FA | Must |  |
| RF-08.1 | El sistema deberá permitir al mecánico solicitar piezas vinculadas a una orden de servicio. | M6 – Almacén y Refacciones | Should |  |
| RF-08.2 | El sistema deberá permitir al encargado de almacén mantener un directorio de proveedores locales (teléfonos o correos) y registrar costos y fechas de llegada de las piezas. | M6 – Almacén y Refacciones | Should |  |
| RF-08.3 | El sistema deberá de emitir un ticket e historial de compras asociado a cada orden de servicio. | M6 – Almacén y Refacciones | Could |  |
| RF-09 | El sistema deberá ofrecer una agenda digital por día y bahía, donde las citas solicitadas en línea quedan “Pendientes” hasta que la recepcionista verifique disponibilidad y las confirme manualmente | M2 – Citas y Solicitudes | Should |  |
| RF-10 | El sistema deberá impedir la entrega física del vehículo con saldo pendiente, a menos que el gerente autorice la entrega a crédito para vehículos de flotillas empresariales previamente registradas. | M7 – Portal del Cliente, Cobro y Gerencia | Must |  |

## 4.5 Historias de usuario (Product Backlog)
| ID / issue | Historia (Como… quiero… para…) | Prioridad | Puntos | Release | Estado |
| --- | --- | --- | --- | --- | --- |
| HU-01 / #[1] | Como recepcionista del taller, quiero registrar la recepción del vehículo adjuntando kilometraje, nivel de combustible, checklist de carrocería y fotografías del estado inicial, para contar con un respaldo digital inalterable que evite reclamos infundados por daños o faltantes al entregar la unidad. | Must | 3 | v0.1.0 | Terminada |
| HU-02 / #[2] | Como cliente del taller, quiero recibir un enlace web seguro con la cotización detallada (mano de obra y refacciones) y botones claros de aprobación o rechazo, para revisar y autorizar los trabajos desde mi teléfono sin necesidad de realizar llamadas ni acudir físicamente al taller | Must | 3 | v0.1.0 | Terminada |
| HU-03 / #[3] | Como cliente del taller, quiero solicitar una cita en línea seleccionando el día y la hora disponible, para apartar un espacio sin necesidad de realizar llamadas telefónicas. | Must | 3 | v0.1.0 | Pendiente |
| HU-04 / #[4] | Como recepcionista del taller, quiero consultar la agenda digital por día y por bahía, para verificar las solicitudes pendientes de los clientes y realizar su confirmación manual. | Must | 3 | v0.1.0 | Terminada |
| HU-05 / #[5] | Como recepcionista del taller, quiero buscar a un cliente o vehículo registrado mediante su número telefónico o placas, para agilizar el proceso de recepción en visitas recurrentes. | Should | 2 | Fase 2 | Pendiente |
| HU-06 / #[6] | Como recepcionista del taller, quiero registrar un vehículo con cita previa seleccionando su folio de origen, para que el sistema precargue automáticamente los datos del cliente y del auto. | Should | 2 | v0.1.0 | Terminada |
| HU-07 / #[7] | Como recepcionista del taller, quiero ver la alerta de "Sin Bahías Disponibles" cuando las 4 bahías físicas estén ocupadas, para ubicar temporalmente el vehículo en el estacionamiento de recepción. | Must | 3 | v0.1.0 | Terminada |
| HU-08 / #[8] | Como jefe de mecánicos, quiero asignar la orden de servicio a una de las 4 bahías físicas disponibles y a un mecánico responsable, para iniciar formalmente los trabajos en el taller. | Must | 5 | v0.1.0 | Terminada |
| HU-09 / #[9] | Como jefe de mecánicos, quiero registrar el diagnóstico técnico y las observaciones iniciales en la tableta, para cambiar el estado de la orden a "En Diagnóstico". | Must | 3 | v0.1.0 | Terminada |
| HU-10 / #[10] | Como mecánico del taller, quiero registrar las refacciones e insumos requeridos detectados durante la revisión, para que el área de almacén gestione su cotización o pedido. | Should | 3 | v0.1.0 | Pendiente |
| HU-11 / #[11] | Como jefe de mecánicos, quiero visualizar el estatus actual de las 4 bahías de trabajo en una interfaz simplificada para tabletas, para conocer rápidamente qué unidades están listas o en proceso. | Should | 3 | Fase 2 | Pendiente |
| HU-12 / #[12] | Como recepcionista o jefe de mecánicos, quiero generar un presupuesto desglosado de mano de obra y refacciones con vigencia de 5 días naturales, para enviarlo de forma transparente al cliente. | Must | 5 | v0.1.0 | Terminada |
| HU-13 / #[13] | Como cliente del taller, quiero seleccionar o deseleccionar servicios opcionales dentro de mi cotización antes de aprobarla, para adaptar el presupuesto a mis necesidades financieras. | Should | 3 | v0.1.0 | Pendiente |
| HU-14 / #[14] | Como cliente del taller, quiero realizar la firma digital de aprobación mediante un código de verificación de 2 pasos enviado a mi correo, para autorizar los trabajos de forma segura ya sea de forma presencial o remota. | Must | 5 | v0.1.0 | Terminada |
| HU-15 / #[15] | Como cliente del taller, quiero presionar un botón de rechazo en la cotización digital, para cancelar la orden y coordinar la recolección del vehículo sin autorizar reparaciones. | Should | 2 | v0.1.0 | Pendiente |
| HU-16 / #[16] | Como sistema, quiero bloquear el avance del taller y exigir una nueva cotización validada por 2FA si los costos imprevistos superan el 10% del presupuesto inicial, para cumplir con las reglas de negocio de sobrecostos. | Must | 5 | v0.1.0 | Pendiente |
| HU-17 / #[17] | Como encargado de almacén, quiero consultar y administrar un directorio de proveedores locales con teléfonos y correos electrónicos, para solicitar refacciones especiales rápidamente. | Should | 3 | v0.1.0 | Pendiente |
| HU-18 / #[18] | Como encargado de almacén, quiero registrar los costos, fechas de llegada y tickets de compra de las refacciones asociadas a una orden, para mantener un control financiero estricto. | Should | 3 | v0.1.0 | Pendiente |
| HU-19 / #[19] | Como mecánico del taller, quiero verificar el stock de refacciones comunes en el inventario interno, para saber si se dispone de la pieza de forma inmediata. | Could | 2 | Fase 2 | Pendiente |
| HU-20 / #[20] | Como recepcionista, quiero recibir una notificación automática cuando los trabajos del vehículo finalicen, para avisar al cliente que su unidad está lista para entrega. | Should | 2 | v0.1.0 | Pendiente |
| HU-21 / #[21] | Como sistema, quiero impedir la entrega física del vehículo si la orden cuenta con saldo pendiente, para evitar pérdidas financieras al taller. | Must | 3 | V0.1.0 | Pendiente |
| HU-22 / #[22] | Como gerente del taller, quiero autorizar de forma excepcional la entrega a crédito únicamente para vehículos de flotillas empresariales registradas, para cumplir con los convenios comerciales. | Should | 3 | V0.1.0 | Pendiente |
| HU-23 / #[23] | Como recepcionista, quiero registrar el pago total del servicio y cerrar formalmente la orden, para liberar la bahía de trabajo y archivar el historial del vehículo. | Must | 3 | V0.1.0 | Pendiente |
| HU-24 / #[24] | Como cliente, quiero consultar la vigencia de la garantía de 30 días en mano de obra asociada a mi servicio anterior, para reclamar ajustes en caso de incidencias. | Could | 2 | Fase 2 | Pendiente |
| HU-25/ #[25] | Como recepcionista o jefe de mecánicos, quiero registrar la llegada de autos, tomar fotografías y hacer diagnósticos sin conexión a internet usando la batería del equipo, para que la operación no se detenga ante fallas eléctricas. | Must | 8 | V0.1.0 | Pendiente |
| HU-26 / #[26] | Como sistema, quiero sincronizar automáticamente en la nube todos los registros y archivos multimedia guardados localmente en modo offline una vez que se restablezca la red, para evitar pérdida de datos. | Must | 8 | V0.1.0 | Pendiente |
| HU-27 / #[27] | Como administrador del sistema, quiero gestionar roles y permisos seguros (Gerente, Recepcionista, Mecánico y Encargado de Almacén), para proteger la información confidencial del taller. | Must | 3 | V0.1.0 | Terminada |
| HU-28 / #[28] | Como cliente, quiero visualizar la plataforma web desde mi teléfono celular de forma responsiva y sin instalar aplicaciones adicionales, para consultar mi estatus con facilidad. | Must | 5 | v0.1.0 | Terminada |
| HU-29 / #[29] | Como gerente, quiero generar reportes mensuales de ingresos, servicios realizados y tiempos de ocupación de las 4 bahías, para evaluar el rendimiento general del taller. | Could | 5 | Fase 2 | Pendiente |
| HU-30 / #[30] | Como administrador del sistema, quiero asegurar que el manejo de datos personales cumpla con la Ley Federal de Protección de Datos Personales (LFPDPPP) utilizando exclusivamente datos ficticios en las pruebas, para cumplir con el marco legal vigente. | Must | 3 | v0.1.0 | Terminada |


Detalle de una historia (repetir por cada historia del flujo núcleo)
HU-01: Recepción e Inspección con Evidencia Fotográfica
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-01 / #[1] |
| Historia | Como recepcionista del taller, quiero registrar la recepción del vehículo adjuntando kilometraje, nivel de combustible, checklist de carrocería y fotografías del estado inicial, para contar con un respaldo digital inalterable que evite reclamos infundados por daños o faltantes al entregar la unidad. |
| Criterio de aceptación 1 | Dado que la recepcionista se encuentra en el módulo de recepción vehicular, cuando intenta registrar una unidad nueva, entonces el sistema exige obligatoriamente adjuntar al menos 4 fotografías (frente, parte trasera, costado izquierdo y costado derecho). |
| Criterio de aceptación 2 | Dado que se capturan las evidencias, cuando se finaliza el formulario de inspección, entonces el sistema genera una firma visual o sello digital con fecha y hora exacta de recepción, bloqueando el avance al estado "En Diagnóstico" si falta completar algún punto del checklist obligatorio. |
| Reglas de negocio | RN-03 (Trazabilidad y Respaldo Fotográfico), RN-04 (Control de Estados de Orden) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-02: Autorización Digital de Cotización por Parte del Cliente
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-02 / #[2] |
| Historia | Como cliente del taller, quiero recibir un enlace web seguro con la cotización detallada (mano de obra y refacciones) y botones claros de aprobación o rechazo, para revisar y autorizar los trabajos desde mi teléfono sin necesidad de realizar llamadas ni acudir físicamente al taller. |
| Criterio de aceptación 1 | Dado que la cotización ha sido generada por el taller, cuando el sistema envía el aviso, entonces el cliente recibe un enlace vía SMS o correo electrónico que no requiere registro previo ni contraseña, operando mediante un token temporal firmado. |
| Criterio de aceptación 2 | Dado que el cliente revisa el desglose en su dispositivo móvil, cuando presiona el botón "Autorizar", entonces el sistema registra de forma inalterable la dirección IP, fecha, hora y el monto final aceptado, cambiando automáticamente el estado de la orden a "Autorizada" y notificando al mecánico responsable. |
| Reglas de negocio | RN-06 (Validación y Doble Factor de Autorización de Presupuestos) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-03: Solicitud de Cita en Línea
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-03 / #[3] |
| Historia | Como cliente del taller, quiero solicitar una cita en línea seleccionando el día y la hora disponible, para apartar un espacio sin necesidad de llamadas. |
| Criterio de aceptación 1 | Dado que el cliente accede al portal web, cuando selecciona fecha, hora y tipo de servicio, entonces el sistema valida que exista disponibilidad en la agenda del taller. |
| Criterio de aceptación 2 | Dado que se envía la solicitud, cuando se registra con éxito, entonces queda en estado "Pendiente" a la espera de la confirmación manual de la recepcionista. |
| Reglas de negocio | RN-09 (Gestión y Agenda de Citas) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-04: Consulta y Confirmación Manual de Citas
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-04 / #[4] |
| Historia | Como recepcionista del taller, quiero consultar la agenda digital por día y por bahía, para verificar las solicitudes pendientes de los clientes y realizar su confirmación manual. |
| Criterio de aceptación 1 | Dado que la recepcionista accede al módulo de agenda, cuando filtra los registros por el día actual, entonces el sistema despliega todas las citas con estatus "Pendiente". |
| Criterio de aceptación 2 | Dado que la recepcionista revisa una cita solicitada, cuando presiona el botón "Confirmar", entonces el estatus cambia a "Confirmada" y se habilita la asignación de la bahía correspondiente. |
| Reglas de negocio | RN-09 (Gestión de Citas en Línea) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-05: Búsqueda Rápida de Clientes y Vehículos
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-05 / #[5] |
| Historia | Como recepcionista del taller, quiero buscar a un cliente o vehículo registrado mediante su número telefónico o placas, para agilizar el proceso de recepción en visitas recurrentes. |
| Criterio de aceptación 1 | Dado que la recepcionista se encuentra en el módulo de búsqueda, cuando ingresa los dígitos de las placas o el teléfono, entonces el sistema filtra instantáneamente la base de datos de clientes recurrentes. |
| Criterio de aceptación 2 | Dado que se localiza el expediente, cuando el usuario lo selecciona, entonces el sistema precarga los datos generales del cliente y del auto para evitar duplicidad de registros. |
| Reglas de negocio | RN-03 (Gestión Integral de Clientes y Vehículos) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-06: Registro de Vehículos con Cita Previa
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-06 / #[6] |
| Historia | Como recepcionista del taller, quiero registrar un vehículo con cita previa seleccionando su folio de origen, para que el sistema precargue automáticamente los datos del cliente y del auto. |
| Criterio de aceptación 1 | Dado que el cliente llega al taller con cita agendada, cuando la recepcionista introduce el número de folio de la cita, entonces el sistema recupera la información asociada. |
| Criterio de aceptación 2 | Dado que los datos están precargados, cuando se procede con el ingreso, entonces el sistema vincula la cita directamente con la nueva orden de servicio abierta. |
| Reglas de negocio | RN-09 (Gestión y Agenda de Citas) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-07: Alerta de Bahías Ocupadas
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-07 / #[7] |
| Historia | Como recepcionista del taller, quiero ver la alerta de "Sin Bahías Disponibles" cuando las 4 bahías físicas estén ocupadas, para ubicar temporalmente el vehículo en el estacionamiento de recepción. |
| Criterio de aceptación 1 | Dado que las 4 bahías físicas del taller registran una orden activa, cuando la recepcionista intenta registrar la entrada de un nuevo vehículo, entonces el sistema emite una advertencia visual en pantalla indicando "Sin Bahías Disponibles". |
| Criterio de aceptación 2 | Dado que se activa la alerta de saturación, cuando el usuario acepta la notificación, entonces el sistema permite guardar el registro temporal asignando la unidad al estacionamiento de espera. |
| Reglas de negocio | RN-05 (Límite Físico de Operación en 4 Bahías) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-08: Asignación de Bahía y Mecánico
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-08 / #[8] |
| Historia | Como jefe de mecánicos, quiero asignar la orden de servicio a una de las 4 bahías físicas disponibles y a un mecánico responsable, para iniciar formalmente los trabajos. |
| Criterio de aceptación 1 | Dado que la orden se encuentra abierta, cuando el jefe de mecánicos selecciona una de las 4 bahías físicas libres, entonces el sistema actualiza el estado de la bahía a "Ocupada". |
| Criterio de aceptación 2 | Dado que las 4 bahías están ocupadas, cuando se intenta una asignación, entonces el sistema emite una alerta impidiendo el cruce de unidades en la misma bahía. |
| Reglas de negocio | RN-05 (Capacidad Máxima de Bahías Físicas) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-09: Registro de Diagnóstico en Tableta
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-09 / #[9] |
| Historia | Como jefe de mecánicos, quiero registrar el diagnóstico técnico y las observaciones iniciales en la tableta, para cambiar el estado de la orden a "En Diagnóstico". |
| Criterio de aceptación 1 | Dado que el jefe de mecánicos se encuentra autenticado en la tableta, cuando selecciona una orden con vehículo en bahía, entonces visualiza un formulario táctil optimizado con campos amplios para el dictamen técnico. |
| Criterio de aceptación 2 | Dado que se ingresan las observaciones de la revisión, cuando se presiona "Guardar Diagnóstico", entonces el sistema actualiza automáticamente el estado de la orden a "En Diagnóstico" y habilita la creación de cotizaciones. |
| Reglas de negocio | RN-02 (Usabilidad y Roles en Dispositivos Táctiles) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-10: Solicitud de Refacciones e Insumos
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-10 / #[10] |
| Historia | Como mecánico del taller, quiero registrar las refacciones e insumos requeridos detectados durante la revisión, para que el área de almacén gestione su cotización o pedido. |
| Criterio de aceptación 1 | Dado que el mecánico detecta piezas necesarias en la bahía, cuando añade los elementos desde su interfaz y los vincula a la orden, entonces la solicitud se envía automáticamente al módulo de almacén. |
| Criterio de aceptación 2 | Dado que el almacén recibe el requerimiento, cuando se procesa, entonces el sistema refleja el estatus de la refacción como "Solicitada" o "En Proceso de Compra". |
| Reglas de negocio | RN-08 (Gestión de Refacciones y Proveedores) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-11: Visualización del Estatus de Bahías
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-11 / #[11] |
| Historia | Como jefe de mecánicos, quiero visualizar el estatus actual de las 4 bahías de trabajo en una interfaz simplificada para tabletas, para conocer rápidamente qué unidades están listas o en proceso. |
| Criterio de aceptación 1 | Dado que el jefe de mecánicos accede al tablero de control, cuando visualiza la sección de bahías, entonces identifica mediante códigos de color las unidades activas, en diagnóstico o listas. |
| Criterio de aceptación 2 | Dado que se actualiza el estado de una reparación, cuando cambia de fase, entonces el tablero refresca la información en tiempo real para optimizar la supervisión del taller. |
| Reglas de negocio | RN-02 (Usabilidad Operativa en Taller) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-12: Generación de Presupuesto Desglosado
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-12 / #[12] |
| Historia | Como recepcionista o jefe de mecánicos, quiero generar un presupuesto desglosado de mano de obra y refacciones con vigencia de 5 días naturales, para enviarlo de forma transparente al cliente. |
| Criterio de aceptación 1 | Dado que el diagnóstico ha concluido, cuando el personal selecciona la opción de cotizar, entonces el sistema presenta apartados separados para costos de mano de obra y refacciones. |
| Criterio de aceptación 2 | Dado que se emite la cotización, entonces el sistema calcula automáticamente el total con IVA e integra una fecha de expiración exactamente a los 5 días naturales posteriores a su emisión. |
| Reglas de negocio | RN-06 (Vigencia y Estructura de Cotizaciones) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-13: Selección de Servicios Opcionales en Cotización
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-13 / #[13] |
| Historia | Como cliente del taller, quiero seleccionar o deseleccionar servicios opcionales dentro de mi cotización antes de aprobarla, para adaptar el presupuesto a mis necesidades financieras. |
| Criterio de aceptación 1 | Dado que el cliente revisa el presupuesto desglosado en su celular, cuando marca o desmarca las casillas de servicios opcionales o sugeridos, entonces el sistema recalcula el costo total en tiempo real. |
| Criterio de aceptación 2 | Dado que se ajustan los opcionales, cuando el cliente procede a la firma, entonces el sistema guarda únicamente los conceptos seleccionados como parte oficial de la orden. |
| Reglas de negocio | RN-06 (Transparencia y Opciones de Cotización) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-14: Firma Digital y Autorización por 2FA
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-14 / #[14] |
| Historia | Como cliente del taller, quiero realizar la firma digital de aprobación mediante un código de verificación de 2 pasos enviado a mi correo, para autorizar los trabajos de forma segura ya sea de forma presencial o remota. |
| Criterio de aceptación 1 | Dado que el cliente accede al enlace web de cotización, when solicita el código de autorización, entonces el sistema envía un token numérico de 6 dígitos al correo electrónico registrado del cliente. |
| Criterio de aceptación 2 | Dado que el cliente ingresa el código recibido en la interfaz, cuando presiona "Autorizar Presupuesto", entonces el sistema valida el token, registra la dirección IP y la marca de tiempo, cambiando la orden a "Autorizada". |
| Reglas de negocio | RN-06 (Seguridad y No Repudio en Autorizaciones) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-15: Rechazo de Cotización y Cancelación
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-15 / #[15] |
| Historia | Como cliente del taller, quiero presionar un botón de rechazo en la cotización digital, para cancelar la orden y coordinar la recolección del vehículo sin autorizar reparaciones. |
| Criterio de aceptación 1 | Dado que el cliente evalúa la cotización en su dispositivo, cuando presiona el botón "Rechazar", entonces el sistema solicita una confirmación de la acción. |
| Criterio de aceptación 2 | Dado que se confirma el rechazo, cuando se procesa, entonces la orden cambia a estatus "Rechazada" y notifica a recepción para coordinar la entrega física del auto sin costo de reparación. |
| Reglas de negocio | RN-06 (Gestión de Presupuestos) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-16: Re-cotización por Incremento >10%
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-16 / #[16] |
| Historia | Como sistema, quiero bloquear el avance del taller y exigir una nueva cotización validada por 2FA si los costos imprevistos superan el 10% del presupuesto inicial. |
| Criterio de aceptación 1 | Dado que surgen refacciones imprevistas, cuando el incremento total supera el 10% del presupuesto aprobado, entonces el sistema bloquea el flujo y solicita un nuevo token 2FA. |
| Criterio de aceptación 2 | Dado que el cliente recibe la notificación del sobrecosto, cuando aprueba mediante el código digital, entonces se actualiza el monto total e historial de la orden. |
| Reglas de negocio | RN-07 (Re-cotización Obligatoria por Sobreprecio) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-17: Directorio y Gestión de Proveedores Locales
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-17 / #[17] |
| Historia | Como encargado de almacén, quiero consultar y administrar un directorio de proveedores locales con teléfonos y correos electrónicos, para solicitar refacciones especiales rápidamente. |
| Criterio de aceptación 1 | Dado que el almacenista ingresa al módulo de refacciones, cuando abre el directorio de proveedores, entonces visualiza la lista con datos de contacto actualizados (teléfonos y correos). |
| Criterio de aceptación 2 | Dado que se requiere dar de alta un nuevo proveedor, cuando el almacenista completa el formulario de registro, entonces el sistema lo almacena para futuras solicitudes de piezas. |
| Reglas de negocio | RN-08 (Directorio y Contacto con Proveedores) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-18: Registro de Costos e Historial de Compras
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-18 / #[18] |
| Historia | Como encargado de almacén, quiero registrar los costos, fechas de llegada y tickets de compra de las refacciones asociadas a una orden, para mantener un control financiero estricto. |
| Criterio de aceptación 1 | Dado que se adquiere una pieza externa con un proveedor, cuando el almacenista registra el ticket, costo unitario y fecha estimada de entrega, entonces el sistema lo vincula a la orden de servicio. |
| Criterio de aceptación 2 | Dado que se ingresa la compra, cuando se consolida el registro, entonces el sistema actualiza el historial de adquisiciones de la refacción para auditoría interna. |
| Reglas de negocio | RN-08 (Control Financiero de Refacciones) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-19: Verificación de Stock Interno
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-19 / #[19] |
| Historia | Como mecánico del taller, quiero verificar el stock de refacciones comunes en el inventario interno, para saber si se dispone de la pieza de forma inmediata. |
| Criterio de aceptación 1 | Dado que el mecánico busca un insumo estándar, cuando consulta el inventario en el sistema, entonces visualiza las existencias disponibles en almacén. |
| Criterio de aceptación 2 | Dado que hay existencia en stock, cuando se selecciona la pieza, entonces el sistema descuenta automáticamente la cantidad del inventario interno. |
| Reglas de negocio | RN-08 (Control de Inventario) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-20: Notificación Automática de Fin de Trabajos
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-20 / #[20] |
| Historia | Como recepcionista, quiero recibir una notificación automática cuando los trabajos del vehículo finalicen, para avisar al cliente que su unidad está lista para entrega. |
| Criterio de aceptación 1 | Dado que el mecánico marca la orden como terminada en bahía, cuando se actualiza el estatus, entonces el sistema envía una alerta interna a la recepcionista. |
| Criterio de aceptación 2 | Dado que la recepción recibe la alerta, cuando se verifica el estado, entonces se habilita el aviso automatizado al cliente de que su vehículo está listo. |
| Reglas de negocio | RN-10 (Cierre y Comunicación con Cliente) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-21: Bloqueo de Entrega por Saldo Pendiente
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-21 / #[21] |
| Historia | Como sistema, quiero impedir la entrega física del vehículo si la orden cuenta con saldo pendiente, para evitar pérdidas financieras al taller. |
| Criterio de aceptación 1 | Dado que un vehículo se encuentra en estado "Lista para Entrega", cuando la recepcionista intenta registrar la salida y el balance de pago es mayor a cero, entonces el sistema bloquea la acción de liberación. |
| Criterio de aceptación 2 | Dado que se activa el bloqueo por saldo pendiente, cuando el sistema detecta que cuenta con un convenio de crédito autorizado, entonces permite omitir la restricción exclusivamente bajo permisos del rol Gerente. |
| Reglas de negocio | RN-10 (Control de Cobro y Restricción de Crédito) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-22: Autorización Excepcional de Crédito a Flotillas
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-22 / #[22] |
| Historia | Como gerente del taller, quiero autorizar de forma excepcional la entrega a crédito únicamente para vehículos de flotillas empresariales registradas, para cumplir con los convenios comerciales. |
| Criterio de aceptación 1 | Dado que un vehículo pertenece a una empresa con cuenta de flotilla registrada, cuando se intenta liberar sin pago en caja, entonces el sistema solicita la clave de autorización gerencial. |
| Criterio de aceptación 2 | Dado que el gerente ingresa su contraseña de aprobación, cuando valida el convenio comercial, entonces el sistema permite liberar la unidad y factura el adeudo a crédito empresarial. |
| Reglas de negocio | RN-10 (Liberación de Crédito a Flotillas) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-23: Registro de Pago Total y Cierre de Orden
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-23 / #[23] |
| Historia | Como recepcionista, quiero registrar el pago total del servicio y cerrar formalmente la orden, para liberar la bahía de trabajo y archivar el historial del vehículo. |
| Criterio de aceptación 1 | Dado que el cliente cubre el monto total en caja, cuando la recepcionista registra el método de pago y confirma la transacción, entonces el sistema salda la cuenta a cero. |
| Criterio de aceptación 2 | Dado que el pago ha sido registrado con éxito, cuando se ejecuta el cierre, entonces la orden cambia a estado "Cerrada", liberando de inmediato la bahía física ocupada y generando el comprobante digital. |
| Reglas de negocio | RN-10 (Cierre Operativo y Liberación de Bahías) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-24: Consulta de Vigencia de Garantía
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-24 / #[24] |
| Historia | Como cliente, quiero consultar la vigencia de la garantía de 30 días en mano de obra asociada a mi servicio anterior, para reclamar ajustes en caso de incidencias. |
| Criterio de aceptación 1 | Dado que el cliente revisa el expediente de su servicio pasado en el portal web, cuando consulta el apartado de garantías, entonces visualiza la fecha exacta de expiración (30 días naturales en mano de obra). |
| Criterio de aceptación 2 | Dado que la garantía se encuentra vigente, cuando se solicita una revisión por el mismo concepto, entonces el sistema valida el estatus sin generar cargos adicionales de mano de obra. |
| Reglas de negocio | RN-03 (Trazabilidad y Garantías de Servicio) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-25: Operación Offline del Personal Interno
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-25 / #[25] |
| Historia | Como recepcionista o jefe de mecánicos, quiero registrar la llegada de autos, tomar fotografías y hacer diagnósticos sin conexión a internet usando la batería del equipo, para que la operación no se detenga ante fallas eléctricas. |
| Criterio de aceptación 1 | Dado que ocurre un corte de energía o caída de internet en el taller, cuando el personal opera mediante las baterías de laptops o tabletas, entonces el sistema local permite continuar capturando registros, checklists y fotografías. |
| Criterio de aceptación 2 | Dado que se trabaja de forma local (offline), cuando se guardan los datos, entonces el almacenamiento temporal mediante Service Workers e IndexedDB asegura que no exista pérdida de información. |
| Reglas de negocio | RN-06 (Resiliencia y Operación Fuera de Línea) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-26: Sincronización Automática en la Nube
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-26 / #[26] |
| Historia | Como sistema, quiero sincronizar automáticamente en la nube todos los registros y archivos multimedia guardados localmente en modo offline una vez que se restablezca la red, para evitar pérdida de datos. |
| Criterio de aceptación 1 | Dado que se restablece la conexión a internet en el taller, cuando el sistema detecta conectividad, entonces inicia de forma automática la sincronización de los datos almacenados localmente. |
| Criterio de aceptación 2 | Dado que finaliza el proceso de sincronización, cuando se actualiza la base de datos central en la nube, entonces la información multimedia y de auditoría se consolida sin duplicidades. |
| Reglas de negocio | RN-06 (Sincronización Diferida y Local-First) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-27: Gestión de Roles y Permisos de Seguridad
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-27 / #[27] |
| Historia | Como administrador del sistema, quiero gestionar roles y permisos seguros (Gerente, Recepcionista, Mecánico y Encargado de Almacén), para proteger la información confidencial del taller. |
| Criterio de aceptación 1 | Dado que un usuario intenta acceder a la plataforma, cuando introduce sus credenciales, entonces el sistema autentica su identidad y restringe los menús según su rol asignado (Gerente, Recepcionista, Mecánico o Almacén). |
| Criterio de aceptación 2 | Dado que un usuario sin privilegios intenta ingresar a una ruta protegida (como reportes gerenciales), entonces el sistema deniega el acceso y muestra una pantalla de error por permisos insuficientes. |
| Reglas de negocio | RN-01 (Autenticación y Control de Acceso Basado en Roles) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-28: Accesibilidad PWA Responsiva para Clientes
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-28 / #[28] |
| Historia | Como cliente, quiero visualizar la plataforma web desde mi teléfono celular de forma responsiva y sin instalar aplicaciones adicionales, para consultar mi estatus con facilidad. |
| Criterio de aceptación 1 | Dado que el cliente abre el enlace recibido por SMS o correo en un navegador móvil (iOS/Android), cuando carga la página, entonces el diseño se adapta responsivamente a la pantalla sin requerir descargas de tiendas de aplicaciones. |
| Criterio de aceptación 2 | Dado que el cliente navega por el portal web, cuando consulta el progreso de su vehículo o galería de fotos, entonces los elementos táctiles responden de manera fluida y adaptada a dispositivos móviles. |
| Reglas de negocio | RN-01 (Accesibilidad Multiplataforma y PWA) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-29: Generación de Reportes Gerenciales
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-29 / #[29] |
| Historia | Como gerente, quiero generar reportes mensuales de ingresos, servicios realizados y tiempos de ocupación de las 4 bahías, para evaluar el rendimiento general del taller. |
| Criterio de aceptación 1 | Dado que el gerente ingresa al módulo de reportes, cuando selecciona el intervalo de fechas mensual, entonces el sistema genera métricas consolidadas de ingresos y servicios completados. |
| Criterio de aceptación 2 | Dado que se consultan los tiempos operativos, cuando el sistema procesa las órdenes, entonces muestra gráficos de ocupación de las 4 bahías para medir la eficiencia del taller. |
| Reglas de negocio | RN-02 (Indicadores y Reportes Gerenciales) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

HU-30: Cumplimiento de Privacidad y Uso de Datos Ficticios
| Campo | Contenido |
| --- | --- |
| ID e issue | HU-30 / #[30] |
| Historia | Como administrador del sistema, quiero asegurar que el manejo de datos personales cumpla con la Ley Federal de Protección de Datos Personales (LFPDPPP) utilizando exclusivamente datos ficticios en las pruebas, para cumplir con el marco legal vigente. |
| Criterio de aceptación 1 | Dado que el sistema se encuentra en ambiente de pruebas o demostración, cuando se consultan los expedientes de clientes, entonces la base de datos despliega estrictamente información ficticia validada. |
| Criterio de aceptación 2 | Dado que se genera el aviso de privacidad, cuando el usuario accede al sistema por primera vez, entonces se despliega el marco legal conforme a la normatividad mexicana vigente sobre protección de datos. |
| Reglas de negocio | RN-04 (Protección de Datos Personales y LFPDPPP) |
| Wireframe | No aplica |
| Casos de prueba | No aplica |

[Figura 4.1. Story map con el corte del release v0.1.0.]


## 4.6 Requisitos no funcionales
| ID | Característica ISO/IEC 25010:2023 | Requisito | Métrica y umbral | Cómo se verificará |
| --- | --- | --- | --- | --- |
| RNF-01 | Flexibilidad (instalabilidad y adaptabilidad) | El portal del cliente deberá ser una PWA responsiva que funcione en navegadores móviles iOS y Android sin instalar software ni conceder permisos especiales. | Funciona sin errores bloqueantes en las 2 últimas versiones de Safari (iOS) y Chrome (Android); 0 permisos solicitados al cliente; sin desplazamiento horizontal en anchos de 360 a 430 px. | Pruebas manuales en 2 móviles reales (iOS y Android) con una lista de verificación de las pantallas del cliente y revisión con las herramientas de desarrollo del navegador. |
| RNF-02 | Capacidad de interacción | La interfaz de la tableta del jefe de Mecánicos deberá tener botones grandes, alto contraste y controles táctiles adaptados al uso con manos sucias y en ambiente ruidoso. | Botones de al menos 48 × 48 px con separación mínima de 8 px; contraste de texto de al menos 7:1; al menos 95 % de aciertos en 20 toques con guantes de trabajo. | Auditoría con Lighthouse o axe DevTools (gratuitos), medición del contraste con un verificador y prueba en la tableta real con guantes. |
| RNF-03 | Capacidad de interacción | La interfaz de la tableta deberá ofrecer flujos de pocos pasos para las operaciones frecuentes del taller. | Asignar bahía, actualizar el estado de una orden y sellar un trabajo en máximo 4 toques y 30 s cada una. | Prueba de usabilidad cronometrada con al menos 3 usuarios (o compañeros que simulen el rol), repitiendo cada operación 3 veces. |
| RNF-04 | Seguridad (no repudio e integridad) | Toda autorización de presupuesto o de sobrecosto mayor al 10 % deberá registrar marca de tiempo y metadatos inalterables, incluida la dirección IP, para evitar disputas con el cliente. | 100 % de las autorizaciones guardan fecha y hora UTC, IP, identificador de orden y huella SHA-256 del documento; 100 % de los intentos de alterar un registro se detectan al verificar la huella. | Prueba con 20 autorizaciones, revisión de los registros guardados e intento de modificar directamente la base de datos para confirmar que la verificación lo detecta. |
| RNF-05 | Seguridad (confidencialidad y cumplimiento legal) | El manejo de datos personales deberá apegarse a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares y usar solo datos ficticios en las pruebas. | 100 % de las conexiones con HTTPS (TLS 1.2 o superior); datos personales sensibles cifrados en reposo; aviso de privacidad visible en el 100 % de los formularios que capturan datos; 0 registros reales en el ambiente de pruebas. | Análisis con testssl.sh o SSL Labs, lista de verificación de la ley revisada por el equipo y revisión de los datos de prueba antes de cada entrega. |
| RNF-06 | Eficiencia de desempeño | El registro de recepción se deberá guardar de forma local con rapidez, aun sin conexión. | Guardar un registro con 5 fotografías en máximo 2 s (percentil 95) en la tableta o laptop del taller. | 20 repeticiones cronometradas con la herramienta de rendimiento del navegador, calculando el percentil 95. |
| RNF-07 | Mantenibilidad (modificabilidad) | El desarrollo deberá usar únicamente herramientas de código abierto, frameworks de uso libre (como FastAPI y Python) y planes educativos. | 100 % de las dependencias con licencia de código abierto o plan educativo vigente; costo de licenciamiento de $0 en esta fase. | Inventario de dependencias con herramientas de revisión de licencias (por ejemplo, pip-licenses) y registro de los planes educativos usados. |
| RNF-08 | Fiabilidad (tolerancia a fallos) | El personal interno deberá poder operar sin internet o sin energía eléctrica, con equipos en batería, bajo una arquitectura local con sincronización diferida. | Las 7 operaciones definidas (registro de entrada, checklist, fotografías, diagnósticos, asignación de bahías, consulta de proveedores y autorizaciones gerenciales) funcionan al 100 % durante al menos 4 h sin conexión; 0 datos perdidos. | Casos de prueba de las 7 operaciones con la red desconectada y un equipo con batería, comparando los registros al terminar. |
| RNF-09 | Fiabilidad (recuperabilidad) | Al restablecerse la conexión, el sistema deberá sincronizar automáticamente datos, archivos multimedia y registros de auditoría con la base de datos central, sin duplicados. | 100 % de los registros sincronizados, 0 duplicados y 0 pérdidas; 200 registros con 50 fotografías en máximo 5 min. | Crear 200 registros sin conexión, reconectar y comparar conteos y huellas con la base central; repetir 3 veces e interrumpir la conexión a mitad de una sincronización. |
| RNF-10 | Fiabilidad (tolerancia a fallos del cliente) | Ante una falla de conectividad durante la consulta de estatus o la autorización 2FA, la interfaz del cliente deberá informar el estado y reintentar automáticamente. | Mensaje de estado en máximo 3 s; reintento automático cada 30 s o menos hasta completar; 0 autorizaciones duplicadas o perdidas. | Cortar el servidor durante la consulta y durante el envío del código, cronometrar el mensaje y revisar la base de datos tras restablecer el servicio. |

## 4.7 Reglas de negocio y requisitos de dominio
| ID | Regla de negocio | Fuente (anteproyecto / entrevista con fecha) | Requisitos que afecta |
| --- | --- | --- | --- |
| RN-01 | Expiración y vigencia de enlaces: El enlace web de seguimiento permanecerá activo durante la estancia del vehículo en el taller. Expirará automáticamente al entregar y saldar la unidad. Si el cliente requiere ver su historial posteriormente, deberá solicitar la generación de un nuevo enlace. | Entrevista con el cliente (19/10/2026) | RF-02.1, RF-02.2 |
| RN-02 | Doble verificación en autorizaciones: Toda aprobación remota o presencial de cotización exigirá una doble verificación (código de 6 dígitos 2FA enviado al correo o verificación en pantalla) para evitar reclamos por trabajos no autorizados. | Entrevista con el cliente (19/10/2026) | RF-06, RNF-04 |
| RN-03 | Selección granular de rubros: El cliente puede aprobar o rechazar de manera independiente los conceptos opcionales desglosados en el presupuesto (mano de obra o refacciones), ejecutando únicamente lo autorizado explícitamente. | Entrevista con el cliente (19/10/2026) | RF-06 |
| RN-04 | Re-cotización obligatoria por sobrecostos (>10%): Cualquier trabajo o repuesto imprevisto durante la reparación que incremente el costo inicial más de un 10% detendrá el avance hasta contar con una nueva autorización validada por el cliente. | Anteproyecto y propuesta técnica | RF-07, RNF-04 |
| RN-05 | Capacidad física del taller: La atención simultánea está limitada estrictamente a 4 bahías físicas (1 vehículo por bahía) y un área de estacionamiento de recepción/espera con capacidad máxima para 5 vehículos. | Anteproyecto y entrevista con el cliente | RF-05, RF-09 |
| RN-06 | Reubicación por espera de refacciones: Si un vehículo requiere refacciones externas con demora de entrega de varios días, se liberará la bahía de trabajo reubicando la unidad en el estacionamiento hasta el arribo de las piezas. | Entrevista con el cliente (19/10/2026) | RF-05, RF-08.2 |
| RN-07 | Clasificación de vehículos autorizados: El sistema operará exclusivamente con vehículos automotrices ligeros (automóviles particulares, motocicletas y camionetas hasta de 3 toneladas). Se excluyen bicicletas, tráilers y maquinaria pesada. | Entrevista con el cliente (19/10/2026) | RF-03.1 |
| RN-08 | Confirmación manual de citas web: Las solicitudes de cita agendadas desde el portal público ingresarán en estado "Pendiente" y no reservarán espacio en la agenda hasta que la recepcionista las confirme manualmente. | Entrevista con el cliente (19/10/2026) | RF-09 |
| RN-09 | Asignación y colaboración de mecánicos: Cada orden mantendrá un mecánico principal responsable. Otros mecánicos podrán colaborar en el trabajo técnico sin alterar la titularidad de la orden, salvo reasignación formal. | Entrevista con el cliente (19/10/2026) | RF-05 |
| RN-10 | Restricción de entrega y excepción a flotillas: Queda prohibida la entrega física del vehículo con saldo pendiente. Como única excepción, el Gerente podrá autorizar la entrega a crédito para vehículos pertenecientes a flotillas empresariales registradas. | Anteproyecto y entrevista con el cliente | RF-10 |


## 4.8 Requisitos de protección de datos personales
En cumplimiento con la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (LFPDPPP - DOF):
- Datos Personales Recabados
El sistema capturará y procesará los siguientes datos de clientes particulares y representantes de flotillas:
- Datos de identificación y contacto: Nombre completo, número telefónico celular (WhatsApp/SMS) y correo electrónico.
- Datos del vehículo y de la propiedad: Placas, marca, modelo, año, número de serie (VIN - opcional), kilometraje, nivel de combustible, fotografías del estado físico de la unidad, historial de servicios e importes de facturación.
- Finalidad del Tratamiento
- Finalidades primarias: Identificación del cliente, vinculación del vehículo a la orden de servicio, generación y envío de enlaces temporales de seguimiento, envío de códigos 2FA para validación de presupuestos, cobro, emisión de comprobantes de pago y aplicación de garantías de mano de obra (30 días).
- Finalidades secundarias: Recordatorios de mantenimiento preventivo y consulta de historial a solicitud del cliente.
- Medidas de Seguridad y Control de Accesos
- Control de Acceso Basado en Roles (RBAC): La información personal del cliente solo estará accesible para los roles de Recepcionista y Gerente. Los Mecánicos y Encargados de Almacén únicamente visualizarán datos técnicos del vehículo y requerimientos de refacciones.
- Acceso mediante Tokens Temporales: Los clientes accederán a sus cotizaciones y estatus vía tokens dinámicos sin necesidad de almacenar contraseñas de usuarios externos en la base de datos.   Protección de Datos en Pruebas: Se garantiza el uso exclusivo de datos sintéticos o ficticios (mock data) durante todas las fases de desarrollo, pruebas y demostraciones académicas, sin almacenar registros reales en los entornos de staging o prueba.
- Seguridad en Tránsito: Las comunicaciones entre navegadores móviles, tabletas y servidores se realizarán mediante protocolos cifrados HTTPS (TLS 1.2 o superior).
- Borrador del Aviso de Privacidad Simplificado
AVISO DE PRIVACIDAD SIMPLIFICADO
Servicio Automotriz Hermanos Ruiz, S.A. de C.V., con domicilio en las instalaciones operativas del taller, es responsable del tratamiento de los datos personales (contacto, identificación y datos de su vehículo) proporcionados en la recepción.
Sus datos serán utilizados exclusivamente para la apertura de órdenes de servicio, seguimiento en vivo, envío de cotizaciones para su autorización remota o presencial mediante doble verificación (2FA), cobro, entrega y aplicación de garantías. Sus datos no serán transferidos ni compartidos con terceros sin su consentimiento explícito.   Para consultar el Aviso de Privacidad Integral o ejercer sus derechos ARCO (Acceso, Rectificación, Cancelación y Oposición), puede acudir a la recepción de nuestro taller o solicitarlo a través de nuestro portal web de atención a clientes.

## 4.9 Casos de uso
CU-01 — Confirmación de cita web
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-01 Confirmación de cita web |
| Actor principal | Recepcionista |
| Actores secundarios | Cliente; servicio de correo electrónico. |
| Descripción breve | Permite revisar solicitudes de citas realizadas desde el sitio web, verificar la disponibilidad del taller y confirmar fecha, hora y bahía preliminar. El sistema actualiza el estado y notifica al cliente. |
| Precondiciones | 1. El cliente solicitó previamente una cita mediante el sitio web. 2. La solicitud está registrada y pendiente de revisión. 3. La recepcionista dispone de credenciales válidas. |
| Flujo principal | 1. La recepcionista inicia sesión desde la computadora de mostrador. 2. El sistema valida las credenciales y muestra el menú principal. 3. La recepcionista abre el módulo de Gestión de Citas. 4. El sistema muestra las solicitudes pendientes. 5. La recepcionista selecciona una solicitud y revisa los datos del cliente. 6. El sistema muestra la agenda y la disponibilidad de horarios y bahías. 7. La recepcionista verifica la disponibilidad y selecciona fecha, hora y bahía preliminar. 8. La recepcionista confirma la programación. 9. El sistema actualiza la cita a «Confirmada» y guarda la programación. 10. El sistema envía una notificación al cliente por correo electrónico. 11. El sistema informa a la recepcionista que la cita fue confirmada. |
| Flujos alternos | A1 (paso 7): Horario o fecha sin disponibilidad. El sistema muestra que no hay espacio y permite seleccionar una alternativa; recepción propone la nueva fecha u hora al cliente y continúa con la confirmación. A2 (paso 4): No hay solicitudes pendientes. El sistema informa que la bandeja está vacía y la recepcionista puede salir del módulo. |
| Flujos de excepción | E1 (paso 1): Credenciales incorrectas o cuenta bloqueada. El sistema rechaza el acceso; después de tres intentos fallidos consecutivos bloquea temporalmente la cuenta durante 15 minutos. E2 (paso 9): Error al guardar. El sistema informa que no fue posible actualizar la cita y conserva el estado anterior. E3 (paso 10): Fallo de correo. La cita permanece confirmada y el envío queda para seguimiento o reintento. |
| Postcondiciones | La cita queda registrada con estado «Confirmada» y con fecha y hora asignadas. El sistema conserva el resultado del envío de la notificación. |
| Reglas de negocio | RN-CIT-01: Solo se confirma una solicitud registrada. RN-CIT-02: La programación debe respetar la disponibilidad de horarios y bahías. RN-CIT-03: La cita confirmada debe contar con fecha y hora. RN-CIT-04: La notificación se envía al correo registrado. |
| Requisitos relacionados | RF-CIT-01: Consultar solicitudes web. RF-CIT-02: Consultar agenda y disponibilidad. RF-CIT-03: Confirmar y actualizar una cita. RF-CIT-04: Notificar al cliente. HU-REC-01: Como recepcionista, quiero confirmar citas para organizar la atención del taller. |


CU-02 — Recepción del vehículo y apertura de orden
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-02 Recepción del vehículo y apertura de orden |
| Actor principal | Recepcionista |
| Actores secundarios | Cliente. |
| Descripción breve | Registra la llegada del vehículo, verifica o captura los datos del cliente y del automóvil, documenta sus condiciones iniciales y abre una orden de servicio para dar seguimiento al trabajo. |
| Precondiciones | 1. El cliente se presenta físicamente en el taller con su vehículo. 2. La recepcionista tiene acceso autorizado al sistema. 3. El sistema permite registrar clientes, vehículos y órdenes. |
| Flujo principal | 1. La recepcionista inicia sesión o continúa con una sesión activa. 2. Accede al módulo de Registro de Cliente y Vehículo. 3. Busca al cliente por los datos disponibles. 4. El sistema muestra al cliente y sus vehículos registrados, si existen. 5. La recepcionista verifica o registra los datos del cliente y del vehículo: placas, marca, modelo y VIN. 6. Accede al módulo de Check-in y Registro de Entrada. 7. El sistema solicita los datos iniciales del vehículo. 8. La recepcionista registra kilometraje y nivel de combustible. 9. Completa la lista de inspección inicial, incluyendo herramientas y llanta de refacción, entre otros elementos definidos por el taller. 10. Toma o carga fotografías de la carrocería para documentar daños previos. 11. Revisa los datos y selecciona «Abrir Orden de Servicio». 12. El sistema valida los datos obligatorios y registra la orden con estado «Abierta». 13. El sistema genera un enlace seguro asociado a la orden para el cliente. 14. El sistema confirma la apertura de la orden. |
| Flujos alternos | A1 (paso 3): Cliente no registrado. La recepcionista captura sus datos y continúa con el registro del vehículo. A2 (paso 5): Vehículo no registrado. La recepcionista captura sus datos y lo vincula con el cliente. A3 (paso 10): No se observan daños visibles. La recepcionista registra el resultado de la inspección y continúa. |
| Flujos de excepción | E1 (paso 5): Datos obligatorios incompletos. El sistema identifica los campos faltantes y no permite guardar hasta completarlos. E2 (paso 5): Vehículo con orden previa abierta. Si las placas corresponden a una orden activa, el sistema muestra el folio y dirige a la orden existente para actualizarla o cerrarla antes de abrir otra. E3 (paso 10): Fotografía inválida o mayor a 10 MB. El sistema muestra un error de formato o tamaño y solicita seleccionar una imagen compatible o comprimida. E4 (paso 12): Error al abrir la orden. El sistema informa que la operación no se completó y no debe mostrar una orden como abierta si no fue guardada. |
| Postcondiciones | Quedan registrados el check-in y la orden de servicio en estado «Abierta»; el vehículo se asocia al cliente y se genera el enlace seguro correspondiente. |
| Reglas de negocio | RN-REC-01: Cada vehículo debe estar asociado con un cliente. RN-REC-02: Se registra kilometraje y nivel de combustible al ingreso. RN-REC-03: La inspección inicial documenta el estado del vehículo. RN-REC-04: La orden requiere los datos obligatorios completos. RN-REC-05: La orden tiene folio único y estado inicial «Abierta». RN-REC-06: El enlace seguro debe corresponder a la orden correcta. |
| Requisitos relacionados | RF-REC-01: Buscar y registrar clientes. RF-REC-02: Registrar y consultar vehículos. RF-REC-03: Registrar datos de entrada. RF-REC-04: Realizar inspección y adjuntar fotografías. RF-ORD-01: Abrir una orden de servicio. RF-ORD-02: Generar enlace seguro para el cliente. HU-REC-02: Como recepcionista, quiero registrar la entrada del vehículo y abrir una orden para dar seguimiento al servicio |

CU-03 — Firma de contrato presencial (2FA)
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-03 Firma de contrato presencial (2FA) |
| Actor principal | Recepcionista |
| Actores secundarios | Cliente; servicio de correo electrónico. |
| Descripción breve | Formaliza en el mostrador la autorización de una cotización técnica mediante un código de un solo uso enviado al correo registrado del cliente. |
| Precondiciones | 1. El jefe de mecánicos ya generó el diagnóstico y la cotización técnica. 2. La cotización está asociada a una orden y disponible para revisión. 3. El cliente decide autorizar de forma presencial. 4. El cliente tiene un correo registrado y accesible. 5. La recepcionista tiene acceso al sistema. |
| Flujo principal | 1. El clnte comunica que desea autorizar presencialmente la cotización. 2. La recepcionista abre el módulo de Firma de Contrato Presencial. 3. El sistema muestra las órdenes y cotizaciones pendientes de autorización. 4. La recepcionista selecciona la orden correspondiente. 5. El sistema muestra el desglose de la cotización. 6. El cliente revisa el alcance y el importe cotizado. 7. La recepcionista selecciona «Enviar Código 2FA». 8. El sistema genera un código de verificación y lo envía al correo registrado. 9. El cliente recibe el código y se lo proporciona a la recepcionista. 10. La recepcionista introduce los seis dígitos. 11. La recepcionista selecciona «Validar y Firmar». 12. El sistema comprueba que el código sea correcto, vigente y no utilizado. 13. El sistema registra la autorización y cambia la orden a «Autorizada». 14. El sistema muestra la confirmación de la operación. |
| Flujos alternos | A1 (paso 6): El cliente solicita aclaraciones. La recepcionista aclara la información disponible o consulta al jefe de mecánicos; después el cliente puede continuar o rechazar la cotización. A2 (paso 9): El cliente no recibe el código. Se verifica el correo y el estado del envío; si está habilitado, se reenvía el código. A3 (paso 10): Si el sistema lo permite, el cliente introduce personalmente el código. |
| Flujos de excepción | E1 (paso 8): Fallo de envío. El sistema informa que no pudo enviar el código y no permite autorizar hasta completar la verificación. E2 (paso 12): Código incorrecto o expirado tras cinco minutos. El sistema lo rechaza y permite introducir un código vigente o solicitar un reenvío. E3 (paso 12): Límite de intentos excedido. El sistema bloquea temporalmente la validación o exige iniciar nuevamente el proceso. E4 (paso 13): Error al registrar la autorización. La orden conserva el estado anterior hasta que se registre correctamente. E5: El cliente rechaza la cotización. La recepcionista registra el rechazo; la orden queda «Cancelada/Rechazada» y se coordina el cobro de revisión y la entrega del vehículo sin reparar, si aplica. |
| Postcondiciones | Si la validación tiene éxito, la autorización queda registrada y la orden cambia a «Autorizada». Si el cliente rechaza la cotización, se registra el rechazo y no continúa la reparación cotizada. |
| Reglas de negocio | RN-AUT-01: La cotización debe haberse generado y estar asociada a la orden. RN-AUT-02: El cliente debe revisar la cotización antes de autorizarla. RN-AUT-03: El código es de un solo uso y tiene vigencia definida de cinco minutos, según la especificación recibida. RN-AUT-04: Se rechazan códigos incorrectos, vencidos o ya utilizados. RN-AUT-05: La orden solo cambia a «Autorizada» después de validar y registrar la aceptación. |
| Requisitos relacionados | RF-AUT-01: Consultar y mostrar la cotización. RF-AUT-02: Generar y enviar código 2FA. RF-AUT-03: Validar el código. RF-AUT-04: Registrar la autorización o el rechazo. RF-AUT-05: Actualizar el estado de la orden. RF-SEG-01: Controlar vigencia e intentos del código. HU-REC-03: Como recepcionista, quiero formalizar la autorización presencial para dejar constancia de la aprobación del cliente. |


CU-04 — Cobro y entrega del vehículo
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-04 Cobro y entrega del vehículo |
| Actor principal | Recepcionista |
| Actores secundarios | Cliente; gerente (cuando se requiera autorización de crédito); sistema de registro de pagos. |
| Descripción breve | Registra el pago de la orden, emite el comprobante, entrega las llaves al cliente y cierra la orden de servicio cuando se cumplen las condiciones de salida. |
| Precondiciones | 1. El jefe de mecánicos marcó el trabajo como «Terminado» y el vehículo está listo para entrega. 2. Existe una orden de servicio registrada. 3. La recepcionista tiene permiso para realizar el cobro y registrar la entrega. |
| Flujo principal | 1. El cliente acude al taller a recoger su vehículo. 2. La recepcionista abre el módulo de Cobro y Entrega. 3. El sistema muestra el saldo pendiente de la orden. 4. La recepcionista verifica el importe, registra el pago y emite el comprobante. 5. La recepcionista entrega las llaves al cliente. 6. La recepcionista selecciona «Registrar Entrega». 7. El sistema guarda la orden en el Historial de Servicio del vehículo y cambia el estado a «Cerrada». 8. El sistema confirma el cierre de la orden. |
| Flujos alternos | A1: Entrega a crédito para flotilla empresarial. Si el vehículo pertenece a una flotilla y queda saldo pendiente, la recepcionista solicita autorización al gerente. Si el gerente autoriza, se continúa con el registro de entrega sin pago inmediato de contado (véase CU-13). A2: El cliente paga el saldo pendiente y se reanuda el proceso de cobro y entrega. |
| Flujos de excepción | E1: Saldo pendiente sin autorización de crédito. El sistema bloquea la entrega y muestra que se requiere liquidación completa o autorización expresa de Gerencia. E2: Sesión expirada por más de 30 minutos de inactividad. El sistema redirige al inicio de sesión y conserva el borrador del formulario de cobro; tras autenticarse, la recepcionista retoma el proceso. |
| Postcondiciones | La orden queda «Cerrada», el pago queda registrado, se emite un comprobante y la orden se conserva en el historial de servicio del vehículo. |
| Reglas de negocio | RN-COB-01: No se entrega un vehículo con saldo pendiente salvo autorización expresa de Gerencia para crédito de flotilla. RN-COB-02: El pago debe registrarse en el sistema y producir un comprobante. RN-COB-03: La orden se cierra después de registrar la entrega. RN-COB-04: El cierre debe quedar en el historial de servicio del vehículo. |
| Requisitos relacionados | RF-COB-01: Consultar saldo de la orden. RF-COB-02: Registrar pago y emitir comprobante. RF-COB-03: Registrar la entrega del vehículo. RF-COB-04: Actualizar orden a «Cerrada». RF-HIS-01: Guardar la orden en el historial de servicio. HU-REC-04: Como recepcionista, quiero cobrar y registrar la entrega para cerrar correctamente la orden. |


CU-05 — Diagnóstico, cotización técnica y asignación de trabajo
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-05 Diagnóstico, cotización técnica y asignación de trabajo |
| Actor principal | Jefe de Mecánicos (líder técnico) |
| Actores secundarios | Recepcionista; mecánico asignado; sistema de agenda de bahías. |
| Descripción breve | Permite inspeccionar técnicamente un vehículo con orden abierta, elaborar el diagnóstico y la cotización de mano de obra y refacciones, y asignar una bahía y un mecánico. |
| Precondiciones | 1. Existe una orden de servicio en estado «Abierta». 2. El jefe de mecánicos tiene acceso autorizado desde la tableta del taller. 3. Hay información suficiente para identificar la orden y el vehículo. |
| Flujo principal | 1. El jefe de mecánicos inicia sesión en la tableta del taller. 2. Revisa las órdenes abiertas y localiza el vehículo en el área de recepción. 3. Inspecciona físicamente el automóvil. 4. Abre el módulo de Diagnóstico y Cotización Técnica. 5. Registra el diagnóstico y desglosa la mano de obra estimada y las refacciones necesarias. 6. Consulta el Tablero de Bahías y Mecánicos. 7. Asigna la orden a una bahía disponible y a un mecánico de su equipo. 8. Selecciona «Guardar Diagnóstico». 9. El sistema guarda el diagnóstico y cambia la orden a «Diagnosticada». 10. El sistema deja disponible la cotización para que se gestione la autorización del cliente. |
| Flujos alternos | A1 (paso 7): Las cuatro bahías están ocupadas. El sistema muestra «Capacidad máxima alcanzada (4/4 bahías ocupadas)» y coloca la orden en la lista de espera; al liberarse una bahía, el jefe retoma la asignación. A2: La orden se diagnostica pero queda en espera de asignación hasta que exista capacidad disponible. |
| Flujos de excepción | E1: Credenciales incorrectas. El sistema rechaza el acceso y permite volver a intentar. E2: Pérdida de Wi‑Fi o sesión pausada al guardar. El sistema informa que no hay conexión o que la sesión se pausó, conserva una copia local si está disponible y solicita volver a iniciar sesión al restablecer la red. E3: Durante la reparación se detecta una falla adicional cuyo costo incrementa más del 10 % respecto de lo autorizado. El sistema detiene el avance, cambia la orden a «Pendiente de Re-cotización» y deshabilita nuevas requisiciones hasta obtener una nueva autorización mediante 2FA. |
| Postcondiciones | El diagnóstico y la cotización quedan guardados; la orden cambia a «Diagnosticada». La asignación queda establecida o la orden queda en lista de espera si todas las bahías están ocupadas. |
| Reglas de negocio | RN-DIA-01: El diagnóstico se registra sobre una orden existente en estado «Abierta». RN-DIA-02: La asignación física requiere una bahía disponible y un mecánico asignado. RN-DIA-03: El taller dispone de cuatro bahías; si todas están ocupadas, se utiliza lista de espera. RN-DIA-04: Un incremento superior al 10 % del costo autorizado requiere re-cotización y nueva autorización del cliente antes de solicitar refacciones adicionales. |
| Requisitos relacionados | RF-DIA-01: Consultar órdenes abiertas. RF-DIA-02: Capturar diagnóstico técnico. RF-DIA-03: Desglosar mano de obra y refacciones. RF-DIA-04: Consultar disponibilidad y asignar bahía/mecánico. RF-DIA-05: Guardar diagnóstico y actualizar estado. RF-DIA-06: Gestionar lista de espera y re-cotización. HU-JM-01: Como jefe de mecánicos, quiero diagnosticar y asignar trabajos para organizar la reparación. |


CU-06 — Requisición de refacciones
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-06 Requisición de refacciones |
| Actor principal | Jefe de Mecánicos (líder técnico) |
| Actores secundarios | Encargado de almacén; cliente (cuando se requiere nueva autorización). |
| Descripción breve | Registra y envía al almacén la solicitud de refacciones necesarias para ejecutar una reparación autorizada. |
| Precondiciones | 1. La orden está autorizada por el cliente. 2. La reparación se encuentra en proceso. 3. El jefe de mecánicos tiene acceso a la tableta y a la orden activa. |
| Flujo principal | 1. El jefe de mecánicos inicia sesión y abre el módulo de Requisición de Refacciones en la tableta. 2. Selecciona la orden de servicio activa. 3. Ingresa las refacciones requeridas para realizar el trabajo autorizado. 4. Revisa la lista de piezas solicitadas. 5. Selecciona «Enviar Solicitud a Almacén». 6. El sistema registra la requisición y notifica al encargado de almacén. 7. El encargado de almacén puede consultar la solicitud pendiente para atenderla. |
| Flujos alternos | A1: Si las piezas solicitadas corresponden a una re-cotización previamente autorizada por el cliente, el jefe registra la requisición adicional y continúa el flujo normal. |
| Flujos de excepción | E1: Se detecta durante la reparación una falla oculta que incrementa el costo en más del 10 % del importe autorizado. El sistema detiene la orden, la cambia a «Pendiente de Re-cotización» y deshabilita la solicitud de nuevas refacciones. El jefe prepara la cotización complementaria; tras una nueva autorización 2FA por Recepción o por la Web, puede volver a requisar. E2: Pérdida de conexión o sesión pausada al guardar. El sistema muestra el aviso correspondiente y, si está disponible, conserva una copia local para reintentar cuando se restablezca la conexión. |
| Postcondiciones | La requisición queda registrada y disponible para el encargado de almacén, que recibe una notificación. Si se requiere re-cotización, las nuevas piezas quedan bloqueadas hasta obtener autorización. |
| Reglas de negocio | RN-REF-01: La requisición ordinaria corresponde a una orden autorizada y en proceso de reparación. RN-REF-02: Las piezas adicionales asociadas a un aumento superior al 10 % requieren re-cotización y autorización 2FA. RN-REF-03: La solicitud enviada debe quedar asociada a la orden de servicio. |
| Requisitos relacionados | RF-REF-01: Seleccionar orden activa. RF-REF-02: Registrar refacciones requeridas. RF-REF-03: Enviar solicitud al almacén. RF-REF-04: Notificar al encargado de almacén. RF-REF-05: Bloquear solicitudes durante una re-cotización pendiente. HU-JM-02: Como jefe de mecánicos, quiero requisar refacciones para obtener las piezas necesarias para la reparación. |


CU-07 — Finalización de trabajo y sellado de historial
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-07 Finalización de trabajo y sellado de historial |
| Actor principal | Jefe de Mecánicos (líder técnico) |
| Actores secundarios | Mecánico asignado; cliente; servicio de notificaciones. |
| Descripción breve | Registra las notas técnicas finales, verifica que las tareas autorizadas estén completadas y finaliza el trabajo para habilitar la entrega del vehículo. |
| Precondiciones | 1. El mecánico asignado terminó físicamente las reparaciones. 2. La orden está en reparación y cuenta con diagnóstico y autorización del cliente. 3. El jefe de mecánicos tiene acceso al sistema desde la tableta. |
| Flujo principal | 1. El jefe de mecánicos inicia sesión en la tableta y supervisa el vehículo. 2. Abre el módulo de Cierre Técnico y Sellado de Historial. 3. Redacta las notas técnicas finales del trabajo realizado y verifica su correspondencia con lo autorizado por el cliente. 4. Marca las tareas realizadas como completadas. 5. Selecciona «Finalizar Trabajo». 6. El sistema valida el cierre técnico. 7. El sistema cambia el estado de la orden a «Lista para Entrega». 8. El sistema envía una notificación automática al cliente. |
| Flujos alternos | A1: Si faltan tareas por marcar, el jefe revisa el estado de las reparaciones, completa las tareas correspondientes y vuelve a intentar finalizar el trabajo. |
| Flujos de excepción | E1: El jefe intenta cerrar la orden con tareas autorizadas pendientes. El sistema muestra «Existen tareas autorizadas pendientes por marcar como concluidas» y no finaliza la orden. E2: La sesión se pausa o se pierde la conexión Wi‑Fi antes de guardar. El sistema informa el problema y permite reanudar el proceso tras recuperar conexión y autenticarse. |
| Postcondiciones | Las notas técnicas y las tareas completadas quedan registradas; la orden cambia a «Lista para Entrega» y se envía la notificación al cliente. |
| Reglas de negocio | RN-CIE-01: Solo se finaliza técnicamente una reparación concluida. RN-CIE-02: Las tareas completadas deben corresponder con lo autorizado por el cliente. RN-CIE-03: No se cambia la orden a «Lista para Entrega» si quedan tareas autorizadas pendientes. RN-CIE-04: La finalización genera una notificación al cliente. |
| Requisitos relacionados | RF-CIE-01: Registrar notas técnicas finales. RF-CIE-02: Marcar tareas completadas. RF-CIE-03: Validar cierre técnico. RF-CIE-04: Cambiar estado a «Lista para Entrega». RF-CIE-05: Notificar al cliente. HU-JM-03: Como jefe de mecánicos, quiero sellar el historial técnico para dejar constancia del trabajo realizado y habilitar la entrega. |


CU-08 — Atender solicitud de refacciones y registrar compra
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-08 Atender solicitud de refacciones y registrar compra |
| Actor principal | Encargado de Almacén |
| Actores secundarios | Jefe de Mecánicos; proveedor local; sistema de inventario. |
| Descripción breve | Atiende una solicitud de refacciones, contacta a un proveedor, registra la compra y el ticket, y actualiza la disponibilidad de las piezas para que continúe la reparación. |
| Precondiciones | 1. El jefe de mecánicos envió una solicitud de refacciones asociada a una orden. 2. El encargado de almacén tiene acceso a la computadora y al sistema. |
| Flujo principal | 1. El encargado de almacén inicia sesión en la computadora de almacén. 2. Abre Solicitudes Pendientes y selecciona el pedido recibido. 3. Consulta el Directorio de Proveedores Locales y localiza un proveedor. 4. Realiza la compra o pedido por teléfono o correo con el proveedor seleccionado. 5. Abre el módulo de Registro de Compra y Ticket. 6. Captura los costos de las piezas, el proveedor y la fecha de recepción. 7. Selecciona «Confirmar Compra y Generar Ticket». 8. El sistema genera el historial de compra, descuenta del inventario si aplica y marca la refacción como «Recibida». 9. El sistema deja la solicitud registrada para que el taller continúe la reparación. |
| Flujos alternos | A1: Si existe stock local disponible, el encargado puede registrar el surtido de las piezas correspondientes sin efectuar una nueva compra, actualizando el inventario y la solicitud según corresponda. |
| Flujos de excepción | E1: No hay existencia en almacén y ningún proveedor local tiene la pieza para entrega inmediata. El encargado selecciona «Sin disponibilidad de proveedor»; el sistema cambia la orden a «Detenida por Refacción» y avisa al jefe de mecánicos y al portal del cliente. Cuando se confirma la llegada de la pieza, el encargado registra el pedido y marca las piezas como recibidas. E2: Credenciales incorrectas o tres intentos fallidos. El sistema rechaza el acceso y bloquea temporalmente la cuenta conforme a la política descrita. E3: Cuenta abierta en otro dispositivo o sesión expirada. El sistema cierra la sesión anterior o informa que la sesión expiró. |
| Postcondiciones | La compra queda en el historial, el ticket se genera, el inventario se actualiza si aplica y las refacciones quedan marcadas como «Recibida»; si no hay disponibilidad, la orden queda «Detenida por Refacción». |
| Reglas de negocio | RN-ALM-01: Toda compra debe asociarse a la solicitud y a su orden de servicio. RN-ALM-02: Se registra el proveedor, los costos y la fecha de recepción. RN-ALM-03: El inventario solo se descuenta o actualiza según aplique al movimiento registrado. RN-ALM-04: La falta de pieza disponible debe comunicarse al taller y al portal del cliente. |
| Requisitos relacionados | RF-ALM-01: Consultar solicitudes pendientes. RF-ALM-02: Consultar directorio de proveedores. RF-ALM-03: Registrar compra y ticket. RF-ALM-04: Actualizar inventario cuando aplique. RF-ALM-05: Marcar refacciones recibidas o reportar falta de disponibilidad. HU-ALM-01: Como encargado de almacén, quiero atender solicitudes y registrar compras para suministrar las piezas necesarias. |


CU-09 — Solicitud de cita desde la web
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-09 Solicitud de cita desde la web |
| Actor principal | Cliente |
| Actores secundarios | Sistema web; recepcionista (revisa posteriormente la solicitud). |
| Descripción breve | Permite que el cliente solicite una cita en el sitio web público sin crear una cuenta ni iniciar sesión, proporcionando sus datos, los de su vehículo y el horario deseado. |
| Precondiciones | 1. El cliente puede acceder a la página web pública del taller. 2. El servicio web de solicitud de citas está disponible. |
| Flujo principal | 1. El cliente abre la pantalla de Solicitud de Cita desde el sitio web, sin registrarse ni introducir contraseña. 2. Llena sus datos personales y la información de su automóvil. 3. Selecciona la fecha y hora deseadas. 4. Revisa la información y selecciona «Solicitar Cita». 5. El sistema registra la solicitud como pendiente de revisión. 6. El sistema muestra un mensaje que indica que Recepción revisará la petición. |
| Flujos alternos | A1: Si la fecha u hora solicitada no tiene espacio disponible, Recepción revisa la solicitud y puede proponer al cliente un día u horario alternativo antes de confirmar la cita. |
| Flujos de excepción | E1: No se puede enviar o registrar la solicitud. El material proporcionado no especifica el mensaje ni el procedimiento concreto de recuperación; la solicitud no debe considerarse recibida hasta que el sistema confirme el registro. |
| Postcondiciones | La solicitud queda registrada para revisión de Recepción y el cliente recibe confirmación en pantalla de que su petición fue enviada. |
| Reglas de negocio | RN-WEB-01: El cliente puede solicitar la cita sin usuario ni contraseña. RN-WEB-02: La solicitud requiere datos del cliente, información del vehículo y fecha/hora deseadas. RN-WEB-03: Enviar una solicitud no equivale a confirmar la cita; Recepción debe revisarla. |
| Requisitos relacionados | RF-WEB-01: Mostrar formulario público de solicitud. RF-WEB-02: Capturar datos del cliente y del vehículo. RF-WEB-03: Capturar fecha y hora deseadas. RF-WEB-04: Registrar solicitud pendiente y mostrar confirmación. HU-CLI-01: Como cliente, quiero solicitar una cita en línea para pedir atención sin acudir previamente al taller. |

CU-10 — Consulta del estado del vehículo en vivo
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-10 Consulta del estado del vehículo en vivo |
| Actor principal | Cliente |
| Actores secundarios | Sistema web; servicio de generación y validación de enlaces seguros. |
| Descripción breve | Permite consultar el avance del automóvil desde un teléfono mediante un enlace seguro asociado a la orden, sin requerir usuario, contraseña ni descarga de una aplicación. |
| Precondiciones | 1. El vehículo fue recibido en el taller y cuenta con una orden de servicio. 2. El cliente recibió por correo o SMS el enlace seguro correspondiente. |
| Flujo principal | 1. El cliente abre desde su teléfono el enlace seguro recibido. 2. El sistema valida automáticamente el token incluido en el enlace. 3. El sistema muestra la pantalla de Seguimiento en Vivo. 4. El cliente visualiza la barra de progreso y el estado actual del vehículo. 5. El sistema presenta el avance disponible, que puede incluir Recepción, Diagnóstico, En Reparación y Listo. |
| Flujos alternos | A1: El cliente vuelve a abrir el mismo enlace vigente para consultar el estado actualizado de la orden. |
| Flujos de excepción | E1: El enlace ha expirado o el token fue alterado. El sistema bloquea el acceso y muestra: «Su enlace de acceso ha expirado o es inválido. Por favor, solicite un nuevo enlace de seguimiento a la recepción del taller». |
| Postcondiciones | El cliente visualiza el estado asociado a la orden si el token es válido. No se modifican los datos ni el estado de la orden mediante esta consulta. |
| Reglas de negocio | RN-SEG-01: El acceso del cliente se realiza mediante un token seguro, sin usuario ni contraseña. RN-SEG-02: Un enlace expirado o alterado no debe permitir consultar la información. RN-SEG-03: La información mostrada corresponde a la orden asociada al enlace. |
| Requisitos relacionados | RF-SEG-01: Generar y validar enlaces seguros. RF-SEG-02: Mostrar el seguimiento y el estado actual del vehículo. RF-SEG-03: Bloquear enlaces inválidos o expirados e indicar cómo solicitar uno nuevo. HU-CLI-02: Como cliente, quiero consultar el estado de mi vehículo en vivo para conocer el avance de la reparación. |


# CU-11 — Aprobación remota de cotización (2FA)
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-11 Aprobación remota de cotización (2FA) |
| Actor principal | Cliente |
| Actores secundarios | Recepcionista; servicio de correo electrónico; sistema web. |
| Descripción breve | Permite que el cliente revise y autorice a distancia la cotización técnica mediante un enlace seguro y un código 2FA de seis dígitos enviado por correo electrónico. |
| Precondiciones | 1. El vehículo ya fue diagnosticado. 2. La cotización fue enviada al cliente mediante un enlace seguro. 3. El enlace está vigente y asociado a la orden correcta. 4. El cliente puede acceder al correo registrado. |
| Flujo principal | 1. El cliente abre el enlace dinámico desde su teléfono. 2. El sistema valida el enlace y muestra el desglose de mano de obra y refacciones. 3. El cliente revisa los conceptos y el importe cotizado. 4. Presiona «Solicitar Código 2FA para Autorizar». 5. El sistema envía por correo un código de verificación de seis dígitos. 6. El cliente introduce el código en la página web. 7. Presiona «Aceptar y Autorizar». 8. El sistema valida el código y registra el monto, la fecha y la hora de la autorización. 9. El sistema cambia la orden a «Autorizada» y muestra el resultado. |
| Flujos alternos | A1 (paso 3): El cliente no está de acuerdo con el costo y selecciona «Rechazar Cotización». El sistema solicita confirmar el rechazo; tras la confirmación cambia la orden a «Cancelada/Rechazada», notifica a Recepción para coordinar la entrega del vehículo sin reparar y finaliza la sesión web. |
| Flujos de excepción | E1: Enlace expirado o token alterado. El sistema bloquea el acceso e indica al cliente que solicite un nuevo enlace a Recepción. E2 (paso 8): Código 2FA incorrecto o expirado después de cinco minutos. El sistema rechaza la autorización e indica que debe solicitarse un código nuevo. E3: El código no llega al correo. El material indica que el cliente debe solicitar un nuevo código; el flujo no concluye hasta que la verificación sea satisfactoria. |
| Postcondiciones | Si la autorización es válida, queda registrada la cotización aprobada y la orden pasa a «Autorizada». Si el cliente la rechaza, la orden queda «Cancelada/Rechazada» y Recepción recibe aviso para coordinar la entrega sin reparar. |
| Reglas de negocio | RN-REM-01: La cotización debe estar asociada a una orden diagnosticada. RN-REM-02: El enlace seguro debe ser vigente y válido. RN-REM-03: El código 2FA es de seis dígitos y su vigencia indicada es de cinco minutos. RN-REM-04: La orden solo se autoriza después de validar el código y registrar el consentimiento del cliente. RN-REM-05: El rechazo confirmado debe notificarse a Recepción. |
| Requisitos relacionados | RF-REM-01: Mostrar cotización por enlace seguro. RF-REM-02: Generar y enviar código 2FA. RF-REM-03: Validar código y registrar monto, fecha y hora. RF-REM-04: Actualizar estado a «Autorizada». RF-REM-05: Registrar rechazo y notificar a Recepción. HU-CLI-03: Como cliente, quiero aprobar o rechazar remotamente una cotización para decidir sobre la reparación sin acudir al taller. |


# CU-12 — Monitoreo global del taller y KPIs
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-12 Monitoreo global del taller y KPIs |
| Actor principal | Gerente (dueño) |
| Actores secundarios | Sistema de gestión del taller. |
| Descripción breve | Proporciona al gerente un tablero general para visualizar indicadores operativos y financieros del taller, incluyendo ocupación de bahías, órdenes abiertas, tiempos promedio e ingresos acumulados. |
| Precondiciones | 1. El gerente requiere revisar la operación general. 2. Cuenta con perfil gerencial y credenciales válidas. 3. Existen datos operativos registrados en el sistema. |
| Flujo principal | 1. El gerente inicia sesión en su computadora o teléfono con el perfil gerencial. 2. El sistema valida las credenciales y abre el Dashboard General de Control. 3. El gerente consulta la ocupación de las cuatro bahías. 4. El gerente visualiza las órdenes abiertas. 5. El gerente consulta los tiempos promedio de estancia. 6. El gerente visualiza los ingresos acumulados y los indicadores disponibles en tiempo real. |
| Flujos alternos | A1: El gerente consulta el tablero desde otro dispositivo autorizado y revisa los mismos indicadores según los permisos de su perfil. |
| Flujos de excepción | E1: Credenciales incorrectas u olvido de contraseña. El sistema muestra un error y permite iniciar el flujo de recuperación por correo y verificación de seguridad. E2: Cambio de red o inactividad. Para proteger la información operativa y financiera, el sistema requiere reautenticación mediante huella o contraseña, de acuerdo con el flujo descrito en el material. |
| Postcondiciones | El gerente visualiza los indicadores disponibles del taller. La consulta no modifica las órdenes ni los datos operativos. |
| Reglas de negocio | RN-GER-01: Solo un perfil gerencial autorizado puede consultar el Dashboard General de Control. RN-GER-02: Los indicadores mostrados deben basarse en los datos registrados en el sistema. RN-GER-03: Tras inactividad o cambio de red, el sistema puede exigir reautenticación para proteger la información. |
| Requisitos relacionados | RF-GER-01: Autenticar el perfil gerencial. RF-GER-02: Mostrar ocupación de bahías. RF-GER-03: Mostrar órdenes abiertas y tiempos promedio de estancia. RF-GER-04: Mostrar ingresos acumulados. RF-GER-05: Solicitar reautenticación ante condiciones de seguridad definidas. HU-GER-01: Como gerente, quiero monitorear los indicadores del taller para conocer su situación operativa y financiera. |


# CU-13 — Autorización de entrega a crédito (flotillas)
| Campo | Contenido |
| --- | --- |
| ID y nombre | CU-13 Autorización de entrega a crédito (flotillas) |
| Actor principal | Gerente (dueño) |
| Actores secundarios | Recepcionista; cliente empresarial/flotilla; sistema de control de crédito. |
| Descripción breve | Permite decidir si se libera a crédito un vehículo de una flotilla empresarial que terminó su reparación pero conserva saldo pendiente, con revisión de la línea de crédito de la empresa. |
| Precondiciones | 1. El vehículo de una flotilla empresarial terminó su reparación. 2. La orden conserva saldo pendiente. 3. Recepción solicitó autorización de crédito para liberar el vehículo. 4. El gerente tiene un perfil autorizado para aprobar excepciones. |
| Flujo principal | 1. La recepcionista solicita al gerente autorización de entrega a crédito. 2. El gerente inicia sesión y abre Aprobación de Créditos y Excepciones. 3. Selecciona la orden correspondiente a la flotilla empresarial. 4. El sistema muestra la información de la orden y la línea de crédito aprobada. 5. El gerente revisa la información de crédito y decide autorizar la entrega. 6. El gerente selecciona «Autorizar Entrega a Crédito». 7. El sistema registra la autorización y habilita a Recepción para entregar el vehículo sin pago inmediato de contado. |
| Flujos alternos | A1: La flotilla excede su límite autorizado o presenta facturas vencidas. El sistema muestra una alerta con el saldo vencido y pregunta si el gerente desea forzar la autorización bajo su responsabilidad. • Si acepta, el sistema registra la excepción gerencial y habilita la entrega. • Si rechaza, la entrega continúa bloqueada y se exige liquidar el saldo pendiente. |
| Flujos de excepción | E1: Credenciales gerenciales incorrectas o cuenta inaccesible. El gerente debe corregir los datos o recuperar la contraseña por correo antes de continuar. E2: El sistema detecta que la empresa excedió el límite de crédito. Si no existe autorización expresa del gerente, la entrega permanece bloqueada. |
| Postcondiciones | Si se autoriza, queda registrada la excepción de crédito y Recepción puede continuar con la entrega. Si se deniega, el vehículo no se libera hasta liquidar el saldo o conseguir autorización válida. |
| Reglas de negocio | RN-CRE-01: Esta excepción aplica a vehículos de flotillas empresariales. RN-CRE-02: Se debe revisar la línea de crédito antes de autorizar. RN-CRE-03: El gerente puede forzar una autorización con límite excedido bajo su responsabilidad, según el flujo definido. RN-CRE-04: Si el gerente rechaza la excepción, la entrega permanece bloqueada y se exige pago del saldo. |
| Requisitos relacionados | RF-CRE-01: Solicitar autorización gerencial de entrega a crédito. RF-CRE-02: Consultar orden y línea de crédito de flotilla. RF-CRE-03: Detectar límite de crédito excedido y mostrar alerta. RF-CRE-04: Registrar aprobación o rechazo gerencial. RF-CRE-05: Habilitar o bloquear la entrega según el resultado. HU-GER-02: Como gerente, quiero aprobar o denegar excepciones de crédito para controlar el riesgo de liberar vehículos con saldo pendiente. |


# Anexo A. Flujos transversales de autenticación y sesión
Estos flujos se presentan como apoyo transversal de seguridad, no como casos de uso de negocio adicionales a los 13 anteriores. Los comportamientos se transcriben y ordenan a partir del material entregado.
# FT-01 — Autenticación y sesión de Recepcionista
| Campo | Contenido |
| --- | --- |
| Actor / flujo | Actor: Recepcionista Precondición: la recepcionista intenta acceder desde la computadora de mostrador. Flujo normal: ingresa usuario/correo y contraseña; el sistema valida los datos y muestra la pantalla principal de Recepción. Excepciones: (1) Credenciales incorrectas: muestra «Usuario o contraseña incorrectos. Intentos restantes: 2». (2) Tres intentos fallidos consecutivos: bloquea la cuenta por 15 minutos y muestra aviso de bloqueo. (3) Recuperación: solicita correo corporativo; si no existe muestra «Correo no registrado»; si existe, envía enlace/token válido por 15 minutos; la recepcionista restablece la contraseña y vuelve al login. (4) Más de 30 minutos de inactividad: expira la sesión, guarda el borrador del formulario actual, redirige al login y muestra aviso de sesión expirada. |

# FT-02 — Autenticación y sesión del Jefe de Mecánicos
| Campo | Contenido |
| --- | --- |
| Actor / flujo | Actor: Jefe de Mecánicos Precondición: el jefe intenta acceder desde la tableta del taller. Flujo normal: introduce usuario y contraseña y accede al tablero del taller. Excepciones: (1) Error de captura o credenciales: se rechaza el acceso y se permite reintentar. (2) Recuperación: ingresa el correo, recibe un token de restablecimiento, crea una nueva contraseña y vuelve al login. (3) Pérdida de Wi‑Fi o cierre por inactividad durante el guardado: muestra «Sin conexión / Sesión pausada. Se guardó una copia local. Vuelva a iniciar sesión al restablecer la red». |

# FT-03 — Autenticación y sesión del Encargado de Almacén
| Campo | Contenido |
| --- | --- |
| Actor / flujo | Actor: Encargado de Almacén Precondición: el almacenista intenta acceder a la terminal de inventarios. Flujo normal: introduce credenciales y accede a la pantalla de solicitudes. Excepciones: (1) Tres contraseñas fallidas: bloqueo temporal y notificación al gerente/sistema. (2) Recuperación por correo corporativo y restablecimiento de contraseña. (3) Inicio en dos computadoras o expiración de sesión por inactividad: el sistema cierra la sesión anterior y muestra «Se ha iniciado sesión en otro dispositivo o la sesión ha expirado». |


# Anexo A. Flujos transversales (continuación)
# FT-04 — Acceso del Cliente mediante enlace seguro y token
| Campo | Contenido |
| --- | --- |
| Actor / flujo | Actor: Cliente Precondición: el cliente intenta consultar el estado del vehículo o autorizar una cotización desde el celular. No requiere usuario ni contraseña: la validación se realiza con el token del enlace único. Excepción: enlace expirado (por ejemplo, la vigencia indicada de cinco días para cotización) o token alterado. El sistema bloquea el acceso e indica: «Su enlace de acceso ha expirado o es inválido. Por favor, solicite un nuevo enlace de seguimiento a la recepción del taller». Excepción 2FA: código incorrecto o expirado después de cinco minutos. El sistema rechaza la autorización y solicita un nuevo código. El cliente también puede rechazar expresamente la cotización; tras confirmar, el sistema cambia la orden a «Cancelada/Rechazada», notifica a Recepción y finaliza la sesión web. |

# FT-05 — Autenticación y sesión del Gerente
| Campo | Contenido |
| --- | --- |
| Actor / flujo | Actor: Gerente (dueño) Precondición: el gerente intenta ingresar al dashboard desde su laptop o celular. Flujo normal: inicia sesión con sus credenciales y accede al Dashboard General. Excepciones: (1) Credenciales olvidadas o incorrectas: puede recuperar la cuenta mediante correo personal/gerencial, completar la verificación de seguridad, cambiar la contraseña y volver a iniciar sesión. (2) Cambio de red Wi‑Fi o inactividad: el sistema exige reautenticación mediante huella o contraseña para proteger métricas financieras y operativas. |

## 4.10 Prototipos de baja fidelidad
Instrucción: Wireframes de todas las pantallas del flujo núcleo, cada uno con la historia o el caso de uso que representa.
[Figuras 4.x. Wireframes.]
## 4.11 Validación de requisitos con el cliente
Instrucción: Resumen de las sesiones de validación: qué se mostró, qué cambió y qué acordó el cliente. Incluyan los defectos de documentación que reportó el otro equipo en la revisión cruzada y cómo se atendieron.
| Fecha | Técnica (recorrido, prototipo, revisión) | Hallazgos | Cambios acordados |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |


# 5. Plan de pruebas y trazabilidad
## 5.1 Plan de pruebas
Instrucción: Estructura adaptada de ISO/IEC/IEEE 29119-3:2021.
| Apartado | Contenido |
| --- | --- |
| Alcance | [Qué se prueba y qué no en la Fase 1] |
| Niveles de prueba | [Unitarias, integración, sistema, aceptación] |
| Enfoque | [Manual / automatizado; herramientas] |
| Entornos | [Local, CI, staging; datos ficticios] |
| Criterios de entrada |  |
| Criterios de salida | [Por ejemplo: 0 defectos S1/S2 abiertos] |
| Roles | [QA Lead, developers, equipo contrario, cliente] |
| Riesgos de las pruebas |  |
| Calendario | [Por sprint] |

## 5.2 Casos de prueba de aceptación
Instrucción: Mínimo 25 casos (Equipo A) o 20 (Equipo B), cada uno vinculado a una historia o caso de uso. Incluyan casos de flujos alternos, valores límite y control de acceso por rol. La columna de resultado se llena al ejecutarlos (sección 10).
| ID | Historia / CU | Precondiciones | Pasos | Resultado esperado | Resultado (Pasa / Falla / Bloqueado) |
| --- | --- | --- | --- | --- | --- |
| CPA-01 | HU-… |  | 1. … 2. … |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 5.3 Matriz de trazabilidad
Instrucción: Ningún requisito Must puede quedar sin historia ni caso de prueba. Se actualiza en cada versión y en el Sprint 6 incluye el resultado de las pruebas.
| Requisito | Historias | Caso de uso | Casos de prueba | Componente / módulo | Resultado |
| --- | --- | --- | --- | --- | --- |
| RF-01 | HU-01, HU-02 | CU-01 | CPA-01, CPA-02 | [Paquete o clase] | [Pasa] |
|  |  |  |  |  |  |
|  |  |  |  |  |  |


# 6. Modelos de análisis
Instrucción: Todos los modelos deben ser consistentes con el glosario y el SRS. Notación UML 2.5.1. Cada figura debe tener número, título y ruta de su archivo fuente.
## 6.1 Diagramas de flujo de datos
Instrucción: Nivel de contexto, nivel 0 y nivel 1 de un proceso principal. Los flujos deben estar equilibrados entre niveles.
[Figuras 6.1 a 6.3.]
## 6.2 Modelo de datos
Instrucción: Diagrama entidad-relación normalizado al menos a 3FN, y diccionario de datos.
[Figura 6.4. Modelo entidad-relación.]
| Entidad | Atributo | Tipo | Nulo | Restricciones (PK, FK, único, rango) | Descripción |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

## 6.3 Diagrama de clases del dominio
Instrucción: Mínimo 14 clases (Equipo A) o 12 (Equipo B), con atributos, asociaciones y multiplicidades. Sin métodos de implementación ni clases técnicas (como controladores o repositorios).
[Figura 6.5.]
## 6.4 Diagrama de objetos
Instrucción: Instantánea con datos ficticios realistas que valide un escenario del flujo núcleo.
[Figura 6.6.]
## 6.5 Diagramas de estados
Instrucción: Equipo A: como mínimo Pedido y Entrega. Equipo B: como mínimo Orden de servicio y Cotización. Cada transición indica un evento, una condición y un rol autorizado.
[Figuras 6.7 y 6.8.]
| Estado origen | Evento | Condición | Estado destino | Rol autorizado |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## 6.6 Diagramas de actividades (to-be)
Instrucción: Al menos dos procesos clave cómo funcionarán con el sistema, con carriles por rol.
[Figuras 6.9 y 6.10.]

# 7. Arquitectura y diseño
## 7.1 Estilo arquitectónico
Instrucción: Expliquen el estilo elegido (capas, MVC, cliente-servidor con API…) y cómo atiende al menos 4 requisitos no funcionales de la sección 4.6.
| RNF | Decisión de arquitectura que lo atiende |
| --- | --- |
|  |  |
|  |  |
|  |  |
|  |  |

## 7.2 Diagramas C4
Instrucción: Contexto, Contenedores y Componentes de al menos un contenedor.
[Figuras 7.1 a 7.3.]
## 7.3 Registros de decisiones de arquitectura (ADR)
Instrucción: Mínimo 4 ADR: estilo arquitectónico, pila tecnológica, base de datos y hospedaje. Equipo A: un ADR adicional sobre el soporte sin conexión. Equipo B: un ADR adicional sobre el almacenamiento de fotos y el acceso del cliente mediante un enlace seguro. Cada ADR evalúa al menos dos alternativas.
### Plantilla de ADR (repetir por cada decisión)
| Campo | Contenido |
| --- | --- |
| ID y título | ADR-001 [Decisión] |
| Fecha y estado | [Propuesto / aceptado / reemplazado por ADR-…] |
| Contexto | [Qué problema o fuerza obliga a decidir] |
| Alternativas evaluadas | 1. … 2. … |
| Decisión |  |
| Consecuencias | [Positivas y negativas; qué se vuelve más fácil o más difícil] |
| RNF relacionados | RNF-… |

## 7.4 Diagramas de artefactos y de despliegue
Instrucción: Deben reflejar el ambiente de pruebas real: nodos, artefactos instalados y protocolos de comunicación.
[Figuras 7.4 y 7.5.]
## 7.5 Diagrama de paquetes
Instrucción: Organización de módulos y sus dependencias, sin dependencias circulares.
[Figura 7.6.]
## 7.6 Diagramas de clases de la solución
Instrucción: Clases del flujo del núcleo tal como existen en el código (controladores, servicios, repositorios, entidades). Deben coincidir con el repositorio.
[Figura 7.7.]
## 7.7 Diagramas de secuencia
Instrucción: Mínimo 4, incluido el escenario principal del flujo del núcleo.
[Figuras 7.8 a 7.11.]
## 7.8 Diagrama de comunicación
Instrucción: Al menos uno.
[Figura 7.12.]

# 8. Diseño de la interfaz de usuario
## 8.1 Prototipo de alta fidelidad
Instrucción: Enlace al prototipo navegable y capturas del flujo principal y de dos flujos adicionales. Expliquen las decisiones de diseño según el contexto de uso de cada tipo de usuario (dispositivo, conectividad, experiencia).
[Enlace y figuras.]
## 8.2 Accesibilidad
Instrucción: Qué criterios de WCAG 2.2 se consideraron (contraste, tamaño de objetivos táctiles, textos alternativos, navegación por teclado) y cómo se verificaron.
[Escriba aquí.]
## 8.3 Evaluación heurística recibida
Instrucción: Hallazgos que reportó el otro equipo con las 10 heurísticas de Nielsen, y cómo se atendieron.
| Issue | Heurística | Hallazgo | Severidad | Acción tomada |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

## 8.4 Prueba con usuarios y SUS
Instrucción: Prueba con 3 a 5 personas ajenas al equipo: tareas que realizaron, problemas observados, puntaje promedio del SUS con su cálculo y cambios derivados.
| Participante (perfil, sin nombre) | Tarea | ¿La completó? | Tiempo | Problemas observados | Puntaje SUS |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

Puntaje SUS promedio: [ ] · Cambios realizados a partir de la prueba: [ ]

# 9. Implementación del Release v0.1.0
## 9.1 Pila tecnológica
| Capa | Tecnología y versión | ADR que la justifica |
| --- | --- | --- |
| Interfaz |  |  |
| Lógica de negocio / API |  |  |
| Base de datos |  |  |
| Hospedaje del ambiente de pruebas |  |  |
| Integración continua |  |  |

## 9.2 Instrucciones de instalación y ejecución
Instrucción: Pasos para que una persona ajena al equipo instale y ejecute el sistema localmente siguiendo el README. Incluyan cómo cargar los datos de prueba ficticios.
[Escriba aquí o indique la sección del README.]
## 9.3 Integración continua y flujo de trabajo
Instrucción: Qué ejecuta el pipeline (compilación, linter, pruebas), reglas de protección de main y estadísticas del repositorio: número de pull requests fusionados y revisados.
[Escriba aquí y agregue una captura de pantalla de una ejecución exitosa.]
## 9.4 Evidencia del flujo núcleo
Instrucción: Capturas paso a paso del flujo del núcleo funcionando en el ambiente de pruebas (no en local), con datos ficticios. Equipo A: registro de pedido, cálculo del total por tipo de cliente y consulta de la producción requerida. Equipo B: apertura de orden con checklist, diagnóstico, cotización con autorización registrada y lista de órdenes abiertas.
[Figuras 9.x.]

# 10. Reporte final de pruebas e incidencias
## 10.1 Resultado de los casos de prueba
| Indicador | Valor |
| --- | --- |
| Casos de prueba diseñados |  |
| Casos ejecutados |  |
| Pasan |  |
| Fallan |  |
| Bloqueados |  |
| Pruebas unitarias automatizadas (número y resultado en CI) |  |

## 10.2 Incidencias
Instrucción: Incluyan las de todos los orígenes: internas, QA cruzado y cliente. El tiempo de atención se mide desde que se registró hasta que se cerró.
| Severidad | Registradas | Cerradas | Rechazadas (con justificación) | Abiertas | Tiempo promedio de atención |
| --- | --- | --- | --- | --- | --- |
| S1 |  |  |  |  |  |
| S2 |  |  |  |  |  |
| S3 |  |  |  |  |  |
| S4 |  |  |  |  |  |

## 10.3 Defectos conocidos que pasan a la Fase 2
| Issue | Descripción | Severidad | Prioridad | Motivo por el que no se corrigió |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

## 10.4 QA cruzado realizado al otro equipo
Instrucción: Resumen de los casos ejecutados en el sistema del otro equipo, los defectos reportados y las correcciones verificadas en la ronda 2.
[Escriba aquí.]

# 11. Paquete de transferencia a la Fase 2
Instrucción: Lo necesario para que un equipo, incluso uno distinto, continúe el proyecto de Ingeniería de Software II.
| Apartado | Contenido |
| --- | --- |
| Backlog restante priorizado | [Enlace y resumen por módulo] |
| Deuda técnica conocida |  |
| Riesgos abiertos |  |
| Decisiones pendientes con el cliente |  |
| Accesos y configuración | [Qué cuentas y servicios existen; nunca contraseñas en el documento] |
| Recomendaciones |  |


# 12. Retrospectiva del proyecto y contribución individual
## 12.1 Retrospectiva del proyecto
| ¿Qué funcionó bien? | ¿Qué no funcionó? | ¿Qué haríamos distinto en la Fase 2? |
| --- | --- | --- |
| ~ [ ] | ~ [ ] | ~ [ ] |

## 12.2 Contribución individual
Instrucción: Cada integrante describe, con sus propias palabras, su aporte y enlaza la evidencia. El profesor lo contrasta con el repositorio, el tablero y la coevaluación; esta última se entrega por separado en un formulario privado.
| Integrante | Principales aportes | Evidencia (issues, PR, documentos) | Revisiones de código o documentos hechas a otros |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |


# 13. Referencias
Instrucción: Formato APA 7, en orden alfabético. Solo fuentes que realmente consultaron y que se pueden verificar. Como mínimo deben aparecer las normas y guías que usaron:
Schwaber, K., & Sutherland, J. (2020). La Guía de Scrum. https://scrumguides.org/
ISO/IEC/IEEE. (2018). ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering. ISO.
ISO/IEC. (2023). ISO/IEC 25010:2023 Systems and software engineering — SQuaRE — Product quality model. ISO.
ISO/IEC/IEEE. (2021). ISO/IEC/IEEE 29119-3:2021 Software and systems engineering — Software testing — Part 3: Test documentation. ISO.
Object Management Group. (2017). OMG Unified Modeling Language, Version 2.5.1. https://www.omg.org/spec/UML/2.5.1
[Agreguen aquí el resto de sus referencias.]
# Anexos
Instrucción: Numeren los anexos con letras. Contenido mínimo:
Anexo A. Guiones y minutas de las entrevistas con el cliente (mínimo 20 preguntas en el guion inicial).
Anexo B. Minutas de las Sprint Reviews con aceptaciones y rechazos del cliente.
Anexo C. Detalle completo de las historias de usuario y los casos de prueba, si no caben en el cuerpo.
Anexo D. Manual breve de uso del flujo del núcleo (Equipo A: para la auxiliar de oficina; Equipo B: para la recepcionista).
Anexo E. Aviso de privacidad (borrador).

# Lista de verificación antes de entregar
Instrucción: Revísenla en equipo antes de cada entrega. Bórrenla del documento final o déjenla marcada como evidencia de revisión.
| ✓ | Verificación |
| --- | --- |
| ☐ | Se borraron todas las instrucciones y los marcadores entre corchetes. |
| ☐ | La portada, el control de versiones y los enlaces están actualizados. |
| ☐ | Las secciones del corte están completas según la tabla 0.2. |
| ☐ | Se alcanzan los mínimos de su equipo: historias, RNF, glosario, casos de uso, casos de prueba, clases del dominio, ADR, secuencias y riesgos. |
| ☐ | Todo requisito no funcional tiene una métrica y un umbral. |
| ☐ | La matriz de trazabilidad no tiene requisitos Must con historia ni caso de prueba. |
| ☐ | Los nombres del glosario, del SRS, de los modelos y del código coinciden. |
| ☐ | Cada figura tiene número, título, es legible y su archivo fuente está en el repositorio. |
| ☐ | Las solicitudes de cambio y las incidencias están registradas junto con su decisión. |
| ☐ | Se declaró el uso de IA. |
| ☐ | No hay datos personales reales ni contraseñas en el documento ni en el repositorio. |
| ☐ | Las referencias están en formato APA 7 y son verificables. |
| ☐ | El PDF y el .docx están en docs/entregas/ con el nombre correcto. |
| ☐ | Otro integrante, distinto del autor principal, revisó el documento completo. |

