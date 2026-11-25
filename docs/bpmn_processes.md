# Procesos BPMN - Viajes Aventura (Sprint 2)

Este documento describe los tres procesos principales exigidos en la Semana 2, incluyendo roles (swimlanes), compuertas de decisión y resultados.

---

## 1. BPMN Gestión de Destinos (Hito 1)
* **Carriles:** Administrador | Sistema Viajes Aventura
* **Flujo:**
  1. *(Administrador)* Ingresa nombre, país, descripción y costo base.
  2. *(Sistema)* Valida obligatoriedad de nombre/país, costo >= 0 y unicidad `(name, country)`.
  3. **[Compuerta exclusiva ¿Datos válidos?]**
     * **No:** Muestra mensaje de corrección -> regresa al paso 1.
     * **Sí:** Persiste el destino con `is_active = 1` y muestra confirmación.
  4. *(Retiro)* Cuando el administrador retira un destino, el sistema actualiza `is_active = 0` para impedir nuevos paquetes sin alterar viajes históricos.

---

## 2. BPMN Preparación de Paquetes Turísticos (Hito 2)
* **Carriles:** Administrador | Sistema Viajes Aventura
* **Flujo:**
  1. *(Administrador)* Crea paquete y selecciona destinos activos con su orden de visita (`visit_order`).
  2. *(Sistema)* Verifica que el itinerario tenga al menos **2 destinos activos**.
  3. **[Compuerta exclusiva ¿Itinerario válido (>= 2)?]**
     * **No:** Solicita agregar más destinos.
     * **Sí:** Permite crear salidas (`package_departures`) con fecha inicio/fin, precio y cupos máximos (`max_capacity`).
  4. *(Sistema)* Publica la salida con estado `OPEN`.

---

## 3. BPMN Reservas y Seguimiento de Viaje (Hito 3)
* **Carriles:** Cliente | Sistema Viajes Aventura | Administrador
* **Flujo:**
  1. *(Cliente)* Inicia sesión, elige una salida (`package_departure`) e ingresa los datos de N pasajeros.
  2. *(Sistema)* Calcula cupos disponibles: `max_capacity - pasajeros_confirmados`.
  3. **[Compuerta exclusiva ¿Cupos >= N?]**
     * **No:** Rechaza solicitud informando cupos restantes.
     * **Sí:** Congela el precio unitario (`contracted_unit_price`), guarda reserva `CONFIRMED`, registra pasajeros (`PENDING`) e inicializa etapas en `passenger_stage_progress`.
  4. *(Administrador)* Durante el viaje actualiza el estado de cada etapa (`IN_PROGRESS` / `COMPLETED`) registrando fecha y responsable (`updated_by_admin_id`).
