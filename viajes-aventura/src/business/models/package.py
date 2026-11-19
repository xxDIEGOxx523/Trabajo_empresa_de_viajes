"""Modelo inicial de paquete turístico."""


class Package:
    def __init__(self, name: str, start_date, end_date, max_capacity: int, destinations=None):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.max_capacity = max_capacity
        self.destinations = destinations or []
