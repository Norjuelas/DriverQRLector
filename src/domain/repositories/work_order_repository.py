"""
Puerto de Dominio: Repositorio de Órdenes de Trabajo.
Define el contrato que cualquier implementación de persistencia debe cumplir.
La capa de Dominio/Aplicación depende de esta interfaz, NO de SQLite ni Excel.
"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any

from src.domain.entities.work_order import WorkOrder


class WorkOrderRepository(ABC):

    @abstractmethod
    def save(self, work_order: WorkOrder) -> bool:
        """Guarda o actualiza una orden de trabajo. Retorna True si tiene éxito."""

    @abstractmethod
    def find_by_stage_code(self, stage_code: str) -> Optional[Tuple[WorkOrder, str]]:
        """
        Busca una orden de trabajo por el código de una de sus etapas.
        Retorna (WorkOrder, tipo_de_trabajo_id) o None si no se encuentra.
        El tipo_de_trabajo_id es el identificador programático (ej. 'corte').
        """

    @abstractmethod
    def delete_all(self) -> bool:
        """Elimina todos los registros. Retorna True si tiene éxito."""
