"""Entidad de dominio Customer."""
from dataclasses import dataclass


@dataclass
class Customer:
    full_name: str
    email: str
    phone: str = ""
    id: int | None = None

    def __post_init__(self):
        self.full_name = self.full_name.strip()
        self.email = self.email.strip().lower()
        if not self.full_name:
            raise ValueError("El nombre del cliente es obligatorio.")
        if "@" not in self.email:
            raise ValueError("El correo del cliente no tiene un formato válido.")
