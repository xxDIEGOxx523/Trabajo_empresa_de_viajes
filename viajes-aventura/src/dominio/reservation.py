"""Entidad de dominio Reservation."""
from dataclasses import dataclass


@dataclass
class Reservation:
    customer_id: int
    package_id: int
    number_of_people: int
    total_price: float
    id: int | None = None

    def __post_init__(self):
        if self.customer_id <= 0 or self.package_id <= 0:
            raise ValueError("Cliente y paquete deben tener identificadores válidos.")
        if self.number_of_people <= 0:
            raise ValueError("La cantidad de personas debe ser mayor que cero.")
        if self.total_price < 0:
            raise ValueError("El precio total no puede ser negativo.")
