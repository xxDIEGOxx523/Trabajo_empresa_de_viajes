from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from src.persistence.database import DatabaseConnection

T = TypeVar("T")


class BaseDAO(ABC, Generic[T]):
    def __init__(self, db: DatabaseConnection) -> None:
        self.db = db
        self.ph = db.get_placeholder()

    @abstractmethod
    def create(self, entity: T) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> bool:
        raise NotImplementedError
