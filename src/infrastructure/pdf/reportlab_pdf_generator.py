"""
Adaptador de Infraestructura: Generador de PDFs con ReportLab.
Implementa PdfGeneratorPort delegando en generate_pdf.py existente.

Al estar detrás del puerto, sustituir ReportLab por otra librería solo
requiere cambiar este archivo, sin tocar la capa de Aplicación.
"""
from typing import Dict, Optional, Tuple

from src.application.ports.pdf_generator_port import PdfGeneratorPort
from generate_pdf import generar_vales_pdf


class ReportLabPdfGenerator(PdfGeneratorPort):
    """Genera PDFs de vales dobles usando ReportLab a través de generate_pdf.py."""

    def generate_double_voucher_pdf(
        self,
        left_ticket_info: Dict,
        right_ticket_info: Dict,
        output_filename: str,
        qr_output_folder: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        try:
            return generar_vales_pdf(
                left_ticket_info=left_ticket_info,
                right_ticket_info=right_ticket_info,
                output_filename=output_filename,
                qr_output_folder=qr_output_folder,
            )
        except Exception as exc:
            print(f"[ReportLabPdfGenerator.generate_double_voucher_pdf] Error: {exc}")
            return None, None
