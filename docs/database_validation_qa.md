# Validación del Modelo Físico v2 (10 Preguntas)

## Oferta y Reservas
1. **¿Qué paquetes usan un destino que deja de ofrecerse?**
   Se consulta `itinerary_stops` unido a `travel_packages` y `destinations` filtrando por `destinations.is_active = 0`.
2. **¿Qué destinos incluye el paquete X y en qué orden se visitan?**
   `SELECT d.name, s.visit_order FROM itinerary_stops s JOIN destinations d ON d.id = s.destination_id WHERE s.package_id = X ORDER BY s.visit_order ASC;`
3. **¿El mismo paquete tiene cupos independientes para distintas fechas?**
   Sí. Cada fecha de salida es un registro distinto en `package_departures` con su propio `price` y `max_capacity`.
4. **¿Quién realizó la reserva y qué personas viajarán?**
   El titular está en `reservations.customer_id` (`customers`) y cada viajero en `reservation_passengers` vinculado por `reservation_id`.
5. **¿Cómo calculan los cupos disponibles antes de confirmar?**
   `package_departures.max_capacity` menos el total de filas en `reservation_passengers` cuyas reservas tienen `status = 'CONFIRMED'` para esa `departure_id`.

## Avance e Historial
6. **¿Cuántos pasajeros están pendientes, viajando o con viaje finalizado?**
   `SELECT trip_status, COUNT(*) FROM reservation_passengers GROUP BY trip_status;`
7. **¿Qué etapas completó una persona y cuál está cursando?**
   Consultando `passenger_stage_progress` por `passenger_id` unido a `itinerary_stops` y `destinations` ordenado por `visit_order`.
8. **¿Cada reserva conserva avances, fechas y responsables propios?**
   Sí. `passenger_stage_progress` guarda `stage_status`, `updated_at` y `updated_by_admin_id` por pasajero y etapa.
9. **¿Cuántas personas usaron el paquete X durante un período?**
   Contando `reservation_passengers.id` unidos a `reservations` y `package_departures` filtrando por `package_id = X` y `start_date BETWEEN fecha_inicio AND fecha_fin`.
10. **¿Pueden recuperar el precio y el itinerario de una reserva anterior?**
    Sí. `reservations.contracted_unit_price` congela el precio pactado al momento de reservar y el borrado lógico (`is_active = 0`) impide perder los destinos del itinerario.
