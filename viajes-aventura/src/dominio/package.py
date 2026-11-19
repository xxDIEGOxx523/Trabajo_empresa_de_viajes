"""Entidad de dominio Package."""
from dataclasses import dataclass
from datetime import date


@dataclass
class Package:
    name: str
    start_date: date
    end_date: date
    total_cost: float
    max_capacity: int
    description: str = ""
    id: int | None = None

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("El nombre del paquete es obligatorio.")
        if self.end_date < self.start_date:
            raise ValueError("La fecha de término no puede ser anterior al inicio.")
        if self.total_cost < 0 or self.max_capacity <= 0:
            raise ValueError("Costo o capacidad del paquete no válidos.")
