"""
Puerto de Dominio: Repositorio de Vales.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.voucher import Voucher


class VoucherRepository(ABC):

    @abstractmethod
    def save(self, voucher: Voucher) -> bool:
        """Persiste un vale nuevo. Retorna True si tiene éxito."""

    @abstractmethod
    def exists(self, codigo_serial_trabajo: str, empleado_id: str) -> bool:
        """Verifica si ya existe un vale para esta combinación empleado-trabajo."""

    @abstractmethod
    def find_by_employee(self, empleado_id: str) -> List[Voucher]:
        """Retorna todos los vales de un empleado."""

    @abstractmethod
    def delete_all(self) -> bool:
        """Elimina todos los vales. Retorna True si tiene éxito."""
