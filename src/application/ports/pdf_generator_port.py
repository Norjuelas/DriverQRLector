"""
Puerto de Salida: Generación de PDFs.
Define el contrato para generar el PDF de vales doble.
La capa de Aplicación depende de esta interfaz, no de reportlab.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple


class PdfGeneratorPort(ABC):

    @abstractmethod
    def generate_double_voucher_pdf(
        self,
        left_ticket_info: Dict,
        right_ticket_info: Dict,
        output_filename: str,
        qr_output_folder: str,
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Genera el PDF con los vales dobles y los QR asociados.

        Args:
            left_ticket_info:  Datos del tiquete izquierdo.
            right_ticket_info: Datos del tiquete derecho.
            output_filename:   Ruta completa del PDF a generar.
            qr_output_folder:  Carpeta donde se guardarán los QR.

        Returns:
            Tupla (ruta_pdf, ruta_primer_qr). Cualquiera puede ser None si falla.
        """
