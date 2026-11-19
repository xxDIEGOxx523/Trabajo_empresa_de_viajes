"""Servicio de consulta del historial de reservas."""
class GestionReservas:
    def __init__(self, reservation_dao):
        self.reservation_dao = reservation_dao

    def listar_reservas(self):
        return self.reservation_dao.obtener_todos()
