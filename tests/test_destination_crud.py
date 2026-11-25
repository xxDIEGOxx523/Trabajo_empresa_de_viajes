import os
import tempfile
import unittest

from src.persistence.database import DatabaseConnection
from src.persistence.destination_dao import DestinationDAO
from src.services.destination_service import DestinationService


class TestDestinationCRUD(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_fd)
        self.db = DatabaseConnection(engine="sqlite", sqlite_path=self.temp_db_path)
        self.db.initialize_schema()
        self.dao = DestinationDAO(self.db)
        self.service = DestinationService(self.dao)

    def tearDown(self) -> None:
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_full_crud_lifecycle_and_persistence(self) -> None:
        # Create 3 destinations (from PPT Milestone 1)
        santiago = self.service.register_destination("Santiago", "Chile", "Cordillera", 120000)
        buenos_aires = self.service.register_destination("Buenos Aires", "Argentina", "Tango", 185000)
        mendoza = self.service.register_destination("Mendoza", "Argentina", "Vinos", 150000)

        self.assertEqual(len(self.service.list_destinations()), 3)

        # Update
        updated = self.service.update_destination(
            mendoza.id, "Mendoza", "Argentina", "Ruta del vino premium", 165000
        )
        self.assertEqual(updated.base_cost, 165000)

        # Logical delete (retire)
        self.service.retire_destination(buenos_aires.id)
        self.assertEqual(len(self.service.list_destinations(include_retired=False)), 2)
        self.assertEqual(len(self.service.list_destinations(include_retired=True)), 3)

        # Reactivate
        self.service.reactivate_destination(buenos_aires.id)
        self.assertEqual(len(self.service.list_destinations(include_retired=False)), 3)

        # Verify persistence with a brand-new connection
        new_db = DatabaseConnection(engine="sqlite", sqlite_path=self.temp_db_path)
        new_service = DestinationService(DestinationDAO(new_db))
        persisted = new_service.find_destination(santiago.id)
        self.assertEqual(persisted.name, "Santiago")

    def test_validation_and_duplicate_rejection(self) -> None:
        self.service.register_destination("Santiago", "Chile", "Desc", 100000)
        with self.assertRaises(ValueError):
            self.service.register_destination("santiago", "chile", "Dup", 90000)
        with self.assertRaises(ValueError):
            self.service.register_destination("", "Chile", "No name", 10000)
        with self.assertRaises(ValueError):
            self.service.register_destination("Valparaiso", "Chile", "Neg", -500)


if __name__ == "__main__":
    unittest.main()
