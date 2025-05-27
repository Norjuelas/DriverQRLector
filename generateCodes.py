
import qrcode
from barcode import get_barcode_class

from barcode.writer import ImageWriter
from PIL import ImageFont

import os
import sys
import uuid
import hashlib
from PySide2.QtWidgets import *

def generate_qr_code(data):
    """
    Generate QR code image
    
    Args:
        data: Data to encode in the QR code
        
    Returns:
        str: Path to the generated QR code image or None if generation fails
    """
    try:
        # Create filename
        filename = f"qr_{data.replace('/', '_').replace(' ', '_')}.png"
        filepath = os.path.join("codes", filename)
        
        # Generate QR code
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
        print(f"Error generating QR code: {e}")
        return None
    
def generate_barcode(serial_code):
    """
    Genera una imagen de código de barras Code128 para el serial_code dado.
    """
    try:
        barcode_class = get_barcode_class('code128')

        class CustomImageWriter(ImageWriter):
            def __init__(self):
                super().__init__()
                if getattr(sys, 'frozen', False):
                    base_path = sys._MEIPASS
                else:
                    base_path = os.path.abspath(".")
                font_paths = [
                    os.path.join(base_path, "fonts", "segoeui.ttf"),
                    os.path.join(base_path, "segoeui.ttf")
                ]
                self.font_path = next((p for p in font_paths if os.path.exists(p)), None)
                if not self.font_path:
                    print("ADVERTENCIA: No se encontró la fuente 'segoeui.ttf'.")

            def _paint_text(self, xpos, ypos):
                text_to_paint = self.text
                if self.font_path:
                    try:
                        size = int(getattr(self, "font_size", 10))
                        font = ImageFont.truetype(self.font_path, size)
                        self._draw.text((xpos, ypos), text_to_paint, fill=self.foreground, font=font)
                        return
                    except Exception as e:
                        print(f"Error al usar fuente personalizada '{self.font_path}': {e}")
                self._draw.text((xpos, ypos), text_to_paint, fill=self.foreground)

        writer = CustomImageWriter()
        options = {
            'module_height': 8.0,
            'module_width': 0.2,
            'quiet_zone': 1.0,
            'font_size': 7,
            'text_distance': 1.0,
        }
        for opt_key, opt_value in options.items():
            if hasattr(writer, opt_key):
                setattr(writer, opt_key, opt_value)

        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        codes_dir = os.path.join(application_path, "codes")
        os.makedirs(codes_dir, exist_ok=True)
        barcode_file_path_no_ext = os.path.join(codes_dir, f"barcode_{serial_code}")
        barcode_instance = barcode_class(serial_code, writer=writer)
        full_filename_written = barcode_instance.save(barcode_file_path_no_ext)
        return full_filename_written

    except Exception as e:
        print(f"Error crítico al generar código de barras: {e}")
        QMessageBox.critical("Error de Código de Barras",
                                f"No se pudo generar el código de barras para '{serial_code}':\n{e}")
        return None

# def on_code_type_changed(checked,current_code_type):
#     """Handle change in code type selection"""
#     if checked:
#         return current_code_type = "barcode"
#     else:
#         return current_code_type = "qr"
#     def setup_code_type_selector(self):
#         """Setup UI elements to select between barcode and QR code"""
#         # Create a frame for radio buttons if it doesn't exist
#         if not hasattr(self.ui, 'codeTypeFrame'):
#             self.ui.codeTypeFrame = QFrame()
#             self.ui.codeTypeFrame.setFrameShape(QFrame.StyledPanel)
#             self.ui.codeTypeFrame.setFrameShadow(QFrame.Raised)
            
#             # Create radio buttons
#             self.ui.radioBarcode = QRadioButton("Código de Barras")
#             self.ui.radioQR = QRadioButton("Código QR")
#             self.ui.radioBarcode.setChecked(True)  # Barcode is default
            
#             # Create layout
#             layout = QHBoxLayout(self.ui.codeTypeFrame)
#             layout.addWidget(self.ui.radioBarcode)
#             layout.addWidget(self.ui.radioQR)
            
#             # Connect signals
#             self.ui.radioBarcode.toggled.connect(on_code_type_changed(self.ui.radioBarcode.setChecked(True)))
            
#             # Find a place to add the frame (this depends on your UI layout)
#             # For example, if there's a verticalLayout in the form:
#             if hasattr(self.ui, 'formLayout'):
#                 # Insert at position 0 (top)
#                 self.ui.formLayout.insertRow(0, "Tipo de Código:", self.ui.codeTypeFrame)

def shorten_serial_code(code: str, length: int = 8) -> str:
    """Return a short hash from a given code"""
    hash_object = hashlib.sha1(code.encode())
    short_hash = hash_object.hexdigest()[:length]
    return short_hash.upper()

def generate_serial_code(ticket_number, referencia, color, tallas_cantidades, work_type_abbr):
    """
    Genera un código serial único para un tipo de trabajo específico.
    Formato: {ticket_number[:3]}-{referencia[:2]}-{work_type_abbr}-{talla_char}-{unique_id[:6]}
    """
    talla_char = 'X'
    for i in range(33, 49):
        if str(i) in tallas_cantidades:
            talla_char = str(i)[0]
            break

    unique_id_segment = str(uuid.uuid4())[:6]
    serial_code = (
        f"{ticket_number[:3]}-"
        f"{referencia[:2]}-"
        f"{work_type_abbr}-"
        f"{talla_char}-"
        f"{unique_id_segment}"
    )
    return serial_code.upper()