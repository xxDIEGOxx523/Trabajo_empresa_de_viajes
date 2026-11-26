# Validación del Modelo Físico v2 — 10 Preguntas de Control

## Oferta y Reservas (Lámina 11)
1. **¿Qué paquetes usan un destino que deja de ofrecerse?**
   ```sql
   SELECT p.id, p.name AS package_name, d.name AS retired_destination
   FROM itinerary_stops s
   JOIN travel_packages p ON p.id = s.package_id
   JOIN destinations d ON d.id = s.destination_id
   WHERE d.is_active = 0;
   ```
2. **¿Qué destinos incluye el paquete X y en qué orden se visitan?**
   ```sql
   SELECT s.visit_order, d.name, d.country
   FROM itinerary_stops s
   JOIN destinations d ON d.id = s.destination_id
   WHERE s.package_id = :package_id
   ORDER BY s.visit_order ASC;
   ```
3. **¿El mismo paquete tiene cupos independientes para distintas fechas?**
   Sí. Cada fecha de salida se almacena como una fila independiente en `package_departures` con su propio `max_capacity` y `price`.
4. **¿Quién realizó la reserva y qué personas viajarán?**
   El titular se obtiene desde `reservations.customer_id -> customers` y la nómina completa de viajeros desde `reservation_passengers` filtrando por `reservation_id`.
5. **¿Cómo calculan los cupos disponibles antes de confirmar?**
   Restando a `package_departures.max_capacity` la cantidad de registros en `reservation_passengers` pertenecientes a reservas con `status = 'CONFIRMED'` para esa salida (`departure_id`).

## Avance e Historial (Lámina 12)
6. **¿Cuántos pasajeros están pendientes, viajando o con viaje finalizado?**
   ```sql
   SELECT trip_status, COUNT(*) AS total_passengers
   FROM reservation_passengers
   GROUP BY trip_status;
   ```
7. **¿Qué etapas completó una persona y cuál está cursando?**
   ```sql
   SELECT s.visit_order, d.name AS destination, psp.stage_status, psp.updated_at
   FROM passenger_stage_progress psp
   JOIN itinerary_stops s ON s.id = psp.stop_id
   JOIN destinations d ON d.id = s.destination_id
   WHERE psp.passenger_id = :passenger_id
   ORDER BY s.visit_order ASC;
   ```
8. **¿Cada reserva conserva avances, fechas y responsables propios?**
   Sí. `passenger_stage_progress` registra individualmente `stage_status`, `updated_at` y `updated_by_admin_id` por pasajero y parada del itinerario.
9. **¿Cuántas personas usaron el paquete X durante un período?**
   ```sql
   SELECT COUNT(rp.id) AS total_travelers
   FROM reservation_passengers rp
   JOIN reservations r ON r.id = rp.reservation_id
   JOIN package_departures pd ON pd.id = r.departure_id
   WHERE pd.package_id = :package_id
     AND r.status = 'CONFIRMED'
     AND pd.start_date BETWEEN :from_date AND :to_date;
   ```
10. **¿Pueden recuperar el precio y el itinerario de una reserva anterior?**
    Sí. `reservations.contracted_unit_price` congela la tarifa vigente al momento de la compra y el retiro lógico de destinos (`is_active = 0`) impide eliminar registros referenciados por viajes pasados.
