"""Modelo inicial de destino turístico."""


class Destination:
    def __init__(self, name: str, country: str, city: str, base_cost: float, description: str = ""):
        self.name = name
        self.country = country
        self.city = city
        self.base_cost = base_cost
        self.description = description
