from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    full_name: str
    email: str
    password_hash: str
    role: str = "CLIENT"
    id: Optional[int] = None
