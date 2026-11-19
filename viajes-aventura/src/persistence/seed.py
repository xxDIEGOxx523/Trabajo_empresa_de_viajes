"""Carga datos ficticios de demostración en la base de datos.

Ejecutar desde la raíz del proyecto:
    python -m src.persistence.seed

La carga es idempotente: usa INSERT OR IGNORE para no duplicar los
registros al ejecutar el comando más de una vez.
"""

from __future__ import annotations

import hashlib
import secrets
import sqlite3
from datetime import datetime

from src.persistence.database import Database


DEMO_PASSWORD = "Demo1234!"
PBKDF2_ITERATIONS = 310_000


CUSTOMERS = [
    (1, "Camila Rojas", "camila.rojas@example.com", "+56911110001"),
    (2, "Matías González", "matias.gonzalez@example.com", "+56911110002"),
    (3, "Valentina Muñoz", "valentina.munoz@example.com", "+56911110003"),
    (4, "Benjamín Soto", "benjamin.soto@example.com", "+56911110004"),
    (5, "Isidora Fernández", "isidora.fernandez@example.com", "+56911110005"),
    (6, "Tomás Contreras", "tomas.contreras@example.com", "+56911110006"),
    (7, "Catalina Silva", "catalina.silva@example.com", "+56911110007"),
    (8, "Vicente Morales", "vicente.morales@example.com", "+56911110008"),
    (9, "Florencia Herrera", "florencia.herrera@example.com", "+56911110009"),
    (10, "Lucas Torres", "lucas.torres@example.com", "+56911110010"),
]

DESTINATIONS = [
    (1, "Valle de la Luna", "Chile", "San Pedro de Atacama", "Paisajes desérticos y atardeceres", 85000),
    (2, "Torres del Paine", "Chile", "Puerto Natales", "Parque nacional y senderos panorámicos", 160000),
    (3, "Reloj de Flores", "Chile", "Viña del Mar", "Sector costero y atractivos urbanos", 35000),
    (4, "Lago Villarrica", "Chile", "Pucón", "Actividades al aire libre junto al lago", 70000),
    (5, "Parque Nacional Chiloé", "Chile", "Castro", "Bosques, costa y cultura chilota", 65000),
    (6, "Faro Monumental", "Chile", "La Serena", "Recorrido por el borde costero", 30000),
    (7, "Rano Kau", "Chile", "Rapa Nui", "Paisaje volcánico y patrimonio cultural", 190000),
    (8, "Lago Llanquihue", "Chile", "Puerto Varas", "Vistas al lago y volcanes", 75000),
    (9, "Embalse El Yeso", "Chile", "San José de Maipo", "Paisaje cordillerano", 55000),
    (10, "Observatorio Mamalluca", "Chile", "Vicuña", "Experiencia de observación astronómica", 60000),
]

PACKAGES = [
    (1, "Desierto y estrellas", "Experiencia por el desierto de Atacama", "2027-01-10", "2027-01-14", 145000, 12, "available"),
    (2, "Patagonia natural", "Paisajes y naturaleza de la Patagonia", "2027-02-05", "2027-02-10", 260000, 10, "available"),
    (3, "Costa central", "Recorrido por atractivos de la costa central", "2027-01-20", "2027-01-23", 110000, 15, "available"),
    (4, "Aventura en Pucón", "Descanso y actividades junto al lago", "2027-03-02", "2027-03-06", 130000, 12, "available"),
    (5, "Ruta de Chiloé", "Cultura y naturaleza del archipiélago", "2027-02-15", "2027-02-19", 125000, 10, "available"),
    (6, "Escapada serenense", "Recorrido costero por La Serena", "2027-01-08", "2027-01-11", 80000, 15, "available"),
    (7, "Rapa Nui cultural", "Visita a paisajes y sitios culturales", "2027-04-10", "2027-04-15", 320000, 8, "available"),
    (8, "Lagos del sur", "Paisajes de Puerto Varas y alrededores", "2027-03-12", "2027-03-16", 150000, 12, "available"),
    (9, "Cordillera cercana", "Salida panorámica a la cordillera", "2027-02-22", "2027-02-24", 95000, 14, "available"),
    (10, "Cielos del Elqui", "Turismo de naturaleza y astronomía", "2027-03-20", "2027-03-23", 115000, 12, "available"),
]

PACKAGE_DESTINATIONS = [
    (1, 1, 1), (1, 10, 2),
    (2, 2, 1), (2, 5, 2),
    (3, 3, 1), (3, 6, 2),
    (4, 4, 1), (4, 9, 2),
    (5, 5, 1), (5, 8, 2),
    (6, 6, 1), (6, 3, 2),
    (7, 7, 1), (7, 1, 2),
    (8, 8, 1), (8, 4, 2),
    (9, 9, 1), (9, 2, 2),
    (10, 10, 1), (10, 1, 2),
]

RESERVATIONS = [
    (1, 1, 1, 2, 290000, "confirmed"),
    (2, 2, 2, 3, 780000, "confirmed"),
    (3, 3, 3, 2, 220000, "confirmed"),
    (4, 4, 4, 4, 520000, "confirmed"),
    (5, 5, 5, 2, 250000, "confirmed"),
    (6, 6, 6, 3, 240000, "confirmed"),
    (7, 7, 7, 2, 640000, "confirmed"),
    (8, 8, 8, 2, 300000, "confirmed"),
    (9, 9, 9, 4, 380000, "confirmed"),
    (10, 10, 10, 2, 230000, "confirmed"),
]


def hash_demo_password(password: str) -> str:
    """Devuelve un hash PBKDF2 con sal aleatoria, nunca la clave en texto plano."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def seed_database() -> dict[str, int]:
    database = Database()
    database.create_schema()
    connection = database.connect()
    insert_ignore = "INSERT OR IGNORE" if database.backend == "sqlite" else "INSERT IGNORE"

    try:
        now = datetime.now().isoformat(timespec="seconds")
        customer_rows = [
            (customer_id, full_name, email, phone, hash_demo_password(DEMO_PASSWORD), now, 1)
            for customer_id, full_name, email, phone in CUSTOMERS
        ]

        connection.executemany(
            f"""{insert_ignore} INTO CUSTOMERS
               (id, full_name, email, phone, password_hash, created_at, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            customer_rows,
        )
        connection.executemany(
            f"""{insert_ignore} INTO DESTINATIONS
               (id, name, country, city, description, base_cost, is_active)
               VALUES (?, ?, ?, ?, ?, ?, 1)""",
            DESTINATIONS,
        )
        connection.executemany(
            f"""{insert_ignore} INTO PACKAGES
               (id, name, description, start_date, end_date, total_cost, max_capacity, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            PACKAGES,
        )
        connection.executemany(
            f"""{insert_ignore} INTO PACKAGE_DESTINATIONS
               (package_id, destination_id, display_order)
               VALUES (?, ?, ?)""",
            PACKAGE_DESTINATIONS,
        )
        connection.executemany(
            f"""{insert_ignore} INTO RESERVATIONS
               (id, customer_id, package_id, reservation_date, number_of_people, total_price, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (reservation_id, customer_id, package_id, now, people, total_price, status)
                for reservation_id, customer_id, package_id, people, total_price, status in RESERVATIONS
            ],
        )
        connection.commit()

        table_names = (
            "CUSTOMERS",
            "DESTINATIONS",
            "PACKAGES",
            "PACKAGE_DESTINATIONS",
            "RESERVATIONS",
        )
        counts = {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in table_names
        }
        return counts
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    try:
        counts = seed_database()
    except (sqlite3.Error, OSError, ValueError, RuntimeError) as error:
        print(f"No se pudo cargar la semilla: {error}")
        raise SystemExit(1) from error

    print(f"Semilla cargada correctamente en {Database().backend.upper()}.")
    for table, count in counts.items():
        print(f"- {table}: {count} registros")
    print(f"Clave de demostración para los 10 clientes: {DEMO_PASSWORD}")
    print("Usar estas credenciales solo en el entorno local de pruebas.")


if __name__ == "__main__":
    main()
