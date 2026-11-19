"""DAO de acceso a la tabla DESTINATIONS."""
from .base_dao import BaseDAO


class DestinationDAO(BaseDAO):
    TABLE = "DESTINATIONS"
    COLUMNS = ('id', 'name', 'country', 'city', 'description', 'base_cost', 'is_active')
