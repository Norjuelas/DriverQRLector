#TODOokk
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import os
import sys
from PySide2.QtWidgets import QMessageBox

def generate_vale_pdf(ticket_number, referencia, tallas_cantidades, color,
                          total_producido_calculado, barcode_paths, valores_trabajo):
    """
    Genera un vale de trabajo con múltiples secciones (por tipo de trabajo), cada una con:
    - Encabezado con tipo de trabajo, referencia, color y ticket.
    - Tabla de tallas.
    - Código de barras específico por trabajo.
    - Firma y valor.
    """
    safe_referencia = referencia.replace('/', '-').replace('\\', '-')
    pdf_filename = f"vale_{safe_referencia}_{ticket_number}.pdf"
    pdf_path = os.path.join("codes", pdf_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=30, rightMargin=30,
                            topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    styles['Heading2'].fontSize = 6  # Encabezado tipo de trabajo
    styles['Normal'].fontSize = 6     # Texto normal
    styles['Heading3'].fontSize = 6
    elements = []

    tipos_de_trabajo = {
        "CORTE": "Corte",
        "EMPAQUE": "Empaque",
        "GUARNECEDOR": "Guarnecedor",
        "MONTADOR": "Montador",
        "PLANTILLAS": "Plantillas",
        "SOLDADOR": "Soldador"
    }

    sizes = list(range(33, 49))
    size_row = [str(s) for s in sizes]
    qty_row = [str(tallas_cantidades.get(str(s), 0)) for s in sizes]

    for tipo_clave, tipo_display in tipos_de_trabajo.items():
        barcode_path = barcode_paths.get(tipo_display, "")
        total_producido_calculado = total_producido_calculado

        # Código de barras
        try:
            barcode_img = Image(
                barcode_path, 
                width=300,   # Ancho aumentado
                height=50, 
                kind='proportional',  # Mantiene relación de aspecto
                hAlign='RIGHT'
            )
        except Exception as e:
            print(f"Error cargando código de barras: {e}")
            barcode_img = Paragraph("(Error Código)", styles['Normal'])

        # Encabezado vale
        container_data = [[
            Paragraph(f"{tipo_display}", styles['Heading2']),
            "",
            barcode_img
        ]]
        container_table = Table(container_data, colWidths=[200, 0, 160])
        container_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.grey),
            ('LEFTPADDING', (2,0), (2,0), 0),  # Eliminar padding izquierdo en código
            ('RIGHTPADDING', (2,0), (2,0), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))


        # Detalles de referencia
        details_data = [
            ["Referencia:", referencia, "Color:", color, f"N° {ticket_number}"]
        ]
        details_table = Table(details_data, colWidths=[80, 120, 60, 80, 80])

        details_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 6),
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 1),
        ]))
        # Tabla de tallas
        sizes_table = Table([size_row, qty_row], colWidths=[25] * len(size_row))

        sizes_table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 6),
            ('LEADING', (0,0), (-1,-1), 6),  # Espaciado entre filas
            ('PADDING', (0,0), (-1,-1), 1),
        ]))

        # Pie de vale
        footer_data = [
            ["Firma:", "", "", "total:", f"${total_producido_calculado:.2f}"]
        ]
        footer_table = Table(footer_data, colWidths=[80, 120, 80, 60, 80])

        footer_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 6),
            ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 1),
        ]))

        # Agrupamos todo el vale
        complete_vale_data = [
            [container_table],
            [details_table],
            [sizes_table],
            [footer_table]
        ]
        complete_vale_table = Table(complete_vale_data, colWidths=[480])

        complete_vale_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1),  # Reducido de 4
            ('BOTTOMPADDING', (0,0), (-1,-1), 1), # Reducido de 4
        ]))

        # Añadir vale al documento
        elements.append(KeepTogether([complete_vale_table]))
        elements.append(Spacer(1, 2))

    elements.append(Spacer(1, 1))

    try:
        doc.build(elements)
        
        return pdf_path
    except Exception as e:
        print(f"Error al generar el PDF: {e}")
        QMessageBox.critical(None, "Error PDF", f"No se pudo generar el PDF:\n{e}")
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
        "total_producido_calculado": 60,
        "valores_trabajo": {
            "Corte": 150.50,
            "Empaque": 75.00,
            "Guarnecedor": 200.00,
            "Montador": 180.75,
            "Plantillas": 90.25,
            "Soldador": 300.00
        }
    }
    
    # Generar códigos de barras para cada tipo de trabajo
    barcode_paths = {}
    work_type_abbreviations = {
        "Corte": "CT",
        "Empaque": "EM",
        "Guarnecedor": "GU",
        "Montador": "MO",
        "Plantillas": "PL",
        "Soldador": "SO"
    }
    
    for work_type, abbr in work_type_abbreviations.items():
        from generateCodes import generate_serial_code, generate_barcode
        serial_code = generate_serial_code(
            ticket_number=test_data["ticket_number"],
            referencia=test_data["referencia"],
            color=test_data["color"],
            tallas_cantidades=test_data["tallas_cantidades"],
            work_type_abbr=abbr
        )
        
        barcode_path = generate_barcode(serial_code)
        if barcode_path:
            barcode_paths[work_type] = barcode_path
            print(f"Código generado para {work_type}: {barcode_path}")
        else:
            print(f"Error generando código para {work_type}")
            barcode_paths[work_type] = ""
    
    # Generar el PDF
    pdf_path = generate_vale_pdf(
        ticket_number=test_data["ticket_number"],
        referencia=test_data["referencia"],
        tallas_cantidades=test_data["tallas_cantidades"],
        color=test_data["color"],
        total_producido_calculado=test_data["total_producido_calculado"],
        barcode_paths=barcode_paths,
        valores_trabajo=test_data["valores_trabajo"]
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
    import subprocess
    main()