"""Carga idempotente de datos ficticios para Viajes Aventura.

Ejecutar desde la raíz: python semilla.py
La misma semilla funciona con SQLite y MySQL.
"""
from datetime import datetime
import hashlib
import secrets
import sqlite3

from src.persistencia.conexion import obtener_motor
from src.persistencia.crear_db import crear_base_y_tablas
from src.persistencia.dao_factory import DAOFactory

DEMO_PASSWORD = "Demo1234!"
PBKDF2_ITERATIONS = 310_000

CUSTOMERS = [(1, 'Camila Rojas', 'camila.rojas@example.com', '+56911110001'),
 (2, 'Matías González', 'matias.gonzalez@example.com', '+56911110002'),
 (3, 'Valentina Muñoz', 'valentina.munoz@example.com', '+56911110003'),
 (4, 'Benjamín Soto', 'benjamin.soto@example.com', '+56911110004'),
 (5, 'Isidora Fernández', 'isidora.fernandez@example.com', '+56911110005'),
 (6, 'Tomás Contreras', 'tomas.contreras@example.com', '+56911110006'),
 (7, 'Catalina Silva', 'catalina.silva@example.com', '+56911110007'),
 (8, 'Vicente Morales', 'vicente.morales@example.com', '+56911110008'),
 (9, 'Florencia Herrera', 'florencia.herrera@example.com', '+56911110009'),
 (10, 'Lucas Torres', 'lucas.torres@example.com', '+56911110010')]

DESTINATIONS = [(1,
  'Valle de la Luna',
  'Chile',
  'San Pedro de Atacama',
  'Paisajes desérticos y atardeceres',
  85000),
 (2,
  'Torres del Paine',
  'Chile',
  'Puerto Natales',
  'Parque nacional y senderos panorámicos',
  160000),
 (3, 'Reloj de Flores', 'Chile', 'Viña del Mar', 'Sector costero y atractivos urbanos', 35000),
 (4, 'Lago Villarrica', 'Chile', 'Pucón', 'Actividades al aire libre junto al lago', 70000),
 (5, 'Parque Nacional Chiloé', 'Chile', 'Castro', 'Bosques, costa y cultura chilota', 65000),
 (6, 'Faro Monumental', 'Chile', 'La Serena', 'Recorrido por el borde costero', 30000),
 (7, 'Rano Kau', 'Chile', 'Rapa Nui', 'Paisaje volcánico y patrimonio cultural', 190000),
 (8, 'Lago Llanquihue', 'Chile', 'Puerto Varas', 'Vistas al lago y volcanes', 75000),
 (9, 'Embalse El Yeso', 'Chile', 'San José de Maipo', 'Paisaje cordillerano', 55000),
 (10, 'Observatorio Mamalluca', 'Chile', 'Vicuña', 'Experiencia de observación astronómica', 60000)]

PACKAGES = [(1,
  'Desierto y estrellas',
  'Experiencia por el desierto de Atacama',
  '2027-01-10',
  '2027-01-14',
  145000,
  12,
  'available'),
 (2,
  'Patagonia natural',
  'Paisajes y naturaleza de la Patagonia',
  '2027-02-05',
  '2027-02-10',
  260000,
  10,
  'available'),
 (3,
  'Costa central',
  'Recorrido por atractivos de la costa central',
  '2027-01-20',
  '2027-01-23',
  110000,
  15,
  'available'),
 (4,
  'Aventura en Pucón',
  'Descanso y actividades junto al lago',
  '2027-03-02',
  '2027-03-06',
  130000,
  12,
  'available'),
 (5,
  'Ruta de Chiloé',
  'Cultura y naturaleza del archipiélago',
  '2027-02-15',
  '2027-02-19',
  125000,
  10,
  'available'),
 (6,
  'Escapada serenense',
  'Recorrido costero por La Serena',
  '2027-01-08',
  '2027-01-11',
  80000,
  15,
  'available'),
 (7,
  'Rapa Nui cultural',
  'Visita a paisajes y sitios culturales',
  '2027-04-10',
  '2027-04-15',
  320000,
  8,
  'available'),
 (8,
  'Lagos del sur',
  'Paisajes de Puerto Varas y alrededores',
  '2027-03-12',
  '2027-03-16',
  150000,
  12,
  'available'),
 (9,
  'Cordillera cercana',
  'Salida panorámica a la cordillera',
  '2027-02-22',
  '2027-02-24',
  95000,
  14,
  'available'),
 (10,
  'Cielos del Elqui',
  'Turismo de naturaleza y astronomía',
  '2027-03-20',
  '2027-03-23',
  115000,
  12,
  'available')]

PACKAGE_DESTINATIONS = [(1, 1, 1),
 (1, 10, 2),
 (2, 2, 1),
 (2, 5, 2),
 (3, 3, 1),
 (3, 6, 2),
 (4, 4, 1),
 (4, 9, 2),
 (5, 5, 1),
 (5, 8, 2),
 (6, 6, 1),
 (6, 3, 2),
 (7, 7, 1),
 (7, 1, 2),
 (8, 8, 1),
 (8, 4, 2),
 (9, 9, 1),
 (9, 2, 2),
 (10, 10, 1),
 (10, 1, 2)]

RESERVATIONS = [(1, 1, 1, 2, 290000, 'confirmed'),
 (2, 2, 2, 3, 780000, 'confirmed'),
 (3, 3, 3, 2, 220000, 'confirmed'),
 (4, 4, 4, 4, 520000, 'confirmed'),
 (5, 5, 5, 2, 250000, 'confirmed'),
 (6, 6, 6, 3, 240000, 'confirmed'),
 (7, 7, 7, 2, 640000, 'confirmed'),
 (8, 8, 8, 2, 300000, 'confirmed'),
 (9, 9, 9, 4, 380000, 'confirmed'),
 (10, 10, 10, 2, 230000, 'confirmed')]


def hash_demo_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def cargar_semilla(factory=None):
    crear_base_y_tablas()
    factory = factory or DAOFactory()
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clientes = [
        (customer_id, full_name, email, phone, hash_demo_password(DEMO_PASSWORD), ahora, 1)
        for customer_id, full_name, email, phone in CUSTOMERS
    ]
    destinos = [(*fila, 1) for fila in DESTINATIONS]
    paquetes = PACKAGES
    relaciones = PACKAGE_DESTINATIONS
    reservas = [
        (reservation_id, customer_id, package_id, ahora, people, total_price, status)
        for reservation_id, customer_id, package_id, people, total_price, status in RESERVATIONS
    ]

    resumen = {
        "CUSTOMERS": factory.get_customer_dao().insertar_lote(clientes),
        "DESTINATIONS": factory.get_destination_dao().insertar_lote(destinos),
        "PACKAGES": factory.get_package_dao().insertar_lote(paquetes),
        "PACKAGE_DESTINATIONS": factory.get_package_destination_dao().insertar_lote(relaciones),
        "RESERVATIONS": factory.get_reservation_dao().insertar_lote(reservas),
    }
    # Los conteos muestran el total de cada tabla, incluidos registros previos del usuario.
    resumen_total = {
        "CUSTOMERS": factory.get_customer_dao().contar(),
        "DESTINATIONS": factory.get_destination_dao().contar(),
        "PACKAGES": factory.get_package_dao().contar(),
        "PACKAGE_DESTINATIONS": factory.get_package_destination_dao().contar(),
        "RESERVATIONS": factory.get_reservation_dao().contar(),
    }
    return {"insertados": resumen, "totales": resumen_total}


def imprimir_resumen(resumen):
    print(f"Semilla ejecutada correctamente en {obtener_motor().upper()}.")
    print("Registros totales por tabla:")
    for tabla, cantidad in resumen["totales"].items():
        print(f"- {tabla}: {cantidad}")
    print("La contraseña de demostración para los 10 clientes es: Demo1234!")
    print("Se almacena como hash PBKDF2-SHA256; úsela solo en pruebas locales.")


def main():
    try:
        resumen = cargar_semilla()
    except (sqlite3.Error, OSError, ValueError, RuntimeError) as error:
        print(f"No se pudo cargar la semilla: {error}")
        raise SystemExit(1) from error
    imprimir_resumen(resumen)


if __name__ == "__main__":
    main()
