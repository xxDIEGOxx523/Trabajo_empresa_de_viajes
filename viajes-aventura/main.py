"""Punto de entrada principal de Viajes Aventura."""
from src.persistencia.conexion import obtener_motor
from src.persistencia.dao_factory import DAOFactory
from src.servicios.gestion_destinos import GestionDestinos
from src.servicios.gestion_paquetes import GestionPaquetes
from src.servicios.gestion_reservas import GestionReservas
from src.ux.interfaz import TerminalInterface
from semilla import cargar_semilla, imprimir_resumen


def main():
    try:
        print(f"Preparando base de datos ({obtener_motor().upper()})...")
        print("Cargando datos de demostración...")
        resumen = cargar_semilla()
        imprimir_resumen(resumen)

        factory = DAOFactory()
        app = TerminalInterface(
            GestionDestinos(factory.get_destination_dao()),
            GestionPaquetes(factory.get_package_dao()),
            GestionReservas(factory.get_reservation_dao()),
        )
        app.iniciar()
    except Exception as error:
        print("No fue posible iniciar Viajes Aventura.")
        print("Revise el archivo .env, DB_BACKEND, el servicio de base de datos y requirements.txt.")
        print(f"Detalle técnico: {error}")


if __name__ == "__main__":
    main()
