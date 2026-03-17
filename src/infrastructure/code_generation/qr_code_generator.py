"""
Adaptador de Infraestructura: Generador de Códigos QR.
Implementa CodeGeneratorPort usando la librería qrcode.
"""
import hashlib
import os
import uuid
from typing import Dict, Optional

import qrcode

from src.application.ports.code_generator_port import CodeGeneratorPort


class QRCodeGenerator(CodeGeneratorPort):
    """Genera códigos seriales y sus imágenes QR."""

    def generate_serial_code(
        self,
        ticket_number: str,
        referencia: str,
        color: str,
        tallas_cantidades: Dict[str, int],
        work_type_abbr: str,
    ) -> str:
        """
        Genera un código serial único con el formato:
        <ticket>-<ref>-<abbr>-<talla_inicial>-<uuid_corto>
        """
        talla_char = "X"
        for i in range(33, 49):
            if str(i) in tallas_cantidades:
                talla_char = str(i)[0]
                break

        unique_segment = uuid.uuid4().hex[:6]
        safe_ticket = ticket_number.replace("-", "")[:3]
        safe_ref = referencia.replace("-", "")[:2]

        code = f"{safe_ticket}-{safe_ref}-{work_type_abbr}-{talla_char}-{unique_segment}"
        return code.upper()

    def generate_code_image(self, serial_code: str, output_dir: str) -> Optional[str]:
        """
        Genera el archivo PNG del código QR en output_dir.
        Retorna la ruta del archivo generado, o None si falla.
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            safe_name = "".join(
                c for c in serial_code if c.isalnum() or c in ("-", "_")
            )
            filepath = os.path.join(output_dir, f"qr_{safe_name}.png")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(serial_code)
            qr.make(fit=True)
            qr.make_image(fill_color="black", back_color="white").save(filepath)
            return filepath
        except Exception as exc:
            print(f"[QRCodeGenerator.generate_code_image] Error: {exc}")
            return None
