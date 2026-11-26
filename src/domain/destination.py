from dataclasses import dataclass
from typing import Optional


@dataclass
class Destination:
    name: str
    country: str
    description: str = ""
    base_cost: float = 0.0
    is_active: bool = True
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del destino es obligatorio.")
        if not self.country or not self.country.strip():
            raise ValueError("El país del destino es obligatorio.")
        if len(self.name.strip()) > 90:
            raise ValueError("El nombre del destino no puede exceder 90 caracteres.")
        if len(self.country.strip()) > 90:
            raise ValueError("El país no puede exceder 90 caracteres.")
        if self.base_cost < 0:
            raise ValueError("El costo base no puede ser negativo.")
        self.name = self.name.strip()
        self.country = self.country.strip()
        self.description = (self.description or "").strip()

    def retire(self) -> None:
        self.is_active = False

    def reactivate(self) -> None:
        self.is_active = True
