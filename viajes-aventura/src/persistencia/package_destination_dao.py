"""DAO de acceso a la tabla PACKAGE_DESTINATIONS."""
from .base_dao import BaseDAO


class PackageDestinationDAO(BaseDAO):
    TABLE = "PACKAGE_DESTINATIONS"
    COLUMNS = ('package_id', 'destination_id', 'display_order')
