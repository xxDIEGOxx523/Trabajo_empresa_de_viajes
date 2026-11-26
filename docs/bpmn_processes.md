# Procesos BPMN — Viajes Aventura (Sprint 2)

En la carpeta `docs/bpmn/` se encuentran tanto los **diagramas visuales listos para presentar** (`.png` y `.svg`) como sus **archivos editables** (`.puml`) para los tres hitos funcionales exigidos en la Semana 2:

1. **BPMN 1 — Gestión de Destinos (`docs/bpmn/bpmn_1_gestion_destinos.png`)**
   * **Carriles:** Administrador | Sistema Viajes Aventura
   * **Decisiones:** `¿Datos válidos?` (ciclo de corrección ante datos vacíos, costos negativos o duplicados) y `¿Es retiro lógico?` (actualiza `is_active = 0` conservando viajes históricos).
2. **BPMN 2 — Preparación de Paquetes Turísticos (`docs/bpmn/bpmn_2_preparacion_paquetes.png`)**
   * **Carriles:** Administrador | Sistema Viajes Aventura
   * **Decisiones:** `¿>= 2 destinos activos?` antes de guardar el itinerario (`itinerary_stops`) y habilitar la programación de salidas (`package_departures`) con fechas, tarifa y cupos independientes.
3. **BPMN 3 — Reservas y Seguimiento del Viaje (`docs/bpmn/bpmn_3_reservas_seguimiento.png`)**
   * **Carriles:** Cliente | Sistema Viajes Aventura | Administrador
   * **Decisiones:** `¿Cupos disponibles >= N pasajeros?` (si aprueba, congela `contracted_unit_price` y registra pasajeros) y ciclo de seguimiento `¿Etapas listas?` donde el administrador registra avances en `passenger_stage_progress`.
