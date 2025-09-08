# -*- coding: utf-8 -*-
import os
import sys
import re
import subprocess
import qrcode
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

# --- 1. CONSTANTES Y CONFIGURACIÓN (Sin cambios) ---
TIPOS_DE_TRABAJO = {
    "CORTE": "Corte",
    "GUARNICION": "Guarnicion",
    "ENGRUDAR": "Engrudar",
    "MONTAR": "Montar",
    "ALISTAMIENTO": "Alistamiento para Ensuelado",
    "ENSUELADO": "Ensuelado",
    "PLANTILLAS": "Plantillas TERRY",
    "EMPAQUE": "Empaque"
}

ABREVIATURAS_TRABAJO = {
    "Corte": "CT",
    "Guarnicion": "GU",
    "Engrudar": "EG",
    "Montar": "MO",
    "Alistamiento para Ensuelado": "AE",
    "Ensuelado": "EN",
    "Plantillas TERRY": "PT",
    "Empaque": "EM"
}


# --- 2. FUNCIONES AUXILIARES (Helpers) ---

def generate_serial_code(ticket_number, referencia, work_type_abbr):
    safe_ref = referencia.replace('/', '-').replace('\\', '-')
    return f"TKT:{ticket_number}|REF:{safe_ref}|JOB:{work_type_abbr}"

# La función generate_barcode no necesita cambios, ya que acepta la ruta dinámicamente
def generate_barcode(serial_code, codes_dir="codes"):
    if not os.path.exists(codes_dir):
        os.makedirs(codes_dir)
    safe_filename = "".join(c for c in serial_code if c.isalnum() or c in ('-', '_')).rstrip()
    qr_path = os.path.join(codes_dir, f"qr_{safe_filename}.png")
    try:
        qr_img = qrcode.make(serial_code)
        qr_img.save(qr_path)
        return qr_path
    except Exception as e:
        print(f"Error al generar la imagen QR para '{serial_code}': {e}")
        return None

def increment_ticket_number(ticket_number_str):
    numbers = re.findall(r'\d+', ticket_number_str)
    if not numbers:
        return f"{ticket_number_str}_2"
    last_number_str = numbers[-1]
    incremented_number = int(last_number_str) + 1
    pos = ticket_number_str.rfind(last_number_str)
    if pos == -1:
        return ticket_number_str
    return f"{ticket_number_str[:pos]}{incremented_number}{ticket_number_str[pos+len(last_number_str):]}"

# <-- CAMBIO 1: La función ahora recibe la ruta para guardar los QR
def _procesar_datos_tiquete(ticket_info, qr_save_path):
    """
    Procesa los datos del tiquete y genera los códigos QR en la ruta especificada.
    """
    total = sum(ticket_info["tallas_cantidades"].values())
    barcode_paths = {}
    for tipo_display in TIPOS_DE_TRABAJO.values():
        abbr = ABREVIATURAS_TRABAJO.get(tipo_display)
        if abbr:
            serial = generate_serial_code(ticket_info["ticket_number"], ticket_info["referencia"], abbr)
            # <-- CAMBIO 2: Pasa la ruta específica a la función que genera el código
            barcode_paths[tipo_display] = generate_barcode(serial, codes_dir=qr_save_path)
            
    return {**ticket_info, "total_producido": total, "barcode_paths": barcode_paths}


# --- 3. FUNCIONES DE MAQUETACIÓN DE PDF (Sin cambios) ---
def _build_vale_compacto(ticket_data, tipo_display, styles, col_width):
    referencia = ticket_data.get("referencia", "N/A")
    ticket_number = ticket_data.get("ticket_number", "N/A")
    color = ticket_data.get("color", "N/A")
    tallas = ticket_data.get("tallas_cantidades", {})
    total = ticket_data.get("total_producido", 0)
    barcode_path = ticket_data.get("barcode_paths", {}).get(tipo_display, "")
    qr_image = Paragraph("(Sin QR)", styles["Normal"])
    if barcode_path and os.path.exists(barcode_path):
        try:
            qr_image = Image(barcode_path, width=45, height=45)
        except Exception:
            qr_image = Paragraph("(Error QR)", styles["Normal"])
    detalles_txt = f"<b>Ref:</b> {referencia} <b>Color:</b> {color} <b>N°:</b> {ticket_number} <b>Total: {total}</b>"
    firma_txt = "<b>Firma:</b> _________________________"
    bloque_texto_data = [
        [Paragraph(tipo_display, styles["Heading2"])],
        [Paragraph(detalles_txt, styles["Normal"])],
        [Paragraph(firma_txt, styles["Normal"])]
    ]
    bloque_texto = Table(bloque_texto_data, colWidths=[col_width * 0.7])
    bloque_texto.setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 2),
        ('BOTTOMPADDING', (0, 1), (0, 1), 2),
    ]))
    encabezado_fusionado = Table(
        [[bloque_texto, qr_image]],
        colWidths=[col_width * 0.75, col_width * 0.25]
    )
    encabezado_fusionado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.green),
        ('LEFTPADDING', (0, 0), (0, 0), 2),
    ]))
    sizes_range = list(range(33, 49))
    fila_tallas = [str(s) for s in sizes_range]
    fila_cant = [str(tallas.get(str(s), '0')) for s in sizes_range]
    tallas_tbl = Table([fila_tallas, fila_cant], colWidths=[(col_width / len(sizes_range))] * len(sizes_range))
    tallas_tbl.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.25, colors.green),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    return Table([[encabezado_fusionado], [tallas_tbl]], colWidths=[col_width])

def _maquetar_pdf_denso(left_ticket_data, right_ticket_data, output_filename):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=A4,
        leftMargin=15, rightMargin=15, topMargin=15, bottomMargin=15
    )
    styles = getSampleStyleSheet()
    styles["Heading2"].fontSize = 7
    styles["Heading2"].leading = 8
    styles["Normal"].fontSize = 6
    styles["Normal"].leading = 7
    page_w, page_h = A4
    gutter = 6
    col_w = (page_w - doc.leftMargin - doc.rightMargin - gutter) / 2
    elements = []
    tipos_de_trabajo_lista = list(TIPOS_DE_TRABAJO.values())
    vales_izq = [_build_vale_compacto(left_ticket_data, tipo, styles, col_w) for tipo in tipos_de_trabajo_lista]
    vales_der = [_build_vale_compacto(right_ticket_data, tipo, styles, col_w) for tipo in tipos_de_trabajo_lista]
    for i in range(len(tipos_de_trabajo_lista)):
        fila_tabla = Table(
            [[vales_izq[i], vales_der[i]]],
            colWidths=[col_w, col_w],
            spaceAfter=4
        )
        elements.append(fila_tabla)
    try:
        doc.build(elements)
        print(f"PDF con diseño fusionado generado exitosamente: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error crítico al construir el PDF: {e}")
        return None

# --- 4. FUNCIÓN PRINCIPAL DE ORQUESTACIÓN ---

# <-- CAMBIO 3: La función principal ahora pide la ruta de la carpeta para los QR
def generar_vales_pdf(left_ticket_info, right_ticket_info, output_filename, qr_output_folder):
    """
    Función principal. Orquesta el proceso de creación de PDF y códigos QR.
    """
    print("Iniciando generación de PDF de alta densidad...")
    
    print(f"\nProcesando Tiquete Izquierdo (QR en '{qr_output_folder}')...")
    # <-- CAMBIO 4: Pasa la ruta de los QR a la función de procesamiento
    left_ticket_data = _procesar_datos_tiquete(left_ticket_info, qr_save_path=qr_output_folder)
    
    print(f"\nProcesando Tiquete Derecho (QR en '{qr_output_folder}')...")
    # <-- CAMBIO 5: Hace lo mismo para el tiquete derecho
    right_ticket_data = _procesar_datos_tiquete(right_ticket_info, qr_save_path=qr_output_folder)
    
    pdf_path = _maquetar_pdf_denso(left_ticket_data, right_ticket_data, output_filename)
    
    first_qr_path = next(iter(left_ticket_data.get("barcode_paths", {}).values()), None)
    
    return pdf_path, first_qr_path

# --- 5. BLOQUE DE PRUEBAS (main) ---
if __name__ == "__main__":
    
    tiquete_A = {
        "ticket_number": "855",
        "referencia": "BOTIN-DAMA/CUERO",
        "color": "MIEL",
        "tallas_cantidades": {str(size): 2 for size in range(35, 41)},
    }
    tiquete_B = {
        "ticket_number": "856",
        "referencia": "ZAPATO-HOMBRE-VESTIR",
        "color": "NEGRO",
        "tallas_cantidades": {str(size): 3 for size in range(39, 44)},
    }

    # <-- CAMBIO 6: Se definen las dos rutas de salida por separado
    pdf_output_dir = "codes"
    qr_output_dir = f"qr_images_tiquetes_{tiquete_A['ticket_number']}_{tiquete_B['ticket_number']}"
    
    # Asegurarse de que el directorio del PDF exista
    os.makedirs(pdf_output_dir, exist_ok=True)
    
    # Definir la ruta completa del archivo PDF
    pdf_filename = os.path.join(pdf_output_dir, "vales_diseño_fusionado.pdf")

    # <-- CAMBIO 7: Se llama a la función principal con el nuevo parámetro
    pdf_generado, _ = generar_vales_pdf(
        left_ticket_info=tiquete_A,
        right_ticket_info=tiquete_B,
        output_filename=pdf_filename,
        qr_output_folder=qr_output_dir  # Se pasa la carpeta para los QR
    )

    if pdf_generado and os.path.exists(pdf_generado):
        print(f"\nAbriendo el archivo: {pdf_generado}")
        try:
            if sys.platform == "win32":
                os.startfile(os.path.abspath(pdf_generado))
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, os.path.abspath(pdf_generado)])
        except Exception as e:
            print(f"No se pudo abrir el PDF automáticamente: {e}")
    else:
        print("\nNo se pudo generar el PDF.")