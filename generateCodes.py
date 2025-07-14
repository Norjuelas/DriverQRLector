import os
import sys
import uuid
import hashlib
import qrcode
from PySide2.QtWidgets import QMessageBox, QApplication

def generate_qr_code(data, subfolder_name=None):
    """
    Genera una imagen de código QR y la guarda en un subdirectorio.

    Args:
        data: Datos a codificar en el QR.
        subfolder_name: Nombre del subdirectorio donde guardar el QR (opcional).

    Returns:
        str: Ruta a la imagen QR generada o None si falla.
    """
    try:
        # Definir el directorio base
        base_dir = "codes"
        if subfolder_name:
            folder = os.path.join(base_dir, subfolder_name)
        else:
            folder = base_dir

        # Asegurarse de que el directorio exista
        os.makedirs(folder, exist_ok=True)

        # Crear nombre de archivo seguro
        safe_data = data.replace('/', '_').replace(' ', '_').replace('\\', '_').replace(':', '_')
        filename = f"qr_{safe_data}.png"
        filepath = os.path.join(folder, filename)

        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(filepath)

        return filepath
    except Exception as e:
        print(f"Error generando QR code: {e}")
        return None

def generate_barcode(serial_code, subfolder_name=None):
    """
    Genera una imagen de código QR para el serial_code dado.

    Args:
        serial_code: Código serial para el QR.
        subfolder_name: Nombre del subdirectorio donde guardar el QR.

    Returns:
        str: Ruta a la imagen QR o None si falla.
    """
    print(f"Generando QR (vía generate_barcode) para: {serial_code}")
    try:
        qr_path = generate_qr_code(serial_code, subfolder_name=subfolder_name)
        if qr_path:
            return qr_path
        else:
            raise ValueError("La generación del QR falló.")
    except Exception as e:
        print(f"Error crítico al generar código QR: {e}")
        return None

def shorten_serial_code(code: str, length: int = 8) -> str:
    """Return a short hash from a given code"""
    hash_object = hashlib.sha1(code.encode())
    short_hash = hash_object.hexdigest()[:length]
    return short_hash.upper()

def generate_serial_code(ticket_number, referencia, color, tallas_cantidades, work_type_abbr):
    """
    Genera un código serial único para un tipo de trabajo específico.
    """
    talla_char = 'X'
    for i in range(33, 49):
        if str(i) in tallas_cantidades:
            talla_char = str(i)[0]
            break

    unique_id_segment = str(uuid.uuid4().hex)[:6]
    safe_ticket = ticket_number.replace('-', '')[:3]
    safe_ref = referencia.replace('-', '')[:2]

    serial_code = (
        f"{safe_ticket}-"
        f"{safe_ref}-"
        f"{work_type_abbr}-"
        f"{talla_char}-"
        f"{unique_id_segment}"
    )
    return serial_code.upper()

# Main loop (assuming it's part of a class)
def generate_codes(self, ticket_number, referencia, color, tallas_cantidades, valores_trabajo):
    serial_codes = {}
    barcode_paths = {}
    # Crear nombre del subdirectorio: referenciadetrabajo_numerodeticket
    safe_ref = referencia.replace('-', '').replace(' ', '_')
    safe_ticket = ticket_number.replace('-', '').replace(' ', '_')
    subfolder_name_for_codes = f"{safe_ref}_{safe_ticket}"

    # Itera sobre el diccionario de abreviaturas actualizado
    for work_type, abbr in self.WORK_TYPE_ABBREVIATIONS.items():
        if work_type in valores_trabajo:
            serial_code = generate_serial_code(ticket_number, referencia, color, tallas_cantidades, abbr)
            barcode_path = generate_barcode(serial_code, subfolder_name=subfolder_name_for_codes)
            if not barcode_path:
                QMessageBox.critical(self, "Error", f"Error al generar el código QR para {work_type}.")
                return
            serial_codes[work_type] = serial_code
            barcode_paths[work_type] = barcode_path

    return serial_codes, barcode_paths

# Ejemplo de uso
if __name__ == '__main__':
    app = QApplication(sys.argv)
    test_serial = "TKT-RE-CT-3-A1B2C3"
    subfolder = "REF123_TKT456"
    path = generate_barcode(test_serial, subfolder_name=subfolder)
    if path:
        print(f"Código QR generado en: {path}")
    else:
        print("Fallo al generar código QR.")