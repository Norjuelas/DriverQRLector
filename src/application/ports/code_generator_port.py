"""
Puerto de Salida: Generación de Códigos.
Define el contrato para generar códigos seriales e imágenes QR/barcode.
La capa de Aplicación depende de esta interfaz, no de qrcode/barcode.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional


class CodeGeneratorPort(ABC):

    @abstractmethod
    def generate_serial_code(
        self,
        ticket_number: str,
        referencia: str,
        color: str,
        tallas_cantidades: Dict[str, int],
        work_type_abbr: str,
    ) -> str:
        """
        Genera y retorna un código serial único para una etapa de trabajo.
        No crea ningún archivo; solo produce la cadena del código.
        """

    @abstractmethod
    def generate_code_image(
        self,
        serial_code: str,
        output_dir: str,
    ) -> Optional[str]:
        """
        Genera la imagen (QR o barcode) para un código serial.
        Retorna la ruta del archivo generado, o None si falla.
        """
