from src.persistence.database import DatabaseConnection
from src.persistence.destination_dao import DestinationDAO
from src.services.destination_service import DestinationService
from src.ui.console_ui import ConsoleUI


def main() -> None:
    db = DatabaseConnection()
    db.initialize_schema()

    destination_dao = DestinationDAO(db)
    destination_service = DestinationService(destination_dao)

    app = ConsoleUI(destination_service=destination_service, db_engine=db.engine)
    app.run()


if __name__ == "__main__":
    main()
