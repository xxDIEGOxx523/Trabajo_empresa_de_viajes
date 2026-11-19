"""DAO de acceso a la tabla PACKAGES."""
from .base_dao import BaseDAO


class PackageDAO(BaseDAO):
    TABLE = "PACKAGES"
    COLUMNS = ('id', 'name', 'description', 'start_date', 'end_date', 'total_cost', 'max_capacity', 'status')
