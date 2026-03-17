"""
Adaptador de Infraestructura: Servicio de Backup en ZIP.
Implementa BackupServicePort usando zipfile + shutil.
"""
import os
import shutil
import sys
import zipfile
from datetime import datetime
from typing import Callable, List, Optional

from src.application.ports.backup_service_port import BackupServicePort


def _app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    try:
        return os.path.dirname(os.path.abspath(__file__))
    except NameError:
        return os.getcwd()


class ZipBackupService(BackupServicePort):
    """
    Crea backups comprimidos en ZIP y elimina datos de producción.

    El directorio de datos (excel_path, codes_dir) puede configurarse en el
    constructor para facilitar pruebas y distintos entornos.
    """

    def __init__(
        self,
        excel_path: Optional[str] = None,
        codes_dir: Optional[str] = None,
        backup_folder: Optional[str] = None,
    ):
        base = _app_dir()
        self._excel_path = excel_path or os.path.join(base, "database.xlsx")
        self._codes_dir = codes_dir or os.path.join(base, "codes")
        self._backup_folder = backup_folder or os.path.join(base, "backups_eliminados")

    # ------------------------------------------------------------------
    # BackupServicePort implementation
    # ------------------------------------------------------------------

    def has_data_to_backup(self) -> bool:
        excel_exists = os.path.exists(self._excel_path)
        codes_has_content = (
            os.path.isdir(self._codes_dir)
            and len(os.listdir(self._codes_dir)) > 0
        )
        return excel_exists or codes_has_content

    def create_backup(
        self,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> Optional[str]:
        def _notify(msg: str) -> None:
            if progress_callback:
                progress_callback(msg)

        try:
            os.makedirs(self._backup_folder, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            zip_path = os.path.join(
                self._backup_folder, f"version_eliminada_{timestamp}.zip"
            )

            _notify("Creando archivo ZIP...")
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists(self._excel_path):
                    _notify(f"Respaldando base de datos: {self._excel_path}...")
                    zipf.write(self._excel_path, os.path.basename(self._excel_path))

                if os.path.isdir(self._codes_dir):
                    _notify(f"Respaldando directorio de códigos: {self._codes_dir}...")
                    all_files = [
                        os.path.join(root, f)
                        for root, _, files in os.walk(self._codes_dir)
                        for f in files
                    ]
                    total = len(all_files)
                    for idx, file_path in enumerate(all_files, 1):
                        arcname = os.path.relpath(
                            file_path, os.path.dirname(self._codes_dir)
                        )
                        zipf.write(file_path, arcname)
                        if idx % 10 == 0 or idx == total:
                            _notify(f"Respaldando códigos... {idx}/{total}")

            _notify(f"Backup creado: {zip_path}")
            return zip_path

        except Exception as exc:
            print(f"[ZipBackupService.create_backup] Error: {exc}")
            return None

    def delete_all_data(self) -> List[str]:
        messages: List[str] = []

        if os.path.exists(self._excel_path):
            try:
                os.remove(self._excel_path)
                messages.append(f"Archivo Excel eliminado: {self._excel_path}")
            except Exception as exc:
                messages.append(f"Error al eliminar Excel: {exc}")
        else:
            messages.append(f"Excel no encontrado en {self._excel_path}.")

        if os.path.isdir(self._codes_dir):
            try:
                shutil.rmtree(self._codes_dir)
                messages.append(f"Directorio de códigos eliminado: {self._codes_dir}")
            except Exception as exc:
                messages.append(f"Error al eliminar directorio codes: {exc}")
        else:
            messages.append(f"Directorio codes no encontrado en {self._codes_dir}.")

        return messages
