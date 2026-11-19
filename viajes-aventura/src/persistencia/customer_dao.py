"""DAO de acceso a la tabla CUSTOMERS."""
from .base_dao import BaseDAO


class CustomerDAO(BaseDAO):
    TABLE = "CUSTOMERS"
    COLUMNS = ('id', 'full_name', 'email', 'phone', 'password_hash', 'created_at', 'is_active')
