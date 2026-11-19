"""Prueba de integración de la semilla sobre SQLite."""
import os
import tempfile
import unittest
from pathlib import Path


class SeedSQLiteTest(unittest.TestCase):
    def test_seed_is_idempotent(self):
        with tempfile.TemporaryDirectory() as folder:
            os.environ["DB_BACKEND"] = "sqlite"
            os.environ["DB_PATH"] = str(Path(folder) / "test.db")

            from semilla import cargar_semilla

            first = cargar_semilla()
            second = cargar_semilla()

            expected = {
                "CUSTOMERS": 10,
                "DESTINATIONS": 10,
                "PACKAGES": 10,
                "PACKAGE_DESTINATIONS": 20,
                "RESERVATIONS": 10,
            }
            self.assertEqual(first["totales"], expected)
            self.assertEqual(second["totales"], expected)


if __name__ == "__main__":
    unittest.main()
