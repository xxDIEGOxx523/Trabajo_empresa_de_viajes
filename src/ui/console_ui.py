import os
from typing import List, Optional
from src.domain.destination import Destination
from src.services.destination_service import DestinationService


class ConsoleUI:
    WIDTH = 76

    def __init__(self, destination_service: DestinationService, db_engine: str) -> None:
        self.destination_service = destination_service
        self.db_engine = db_engine.upper()

    def _clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _pause(self) -> None:
        input("\n  Presiona [ENTER] para continuar...")

    def _print_header(self, title: str, breadcrumb: str = "") -> None:
        self._clear_screen()
        print("=" * self.WIDTH)
        print(f"VIAJES AVENTURA  |  Motor BD: {self.db_engine}".center(self.WIDTH))
        print("-" * self.WIDTH)
        print(title.center(self.WIDTH))
        if breadcrumb:
            print(f"Ruta: {breadcrumb}".center(self.WIDTH))
        print("=" * self.WIDTH)

    def _print_destinations_table(self, destinations: List[Destination]) -> None:
        if not destinations:
            print("\n  [i] No hay destinos registrados para mostrar.")
            return

        print(
            f"\n  {'ID':<4} | {'Nombre':<18} | {'País':<14} | {'Costo Base':>12} | {'Estado':<10}"
        )
        print("  " + "-" * (self.WIDTH - 4))
        for dest in destinations:
            status_label = "Activo" if dest.is_active else "Retirado"
            cost_label = f"${dest.base_cost:,.0f}"
            print(
                f"  {dest.id:<4} | {dest.name[:18]:<18} | {dest.country[:14]:<14} | {cost_label:>12} | {status_label:<10}"
            )
        print("  " + "-" * (self.WIDTH - 4))
        print(f"  Total mostrado: {len(destinations)} destino(s).")

    def _read_float(self, prompt: str, default: Optional[float] = None) -> float:
        while True:
            raw = input(prompt).strip()
            if raw == "" and default is not None:
                return default
            try:
                value = float(raw)
                if value < 0:
                    print("  [!] El monto debe ser mayor o igual a 0.")
                    continue
                return value
            except ValueError:
                print("  [!] Ingresa un número válido.")

    def _read_int(self, prompt: str) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                return int(raw)
            except ValueError:
                print("  [!] Ingresa un número entero válido.")

    def run(self) -> None:
        while True:
            self._print_header("MENÚ PRINCIPAL", "Inicio")
            print("\n  [1] Gestión de Destinos")
            print("  [2] Gestión de Paquetes Turísticos")
            print("  [3] Reservas y Seguimiento de Viaje")
            print("  [0] Salir del sistema")

            option = input("\n  Selecciona una opción: ").strip()

            if option == "1":
                self._destinations_menu()
            elif option == "2":
                self._print_header("PAQUETES TURÍSTICOS", "Inicio > Paquetes")
                print("\n  [i] Este módulo integrará itinerarios de 2+ destinos, fechas y cupos.")
                print("  [i] Disponible en el siguiente incremento funcional (Sprint 3).")
                self._pause()
            elif option == "3":
                self._print_header("RESERVAS Y SEGUIMIENTO", "Inicio > Reservas")
                print("\n  [i] Este módulo gestionará pasajeros, cupos y avance por etapas.")
                print("  [i] Disponible en el siguiente incremento funcional (Sprint 3).")
                self._pause()
            elif option == "0":
                print("\n  ¡Hasta pronto! Gracias por usar Viajes Aventura.\n")
                break
            else:
                print("\n  [!] Opción no válida. Intenta nuevamente.")
                self._pause()

    def _destinations_menu(self) -> None:
        while True:
            self._print_header("GESTIÓN DE DESTINOS", "Inicio > Destinos")
            print("\n  [1] Listar destinos activos")
            print("  [2] Listar todos los destinos (activos y retirados)")
            print("  [3] Buscar destino por nombre o país")
            print("  [4] Ver detalle de un destino")
            print("  [5] Registrar nuevo destino")
            print("  [6] Modificar destino existente")
            print("  [7] Retirar destino (conserva historial)")
            print("  [8] Reactivar destino retirado")
            print("  [0] Volver al menú principal")

            option = input("\n  Selecciona una opción: ").strip()

            try:
                if option == "1":
                    self._handle_list(include_retired=False)
                elif option == "2":
                    self._handle_list(include_retired=True)
                elif option == "3":
                    self._handle_search()
                elif option == "4":
                    self._handle_detail()
                elif option == "5":
                    self._handle_create()
                elif option == "6":
                    self._handle_update()
                elif option == "7":
                    self._handle_retire()
                elif option == "8":
                    self._handle_reactivate()
                elif option == "0":
                    break
                else:
                    print("\n  [!] Opción no válida.")
                    self._pause()
            except Exception as error:
                print(f"\n  [Error] {error}")
                self._pause()

    def _handle_list(self, include_retired: bool) -> None:
        title = (
            "TODOS LOS DESTINOS (ACTIVOS Y RETIRADOS)"
            if include_retired
            else "DESTINOS ACTIVOS"
        )
        self._print_header(title, "Inicio > Destinos > Listado")
        destinations = self.destination_service.list_destinations(include_retired)
        self._print_destinations_table(destinations)
        self._pause()

    def _handle_search(self) -> None:
        self._print_header("BUSCAR DESTINOS", "Inicio > Destinos > Buscar")
        term = input("\n  Ingresa nombre o país a buscar: ")
        results = self.destination_service.search_destinations(term=term)
        self._print_destinations_table(results)
        self._pause()

    def _handle_detail(self) -> None:
        self._print_header("DETALLE DE DESTINO", "Inicio > Destinos > Detalle")
        dest_id = self._read_int("\n  ID del destino a consultar: ")
        dest = self.destination_service.find_destination(dest_id)
        status_label = "Activo" if dest.is_active else "Retirado"
        print("\n  " + "-" * 50)
        print(f"  ID          : {dest.id}")
        print(f"  Nombre      : {dest.name}")
        print(f"  País        : {dest.country}")
        print(f"  Costo base  : ${dest.base_cost:,.0f}")
        print(f"  Estado      : {status_label}")
        print(f"  Descripción : {dest.description or 'Sin descripción'}")
        print("  " + "-" * 50)
        self._pause()

    def _handle_create(self) -> None:
        self._print_header("REGISTRAR NUEVO DESTINO", "Inicio > Destinos > Nuevo")
        name = input("\n  Nombre del destino: ")
        country = input("  País: ")
        description = input("  Descripción breve (opcional): ")
        base_cost = self._read_float("  Costo base referencial: ")

        created = self.destination_service.register_destination(
            name=name,
            country=country,
            description=description,
            base_cost=base_cost,
        )
        print(f"\n  [OK] Destino '{created.name}' ({created.country}) registrado con ID {created.id}.")
        self._pause()

    def _handle_update(self) -> None:
        self._print_header("MODIFICAR DESTINO", "Inicio > Destinos > Modificar")
        destinations = self.destination_service.list_destinations(include_retired=True)
        self._print_destinations_table(destinations)
        if not destinations:
            self._pause()
            return

        dest_id = self._read_int("\n  ID del destino a modificar: ")
        current = self.destination_service.find_destination(dest_id)

        print("\n  Deja el campo vacío y presiona [ENTER] para conservar el valor actual.")
        name = input(f"  Nombre [{current.name}]: ").strip() or current.name
        country = input(f"  País [{current.country}]: ").strip() or current.country
        description = (
            input(f"  Descripción [{current.description}]: ").strip()
            or current.description
        )
        base_cost = self._read_float(
            f"  Costo base [{current.base_cost}]: ", default=current.base_cost
        )

        updated = self.destination_service.update_destination(
            destination_id=dest_id,
            name=name,
            country=country,
            description=description,
            base_cost=base_cost,
        )
        print(f"\n  [OK] Destino ID {updated.id} actualizado correctamente.")
        self._pause()

    def _handle_retire(self) -> None:
        self._print_header("RETIRAR DESTINO", "Inicio > Destinos > Retirar")
        destinations = self.destination_service.list_destinations(include_retired=False)
        self._print_destinations_table(destinations)
        if not destinations:
            self._pause()
            return

        dest_id = self._read_int("\n  ID del destino a retirar: ")
        confirm = input("  ¿Confirmas retirar este destino? (s/n): ").strip().lower()
        if confirm == "s":
            retired = self.destination_service.retire_destination(dest_id)
            print(
                f"\n  [OK] Destino '{retired.name}' retirado. Su historial se mantiene intacto."
            )
        else:
            print("\n  [i] Operación cancelada.")
        self._pause()

    def _handle_reactivate(self) -> None:
        self._print_header("REACTIVAR DESTINO", "Inicio > Destinos > Reactivar")
        destinations = [
            d
            for d in self.destination_service.list_destinations(include_retired=True)
            if not d.is_active
        ]
        self._print_destinations_table(destinations)
        if not destinations:
            self._pause()
            return

        dest_id = self._read_int("\n  ID del destino a reactivar: ")
        reactivated = self.destination_service.reactivate_destination(dest_id)
        print(f"\n  [OK] Destino '{reactivated.name}' reactivado correctamente.")
        self._pause()
