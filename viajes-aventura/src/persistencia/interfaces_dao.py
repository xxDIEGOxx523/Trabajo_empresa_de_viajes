"""Contratos mínimos para los objetos de acceso a datos.

Los DAO concretos implementan estas operaciones; se pueden ampliar a medida
que se desarrollen los casos de uso del proyecto.
"""
from abc import ABC, abstractmethod


class IBaseDAO(ABC):
    @abstractmethod
    def obtener_todos(self):
        raise NotImplementedError

    @abstractmethod
    def contar(self):
        raise NotImplementedError
