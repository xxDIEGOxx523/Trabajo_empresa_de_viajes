"""Fábrica central de los DAO de Viajes Aventura."""
from .customer_dao import CustomerDAO
from .destination_dao import DestinationDAO
from .package_dao import PackageDAO
from .package_destination_dao import PackageDestinationDAO
from .reservation_dao import ReservationDAO


class DAOFactory:
    def __init__(self):
        self._customer_dao = CustomerDAO()
        self._destination_dao = DestinationDAO()
        self._package_dao = PackageDAO()
        self._package_destination_dao = PackageDestinationDAO()
        self._reservation_dao = ReservationDAO()

    def get_customer_dao(self):
        return self._customer_dao

    def get_destination_dao(self):
        return self._destination_dao

    def get_package_dao(self):
        return self._package_dao

    def get_package_destination_dao(self):
        return self._package_destination_dao

    def get_reservation_dao(self):
        return self._reservation_dao
