"""
Caso de Uso: Crear Orden de Trabajo

Orquesta la creación de una orden doble (tiquete izquierdo + tiquete derecho):
  1. Construye las entidades WorkOrder con sus códigos seriales.
  2. Persiste ambas órdenes en el repositorio.
  3. Genera el PDF de vales dobles con los QR.

Depende únicamente de abstracciones (puertos/repositorios), no de PySide2
ni de SQLite directamente. Esto lo hace testeable e independiente de la UI.
"""
from __future__ import annotations

import os
import re
import uuid
import datetime as dt
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from src.domain.entities.work_order import WorkOrder
from src.domain.repositories.work_order_repository import WorkOrderRepository
from src.application.ports.code_generator_port import CodeGeneratorPort
from src.application.ports.pdf_generator_port import PdfGeneratorPort
from config import WORK_TYPE_ABBREVIATIONS


def _increment_ticket_number(ticket_number_str: str) -> str:
    """Incrementa el último número encontrado en el string del tiquete."""
    numbers = re.findall(r"\d+", ticket_number_str)
    if not numbers:
        return f"{ticket_number_str}_2"
    last_number_str = numbers[-1]
    incremented = int(last_number_str) + 1
    pos = ticket_number_str.rfind(last_number_str)
    return f"{ticket_number_str[:pos]}{incremented}{ticket_number_str[pos + len(last_number_str):]}"


@dataclass
class CreateWorkOrderResult:
    success: bool
    pdf_path: Optional[str] = None
    first_qr_path: Optional[str] = None
    left_order: Optional[WorkOrder] = None
    right_order: Optional[WorkOrder] = None
    error_message: Optional[str] = None


class CreateWorkOrderUseCase:
    """
    Genera una orden de trabajo doble (dos tiquetes consecutivos),
    la persiste y produce el PDF de vales con sus imágenes QR.
    """

    PDF_OUTPUT_DIR = "codes"

    def __init__(
        self,
        work_order_repo: WorkOrderRepository,
        code_generator: CodeGeneratorPort,
        pdf_generator: PdfGeneratorPort,
    ):
        self._repo = work_order_repo
        self._code_gen = code_generator
        self._pdf_gen = pdf_generator

    def execute(
        self,
        ticket_number: str,
        referencia: str,
        color: str,
        tallas_cantidades: Dict[str, int],
        valores_trabajo: Dict[str, float],
    ) -> CreateWorkOrderResult:
        """
        Punto de entrada del caso de uso.

        Args:
            ticket_number:      Número del tiquete izquierdo.
            referencia:         Referencia del producto.
            color:              Color del producto.
            tallas_cantidades:  Diccionario {"33": 5, "35": 2, ...}.
            valores_trabajo:    Diccionario {"Corte": 1200.0, "Guarnicion": 800.0, ...}.

        Returns:
            CreateWorkOrderResult con el resultado de la operación.
        """
        # 1. Generar los dos tiquetes
        right_ticket_number = _increment_ticket_number(ticket_number)

        left_order = self._build_work_order(
            ticket_number, referencia, color, tallas_cantidades, valores_trabajo
        )
        right_order = self._build_work_order(
            right_ticket_number, referencia, color, tallas_cantidades, valores_trabajo
        )

        # 2. Persistir ambas órdenes
        for order in (left_order, right_order):
            if not self._repo.save(order):
                return CreateWorkOrderResult(
                    success=False,
                    error_message=f"No se pudo guardar el tiquete {order.ticket_number} en la base de datos.",
                )

        # 3. Generar PDF + QR
        pdf_path, first_qr_path = self._generate_pdf(left_order, right_order)
        if not pdf_path:
            return CreateWorkOrderResult(
                success=False,
                left_order=left_order,
                right_order=right_order,
                error_message="Datos guardados, pero falló la generación del PDF.",
            )

        return CreateWorkOrderResult(
            success=True,
            pdf_path=pdf_path,
            first_qr_path=first_qr_path,
            left_order=left_order,
            right_order=right_order,
        )

    # -------------------------------------------------------------------------
    # Helpers privados
    # -------------------------------------------------------------------------

    def _build_work_order(
        self,
        ticket_number: str,
        referencia: str,
        color: str,
        tallas_cantidades: Dict[str, int],
        valores_trabajo: Dict[str, float],
    ) -> WorkOrder:
        """Construye una WorkOrder con sus códigos seriales generados."""
        serial_codes: Dict[str, str] = {}
        for work_type, abbr in WORK_TYPE_ABBREVIATIONS.items():
            if work_type in valores_trabajo:
                serial_codes[work_type] = self._code_gen.generate_serial_code(
                    ticket_number, referencia, color, tallas_cantidades, abbr
                )

        codigo_serial = f"VALE-{ticket_number}-{uuid.uuid4().hex[:8].upper()}"

        return WorkOrder(
            ticket_number=ticket_number,
            referencia=referencia,
            color=color,
            tallas_cantidades=tallas_cantidades,
            valores_trabajo=valores_trabajo,
            serial_codes=serial_codes,
            codigo_serial=codigo_serial,
        )

    def _generate_pdf(
        self, left: WorkOrder, right: WorkOrder
    ) -> Tuple[Optional[str], Optional[str]]:
        """Construye las rutas de salida y delega la generación al puerto."""
        os.makedirs(self.PDF_OUTPUT_DIR, exist_ok=True)
        qr_folder = os.path.join(
            self.PDF_OUTPUT_DIR,
            f"qr_{left.ticket_number}_{right.ticket_number}",
        )
        safe_ref = left.referencia.replace("/", "-").replace("\\", "_")
        pdf_filename = os.path.join(
            self.PDF_OUTPUT_DIR,
            f"VALE_DOBLE_{left.ticket_number}_{safe_ref}.pdf",
        )

        left_info = {
            "ticket_number": left.ticket_number,
            "referencia": left.referencia,
            "color": left.color,
            "tallas_cantidades": left.tallas_cantidades,
        }
        right_info = {
            "ticket_number": right.ticket_number,
            "referencia": right.referencia,
            "color": right.color,
            "tallas_cantidades": right.tallas_cantidades,
        }

        return self._pdf_gen.generate_double_voucher_pdf(
            left_ticket_info=left_info,
            right_ticket_info=right_info,
            output_filename=pdf_filename,
            qr_output_folder=qr_folder,
        )
