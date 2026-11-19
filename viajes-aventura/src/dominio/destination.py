"""Entidad de dominio Destination."""
from dataclasses import dataclass


@dataclass
class Destination:
    name: str
    country: str
    city: str
    base_cost: float
    description: str = ""
    id: int | None = None

    def __post_init__(self):
        self.name = self.name.strip()
        self.country = self.country.strip()
        self.city = self.city.strip()
        if not self.name or not self.country or not self.city:
            raise ValueError("Nombre, país y ciudad son obligatorios.")
        if self.base_cost < 0:
            raise ValueError("El costo base no puede ser negativo.")
