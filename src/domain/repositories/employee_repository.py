"""
Puerto de Dominio: Repositorio de Empleados.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.employee import Employee


class EmployeeRepository(ABC):

    @abstractmethod
    def save(self, employee: Employee) -> bool:
        """Persiste un empleado nuevo. Retorna True si tiene éxito."""

    @abstractmethod
    def find_by_cedula(self, cedula: str) -> Optional[Employee]:
        """Busca un empleado por cédula. Retorna None si no existe."""

    @abstractmethod
    def find_all(self) -> List[Employee]:
        """Retorna todos los empleados."""

    @abstractmethod
    def delete_all(self) -> bool:
        """Elimina todos los empleados. Retorna True si tiene éxito."""
