import sys
from src.persistence.dao_factory import DAOFactory
from src.persistence.database import DatabaseConnection
from src.services.destination_service import DestinationService
from src.ui.console_ui import ConsoleUI


def main() -> None:
    db = DatabaseConnection()
    try:
        db.initialize_schema()
    except Exception as error:
        print(f"\n[Error de conexión con motor '{db.engine.upper()}']: {error}")
        if db.engine == "mysql":
            print(
                "Verifica que WampServer/MySQL esté activo, que la base de datos exista\n"
                "y que las credenciales en tu archivo .env sean correctas."
            )
        sys.exit(1)

    factory = DAOFactory(db)
    destination_service = DestinationService(factory.get_destination_dao())

    db_info = (
        db.sqlite_path
        if db.engine == "sqlite"
        else f"{db.mysql_charset} / {db.mysql_collation}"
    )
    app = ConsoleUI(
        destination_service=destination_service,
        db_engine=db.engine,
        db_info=db_info,
    )
    app.run()


if __name__ == "__main__":
    main()
