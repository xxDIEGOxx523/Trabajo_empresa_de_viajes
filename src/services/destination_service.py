from typing import List, Optional
from src.domain.destination import Destination
from src.persistence.destination_dao import DestinationDAO


class DestinationService:
    def __init__(self, dao: DestinationDAO) -> None:
        self.dao = dao

    def _ensure_unique(
        self, name: str, country: str, exclude_id: Optional[int] = None
    ) -> None:
        existing = self.dao.get_all(include_retired=True)
        for item in existing:
            if exclude_id is not None and item.id == exclude_id:
                continue
            if (
                item.name.lower() == name.strip().lower()
                and item.country.lower() == country.strip().lower()
            ):
                raise ValueError(
                    "Ya existe un destino registrado con ese nombre y país."
                )

    def register_destination(
        self, name: str, country: str, description: str, base_cost: float
    ) -> Destination:
        destination = Destination(
            name=name,
            country=country,
            description=description,
            base_cost=base_cost,
            is_active=True,
        )
        destination.validate()
        self._ensure_unique(destination.name, destination.country)
        return self.dao.create(destination)

    def list_destinations(self, include_retired: bool = False) -> List[Destination]:
        return self.dao.get_all(include_retired=include_retired)

    def search_destinations(
        self, term: str, include_retired: bool = True
    ) -> List[Destination]:
        if not term or not term.strip():
            raise ValueError("Debes ingresar un término de búsqueda.")
        return self.dao.search(term=term, include_retired=include_retired)

    def find_destination(self, destination_id: int) -> Destination:
        destination = self.dao.get_by_id(destination_id)
        if not destination:
            raise LookupError(f"No se encontró un destino con el ID {destination_id}.")
        return destination

    def update_destination(
        self,
        destination_id: int,
        name: str,
        country: str,
        description: str,
        base_cost: float,
    ) -> Destination:
        destination = self.find_destination(destination_id)
        destination.name = name
        destination.country = country
        destination.description = description
        destination.base_cost = base_cost
        destination.validate()
        self._ensure_unique(
            destination.name, destination.country, exclude_id=destination.id
        )
        self.dao.update(destination)
        return destination

    def retire_destination(self, destination_id: int) -> Destination:
        destination = self.find_destination(destination_id)
        if not destination.is_active:
            raise ValueError("El destino ya se encuentra retirado.")
        destination.retire()
        self.dao.set_active_status(destination_id, False)
        return destination

    def reactivate_destination(self, destination_id: int) -> Destination:
        destination = self.find_destination(destination_id)
        if destination.is_active:
            raise ValueError("El destino ya se encuentra activo.")
        destination.reactivate()
        self.dao.set_active_status(destination_id, True)
        return destination
