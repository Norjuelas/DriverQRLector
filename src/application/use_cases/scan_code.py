"""
Caso de Uso: Escanear Código de Trabajo

Al leer un código QR/barcode:
  1. Valida que el código no haya sido procesado ya en esta sesión.
  2. Verifica en la BD que no exista un vale duplicado para este empleado.
  3. Busca la orden de trabajo asociada al código.
  4. Crea el vale y lo persiste.

Sin dependencias de UI: devuelve un resultado tipado que la presentación interpreta.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Set

from src.domain.entities.voucher import Voucher
from src.domain.entities.work_order import WorkOrder
from src.domain.repositories.work_order_repository import WorkOrderRepository
from src.domain.repositories.voucher_repository import VoucherRepository
from config import WORK_TYPES


@dataclass
class ScanCodeResult:
    success: bool
    voucher: Optional[Voucher] = None
    work_order: Optional[WorkOrder] = None
    work_type_display: Optional[str] = None
    error_code: Optional[str] = None   # "EMPTY", "NO_EMPLOYEE", "DUPLICATE_SESSION",
                                        # "DUPLICATE_DB", "NOT_FOUND", "BAD_CONFIG", "SAVE_ERROR"
    error_message: Optional[str] = None


class ScanCodeUseCase:
    """
    Procesa el escaneo de un código de etapa de trabajo y registra el vale
    correspondiente para el empleado activo.
    """

    def __init__(
        self,
        work_order_repo: WorkOrderRepository,
        voucher_repo: VoucherRepository,
    ):
        self._work_order_repo = work_order_repo
        self._voucher_repo = voucher_repo
        # Códigos ya procesados en la sesión actual (en memoria)
        self._session_codes: Set[str] = set()

    def execute(self, scanned_code: str, empleado_id: str) -> ScanCodeResult:
        """
        Procesa el código escaneado para el empleado indicado.

        Args:
            scanned_code:  El código leído por el escáner.
            empleado_id:   ID del empleado seleccionado en la UI.

        Returns:
            ScanCodeResult con el resultado de la operación.
        """
        scanned_code = scanned_code.strip()

        # 1. Validaciones de entrada
        if not scanned_code:
            return ScanCodeResult(
                success=False,
                error_code="EMPTY",
                error_message="Por favor, escanee o ingrese un código válido.",
            )
        if not empleado_id:
            return ScanCodeResult(
                success=False,
                error_code="NO_EMPLOYEE",
                error_message="Por favor, seleccione un empleado.",
            )

        # 2. Duplicado en sesión actual
        if scanned_code in self._session_codes:
            return ScanCodeResult(
                success=False,
                error_code="DUPLICATE_SESSION",
                error_message=f"El código '{scanned_code}' ya fue agregado en esta sesión.",
            )

        # 3. Duplicado en base de datos
        if self._voucher_repo.exists(scanned_code, empleado_id):
            return ScanCodeResult(
                success=False,
                error_code="DUPLICATE_DB",
                error_message=f"Ya existe un vale para este empleado con el código '{scanned_code}'.",
            )

        # 4. Buscar la orden de trabajo
        resultado = self._work_order_repo.find_by_stage_code(scanned_code)
        if not resultado:
            return ScanCodeResult(
                success=False,
                error_code="NOT_FOUND",
                error_message=f"No se encontró ningún trabajo con el código '{scanned_code}'.",
            )

        work_order, work_type_id = resultado

        # 5. Validar configuración de tipo de trabajo
        work_type_info = WORK_TYPES.get(work_type_id)
        if not work_type_info:
            return ScanCodeResult(
                success=False,
                error_code="BAD_CONFIG",
                error_message=f"El tipo de trabajo '{work_type_id}' no está definido en config.py.",
            )

        work_type_display = work_type_info["display"]
        valor_pagado = work_order.valores_trabajo.get(work_type_id, 0.0)

        # 6. Crear y persistir el vale
        voucher = Voucher(
            empleado_id=empleado_id,
            codigo_serial_trabajo_asociado=scanned_code,
            work_type_detected=work_type_display,
            valor_pagado=valor_pagado,
        )
        if not self._voucher_repo.save(voucher):
            return ScanCodeResult(
                success=False,
                error_code="SAVE_ERROR",
                error_message="No se pudo registrar el vale en la base de datos.",
            )

        # 7. Registrar en sesión y retornar éxito
        self._session_codes.add(scanned_code)
        return ScanCodeResult(
            success=True,
            voucher=voucher,
            work_order=work_order,
            work_type_display=work_type_display,
        )

    def clear_session(self) -> None:
        """Limpia los códigos de la sesión actual (llamar al registrar vales)."""
        self._session_codes.clear()
