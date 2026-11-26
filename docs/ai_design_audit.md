# Auditoría de Diseño con IA — Semana 2 (IA como Auditora)

## 1. Regla y Fragmento Evaluado
* **Regla:** *"Un destino retirado deja de ofrecerse para nuevos paquetes, pero los viajes anteriores conservan su información."*
* **Fragmento:** Tabla `destinations` con atributo booleano `is_active` y clave foránea `itinerary_stops.destination_id -> destinations.id`.

## 2. Escenario Límite Detectado
* **Observación:** ¿Qué ocurre si un administrador intenta agregar un destino previamente retirado (`is_active = 0`) al armar un nuevo paquete turístico?
* **Prueba con datos ficticios:**
  1. Se registran *Santiago*, *Buenos Aires* y *Mendoza* (`is_active = 1`).
  2. Se retira *Mendoza* (`is_active = 0`).
  3. Al intentar ejecutar `TravelPackage.add_stop(mendoza, visit_order=2)`, el método de dominio valida `if not destination.is_active` y lanza un `ValueError`, bloqueando el uso de destinos retirados en ofertas nuevas.

## 3. Decisión del Equipo y Justificación
* **Decisión:** **Aceptada e incorporada al diseño.**
* **Justificación:** Garantiza consistencia entre las reglas del negocio, el modelo de dominio (`TravelPackage.add_stop`) y la persistencia, protegiendo tanto las ofertas futuras como el historial pasado.
