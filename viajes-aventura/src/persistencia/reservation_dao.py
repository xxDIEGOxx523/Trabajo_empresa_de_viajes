"""DAO de acceso a la tabla RESERVATIONS."""
from .base_dao import BaseDAO


class ReservationDAO(BaseDAO):
    TABLE = "RESERVATIONS"
    COLUMNS = ('id', 'customer_id', 'package_id', 'reservation_date', 'number_of_people', 'total_price', 'status')
