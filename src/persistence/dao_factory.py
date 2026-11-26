from src.persistence.database import DatabaseConnection
from src.persistence.destination_dao import DestinationDAO


class DAOFactory:
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db

    def get_destination_dao(self) -> DestinationDAO:
        return DestinationDAO(self.db)
