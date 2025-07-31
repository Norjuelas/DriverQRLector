import os
import sys
import subprocess
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.platypus.flowables import Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import qrcode # Asegúrate de tener: pip install qrcode

# --- CONSTANTES FIJAS DE TRABAJO ---
TIPOS_DE_TRABAJO = {
    "CORTE": "Corte",
    "GUARNICION": "Guarnicion",
    "ENGRUDAR": "ENGRUDAR",
    "MONTAR": "Montar",
    "ALISTAMIENTO": "Alistamiento para Ensuelado",
    "ENSUELADO": "Ensuelado",
    "PLANTILLAS": "Plantillas TERRY",
    "EMPAQUE": "Empaque"
}

ABREVIATURAS_TRABAJO = {
    "Corte": "CT",
    "Guarnicion": "GU",
    "ENGRUDAR": "EG",
    "Montar": "MO",
    "Alistamiento para Ensuelado": "AE",
    "Ensuelado": "EN",
    "Plantillas TERRY": "PT",
    "Empaque": "EM"
}


# --- FUNCIONES DE GENERACIÓN DE CÓDIGOS ---
def generate_serial_code(ticket_number, referencia, work_type_abbr):
    safe_ref = referencia.replace('/', '-').replace('\\', '-')
    return f"TKT:{ticket_number}|REF:{safe_ref}|JOB:{work_type_abbr}"

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


# --- FUNCIÓN PARA CONSTRUIR UN VALE INDIVIDUAL (DISEÑO FUSIONADO) ---
def build_vale_compacto(ticket_data, tipo_display, styles, col_width):
    # 1. Extraer datos
    referencia = ticket_data.get("referencia", "N/A")
    ticket_number = ticket_data.get("ticket_number", "N/A")
    color = ticket_data.get("color", "N/A")
    tallas = ticket_data.get("tallas_cantidades", {})
    total = ticket_data.get("total_producido", 0)
    barcode_path = ticket_data.get("barcode_paths", {}).get(tipo_display, "")

    # 2. QR
    qr_image = Paragraph("(Sin QR)", styles["Normal"])
    if barcode_path and os.path.exists(barcode_path):
        try:
            qr_image = Image(barcode_path, width=45, height=45)
        except Exception:
            qr_image = Paragraph("(Error QR)", styles["Normal"])

    # 3. Bloque de Texto Fusionado
    detalles_txt = f"<b>Ref:</b> {referencia} <b>Color:</b> {color} <b>N°:</b> {ticket_number} <b>Total: {total}</b>"
    firma_txt = "<b>Firma:</b> _________________________"
    
    bloque_texto_data = [
        [Paragraph(tipo_display, styles["Heading2"])],
        [Paragraph(detalles_txt, styles["Normal"])],
        [Paragraph(firma_txt, styles["Normal"])]
    ]
    
    bloque_texto = Table(bloque_texto_data, colWidths=[col_width * 0.7])
    bloque_texto.setStyle(TableStyle([
        ('BOTTOMPADDING', (0, 0), (0, 0), 2), # Espacio entre título y detalles
        ('BOTTOMPADDING', (0, 1), (0, 1), 2), # Espacio entre detalles y firma
    ]))

    # 4. Tabla de Encabezado que combina texto y QR
    encabezado_fusionado = Table(
        [[bloque_texto, qr_image]],
        colWidths=[col_width * 0.75, col_width * 0.25]
    )
    encabezado_fusionado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.green),
        ('LEFTPADDING', (0, 0), (0, 0), 2),
    ]))

    # 5. Tallaje (sin cambios)
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

    # 6. Tabla final del vale
    return Table([[encabezado_fusionado], [tallas_tbl]], colWidths=[col_width])


# --- FUNCIÓN DE MAQUETACIÓN DEL PDF ---
def generar_pagina_densa(left_ticket_data, right_ticket_data, output_filename):
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
    row_h = (page_h - doc.topMargin - doc.bottomMargin) / len(TIPOS_DE_TRABAJO)

    elements = []
    
    tipos_de_trabajo_lista = list(TIPOS_DE_TRABAJO.values())
    vales_izq = [build_vale_compacto(left_ticket_data, tipo, styles, col_w) for tipo in tipos_de_trabajo_lista]
    vales_der = [build_vale_compacto(right_ticket_data, tipo, styles, col_w) for tipo in tipos_de_trabajo_lista]
    
    for i in range(len(tipos_de_trabajo_lista)):
        fila_tabla = Table(
            [[vales_izq[i], "", vales_der[i]]], # Se añade una columna vacía en el medio
            colWidths=[col_w, gutter, col_w]      # Se asigna el ancho del gutter a esa columna
        )
        fila_tabla.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)
        ]))
        elements.append(fila_tabla)

    try:
        doc.build(elements)
        print(f"PDF con diseño fusionado generado exitosamente: {output_filename}")
        return output_filename
    except Exception as e:
        print(f"Error crítico al construir el PDF: {e}")
        return None

# --- FUNCIÓN PRINCIPAL PARA INTEGRACIÓN ---
def generate_vale_pdf(left_ticket_info, right_ticket_info, output_filename):
    print("Iniciando generación de PDF de alta densidad...")

    def procesar_tiquete(ticket_info):
        total = sum(ticket_info["tallas_cantidades"].values())
        barcode_paths = {}
        for tipo_display in TIPOS_DE_TRABAJO.values():
            abbr = ABREVIATURAS_TRABAJO.get(tipo_display)
            if abbr:
                serial = generate_serial_code(ticket_info["ticket_number"], ticket_info["referencia"], abbr)
                barcode_paths[tipo_display] = generate_barcode(serial)
        return {**ticket_info, "total_producido": total, "barcode_paths": barcode_paths}

    print("\nProcesando Tiquete Izquierdo...")
    left_ticket_data = procesar_tiquete(left_ticket_info)
    
    print("\nProcesando Tiquete Derecho...")
    right_ticket_data = procesar_tiquete(right_ticket_info)

    pdf_path = generar_pagina_densa(left_ticket_data, right_ticket_data, output_filename)
    return pdf_path

# --- BLOQUE DE TESTEO (main) ---
if __name__ == "__main__":
    
    tiquete_A = {
        "ticket_number": "855",
        "referencia": "BOTIN-DAMA-CUERO",
        "color": "MIEL",
        "tallas_cantidades": {str(size): 2 for size in range(35, 41)},
    }

    tiquete_B = {
        "ticket_number": "856",
        "referencia": "ZAPATO-HOMBRE-VESTIR",
        "color": "NEGRO",
        "tallas_cantidades": {str(size): 3 for size in range(39, 44)},
    }

    pdf_generado = generate_vale_pdf(
        left_ticket_info=tiquete_A,
        right_ticket_info=tiquete_B,
        output_filename="/vales_diseño_fusionado.pdf"
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