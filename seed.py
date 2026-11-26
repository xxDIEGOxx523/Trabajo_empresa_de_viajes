from src.persistence.dao_factory import DAOFactory
from src.persistence.database import DatabaseConnection
from src.services.destination_service import DestinationService


SAMPLE_DESTINATIONS = [
    ("Santiago", "Chile", "Capital andina con viñedos y oferta cultural.", 120000.0),
    ("Buenos Aires", "Argentina", "Gastronomía, arquitectura y tango.", 185000.0),
    ("Mendoza", "Argentina", "Ruta del vino y cordillera de los Andes.", 150000.0),
]


def run_seed() -> None:
    db = DatabaseConnection()
    db.initialize_schema()

    factory = DAOFactory(db)
    service = DestinationService(factory.get_destination_dao())

    print(f"Cargando datos iniciales en motor: {db.engine.upper()}")
    for name, country, description, cost in SAMPLE_DESTINATIONS:
        try:
            created = service.register_destination(name, country, description, cost)
            print(f"  [+] Registrado: {created.name} ({created.country}) - ID {created.id}")
        except ValueError as error:
            print(f"  [=] Omitido ({name}): {error}")

    print("\nDestinos activos actuales:")
    for item in service.list_destinations(include_retired=False):
        print(f"  - [{item.id}] {item.name}, {item.country} (${item.base_cost:,.0f})")


if __name__ == "__main__":
    run_seed()
