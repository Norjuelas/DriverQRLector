"""
Caso de Uso: Resetear Base de Datos

  1. Verifica que existan datos a respaldar.
  2. Crea un backup ZIP mediante el puerto de backup.
  3. Elimina todos los datos de producción.

Sin dependencias de UI ni de infraestructura concreta.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from src.application.ports.backup_service_port import BackupServicePort


@dataclass
class ResetDatabaseResult:
    success: bool
    backup_path: Optional[str] = None
    deleted_items: List[str] = field(default_factory=list)
    error_message: Optional[str] = None


class ResetDatabaseUseCase:
    """Crea un backup y luego elimina todos los datos de producción."""

    def __init__(self, backup_service: BackupServicePort):
        self._backup = backup_service

    def execute(
        self,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> ResetDatabaseResult:
        """
        Args:
            progress_callback: Función opcional que recibe mensajes de progreso.

        Returns:
            ResetDatabaseResult con el resultado de la operación.
        """
        if not self._backup.has_data_to_backup():
            return ResetDatabaseResult(
                success=False,
                error_message="No hay archivos para eliminar. La base de datos ya está limpia.",
            )

        backup_path = self._backup.create_backup(progress_callback=progress_callback)
        if not backup_path:
            return ResetDatabaseResult(
                success=False,
                error_message="No se pudo crear el backup. Se canceló la eliminación.",
            )

        deleted = self._backup.delete_all_data()

        return ResetDatabaseResult(
            success=True,
            backup_path=backup_path,
            deleted_items=deleted,
        )
