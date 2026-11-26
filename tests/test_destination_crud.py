import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

from src.persistence.dao_factory import DAOFactory
from src.persistence.database import DatabaseConnection
from src.services.destination_service import DestinationService


class TestDestinationCRUD(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_fd)
        self.db = DatabaseConnection(engine="sqlite", sqlite_path=self.temp_db_path)
        self.db.initialize_schema()
        factory = DAOFactory(self.db)
        self.service = DestinationService(factory.get_destination_dao())

    def tearDown(self) -> None:
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_full_crud_lifecycle_and_persistence(self) -> None:
        santiago = self.service.register_destination(
            "Santiago", "Chile", "Cordillera y viñedos", 120000
        )
        buenos_aires = self.service.register_destination(
            "Buenos Aires", "Argentina", "Tango y gastronomía", 185000
        )
        mendoza = self.service.register_destination(
            "Mendoza", "Argentina", "Ruta del vino", 150000
        )

        self.assertEqual(len(self.service.list_destinations()), 3)

        argentina_results = self.service.search_destinations("Argentina")
        self.assertEqual(len(argentina_results), 2)

        updated = self.service.update_destination(
            mendoza.id, "Mendoza", "Argentina", "Ruta del vino premium", 165000
        )
        self.assertEqual(updated.base_cost, 165000)

        self.service.retire_destination(buenos_aires.id)
        self.assertEqual(len(self.service.list_destinations(include_retired=False)), 2)
        self.assertEqual(len(self.service.list_destinations(include_retired=True)), 3)

        self.service.reactivate_destination(buenos_aires.id)
        self.assertEqual(len(self.service.list_destinations(include_retired=False)), 3)

        reopened_db = DatabaseConnection(engine="sqlite", sqlite_path=self.temp_db_path)
        reopened_service = DestinationService(
            DAOFactory(reopened_db).get_destination_dao()
        )
        persisted = reopened_service.find_destination(santiago.id)
        self.assertEqual(persisted.name, "Santiago")
        self.assertEqual(persisted.country, "Chile")

    def test_validation_and_duplicate_rejection(self) -> None:
        self.service.register_destination("Santiago", "Chile", "Desc", 100000)

        with self.assertRaises(ValueError):
            self.service.register_destination("santiago", "chile", "Duplicado", 90000)

        with self.assertRaises(ValueError):
            self.service.register_destination("", "Chile", "Sin nombre", 10000)
        with self.assertRaises(ValueError):
            self.service.register_destination("Valparaiso", "   ", "Sin país", 10000)

        with self.assertRaises(ValueError):
            self.service.register_destination("Valparaiso", "Chile", "Negativo", -500)

        with self.assertRaises(LookupError):
            self.service.find_destination(9999)

    def test_mysql_connection_uses_wampserver_compatible_collation(self) -> None:
        mock_mysql_pkg = MagicMock()
        mock_connector = mock_mysql_pkg.connector
        with patch.dict("sys.modules", {"mysql": mock_mysql_pkg, "mysql.connector": mock_connector}):
            db_mysql = DatabaseConnection(engine="mysql")
            db_mysql.get_connection()

            mock_connector.connect.assert_called_once()
            kwargs = mock_connector.connect.call_args.kwargs
            self.assertEqual(kwargs["charset"], "utf8mb4")
            self.assertEqual(kwargs["collation"], "utf8mb4_unicode_ci")


if __name__ == "__main__":
    unittest.main()
