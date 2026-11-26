from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ReservationPassenger:
    passenger_name: str
    document_id: str
    trip_status: str = "PENDING"
    id: Optional[int] = None


@dataclass
class Reservation:
    customer_id: int
    departure_id: int
    contracted_unit_price: float
    status: str = "CONFIRMED"
    passengers: List[ReservationPassenger] = field(default_factory=list)
    id: Optional[int] = None
