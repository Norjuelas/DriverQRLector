#TODOokk
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

from PySide2.QtWidgets import *



from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os
from PySide2.QtWidgets import QMessageBox


def generate_vale_pdf_mejorado(ticket_number, referencia, tallas_cantidades, color,
                              total_producido_calculado, barcode_paths, valores_trabajo):
    """
    Genera un vale de trabajo en PDF con formato limpio y funcionalidad completa.
    Incluye todas las secciones de trabajo con sus respectivos códigos de barras y valores.
    
    Args:
        ticket_number: Número del ticket
        referencia: Referencia del producto
        tallas_cantidades: Dict con cantidades por talla {talla: cantidad}
        color: Color del producto
        total_producido_calculado: Total de unidades producidas
        barcode_paths: Dict con rutas de códigos de barras por tipo de trabajo
        valores_trabajo: Dict con valores monetarios por tipo de trabajo
    
    Returns:
        str: Ruta del archivo PDF generado o None si hay error
    """
    
    # === CONFIGURACIÓN INICIAL ===
    safe_referencia = referencia.replace('/', '-').replace('\\', '-')
    pdf_filename = f"vale_{safe_referencia}_{ticket_number}.pdf"
    pdf_path = os.path.join("codes", pdf_filename)
    
    # Configurar documento
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                           leftMargin=0.4*inch, rightMargin=0.4*inch,
                           topMargin=0.4*inch, bottomMargin=0.4*inch)
    styles = getSampleStyleSheet()
    elements = []
    
    # === TIPOS DE TRABAJO DEFINIDOS ===
    tipos_trabajo = {
        "CORTE": "Corte",
        "EMPAQUE": "Empaque", 
        "GUARNECEDOR": "Guarnecedor",
        "MONTADOR": "Montador",
        "PLANTILLAS": "Plantillas",
        "SOLDADOR": "Soldador"
    }
    
    # === CONFIGURACIÓN DE TALLAS ===
    tallas_disponibles = list(range(33, 49))  # Tallas 33-48
    headers_tallas = [str(talla) for talla in tallas_disponibles]
    datos_cantidades = [str(tallas_cantidades.get(str(talla), "0")) for talla in tallas_disponibles]
    
    # Configurar anchos de tabla
    ancho_total = 7.7 * inch
    ancho_por_columna = ancho_total / len(headers_tallas)
    
    # === CREAR ENCABEZADO PRINCIPAL ===
    def crear_encabezado():
        # Obtener código de barras del primer tipo de trabajo
        primer_tipo = next(iter(barcode_paths), None)
        barcode_header_path = barcode_paths.get(primer_tipo, "") if primer_tipo else ""
        
        # Crear imagen del código de barras
        try:
            if barcode_header_path:
                barcode_img = Image(barcode_header_path, width=1.6*inch, height=0.6*inch)
                barcode_img.hAlign = 'RIGHT'
            else:
                barcode_img = Paragraph("(Sin Código)", styles['Normal'])
        except Exception as e:
            print(f"Error cargando código de barras del header: {e}")
            barcode_img = Paragraph("(Error Código)", styles['Normal'])
        
        # Datos del encabezado
        header_data = [
            [Paragraph(f"<b>REFERENCIA:</b> {referencia}", styles['Normal']),
             Paragraph(f"<b>COLOR:</b> {color}", styles['Normal'])],
            [Paragraph(f"<b>N° TICKET:</b> {ticket_number}", styles['Normal']),
             barcode_img]
        ]
        
        # Crear tabla del encabezado
        header_table = Table(header_data, colWidths=[5.2*inch, 2.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('ALIGN', (1,1), (1,1), 'RIGHT'),
        ]))
        
        return header_table
    
    # === CREAR TABLA DE TALLAS ===
    def crear_tabla_tallas():
        tabla_tallas = Table([headers_tallas, datos_cantidades],
                           colWidths=[ancho_por_columna] * len(headers_tallas))
        
        estilo_tallas = TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#B0B0B0")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ])
        
        tabla_tallas.setStyle(estilo_tallas)
        return tabla_tallas
    
    # === CREAR SECCIÓN DE TRABAJO ===
    def crear_seccion_trabajo(nombre_trabajo, clave_trabajo):
        # Obtener valor y código de barras específicos
        valor_trabajo = valores_trabajo.get(clave_trabajo, 0.00)
        barcode_path = barcode_paths.get(clave_trabajo, "")
        
        # Crear imagen del código de barras
        try:
            if barcode_path:
                barcode_img = Image(barcode_path, width=1.6*inch, height=0.6*inch)
                barcode_img.hAlign = 'RIGHT'
            else:
                barcode_img = Paragraph("(Sin Código)", styles['Normal'])
        except Exception as e:
            print(f"Error cargando código de barras para {nombre_trabajo}: {e}")
            barcode_img = Paragraph("(Error Código)", styles['Normal'])
        
        # Componentes de la sección
        titulo = Paragraph(f"<b>{nombre_trabajo}</b>", styles['Normal'])
        tabla_tallas = crear_tabla_tallas()
        
        # Información de valor y firma
        parrafo_valor = Paragraph(f"<b>Valor:</b> {valor_trabajo:.2f}", styles['Normal'])
        parrafo_firma = Paragraph("<b>Firma:</b> ________________________", styles['Normal'])
        
        # Tabla para valor, firma y código
        info_data = [
            [parrafo_valor, parrafo_firma],
            [barcode_img, ""]
        ]
        
        info_table = Table(info_data, colWidths=[ancho_total * 0.5, ancho_total * 0.5])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        # Ensamblar sección completa
        seccion_data = [
            [titulo],
            [tabla_tallas], 
            [info_table]
        ]
        
        seccion_table = Table(seccion_data, colWidths=[ancho_total])
        seccion_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#808080")),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ]))
        
        return seccion_table
    
    # === ENSAMBLAR DOCUMENTO ===
    try:
        # Agregar encabezado
        elements.append(crear_encabezado())
        elements.append(Spacer(1, 0.15*inch))
        
        # Agregar secciones de trabajo
        for nombre_display, clave_interna in tipos_trabajo.items():
            seccion = crear_seccion_trabajo(nombre_display, clave_interna)
            elements.append(seccion)
            elements.append(Spacer(1, 0.1*inch))
        
        # Agregar total general
        total_paragraph = Paragraph(
            f"<b>TOTAL GENERAL PRODUCIDO (UNIDADES): {total_producido_calculado}</b>", 
            styles['Heading3']
        )
        total_paragraph.hAlign = 'CENTER'
        elements.append(Spacer(1, 0.15*inch))
        elements.append(total_paragraph)
        
        # Generar PDF
        doc.build(elements)
        print(f"PDF generado exitosamente: {pdf_path}")
        return pdf_path
        
    except Exception as e:
        print(f"Error al generar el PDF del vale '{pdf_filename}': {e}")
        QMessageBox.critical(None, "Error PDF", f"No se pudo generar el PDF:\n{e}")
        return None











def generate_vale_pdf( ticket_number, referencia, tallas_cantidades, color,
                    total_producido_calculado, barcode_paths, valores_trabajo):
    """
    Genera un vale de trabajo en PDF con 6 secciones (una por tipo de trabajo)
    en una sola página, detallando las cantidades por talla y el código de barras para cada sección.
    The header uses the first work type's barcode path, accessed via barcode_paths.get(first_work_type, "").
    """
    safe_referencia = referencia.replace('/', '-').replace('\\', '-')
    pdf_filename = f"vale_{safe_referencia}_{ticket_number}.pdf"
    pdf_path = os.path.join("codes", pdf_filename)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=0.4*inch, rightMargin=0.4*inch,
                            topMargin=0.4*inch, bottomMargin=0.4*inch)
    styles = getSampleStyleSheet()
    elements = []

    # --- 1. Encabezado General del Ticket ---
    first_work_type = next(iter(barcode_paths), None)
    header_barcode_path = barcode_paths.get(first_work_type, "") if first_work_type else ""
    try:
        barcode_img_obj = Image(header_barcode_path, width=1.6*inch, height=0.6*inch) if header_barcode_path else Paragraph("(Sin Código)", styles['Normal'])
        barcode_img_obj.hAlign = 'RIGHT'
    except Exception as e:
        print(f"Advertencia: No se pudo cargar la imagen del código de barras {header_barcode_path}: {e}")
        barcode_img_obj = Paragraph("(Error Código Barras)", styles['Normal'])

    header_content_data = [
        [Paragraph(f"<b>REFERENCIA:</b> {referencia}", styles['Normal']),
        Paragraph(f"<b>COLOR:</b> {color}", styles['Normal'])],
        [Paragraph(f"<b>N° TICKET:</b> {ticket_number}", styles['Normal']),
        barcode_img_obj]
    ]
    
    header_table = Table(header_content_data, colWidths=[5.2*inch, 2.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('SPAN', (1,1), (1,1)),
        ('ALIGN', (1,1), (1,1), 'RIGHT'),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.15*inch))

    # --- 2. Secciones por Tipo de Trabajo ---
    tipos_de_trabajo_definidos = {
        "CORTE": "Corte",
        "EMPAQUE": "Empaque",
        "GUARNECEDOR": "Guarnecedor",
        "MONTADOR": "Montador",
        "PLANTILLAS": "Plantillas",
        "SOLDADOR": "Soldador"
    }

    tallas_column_headers = [str(s) for s in range(33, 49)]
    num_tallas_columnas = len(tallas_column_headers)
    fila_datos_cantidades = [str(tallas_cantidades.get(str(s), "0")) for s in range(33, 49)]
    ancho_tabla_tallas_disponible = 7.7 * inch
    ancho_columna_talla = ancho_tabla_tallas_disponible / num_tallas_columnas

    estilo_tabla_tallas = TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#B0B0B0")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E8E8E8")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ])

    for nombre_display, llave_valor in tipos_de_trabajo_definidos.items():
        valor_especifico_trabajo = valores_trabajo.get(llave_valor, 0.00)
        barcode_path = barcode_paths.get(llave_valor, "")
        try:
            barcode_img = Image(barcode_path, width=1.6*inch, height=0.6*inch) if barcode_path else Paragraph("(Sin Código)", styles['Normal'])
            barcode_img.hAlign = 'RIGHT'
        except Exception as e:
            print(f"Advertencia: No se pudo cargar la imagen del código de barras {barcode_path}: {e}")
            barcode_img = Paragraph("(Error Código Barras)", styles['Normal'])

        tabla_tallas_actual = Table([tallas_column_headers, fila_datos_cantidades],
                                    colWidths=[ancho_columna_talla] * num_tallas_columnas)
        tabla_tallas_actual.setStyle(estilo_tabla_tallas)

        titulo_seccion = Paragraph(f"<b>{nombre_display}</b>", styles['Normal'])
        parrafo_valor = Paragraph(f"<b>Valor:</b> {valor_especifico_trabajo:.2f}", styles['Normal'])
        parrafo_firma = Paragraph("<b>Firma:</b> ________________________", styles['Normal'])
        parrafo_codigo = barcode_img

        tabla_valor_firma_codigo_data = [
            [parrafo_valor, parrafo_firma],
            [parrafo_codigo, ""]
        ]
        tabla_valor_firma_codigo = Table(tabla_valor_firma_codigo_data,
                                        colWidths=[ancho_tabla_tallas_disponible * 0.5,
                                                    ancho_tabla_tallas_disponible * 0.5])
        tabla_valor_firma_codigo.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (0,0), 'LEFT'),
            ('ALIGN', (0,1), (0,1), 'RIGHT'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 3),
        ]))

        datos_tabla_seccion = [
            [titulo_seccion],
            [tabla_tallas_actual],
            [tabla_valor_firma_codigo]
        ]
        tabla_seccion = Table(datos_tabla_seccion, colWidths=[ancho_tabla_tallas_disponible])
        tabla_seccion.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#808080")),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (0,0), 5),
        ]))
        
        elements.append(tabla_seccion)
        elements.append(Spacer(1, 0.1*inch))

    parrafo_total_general = Paragraph(f"<b>TOTAL GENERAL PRODUCIDO (UNIDADES): {total_producido_calculado}</b>", styles['h3'])
    parrafo_total_general.hAlign = 'CENTER'
    elements.append(Spacer(1, 0.15*inch))
    elements.append(parrafo_total_general)

    try:
        doc.build(elements)
        return pdf_path
    except Exception as e:
        print(f"Error al generar el PDF del vale '{pdf_filename}': {e}")
        QMessageBox.critical( "Error PDF", f"No se pudo generar el PDF:\n{e}")
        return None
    




def generate_vale_pdf_formatoquemegusta( ticket_numbers, tipo_trabajo, referencia, tallas_cantidades, color, total_producido, serial_code_path):
    """
    Generate a PDF work voucher with multiple tickets on a single page.
    """
    # Create PDF filename and path
    pdf_filename = f"vale_{tipo_trabajo}_{ticket_numbers}.pdf"
    pdf_path = os.path.join("codes", pdf_filename)

    # Create the PDF document
    doc = SimpleDocTemplate(pdf_path, pagesize=letter,
                            leftMargin=30, rightMargin=30,
                            topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    elements = []

    # Define sizes (columns: 33 to 48 inclusive)
    sizes = list(range(33, 49))
    size_row = [str(size) for size in sizes]

    # Calculate how many vales we need to fill the PDF
    vales_per_page = 5  # Based on your PageBreak logic
    total_pages_needed = 1  # You can adjust this or make it a parameter
    total_vales_needed = vales_per_page * total_pages_needed
    
    # If we have fewer ticket numbers than needed, repeat them
    extended_ticket_numbers = []
    ticket_count = len(ticket_numbers)
    
    for i in range(total_vales_needed):
        # Cycle through the ticket numbers if we need more vales than tickets
        ticket_index = i % ticket_count
        extended_ticket_numbers.append(ticket_numbers[ticket_index])
    
    # Create a frame for multiple tickets
    for i, ticket_number in enumerate(extended_ticket_numbers):
        # Prepare quantities row
        qty_row = [str(tallas_cantidades.get(str(size), 0)) for size in sizes]

        # Prepare barcode image
        barcode_img = Image(serial_code_path, width=100, height=40)

        # Create main container table
        container_data = [[
            Paragraph(f"{tipo_trabajo.upper()}", styles['Heading2']),
            "",
            barcode_img
        ]]
        container_table = Table(container_data, colWidths=[300, 50, 200])
        container_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX', (0, 0), (-1, -1), 2, colors.green)
        ]))

        # Ticket details table
        details_data = [
            ["Referencia:", referencia, "Color:", color, f"N° {ticket_number}"]
        ]
        details_table = Table(details_data, colWidths=[100, 150, 80, 100, 100])
        details_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOX', (0, 0), (-1, -1), 1, colors.green)
        ]))

        # Sizes and quantities table
        sizes_table = Table([size_row, qty_row], colWidths=[30] * len(size_row))
        sizes_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.green),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
        ]))

        # Footer table
        footer_data = [["Firma:", "", "", "Total:", str(total_producido)]]
        footer_table = Table(footer_data, colWidths=[100, 150, 100, 80, 100])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('BOX', (0, 0), (-1, -1), 1, colors.green)
        ]))

        # **SOLUCIÓN**: Agrupar todos los componentes en una sola tabla contenedora
        complete_vale_data = [
            [container_table],
            [details_table],
            [sizes_table],
            [footer_table]
        ]
        
        complete_vale_table = Table(complete_vale_data, colWidths=[530])
        complete_vale_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        # Agregar el vale completo como una unidad
        elements.append(KeepTogether([complete_vale_table]))
        
        # Agregar espaciado entre vales
        if i < len(extended_ticket_numbers) - 1:
            elements.append(Spacer(1, 10))

        # Insert page break every 3 tickets
        if (i + 1) % 5 == 0 and (i + 1) < len(extended_ticket_numbers):
            elements.append(PageBreak())

    # Build PDF
    doc.build(elements)
    return pdf_path


