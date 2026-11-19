"""Servicio de consulta de destinos."""
class GestionDestinos:
    def __init__(self, destination_dao):
        self.destination_dao = destination_dao

    def listar_destinos(self):
        return self.destination_dao.obtener_todos()
