▒▒▒▒▒▒▒▓
▒▒▒▒▒▒▒▓▓▓
▒▓▓▓▓▓▓░░░▓
▒▓░░░░▓░░░░▓
▓░░░░░░▓░▓░▓
▓░░░░░░▓░░░▓
▓░░▓░░░▓▓▓▓
▒▓░░░░▓▒▒▒▒▓
▒▒▓▓▓▓▒▒▒▒▒▓
▒▒▒▒▒▒▒▒▓▓▓▓
▒▒▒▒▒▓▓▓▒▒▒▒▓
▒▒▒▒▓▒▒▒▒▒▒▒▒▓
▒▒▒▓▒▒▒▒▒▒▒▒▒▓
▒▒▓▒▒▒▒▒▒▒▒▒▒▒▓
▒▓▒▓▒▒▒▒▒▒▒▒▒▓
▒▓▒▓▓▓▓▓▓▓▓▓▓
▒▓▒▒▒▒▒▒▒▓
▒▒▓▒▒▒▒▒▓

# Viajes Aventura

**Proyecto académico | TI3021 - Programación Orientada a Objeto Seguro | Unidad 4**

## 1. Descripción del proyecto

Viajes Aventura es una agencia dedicada a la planificación y venta de servicios turísticos. El proyecto consiste en diseñar y desarrollar una aplicación en Python que permita administrar destinos turísticos, paquetes y reservas de clientes, incorporando persistencia de datos y mecanismos de acceso seguro.

El desarrollo integra levantamiento de requerimientos, modelado UML y BPMN, organización ágil del trabajo, programación orientada a objetos y revisión técnica del código, incluido el que se genere con apoyo de herramientas de inteligencia artificial.

## 2. Problemática

Actualmente, Viajes Aventura no dispone de un sistema informatizado para administrar su operación. Esta situación provoca las siguientes dificultades:

- Falta de control y actualización de los destinos turísticos disponibles.
- Dificultades para crear y administrar paquetes que combinan varios destinos.
- Problemas para registrar, consultar y realizar seguimiento de las reservas.
- Riesgos asociados al almacenamiento y tratamiento de datos personales y credenciales de los clientes.
- Dependencia de procesos manuales que disminuyen la eficiencia de la gestión.

Por lo tanto, se necesita una solución centralizada que permita administrar la información turística y las reservas, validar los datos ingresados y proteger el acceso a la información de los clientes.

## 3. Objetivo general

Desarrollar una aplicación en Python para Viajes Aventura que permita gestionar destinos, paquetes turísticos y reservas de clientes mediante una solución orientada a objetos, con persistencia de datos y autenticación segura.

## 4. Alcance inicial

La solución contempla los siguientes módulos:

1. **Gestión de destinos:** registrar, modificar, eliminar y listar destinos turísticos.
2. **Gestión de paquetes:** crear paquetes con varios destinos, definir fechas y costos, calcular su costo y consultar su disponibilidad.
3. **Gestión de clientes y reservas:** permitir el registro y autenticación de clientes, realizar reservas, almacenar sus datos y consultar el historial.
4. **Seguridad y validación:** validar los datos de entrada y proteger las credenciales y la información sensible.

## 5. Requerimientos funcionales

Los requerimientos funcionales describen las operaciones que el sistema debe realizar.

| ID | Requerimiento | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-01 | El sistema debe permitir registrar destinos turísticos con nombre, país, ciudad, descripción y costo base. | Alta | Un destino válido queda guardado y aparece en el listado. |
| RF-02 | El sistema debe permitir modificar la información de un destino existente. | Alta | Los cambios quedan guardados y se muestran al consultar el destino. |
| RF-03 | El sistema debe permitir eliminar destinos existentes. | Alta | El destino deja de aparecer como disponible, respetando las restricciones por asociaciones existentes. |
| RF-04 | El sistema debe permitir listar y consultar los destinos disponibles. | Alta | Se muestran los destinos registrados y su estado de disponibilidad. |
| RF-05 | El sistema debe permitir crear paquetes turísticos que agrupen varios destinos. | Alta | Los destinos seleccionados quedan asociados al paquete creado. |
| RF-06 | El sistema debe permitir definir fechas y costos para cada paquete turístico. | Alta | El paquete muestra sus fechas y el costo definido. |
| RF-07 | El sistema debe calcular el costo de un paquete considerando los destinos asociados. | Alta | El costo calculado corresponde a la regla de cálculo acordada y puede consultarse en el paquete. |
| RF-08 | El sistema debe permitir consultar la disponibilidad de los paquetes turísticos. | Alta | El sistema informa si un paquete puede recibir reservas según las reglas de disponibilidad definidas. |
| RF-09 | El sistema debe permitir que los clientes se registren y creen una cuenta. | Alta | Un cliente con datos válidos queda registrado y puede utilizar sus credenciales. |
| RF-10 | El sistema debe permitir que los clientes se autentiquen mediante sus credenciales. | Alta | Las credenciales válidas permiten iniciar sesión y las incorrectas son rechazadas. |
| RF-11 | El sistema debe permitir que un cliente autenticado realice una reserva de un paquete disponible. | Alta | La reserva se registra y el sistema informa el resultado de la operación. |
| RF-12 | El sistema debe almacenar las reservas en la base de datos. | Alta | Una reserva guardada puede recuperarse después de cerrar y volver a iniciar la aplicación. |
| RF-13 | El sistema debe permitir que los clientes consulten su historial de reservas. | Alta | El cliente puede consultar las reservas asociadas a su propia cuenta. |

## 6. Requerimientos no funcionales

Los requerimientos no funcionales establecen condiciones de seguridad, calidad y organización que debe cumplir la solución.

| ID | Requerimiento | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RNF-01 | Las contraseñas deben almacenarse mediante hashes seguros, nunca como texto plano. | Alta | La base de datos contiene el hash de la contraseña y no la contraseña original. |
| RNF-02 | El sistema debe validar los datos ingresados antes de procesarlos o guardarlos. | Alta | Los datos vacíos, inválidos o con formato incorrecto son rechazados con un mensaje comprensible. |
| RNF-03 | La información personal y las reservas de los clientes deben estar protegidas contra accesos no autorizados. | Alta | Un cliente solo puede consultar la información permitida para su propia cuenta. |
| RNF-04 | La aplicación debe mantener la persistencia de destinos, paquetes, clientes y reservas. | Alta | La información continúa disponible después de reiniciar la aplicación. |
| RNF-05 | El código debe aplicar programación orientada a objetos y separar presentación, lógica de negocio y persistencia. | Alta | La estructura del proyecto permite identificar y mantener las tres capas. |
| RNF-06 | El proyecto debe mantener una nomenclatura coherente: código Python y SQL en inglés, mensajes al usuario en español. | Media | Los identificadores técnicos están en inglés y los mensajes visibles para el usuario están en español. |

## 7. Modelo inicial de datos

El archivo `diagrama_bd_viajes_aventura.puml` contiene el primer modelo entidad-relación de la base de datos.

El modelo considera estas tablas:

| Tabla | Responsabilidad |
|---|---|
| `CUSTOMERS` | Datos de los clientes y credenciales de acceso. |
| `DESTINATIONS` | Información de los destinos turísticos y su costo base. |
| `PACKAGES` | Información, fechas, costo y capacidad de los paquetes. |
| `PACKAGE_DESTINATIONS` | Relaciona paquetes y destinos mediante una relación muchos a muchos. |
| `RESERVATIONS` | Registra las reservas realizadas por los clientes. |

### Relaciones principales

- Un cliente puede realizar varias reservas; cada reserva pertenece a un cliente.
- Un paquete puede aparecer en varias reservas; cada reserva corresponde a un paquete.
- Un paquete puede contener varios destinos y un destino puede formar parte de varios paquetes. La tabla `PACKAGE_DESTINATIONS` resuelve esta relación muchos a muchos.

### Reglas de negocio pendientes de validar

El enunciado solicita calcular costos y consultar disponibilidad, pero no especifica por completo las fórmulas ni las condiciones. Antes de implementar estas funciones, el equipo debe acordar y documentar:

- **Cálculo del costo:** como regla inicial se puede considerar la suma de los costos base de los destinos asociados. Cualquier recargo, descuento u otro concepto debe definirse expresamente.
- **Disponibilidad:** se propone considerar el estado del paquete, sus fechas y su capacidad máxima. La disponibilidad restante podría calcularse restando de la capacidad las personas incluidas en reservas confirmadas.
- **Eliminación de destinos:** se debe definir qué ocurre cuando un destino ya está asociado a un paquete o a información histórica. No se deben eliminar registros relacionados sin una regla definida.
- **Estados:** el equipo debe acordar los valores permitidos para los estados de paquetes y reservas, por ejemplo, activo, cancelado o confirmado, según corresponda.

Estas reglas son propuestas de diseño y deben validarse con el equipo y el docente antes de considerarlas definitivas.

## 8. Organización técnica prevista

La aplicación se desarrollará en Python mediante programación orientada a objetos y separación por capas:

- **Presentación:** interacción con el usuario y visualización de mensajes en español.
- **Lógica de negocio:** validaciones, reglas de costos, disponibilidad y operaciones de reservas.
- **Persistencia:** conexión y operaciones de lectura y escritura en la base de datos.

### Persistencia por hitos

Según las indicaciones de la clase, para la prueba inicial del Hito 1 se debe comprobar la conexión con **SQLite**. La incorporación de **MySQL** está prevista para el primer flujo del Hito 2.

La configuración sensible debe mantenerse local. Se debe versionar un archivo de ejemplo como `.env.example` y utilizar `.gitignore` para evitar subir el `.env` real al repositorio.

## 9. Metodología ágil, Jira y Git

El trabajo se organizará mediante un Product Backlog y tareas priorizadas. Cada tarjeta de Jira debe indicar responsable, fecha, resultado esperado y evidencia del avance.

Estados de las tareas en Jira:

- **Por hacer:** tarea pendiente.
- **En progreso:** tarea en desarrollo.
- **Hecho:** tarea terminada y con evidencia asociada.

### Convención de ramas

El nombre de cada rama debe indicar el propósito del cambio y la tarjeta Jira relacionada:

`<prefix>/<jira-key>-<description>`

Ejemplos:

- `docs/VA-12-requirements`
- `feature/VA-18-create-reservation`
- `fix/VA-21-validate-dates`

### Flujo obligatorio de integración

1. El autor crea una rama y realiza sus commits.
2. Publica la rama en el repositorio remoto.
3. Abre un Pull Request con destino a `main`.
4. Un compañero revisa el cambio y lo aprueba o solicita ajustes.
5. Si se aprueba, se integra el Pull Request y se enlaza la evidencia en Jira.

**No se debe realizar push directo a `main`. Toda integración debe pasar por un Pull Request aprobado por un compañero.**

## 10. Planes a futuro

La planificación siguiente organiza el trabajo pendiente a partir de las actividades indicadas en la guía y en la presentación de clase.

### Hito 1: análisis y base del proyecto

- Revisar y priorizar los requerimientos funcionales y no funcionales.
- Validar el modelo de base de datos y preparar su versión física inicial.
- Guardar los requerimientos y el modelo corregido dentro de `docs/`.
- Crear y configurar el repositorio del proyecto.
- Preparar la estructura por capas en Python.
- Configurar y ejecutar una prueba reproducible de conexión con SQLite.
- Registrar tareas, commits, Pull Requests y evidencias en Jira.

### Hito 2: persistencia e implementación

- Incorporar MySQL en el flujo de persistencia previsto para este hito.
- Implementar las operaciones CRUD de destinos y paquetes.
- Implementar el registro y la autenticación segura de clientes.
- Implementar la creación y consulta de reservas.
- Incorporar las reglas acordadas para el cálculo de costos y la disponibilidad.
- Validar los datos y proteger la información sensible.

### Etapa de modelado y documentación final

- Elaborar y mantener coherentes los diagramas UML de casos de uso y clases.
- Elaborar los diagramas BPMN de procesos, especialmente la gestión de paquetes y el flujo de reservas.
- Documentar las decisiones técnicas y las reglas de negocio.
- Completar el informe técnico grupal con requerimientos, diagramas, planificación, justificación técnica y evidencia del sistema.

### Validación y defensa individual

- Probar las funcionalidades principales y los mecanismos de seguridad.
- Revisar el código generado con apoyo de IA, justificar los cambios realizados y explicar las decisiones técnicas.
- Preparar la explicación del aporte individual, modelado, persistencia y seguridad del sistema.

## 11. Uso responsable de herramientas de IA

Las herramientas de inteligencia artificial pueden utilizarse como apoyo para analizar requerimientos, proponer modelos, revisar código y detectar posibles errores. Sin embargo, el equipo debe comprender, comprobar y mejorar técnicamente las sugerencias antes de incorporarlas al proyecto.

Las decisiones de aceptar, modificar o descartar recomendaciones deben poder justificarse durante la defensa individual.

## 12. Estructura documental prevista

```text
viajes-aventura/
├── docs/
│   ├── requerimientos.md
│   ├── diagrama_bd_viajes_aventura.puml
│   ├── modelo_fisico_v1.sql
│   ├── uml/
│   └── bpmn/
├── src/
│   ├── presentation/
│   ├── business/
│   └── persistence/
├── tests/
├── .env.example
├── .gitignore
└── README.md
