"""Servicio de consulta de paquetes."""
class GestionPaquetes:
    def __init__(self, package_dao):
        self.package_dao = package_dao

    def listar_paquetes(self):
        return self.package_dao.obtener_todos()
