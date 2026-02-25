# Project Brief

## 1. Context and Objective
La Biblioteca Municipal de San Gregorio gestiona manualmente la inscripción y seguimiento de actividades culturales, generando errores, duplicidades, sobreasignación de plazas y falta de información consolidada.

El objetivo del proyecto es implantar una solución digital sencilla que permita:
- Centralizar la gestión de actividades e inscripciones.
- Reducir errores administrativos.
- Disponer de información actualizada en tiempo real.
- Mejorar la experiencia de usuarios y personal.
- Cumplir con la normativa de protección de datos.
- Ajustarse a recursos limitados y conocimientos tecnológicos básicos.

## 2. Scope of the System

### Includes
- Gestión de actividades.
- Gestión de participantes.
- Inscripciones con control automático de plazas.
- Confirmaciones automáticas básicas.
- Control de asistencia.
- Informes básicos y exportación de datos.
- Gestión de usuarios internos y roles.

### Excludes
- Integraciones con otros sistemas municipales.
- Gestión de pagos.
- Aplicación móvil nativa.
- Analítica avanzada o inteligencia de negocio compleja.
- Automatizaciones avanzadas.
- Lista de espera.

## 3. System Actors
- Administrador: Responsable de configuración y supervisión con gestión total del sistema y usuarios.
- Personal administrativo: Gestión operativa diaria de actividades y usuarios.
- Usuario (ciudadano): Consultar actividades e inscribirse.

## 4. Functional Requirements
- RF01: Crear, editar, cerrar y cancelar actividades con información completa.
- RF02: Gestionar estados de actividad: borrador, abierta, cerrada, finalizada.
- RF03: Mostrar plazas disponibles en tiempo real.
- RF04: Consultar listado de inscritos.
- RF05: Registro de participantes con datos y consentimiento.
- RF06: Validar para impedir inscripciones duplicadas.
- RF07: Reutilizar datos de participantes previos.
- RF08: Inscripción interna por personal administrativo.
- RF09: Inscripción online vía formulario web.
- RF10: Control automático de plazas to bloquear inscripciones al límite.
- RF11: Confirmación automática de inscripción con correo.
- RF12: Informes básicos.
- RF13: Exportación de datos en CSV o Excel.
- RF14: Autenticación segura.
- RF15: Gestión de roles diferenciados.

## 5. Non-Functional Requirements
- Usabilidad: Interfaz sencilla e intuitiva para personal con conocimientos básicos.
- Compatibilidad: Navegadores web comunes.
- Rendimiento: Actualización en tiempo real del número de plazas.
- Consistencia: Integridad de datos ante inscripciones simultáneas.
- Seguridad: Protección del acceso y cumplimiento RGPD.
- Privacidad: Acceso restringido según rol.
- Consentimiento: Registro explícito informado.
- Mantenibilidad: Arquitectura simple para mantenimiento básico.
- Coste: Tecnologías de bajo coste acorde a presupuesto.
- Adaptabilidad: Integración a horarios y recursos sin alterar servicio.
- Fiabilidad: Disponibilidad durante horario administrativo.

## 6. Conceptual Data Model (High Level)
- Actividad: id, título, descripción, tipo, fecha, hora, duración, plazas_max, estado.
- Usuario: id, nombre, apellidos, identificador único, teléfono, email, consentimiento_datos.
- Inscripción: id, id_usuario, id_actividad, fecha_inscripción, estado, asistencia.
- Relación: usuario puede tener múltiples inscripciones; actividad puede tener múltiples inscritos.

## 7. Acceptance Criteria
- Permitir creación y gestión de actividades desde interfaz única.
- Control automático de plazas.
- Evitar duplicidades.
- Consulta inmediata de inscritos y asistencia.
- Confirmaciones automáticas.
- Exportación de datos.
- Cumplimiento normativo.
- Usabilidad para personal sin formación avanzada.

## 8. Expected Benefits
- Reducción significativa de errores administrativos.
- Eliminación de duplicidades.
- Información actualizada en tiempo real.
- Mejor planificación futura por datos fiables.
- Menos quejas por sobreasignación o falta de confirmación.
- Optimización del trabajo administrativo.
- Mayor satisfacción de usuarios.

Este documento define una solución sencilla, viable y alineada con restricciones operativas, presupuestarias y normativas.
