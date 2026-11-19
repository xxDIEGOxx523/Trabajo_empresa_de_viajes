"""Configuración inicial de SQLite, pendiente de implementación."""


class Database:
    def __init__(self, db_path: str = "./data/viajes_aventura.db"):
        self.db_path = db_path

    def connect(self):
        raise NotImplementedError("La conexión SQLite se implementará durante el Hito 1.")
