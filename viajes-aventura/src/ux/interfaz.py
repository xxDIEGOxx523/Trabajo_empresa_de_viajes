"""Interfaz inicial de terminal para Viajes Aventura."""


class TerminalInterface:
    def __init__(self, gestion_destinos, gestion_paquetes, gestion_reservas):
        self.gestion_destinos = gestion_destinos
        self.gestion_paquetes = gestion_paquetes
        self.gestion_reservas = gestion_reservas

    @staticmethod
    def _mostrar_registros(titulo, registros):
        print(f"\n{titulo}")
        print("-" * len(titulo))
        if not registros:
            print("No hay registros disponibles.")
            return
        for registro in registros:
            print(" | ".join(f"{clave}: {valor}" for clave, valor in registro.items()))

    def iniciar(self):
        while True:
            print("\n====================================")
            print("          VIAJES AVENTURA")
            print("====================================")
            print("1. Listar destinos")
            print("2. Listar paquetes turísticos")
            print("3. Listar reservas de demostración")
            print("4. Salir")
            opcion = input("Seleccione una opción: ").strip()
            if opcion == "1":
                self._mostrar_registros("DESTINOS", self.gestion_destinos.listar_destinos())
            elif opcion == "2":
                self._mostrar_registros("PAQUETES", self.gestion_paquetes.listar_paquetes())
            elif opcion == "3":
                self._mostrar_registros("RESERVAS", self.gestion_reservas.listar_reservas())
            elif opcion == "4":
                print("Sistema finalizado.")
                return
            else:
                print("Opción no válida. Intente nuevamente.")
