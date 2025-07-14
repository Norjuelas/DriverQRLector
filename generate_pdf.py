from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet

# Importa las funciones necesarias desde tu módulo
from generateCodes import generate_serial_code, generate_barcode

import os
import sys
import subprocess # Necesario para abrir el PDF
# from PySide2.QtWidgets import QMessageBox # Comentado como en tu original

def generate_vale_pdf(ticket_number, referencia, tallas_cantidades, color,
                      total_producido_calculado, barcode_paths, valores_trabajo,
                      tipos_de_trabajo): # Añadido tipos_de_trabajo como argumento
    """
    Genera un vale de trabajo con múltiples secciones (por tipo de trabajo), cada una con:
    - Encabezado con tipo de trabajo, referencia, color y ticket.
    - Tabla de tallas.
    - Código QR específico por trabajo (en lugar de código de barras).
    - Firma y valor.
    """
    safe_referencia = referencia.replace('/', '-').replace('\\', '-')
    pdf_filename = f"vale_{safe_referencia}_{ticket_number}.pdf"
    pdf_path = os.path.join("codes", pdf_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=30, rightMargin=30,
                            topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    styles['Heading2'].fontSize = 8 # Aumentado un poco para visibilidad
    styles['Normal'].fontSize = 7   # Aumentado un poco
    styles['Heading3'].fontSize = 6
    elements = []

    sizes = list(range(33, 49))
    size_row = [str(s) for s in sizes]
    qty_row = [str(tallas_cantidades.get(str(s), 0)) for s in sizes]

    for tipo_clave, tipo_display in tipos_de_trabajo.items():
        barcode_path = barcode_paths.get(tipo_display, "")
        # total_producido_calculado = total_producido_calculado # Esta línea es redundante

        # Código QR
        try:
            if barcode_path and os.path.exists(barcode_path):
                barcode_img = Image(
                    barcode_path,
                    width=45,  # Ajustado para QR (más pequeño y cuadrado)
                    height=45, # Ajustado para QR
                    kind='proportional',
                    hAlign='RIGHT'
                )
            else:
                print(f"Ruta inválida para código QR de '{tipo_display}': {barcode_path}")
                barcode_img = Paragraph("(Código no disponible)", styles['Normal'])
        except Exception as e:
            print(f"Error cargando código QR: {e}")
            barcode_img = Paragraph("(Error Código)", styles['Normal'])

        # Encabezado vale
        container_data = [[
            Paragraph(f"{tipo_display}", styles['Heading2']),
            "",
            barcode_img
        ]]
        # Ajustar colWidths: Más espacio para el texto, suficiente para el QR
        container_table = Table(container_data, colWidths=[360, 0, 60])
        container_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (2,0), (2,0), 'CENTER'), # Centrar el QR puede verse mejor
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.grey),
            ('LEFTPADDING', (2,0), (2,0), 5), # Añadir padding alrededor del QR
            ('RIGHTPADDING', (2,0), (2,0), 5),
            ('TOPPADDING', (0,0), (-1,-1), 2), # Un poco de padding vertical
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))

        # Detalles de referencia
        details_data = [
            ["Referencia:", referencia, "Color:", color, f"N° {ticket_number}"]
        ]
        details_table = Table(details_data, colWidths=[80, 120, 60, 80, 80])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7), # Aumentado un poco
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 2), # Aumentado padding
        ]))

        # Tabla de tallas
        sizes_table = Table([size_row, qty_row], colWidths=[25] * len(size_row))
        sizes_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7), # Aumentado un poco
            ('LEADING', (0,0), (-1,-1), 8),  # Aumentado un poco
            ('PADDING', (0,0), (-1,-1), 2), # Aumentado padding
        ]))

        # Pie de vale
        footer_data = [
            ["Firma:", "__________________", "total:", f"{total_producido_calculado:.2f}"]
        ]
        # Ajustar colWidths para que quepa la firma y el total
        footer_table = Table(footer_data, colWidths=[50, 250, 60, 60])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7), # Aumentado un poco
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 2), # Aumentado padding
            ('ALIGN', (2,0), (3,0), 'RIGHT'), # Alinear total a la derecha
            ('SPAN', (1,0), (1,0)), # Unir celdas para firma si es necesario
        ]))

        # Agrupamos todo el vale
        complete_vale_data = [
            [container_table],
            [details_table],
            [sizes_table],
            [footer_table]
        ]
        # Asegurarse que colWidths cubra el total (360+0+60 = 420; 80+120+60+80+80=420; 25*16=400; 50+250+60+60=420. Parece que 420 es el ancho)
        # Ajustamos el ancho total a 420 (o el que corresponda)
        complete_vale_table = Table(complete_vale_data, colWidths=[420]) # Ajustado ancho
        complete_vale_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))

        # Añadir vale al documento y un espacio mayor
        elements.append(KeepTogether([complete_vale_table]))
        elements.append(Spacer(1, 15)) # Aumentar espacio entre vales

    try:
        doc.build(elements)
        return pdf_path
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        # QMessageBox.critical(None, "Error PDF", f"No se pudo generar el PDF:\n{e}")
        return None

def main():
    # Configuración inicial
    if not os.path.exists("codes"):
        os.makedirs("codes")

    # Datos de prueba
    test_data = {
        "ticket_number": "TKT-2024-001",
        "referencia": "REF-789",
        "color": "Azul Marino",
        "tallas_cantidades": {str(size): 10 for size in range(35, 41)},
        "total_producido_calculado": 60, # Es el total de pares, no el valor monetario
        "valores_trabajo": { # Estos no se usan actualmente en el pie de página
            "Corte": 150.50,
            "Empaque": 75.00,
            "Guarnicion": 200.00, # Ajustado para coincidir
            "Montar": 180.75, # Ajustado para coincidir
            "Plantillas TERRY": 90.25, # Ajustado para coincidir
            "Ensuelado": 300.00 # Ajustado para coincidir
        }
    }

    # *** CORRECCIÓN: Definir tipos_de_trabajo aquí ***
    tipos_de_trabajo = {
        "Plantillas TERRY": "Plantillas TERRY",
        "EMPAQUE": "Empaque",
        "ENSUELADO": "Ensuelado",
        "ALISTAMIENTO PARA ENSUELADO": "Alistamiento para Ensuelado",
        "MONTAR": "Montar",
        "ENGRUDAR": "ENGRUDAR",
        "GUARNICION": "Guarnicion",
        "CORTE": "Corte"
    }

    # Usar los valores de tipos_de_trabajo como claves aquí
    work_type_abbreviations = {
        "Plantillas TERRY": "PT",
        "Empaque": "EM",
        "Ensuelado": "EN",
        "Alistamiento para Ensuelado": "AE",
        "Montar": "MO",
        "ENGRUDAR": "EG",
        "Guarnicion": "GU",
        "Corte": "CT"
    }

    barcode_paths = {}

    # Itera sobre los tipos de trabajo definidos para el PDF
    for tipo_clave, tipo_display in tipos_de_trabajo.items():
        # Busca la abreviatura usando el nombre de display
        abbr = work_type_abbreviations.get(tipo_display)

        if abbr: # Si encontramos una abreviatura
            serial_code = generate_serial_code(
                ticket_number=test_data["ticket_number"],
                referencia=test_data["referencia"],
                color=test_data["color"],
                tallas_cantidades=test_data["tallas_cantidades"],
                work_type_abbr=abbr
            )
            # Llama a generate_barcode (que ahora genera QR)
            barcode_path = generate_barcode(serial_code)
            if barcode_path and os.path.exists(barcode_path):
                # Guarda usando tipo_display como clave
                barcode_paths[tipo_display] = barcode_path
                print(f"Código QR generado para {tipo_display}: {barcode_path}")
            else:
                print(f"Error generando código QR para {tipo_display}")
                barcode_paths[tipo_display] = ""
        else:
            print(f"No se encontró abreviatura para {tipo_display}")
            barcode_paths[tipo_display] = ""

    # Generar el PDF, pasando tipos_de_trabajo
    pdf_path = generate_vale_pdf(
        ticket_number=test_data["ticket_number"],
        referencia=test_data["referencia"],
        tallas_cantidades=test_data["tallas_cantidades"],
        color=test_data["color"],
        total_producido_calculado=test_data["total_producido_calculado"],
        barcode_paths=barcode_paths,
        valores_trabajo=test_data["valores_trabajo"],
        tipos_de_trabajo=tipos_de_trabajo # Pasar el diccionario
    )

    if pdf_path and os.path.exists(pdf_path):
        print(f"\nPDF generado exitosamente: {pdf_path}")
        # Abrir el PDF automáticamente
        try:
            if sys.platform == "win32":
                os.startfile(pdf_path)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.call([opener, pdf_path])
        except Exception as e:
            print(f"Error al abrir el PDF: {e}")
    else:
        print("\nError al generar el PDF")

if __name__ == "__main__":
    main()