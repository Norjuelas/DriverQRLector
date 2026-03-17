"""
Puerto de Salida: Servicio de Backup.
Define el contrato para crear backups y eliminar datos.
"""
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple


class BackupServicePort(ABC):

    @abstractmethod
    def has_data_to_backup(self) -> bool:
        """Retorna True si existe algo que respaldar."""

    @abstractmethod
    def create_backup(
        self,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> Optional[str]:
        """
        Crea un archivo ZIP de backup.
        Retorna la ruta del archivo ZIP creado, o None si falla.
        """

    @abstractmethod
    def delete_all_data(self) -> List[str]:
        """
        Elimina los datos de producción (Excel y directorio codes).
        Retorna una lista de mensajes describiendo qué se eliminó.
        """
