# Requerimientos del Sistema — Viajes Aventura

## Requerimientos Funcionales (RF)
| ID | Prioridad | Descripción | Criterio de Aceptación |
| :--- | :--- | :--- | :--- |
| **RF-01** | Alta | Registrar, consultar, modificar y retirar destinos turísticos. | El destino queda persistido en BD; al retirarlo (`is_active = 0`) no aparece en nuevas ofertas pero conserva su historial. |
| **RF-02** | Alta | Crear paquetes turísticos combinando al menos dos destinos en un orden definido. | El sistema rechaza paquetes con menos de 2 destinos activos y guarda el orden en `itinerary_stops`. |
| **RF-03** | Alta | Programar salidas de un paquete con fechas, precio y cupos independientes. | Dos salidas del mismo paquete en fechas distintas mantienen precios y cupos separados en `package_departures`. |
| **RF-04** | Alta | Registrar clientes e iniciar sesión con credenciales seguras. | El cliente accede a su perfil y solo visualiza/gestiona sus propias reservas. |
| **RF-05** | Alta | Reservar paquetes para uno o más pasajeros validando cupos disponibles. | Si `cupos_disponibles >= pasajeros`, confirma la reserva, congela `contracted_unit_price` y descuenta cupos. |
| **RF-06** | Media | Registrar avance por etapas del viaje y consultar pasajeros por paquete/período/estado. | El administrador actualiza `passenger_stage_progress` con fecha y responsable; las consultas reflejan el estado actualizado. |

## Requerimientos No Funcionales (RNF)
| ID | Prioridad | Categoría | Descripción | Criterio de Aceptación |
| :--- | :--- | :--- | :--- | :--- |
| **RNF-01** | Alta | Seguridad | Almacenar contraseñas de usuarios como hashes criptográficos. | La columna `password_hash` nunca contiene texto plano. |
| **RNF-02** | Alta | Arquitectura | Separar presentación, servicios/negocio, dominio y persistencia. | Las consultas SQL residen exclusivamente en `src/persistence/` y las reglas de negocio en `src/services/` y `src/domain/`. |
| **RNF-03** | Alta | Portabilidad | Soportar ejecución con SQLite y MySQL (incluyendo WampServer MySQL 5.7+/MariaDB). | Al cambiar `DB_ENGINE` en `.env`, el flujo funciona sin modificar el código fuente. |
| **RNF-04** | Media | Mantenibilidad | Código fuente y SQL en inglés; mensajes e interfaz al usuario en español. | Todas las clases, métodos, variables y tablas están en inglés; menús y errores mostrados en español. |
