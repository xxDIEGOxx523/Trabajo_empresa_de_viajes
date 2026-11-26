from dataclasses import dataclass, field
from typing import List, Optional
from src.domain.destination import Destination


@dataclass
class ItineraryStop:
    destination: Destination
    visit_order: int
    id: Optional[int] = None

    def change_order(self, new_order: int) -> None:
        if new_order <= 0:
            raise ValueError("El orden de visita debe ser mayor que cero.")
        self.visit_order = new_order


@dataclass
class TravelPackage:
    name: str
    description: str = ""
    is_active: bool = True
    stops: List[ItineraryStop] = field(default_factory=list)
    id: Optional[int] = None

    def add_stop(self, destination: Destination, visit_order: int) -> None:
        if not destination.is_active:
            raise ValueError("No se puede agregar un destino retirado a un paquete nuevo.")
        self.stops.append(ItineraryStop(destination=destination, visit_order=visit_order))

    def get_itinerary(self) -> List[ItineraryStop]:
        return sorted(self.stops, key=lambda stop: stop.visit_order)

    def validate_itinerary(self) -> None:
        if len(self.stops) < 2:
            raise ValueError("Un paquete turístico debe combinar al menos dos destinos.")


@dataclass
class PackageDeparture:
    package_id: int
    start_date: str
    end_date: str
    price: float
    max_capacity: int
    status: str = "OPEN"
    id: Optional[int] = None
