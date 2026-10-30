<!-- converted from Propuesta de Solución Tecnológica.docx -->

Propuesta de Solución Tecnológica: Sistema de Órdenes de Servicio y Citas
Proyecto: Automatización y Control del Ciclo de Servicio
Empresa Solicitante: Servicio Automotriz Hermanos Ruiz, S.A. de C.V.
Equipo Proveedor: Equipo B (5 integrantes)
- Resumen Ejecutivo y Enfoque
Nuestro objetivo es transformar la operación manual actual (cuadernos, llamadas constantes y órdenes en papel) en una plataforma digital ágil, transparente y segura. Trabajaremos bajo la metodología Scrum en sprints de dos semanas, garantizando entregas incrementales y revisiones continuas (Sprint Reviews) para asegurar que el sistema se adapte exactamente a las necesidades reales del taller.
- Solución a los problemas actuales del taller
La propuesta de software ataca directamente los 5 puntos críticos que hoy le cuestan dinero y clientes a la empresa:
Fin a las disputas por costos: Toda cotización y su respectiva autorización quedarán registradas digitalmente con fecha, hora, monto y medio de aprobación, eliminando el "dijo que sí, pero cobra otra cosa".
Reducción de llamadas innecesarias: Implementaremos un sistema de notificaciones y un enlace seguro web para que los clientes consulten el estado de su vehículo desde su celular sin saturar a la recepcionista.
Control de vehículos y bahías: Visualización en tiempo real de las 4 bahías de trabajo y el estatus de las refacciones para evitar unidades detenidas sin justificación.
Historial vehicular unificado: Cada vez que un cliente regrese, el sistema mostrará el historial completo de reparaciones anteriores y garantías vigentes.
Evidencia contra reclamos por daños: El módulo de recepción incluirá un checklist digital y carga fotográfica obligatoria del estado inicial del vehículo.
- Propuesta de Arquitectura y Alcance Funcional
Para cumplir con las restricciones del proyecto (uso exclusivo de herramientas gratuitas, de código abierto y planes educativos), proponemos una arquitectura moderna basada en cliente-servidor con una API REST, organizada como un monolito modular (más sencilla de construir, probar y desplegar para un equipo de 5 personas):
Backend / Lógica de Negocio: Desarrollado en Python con FastAPI, garantizando alta velocidad de respuesta, seguridad y la generación automática de documentación técnica.
Interfaz de Usuario (Frontend):
Para el personal (Gerente, Recepción, Mecánicos, Almacén): Una interfaz web optimizada (con botones grandes y accesibles para tabletas en el área de trabajo con ruido y manos sucias).

Para el Cliente: Una vista web responsiva accesible mediante un enlace seguro enviado por correo o mensaje, sin necesidad de instalar aplicaciones móviles.
Control de Versiones y Despliegue: Repositorio centralizado en GitHub de la organización del curso, asegurando transparencia y trazabilidad mediante Pull Requests y ramas de desarrollo.
- Enfoque del Primer Producto Mínimo Funcional (Release v0.1.0)
Para la Fase 1, nos enfocaremos en construir y desplegar el flujo núcleo operativo de extremo a extremo:
Recepción: La recepcionista registra al cliente, vehículo, kilometraje, nivel de combustible y fotos de ingreso.
Diagnóstico y Asignación: La orden se asigna a un mecánico y a una de las 4 bahías disponibles, registrando el diagnóstico técnico.
Cotización y Autorización: Se genera el presupuesto de mano de obra y refacciones, enviándolo al cliente para su validación digital registrada.
Monitoreo Gerencial: El gerente cuenta con un panel para visualizar las órdenes abiertas, sus estados actuales y la carga de trabajo del taller.
5. Consideraciones Legales y de Seguridad
Debido al manejo de información de clientes, el sistema cumplirá estrictamente con las directrices de la Ley Federal de Protección de Datos Personales en Posesión de los Particulares (DOF), incorporando avisos de privacidad y uso exclusivo de datos ficticios durante las fases de prueba y desarrollo.
6. Requerimientos Extraídos del Anteproyecto
A partir del documento del anteproyecto, podemos clasificar los requerimientos iniciales de la siguiente manera:
Requerimientos Funcionales (Lo que el sistema debe hacer):
El sistema debe permitir el registro y búsqueda de clientes y sus vehículos (placas, marca, modelo, año).
El sistema debe permitir abrir una orden de servicio registrando kilometraje, nivel de combustible, checklist y fotos de daños previos.
El sistema debe permitir la asignación de órdenes de trabajo a mecánicos y a una de las 4 bahías del taller.
El sistema debe generar cotizaciones de mano de obra y refacciones, enviándolas al cliente para su autorización digital.
El sistema debe permitir al cliente consultar el estado de su vehículo mediante un enlace seguro desde su celular sin instalar aplicaciones.
El gerente debe contar con un panel de control para ver las órdenes abiertas, tiempos, ingresos y carga de trabajo de las bahías.
Requerimientos No Funcionales / Restricciones (Cómo debe comportarse):
Restricción de Presupuesto: No se deben pagar licencias en esta fase; se deben usar herramientas gratuitas, de código abierto o planes educativos.
Usabilidad: Los mecánicos necesitan una interfaz con botones grandes, pocos pasos y optimizada para uso en tabletas o celulares (con manos sucias y ruido en el área de trabajo).
Seguridad y Trazabilidad: La autorización del cliente debe registrar fecha, hora, medio y monto de forma inalterable.
Cumplimiento Legal: El sistema debe cumplir con la Ley Federal de Protección de Datos Personales (aviso de privacidad y medidas de seguridad), utilizando datos ficticios para pruebas.
7. Preguntas Estratégicas para el Negocio
Para afinar el alcance y entender la viabilidad técnica y operativa, estas son las preguntas clave que el equipo plantea al cliente (Gerencia):
Sobre dispositivos y recursos económicos:
"Dado que los mecánicos trabajarán en el área de servicio y requerimos una interfaz con tabletas o celulares, ¿el taller ya cuenta con dispositivos móviles (tabletas) para el personal o el equipo proveedor debe presupuestar/considerar el uso de los teléfonos personales de los mecánicos (BYOD)?"
"Para el envío de notificaciones y cotizaciones a los clientes (vía correo electrónico o posibles futuros canales), ¿cuentan con un servidor de correo corporativo o prefieren que utilicemos servicios gratuitos en la nube (como SMTP de pruebas o APIs básicas)?"
Sobre las reglas del negocio y el flujo operativo:
"Mencionan que una cotización tiene vigencia de 5 días naturales y que si un trabajo adicional incrementa el costo en más del 10% requiere reautorización. ¿El sistema debe bloquear automáticamente la orden hasta que llegue esa nueva autorización o solo debe alertar al asesor?"
"Para el caso de las 3 pequeñas flotillas empresariales que atienden, ¿el crédito autorizado lo maneja directamente el gerente con aprobación manual o el sistema debe registrar un límite de crédito por empresa?"
Sobre la recepción y evidencias:
"Para las fotografías de recepción de los vehículos, ¿existe alguna restricción de almacenamiento o tamaño máximo de las imágenes para evitar saturar el servidor gratuito que utilizaremos en el proyecto?"
8. Ejemplo de Historia de Usuario basada en el Anteproyecto
Tomando un requisito crítico del documento (la autorización de la cotización), así se estructura una historia de usuario lista para el Product Backlog:
Título: Autorización digital de cotización por parte del cliente.
Historia de Usuario:
Como cliente del taller, quiero recibir un enlace seguro en mi celular para revisar el detalle de la cotización (mano de obra y refacciones) y poder aceptarla o rechazarla confirmando con un código de verificación enviado a mi correo, para autorizar los trabajos de mi vehículo de forma rápida y sin necesidad de llamadas telefónicas o visitas presenciales.
Criterios de Aceptación:
El sistema genera un enlace web único y seguro al crear la cotización.
Al abrir el enlace en cualquier navegador móvil, el cliente visualiza el desglose de la cotización (vigente por 5 días).
La interfaz cuenta con dos botones claros: "Autorizar" y "Rechazar".
Al hacer clic en autorizar e ingresar el código de verificación (2FA) enviado a su correo, el sistema registra de forma inalterable la fecha, hora, monto y dirección IP, cambiando el estatus de la orden de servicio automáticamente.
