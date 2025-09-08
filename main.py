import sys
import os
import platform
from typing import Any, Dict
import uuid
import traceback
import datetime as dt
import time
import pandas as pd
import re
from openpyxl import Workbook, load_workbook

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (
    QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, 
    QObject, QPoint, QRect, QSize, QTime, QThread, QUrl, Qt, QEvent
)
from PySide2.QtGui import (
    QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, 
    QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient
)
from PySide2.QtWidgets import *
from openpyxl.styles import Font, PatternFill, Alignment

from PySide2.QtWidgets import QTableView, QVBoxLayout
from PySide2.QtGui import QStandardItemModel

# Imports 
from generate_pdf import generar_vales_pdf,increment_ticket_number

from utils import validate_cedula, display_code_image

from config import TIPOS_DE_TRABAJO, WORK_TYPE_ABBREVIATIONS, CAMPOS_VALOR_TRABAJO_MAP, WORK_TYPES # Importamos la configuración central

# GUI FILE

# GUI FILE
from ui_main import Ui_MainWindow

# IMPORT QSS CUSTOM
from ui_styles import Style

## ==> APP FUNCTIONS
from backup_thread import BackupThread, BackupManager

from autocompletado import *

from generate_pdf import *

from generateCodes import *
from db import init_db

from dao import guardar_o_actualizar_trabajo,buscar_trabajo_por_codigo_serial, vale_existe, crear_vale

class MainWindow(QMainWindow):
    DB_EXCEL_PATH = "database.xlsx"
    DB_EXCEL_SHEET_NAME = "Trabajos"
    PDF_OUTPUT_DIR = "codes"
    
    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dragPos = None
        # Current code type (barcode or qr)
        self.current_code_type = "barcode"  # Default to barcode

        # Print system information
        print('System: ' + platform.system())
        print('Version: ' + platform.release())

        # Setup the window
        self.setup_window()
        
        # Setup menus
        self.setup_menus()
        
        # Setup barcode generator functionality
        self.setup_code_generator()
        
        # Setup code reader functionality
        self.setup_code_reader()
        
        # Setup employee management
        self.setup_employee_management()

        # Conectar el botón de eliminarTODO (agregar esta línea)
        self.setup_eliminar_todo_button()

        # Setup update reports button
        self.setup_update_button()
        
        # Setup add employee button
        self.setup_add_employee_button()

        self.autocompletado_manager = AutocompletadoManager()
        self.setup_autocompletado_fields()

        # Show the window
        self.show()

    def setup_code_reader(self):
        """
        Configura el lector de código y la tabla de visualización de vales.
        """
        if not hasattr(self.ui, 'codeReaderInput'):
            print("ERROR: codeReaderInput no encontrado en la UI.")
            return
        
        # Conectar la señal `returnPressed` para activar el escaneo
        self.ui.codeReaderInput.returnPressed.connect(self.on_code_scanned)
        print("Manejador de escaneo de código conectado.")

        # Configurar la tabla de visualización
        if hasattr(self.ui, 'WidgetTabla'):
            # Crear layout si no existe
            if self.ui.WidgetTabla.layout() is None:
                table_layout = QVBoxLayout(self.ui.WidgetTabla)
                self.ui.WidgetTabla.setLayout(table_layout)
            else:
                table_layout = self.ui.WidgetTabla.layout()
            
            # Crear tabla y modelo si no existen
            if not hasattr(self.ui, 'tableViewVale'):
                self.ui.tableViewVale = QTableView()
                table_layout.addWidget(self.ui.tableViewVale)
                self.table_model = QtGui.QStandardItemModel()
                self.ui.tableViewVale.setModel(self.table_model)
            
            # Definir las cabeceras de la tabla (más simples y directas)
            headers = [
                "Código Serial", "N° Ticket", "Referencia", "Tipo Trabajo", 
                "Color", "Total Pares", "Valor Pagado"
            ]
            self.table_model.setHorizontalHeaderLabels(headers)

            # Ajustar el tamaño de las columnas
            header_view = self.ui.tableViewVale.horizontalHeader()
            header_view.setSectionResizeMode(QHeaderView.Stretch)
            print("Tabla de vales configurada.")
        else:
            print("ADVERTENCIA: WidgetTabla no encontrado en la UI.")


    def setup_code_generator(self):
        """
        Configura la funcionalidad del generador de códigos y el archivo Excel.
        (Actualizado para usar los nuevos tipos de trabajo)
        """
        self.excel_path = "database.xlsx"
        self.vales_sheet_name = "Vales"

        if not os.path.exists("codes"):
            os.makedirs("codes")

        # Usar los nuevos tipos de trabajo definidos globalmente o en la clase
        work_types = list(WORK_TYPE_ABBREVIATIONS.keys())

        # Definir las cabeceras para la hoja "Trabajos"
        trabajos_headers = ["Código Serial", "Número Ticket", "Referencia", "Color"]
        for i in range(33, 49):
            trabajos_headers.append(f"Cant_T{i}")
        trabajos_headers.append("Total Producido")

        # Añadir cabeceras para los valores de los nuevos tipos de trabajo
        trabajos_headers.extend([f"Valor {wt}" for wt in work_types])

        trabajos_headers.extend(["Tipo Código", "Ruta Imagen"])

        # Añadir columnas para los códigos seriales por TIPO NUEVO de trabajo
        trabajos_headers.extend([f"Código_{wt}" for wt in work_types])

        # Definir las cabeceras para la hoja "Vales" (Mantener si no cambia)
        vales_headers = [
            "ID_Vale", "EmpleadoID", "FechaHora_Generacion", "Numero_Ticket_Asociado",
            "Referencia_Asociada", "Color_Trabajo", "Resumen_Tallas_Cantidades",
            "Total_Producido_Trabajo", "Suma_Valores_Trabajos", "Codigo_Serial_Trabajo_Asociado",
            "WorkTypeDetected"
        ]

        # Crear/Cargar Excel y verificar/actualizar cabeceras (Tu lógica existente)
        if not os.path.exists(self.excel_path):
            wb = Workbook()
            ws_trabajos = wb.active
            ws_trabajos.title = "Trabajos"
            ws_trabajos.append(trabajos_headers)
            ws_vales = wb.create_sheet(title=self.vales_sheet_name)
            ws_vales.append(vales_headers)
            wb.save(self.excel_path)
        else:
            wb = load_workbook(self.excel_path)
            ws_trabajos = wb["Trabajos"]
            current_headers = [cell.value for cell in ws_trabajos[1]]
            if current_headers != trabajos_headers:
                print("Actualizando cabeceras de la hoja 'Trabajos'...")
                # Considera una migración más segura si ya hay datos
                ws_trabajos.delete_rows(1)
                ws_trabajos.insert_rows(1)
                for col_idx, header in enumerate(trabajos_headers, 1):
                    ws_trabajos.cell(row=1, column=col_idx).value = header
                wb.save(self.excel_path)

            if self.vales_sheet_name not in wb.sheetnames:
                ws_vales = wb.create_sheet(title=self.vales_sheet_name)
                ws_vales.append(vales_headers)
                wb.save(self.excel_path)

        # Conectar botón (Tu lógica existente)
        if hasattr(self.ui, 'pushButtonGuardar'):
            self.ui.pushButtonGuardar.clicked.connect(self.on_save_button_clicked)
        else:
            print("Advertencia: self.ui.pushButtonGuardar no encontrado.")

        # Configurar escena (Tu lógica existente)
        if hasattr(self.ui, 'PreviwImage'):
            if self.ui.PreviwImage.scene() is None:
                self.ui.PreviwImage.setScene(QtWidgets.QGraphicsScene(self))
        else:
            print("Advertencia: self.ui.PreviwImage no encontrado.")

    def save_to_excel(self, data_to_save: Dict[str, Any]) -> bool:
        """
        Guarda o añade eficientemente los datos de un vale a un archivo Excel.

        Esta versión está corregida, mejorada con manejo de errores específico y
        es más robusta contra problemas comunes como archivos abiertos o hojas eliminadas.
        """
        try:
            # 1. DEFINIR LA ESTRUCTURA Y ORDEN CORRECTO DE LAS COLUMNAS
            # Esta lógica se mantiene, ya que define el "contrato" de cómo deben ser los datos.
            all_work_types = WORK_TYPE_ABBREVIATIONS.keys()
            
            headers = [
                'Número Ticket', 'Referencia', 'Color'
            ]
            headers.extend([f'Cant_T{i}' for i in range(33, 49)])
            headers.append('Total Producido')
            headers.extend([f'Valor {wt}' for wt in all_work_types])
            headers.extend([f'Código_{wt.replace(" ", "_")}' for wt in all_work_types])
            headers.extend(['ID_Vale_Unico', 'Timestamp', 'Estado'])

            # 2. PREPARAR LOS DATOS DE LA FILA EN UN DICCIONARIO
            # Se mapean los datos de entrada a los nombres de columna esperados.
            row_data = {
                'Número Ticket': data_to_save.get('ticket_number'),
                'Referencia': data_to_save.get('referencia'),
                'Color': data_to_save.get('color'),
                'Total Producido': data_to_save.get('total_producido'),
                'ID_Vale_Unico': data_to_save.get('id_vale_unico'),
                'Timestamp': data_to_save.get('timestamp'),
                'Estado': data_to_save.get('estado')
            }

            # Añadir tallas (con valor por defecto 0)
            for i in range(33, 49):
                row_data[f'Cant_T{i}'] = data_to_save.get('tallas_cantidades', {}).get(str(i), 0)

            # Añadir valores y códigos
            for work_type in all_work_types:
                # <--- CORRECCIÓN CLAVE ---
                # Se añade la variable 'work_type' a la f-string.
                row_data[f'Valor {work_type}'] = data_to_save.get('valores_trabajo', {}).get(work_type, 0)
                row_data[f'Código_{work_type.replace(" ", "_")}'] = data_to_save.get('serial_codes', {}).get(work_type, "")

            # 3. CONVERTIR A LISTA ORDENADA SEGÚN LOS ENCABEZADOS
            # Esta es la parte más importante para evitar desfases. ¡Excelente práctica!
            ordered_row = [row_data.get(h) for h in headers]

            # 4. GUARDAR LOS DATOS EN EL ARCHIVO EXCEL
            file_path = self.DB_EXCEL_PATH
            sheet_name = self.DB_EXCEL_SHEET_NAME
            
            if not os.path.exists(file_path):
                # Si el archivo no existe, lo creamos con encabezados usando pandas.
                print(f"Archivo '{file_path}' no encontrado. Creando nuevo archivo.")
                df = pd.DataFrame([ordered_row], columns=headers)
                df.to_excel(file_path, index=False, sheet_name=sheet_name)
            else:
                # Si ya existe, usamos openpyxl para añadir la fila eficientemente.
                workbook = load_workbook(file_path)
                
                # --- MEJORA 1: VERIFICAR SI LA HOJA EXISTE ---
                if sheet_name not in workbook.sheetnames:
                    print(f"Hoja '{sheet_name}' no encontrada en el archivo. Creando hoja y añadiendo encabezados.")
                    sheet = workbook.create_sheet(sheet_name)
                    sheet.append(headers) # Añadir encabezados a la nueva hoja
                else:
                    sheet = workbook[sheet_name]
                
                sheet.append(ordered_row)
                workbook.save(file_path)

            print(f"Datos del ticket {data_to_save.get('ticket_number')} guardados exitosamente en Excel.")
            return True

        # --- MEJORA 2: MANEJO DE ERRORES ESPECÍFICO ---
        except PermissionError:
            print(f"ERROR: No se puede escribir en el archivo '{self.DB_EXCEL_PATH}'. ¿Está abierto en Excel?")
            # Aquí podrías usar QMessageBox para notificar al usuario.
            return False
        except KeyError as e:
            print(f"ERROR: Configuración incorrecta. No se encontró la clave o la hoja: {e}")
            return False
        except Exception as e:
            # Captura cualquier otro error inesperado.
            print(f"ERROR: Ocurrió un error inesperado al guardar en Excel: {e}")
            import traceback
            traceback.print_exc() # Imprime el stack trace completo para depuración
            return False

    def find_code_data(self, serial_code):
        """Find data related to a specific serial code in the Excel file"""
        try:
            # Load Excel file
            wb = load_workbook(self.excel_path)
            ws = wb["Trabajos"]  # Explicitly use "Trabajos" sheet

            # Obtener encabezados para buscar índices de columnas
            headers = [cell.value for cell in ws[1]]
            try:
                serial_code_idx = headers.index("Código Serial")
                num_ticket_idx = headers.index("Número Ticket")
                referencia_idx = headers.index("Referencia")
                color_idx = headers.index("Color")
                total_producido_idx = headers.index("Total Producido")
                # Mapear índices de columnas para valores de trabajo
                valor_indices = {}
                for work_type in WORK_TYPE_ABBREVIATIONS.keys():
                    valor_column = f"Valor {work_type}"
                    if valor_column in headers:
                        valor_indices[work_type] = headers.index(valor_column)
            except ValueError as e:
                QMessageBox.critical(self, "Error", f"Columna faltante en 'Trabajos': {e}")
                return None

            # Search for the serial code in the first column
            for row in ws.iter_rows(min_row=2, values_only=True):
                if row[serial_code_idx] == serial_code:
                    # Construir diccionario de datos
                    data = {
                        "serial_code": row[serial_code_idx],
                        "num_ticket": row[num_ticket_idx],
                        "referencia": row[referencia_idx],
                        "color": row[color_idx],
                        "total_producido": row[total_producido_idx]
                    }
                    # Añadir valores de trabajo
                    for work_type, idx in valor_indices.items():
                        key = f"valor_{work_type.lower().replace(' ', '_')}"
                        data[key] = row[idx] if idx < len(row) else 0
                    return data

            return None
        except Exception as e:
            print(f"Error al buscar datos: {e}")
            QMessageBox.critical(self, "Error", f"Error al buscar datos: {str(e)}")
            return None

    def setup_update_button(self):
        """Conecta el botón ActualizarDB para generar reportes de empleados."""
        if hasattr(self.ui, 'btnActualizarDB'):
            try:
                self.ui.btnActualizarDB.clicked.disconnect()
            except RuntimeError:
                pass
            self.ui.btnActualizarDB.clicked.connect(self.update_employee_reports)
            self.ui.btnActualizarDB.setEnabled(True)
            print("Botón 'btnActualizarDB' conectado correctamente.")
        else:
            print("ERROR: El QPushButton 'btnActualizarDB' no se encontró en la UI.")

    def setup_autocompletado_fields(self):
        """
        Configura el autocompletado para los campos QLineEdit relevantes usando la BD.
        """
        campos_a_configurar = {}

        # Mapeo de campos de la UI a columnas de la BD
        # Formato: 'id_unico': {'line_edit': QLineEdit, 'tabla': str, 'columna': str}
        
        # --- Campos de la tabla 'trabajos' ---
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            campos_a_configurar['referencia'] = {
                'line_edit': self.ui.CampoReferenciaTrabajo,
                'tabla': 'trabajos',
                'columna': 'referencia'  # Usar nombres de columna del schema.sql
            }
        if hasattr(self.ui, 'CampoNumeroTicket'):
            campos_a_configurar['numero_ticket'] = {
                'line_edit': self.ui.CampoNumeroTicket,
                'tabla': 'trabajos',
                'columna': 'numero_ticket'
            }
        if hasattr(self.ui, 'CampoColor'):
            campos_a_configurar['color'] = {
                'line_edit': self.ui.CampoColor,
                'tabla': 'trabajos',
                'columna': 'color'
            }
        
        # --- Campos de la tabla 'empleados' (ejemplo) ---
        # Si tienes un campo para buscar empleados por nombre:
        if hasattr(self.ui, 'CampoNombreEmpleado'):
             campos_a_configurar['nombre_empleado'] = {
                'line_edit': self.ui.CampoNombreEmpleado,
                'tabla': 'empleados',
                'columna': 'nombre'
            }

        # Nota: Generalmente no se necesita autocompletado para valores numéricos como
        # cantidades de tallas o valores monetarios, ya que no suelen repetirse
        # de forma que el autocompletado sea útil. Si aún así lo deseas, puedes
        # agregarlos aquí siguiendo el mismo patrón.
        
        if campos_a_configurar:
            print("Configurando autocompletado desde la base de datos...")
            self.autocompletado_manager.configurar_multiples_campos(campos_a_configurar)
            print("Autocompletado configurado.")
        else:
            print("No se encontraron campos de UI para configurar el autocompletado.")



    def update_employee_reports(self):
        """
        Función combinada que:
        1. Genera un reporte consolidado por empleado y lo muestra en tableViewVale
        2. Crea hojas individuales por empleado con detalles completos y consolidados
        3. Maneja la nueva estructura donde cada vale tiene valores diferenciados por tipo de trabajo
        """
        try:
            print("Actualizando reportes de empleados...")
            
            # Cargar el archivo Excel
            wb = load_workbook(self.excel_path)
            
            # Verificar si existen las hojas necesarias
            if "Vales" not in wb.sheetnames or "Empleados" not in wb.sheetnames:
                QMessageBox.warning(self, "Error", "No se encontraron las hojas 'Vales' o 'Empleados' en el archivo Excel.")
                return
            
            ws_vales = wb[self.vales_sheet_name]
            ws_empleados = wb["Empleados"]

            # Obtener información de empleados
            empleados = {}
            for row in ws_empleados.iter_rows(min_row=2, max_col=5, values_only=True):
                if len(row) >= 5 and row[4]:  # EmpleadoID existe
                    empleados[row[4]] = {
                        "Nombre": row[0] or "Sin Nombre",
                        "Cedula": row[1] or "",
                        "Celular": row[2] or "",
                        "Correo": row[3] or ""
                    }

            if not empleados:
                QMessageBox.information(self, "Info", "No hay empleados registrados en la base de datos.")
                return

            # LEER Y PROCESAR DATOS DE VALES
            vales_data = []
            headers = []
            
            # Obtener encabezados
            for cell in ws_vales[1]:
                headers.append(cell.value)
            
            # Buscar índices de columnas importantes
            try:
                empleado_id_idx = headers.index("EmpleadoID")
                fecha_idx = headers.index("FechaHora_Generacion")
                valor_idx = headers.index("Suma_Valores_Trabajos")

                id_col_name = "ID_Vale"
                id_idx = headers.index(id_col_name) if id_col_name in headers else None
                
                num_ticket_col_name = "Numero_Ticket_Asociado"
                num_ticket_idx = headers.index(num_ticket_col_name) if num_ticket_col_name in headers else None
                
                referencia_col_name = "Referencia_Asociada"
                referencia_idx = headers.index(referencia_col_name) if referencia_col_name in headers else None
                
                talla_col_name = "Resumen_Tallas_Cantidades"
                talla_idx = headers.index(talla_col_name) if talla_col_name in headers else None
                
                color_col_name = "Color_Trabajo"
                color_idx = headers.index(color_col_name) if color_col_name in headers else None
                
                total_producido_col_name = "Total_Producido_Trabajo"
                total_producido_idx = headers.index(total_producido_col_name) if total_producido_col_name in headers else None
                
                codigo_serial_col_name = "Codigo_Serial_Trabajo_Asociado"
                codigo_serial_idx = headers.index(codigo_serial_col_name) if codigo_serial_col_name in headers else None
                
                work_type_col_name = "WorkTypeDetected"
                work_type_idx = headers.index(work_type_col_name) if work_type_col_name in headers else None

            except ValueError as e:
                QMessageBox.warning(self, "Error", f"Falta una columna esencial en 'Vales' para generar reportes: {e}")
                return
            
            # Leer datos de vales
            for row in ws_vales.iter_rows(min_row=2, values_only=True):
                if len(row) > empleado_id_idx and row[empleado_id_idx]:
                    vale_dict = {
                        "empleado_id": row[empleado_id_idx],
                        "fecha": row[fecha_idx] if fecha_idx < len(row) else None,
                        "valor": row[valor_idx] if valor_idx < len(row) else None,
                        "id": row[id_idx] if id_idx is not None and id_idx < len(row) else None,
                        "num_ticket": row[num_ticket_idx] if num_ticket_idx is not None and num_ticket_idx < len(row) else None,
                        "referencia": row[referencia_idx] if referencia_idx is not None and referencia_idx < len(row) else None,
                        "talla": row[talla_idx] if talla_idx is not None and talla_idx < len(row) else None,
                        "color": row[color_idx] if color_idx is not None and color_idx < len(row) else None,
                        "total_producido": row[total_producido_idx] if total_producido_idx is not None and total_producido_idx < len(row) else None,
                        "codigo_serial": row[codigo_serial_idx] if codigo_serial_idx is not None and codigo_serial_idx < len(row) else None,
                        "work_type_detected": row[work_type_idx] if work_type_idx is not None and work_type_idx < len(row) else None
                    }
                    vales_data.append(vale_dict)

            # Invertir WORK_TYPE_ABBREVIATIONS para mapear códigos a nombres completos
            work_type_mapping = {v: k for k, v in WORK_TYPE_ABBREVIATIONS.items()}

            # Inicializar datos del reporte consolidado
            report_data = {}
            for emp_id in empleados:
                report_data[emp_id] = {
                    "Nombre": empleados[emp_id]["Nombre"],
                    "Total_Vales": 0,
                    "Total_Valor": 0.0,
                    "Trabajos": {work_type: 0 for work_type in WORK_TYPE_ABBREVIATIONS.keys()}
                }

            # Procesar vales para el reporte consolidado
            for vale in vales_data:
                emp_id = vale["empleado_id"]
                if emp_id in report_data:
                    report_data[emp_id]["Total_Vales"] += 1
                    
                    if vale["valor"] is not None:
                        try:
                            valor = float(vale["valor"])
                            report_data[emp_id]["Total_Valor"] += valor
                        except (ValueError, TypeError):
                            pass
                    
                    work_type = vale["work_type_detected"]
                    if work_type and work_type in work_type_mapping:
                        mapped_work_type = work_type_mapping[work_type]
                        if mapped_work_type in report_data[emp_id]["Trabajos"]:
                            report_data[emp_id]["Trabajos"][mapped_work_type] += 1

            # PARTE 1: Actualizar la tabla de previsualización (reporte consolidado)
            if hasattr(self.ui, 'tableViewVale') and hasattr(self, 'table_model'):
                self.table_model.clear()
                # Definir encabezados: fijos + dinámicos basados en WORK_TYPE_ABBREVIATIONS
                fixed_headers = ["EmpleadoID", "Nombre", "Total Vales", "Total Valor"]
                work_type_headers = list(WORK_TYPE_ABBREVIATIONS.keys())
                self.table_model.setHorizontalHeaderLabels(fixed_headers + work_type_headers)
                
                for emp_id, data in report_data.items():
                    row_data = [
                        emp_id,
                        data["Nombre"],
                        data["Total_Vales"],
                        round(data["Total_Valor"], 2)
                    ] + [data["Trabajos"][work_type] for work_type in WORK_TYPE_ABBREVIATIONS.keys()]
                    items = [QtGui.QStandardItem(str(value)) for value in row_data]
                    self.table_model.appendRow(items)
                
                self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                print("Reporte consolidado generado y mostrado en 'tableViewVale'.")
            else:
                print("Advertencia: No se pudo actualizar la tabla 'tableViewVale'.")

            # PARTE 2: Crear hojas individuales por empleado
            for empleado_id, empleado_info in empleados.items():
                vales_empleado = [vale for vale in vales_data if vale["empleado_id"] == empleado_id]
                
                sheet_name = f"Empleado_{empleado_id}"
                if sheet_name in wb.sheetnames:
                    del wb[sheet_name]
                
                emp_ws = wb.create_sheet(title=sheet_name)
                
                emp_ws['A1'] = "INFORMACIÓN DEL EMPLEADO"
                emp_ws['A1'].font = Font(bold=True, size=14)
                emp_ws.merge_cells('A1:F1')
                
                emp_ws['A2'] = "Nombre:"
                emp_ws['B2'] = empleado_info["Nombre"]
                emp_ws['A3'] = "Cédula:"
                emp_ws['B3'] = empleado_info["Cedula"]
                emp_ws['A4'] = "Celular:"
                emp_ws['B4'] = empleado_info["Celular"]
                emp_ws['A5'] = "Correo:"
                emp_ws['B5'] = empleado_info["Correo"]
                emp_ws['A6'] = "ID Empleado:"
                emp_ws['B6'] = empleado_id
                
                for row in range(2, 7):
                    emp_ws[f'A{row}'].font = Font(bold=True)
                
                emp_ws['A8'] = "RESUMEN POR TIPO DE TRABAJO"
                emp_ws['A8'].font = Font(bold=True, size=12)
                emp_ws.merge_cells('A8:D8')
                
                trabajo_resumen = {}
                valor_total_general = 0
                
                for vale in vales_empleado:
                    if vale["work_type_detected"] and vale["valor"] is not None:
                        trabajo = work_type_mapping.get(vale["work_type_detected"], vale["work_type_detected"])
                        if trabajo not in trabajo_resumen:
                            trabajo_resumen[trabajo] = {"cantidad": 0, "valor_total": 0}
                        
                        trabajo_resumen[trabajo]["cantidad"] += 1
                        try:
                            valor = float(vale["valor"])
                            trabajo_resumen[trabajo]["valor_total"] += valor
                            valor_total_general += valor
                        except (ValueError, TypeError):
                            print(f"Error al convertir valor '{vale['valor']}'")
                
                headers_resumen = ["Tipo de Trabajo", "Cantidad de Vales", "Valor Total", "Promedio por Vale"]
                for col, header in enumerate(headers_resumen, start=1):
                    cell = emp_ws.cell(row=9, column=col)
                    cell.value = header
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="CCCCFF", end_color="CCCCFF", fill_type="solid")
                    cell.alignment = Alignment(horizontal='center')
                
                row_idx = 10
                for trabajo, datos in sorted(trabajo_resumen.items()):
                    emp_ws.cell(row=row_idx, column=1).value = trabajo
                    emp_ws.cell(row=row_idx, column=2).value = datos["cantidad"]
                    
                    valor_cell = emp_ws.cell(row=row_idx, column=3)
                    valor_cell.value = datos["valor_total"]
                    valor_cell.number_format = '#,##0'
                    
                    promedio_cell = emp_ws.cell(row=row_idx, column=4)
                    promedio = datos["valor_total"] / datos["cantidad"] if datos["cantidad"] > 0 else 0
                    promedio_cell.value = promedio
                    promedio_cell.number_format = '#,##0'
                    
                    row_idx += 1
                
                emp_ws.cell(row=row_idx, column=1).value = "TOTAL GENERAL:"
                emp_ws.cell(row=row_idx, column=1).font = Font(bold=True)
                emp_ws.cell(row=row_idx, column=2).value = sum(d["cantidad"] for d in trabajo_resumen.values())
                emp_ws.cell(row=row_idx, column=2).font = Font(bold=True)
                
                total_general_cell = emp_ws.cell(row=row_idx, column=3)
                total_general_cell.value = valor_total_general
                total_general_cell.font = Font(bold=True)
                total_general_cell.number_format = '#,##0'
                
                detalle_start_row = row_idx + 3
                
                emp_ws.cell(row=detalle_start_row, column=1).value = "DETALLE DE VALES"
                emp_ws.cell(row=detalle_start_row, column=1).font = Font(bold=True, size=12)
                emp_ws.merge_cells(f'A{detalle_start_row}:J{detalle_start_row}')
                
                headers_detalle = ["ID", "Fecha", "# Ticket", "Referencia", "Talla", 
                                "Color", "Valor", "Total Producido", "Código Serial", "Trabajo"]
                detalle_start_row += 1
                for col, header in enumerate(headers_detalle, start=1):
                    cell = emp_ws.cell(row=detalle_start_row, column=col)
                    cell.value = header
                    cell.font = Font(bold=True)
                    cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
                    cell.alignment = Alignment(horizontal='center')
                
                row_idx = detalle_start_row + 1
                for vale in vales_empleado:
                    emp_ws.cell(row=row_idx, column=1).value = vale["id"]
                    
                    if vale["fecha"] is not None:
                        if isinstance(vale["fecha"], dt.datetime):
                            emp_ws.cell(row=row_idx, column=2).value = vale["fecha"].strftime("%Y-%m-%d")
                        else:
                            emp_ws.cell(row=row_idx, column=2).value = str(vale["fecha"])
                    else:
                        emp_ws.cell(row=row_idx, column=2).value = "Sin fecha"
                    
                    emp_ws.cell(row=row_idx, column=3).value = vale["num_ticket"]
                    emp_ws.cell(row=row_idx, column=4).value = vale["referencia"]
                    emp_ws.cell(row=row_idx, column=5).value = vale["talla"]
                    emp_ws.cell(row=row_idx, column=6).value = vale["color"]
                    
                    valor_cell = emp_ws.cell(row=row_idx, column=7)
                    valor_cell.value = vale["valor"]
                    valor_cell.number_format = '#,##0'
                    
                    emp_ws.cell(row=row_idx, column=8).value = vale["total_producido"]
                    emp_ws.cell(row=row_idx, column=9).value = vale["codigo_serial"]
                    emp_ws.cell(row=row_idx, column=10).value = work_type_mapping.get(vale["work_type_detected"], vale["work_type_detected"])
                    
                    row_idx += 1
                
                last_row = row_idx
                
                for col in range(1, 11):
                    emp_ws.column_dimensions[chr(64 + col)].width = 15
                
                self._create_consolidados(emp_ws, vales_empleado, last_row, work_type_mapping)

            wb.save(self.excel_path)
            
            QMessageBox.information(
                self, 
                "Reportes Actualizados", 
                f"Se han actualizado exitosamente:\n"
                f"• Reporte consolidado mostrado en la tabla\n"
                f"• {len(empleados)} hojas individuales de empleados\n"
                f"• Consolidados semanales, mensuales y anuales"
            )
            
            print("Reportes de empleados actualizados con éxito (reporte consolidado + hojas individuales).")
            
        except Exception as e:
            print(f"Error al generar los reportes de empleados: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"No se pudieron generar los reportes: {e}")

    def _create_consolidados(self, emp_ws, vales_empleado, start_row, work_type_mapping):
        """
        Método auxiliar para crear las tablas de consolidados (semanal, mensual, anual)
        """
        try:
            consolidado_start_row = start_row + 3
            emp_ws.cell(row=consolidado_start_row, column=1).value = "CONSOLIDADO DE PAGOS"
            emp_ws.cell(row=consolidado_start_row, column=1).font = Font(bold=True, size=12)
            emp_ws.merge_cells(f'A{consolidado_start_row}:F{consolidado_start_row}')
            
            consolidado_start_row += 2
            
            emp_ws.cell(row=consolidado_start_row, column=1).value = "CONSOLIDADO SEMANAL"
            emp_ws.cell(row=consolidado_start_row, column=1).font = Font(bold=True)
            emp_ws.merge_cells(f'A{consolidado_start_row}:D{consolidado_start_row}')
            
            consolidado_start_row += 1
            headers_semanal = ["Semana", "Fecha Inicio", "Fecha Fin", "Valor Total"]
            for col, header in enumerate(headers_semanal, start=1):
                cell = emp_ws.cell(row=consolidado_start_row, column=col)
                cell.value = header
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
                cell.alignment = Alignment(horizontal='center')
            
            weekly_data = {}
            for vale in vales_empleado:
                if vale["fecha"] is not None and isinstance(vale["fecha"], dt.datetime) and vale["valor"] is not None:
                    try:
                        year = vale["fecha"].year
                        week_num = vale["fecha"].isocalendar()[1]
                        week_key = f"{year}-W{week_num:02d}"
                        
                        start_of_week = vale["fecha"] - dt.timedelta(days=vale["fecha"].weekday())
                        end_of_week = start_of_week + dt.timedelta(days=6)
                        
                        if week_key not in weekly_data:
                            weekly_data[week_key] = {
                                "start_date": start_of_week,
                                "end_date": end_of_week,
                                "total": 0
                            }
                        
                        weekly_data[week_key]["total"] += float(vale["valor"])
                    except Exception as e:
                        print(f"Error procesando fecha semanal: {e}")
            
            row_idx = consolidado_start_row + 1
            for week_key, data in sorted(weekly_data.items()):
                emp_ws.cell(row=row_idx, column=1).value = week_key
                emp_ws.cell(row=row_idx, column=2).value = data["start_date"].strftime("%Y-%m-%d")
                emp_ws.cell(row=row_idx, column=3).value = data["end_date"].strftime("%Y-%m-%d")
                valor_cell = emp_ws.cell(row=row_idx, column=4)
                valor_cell.value = data["total"]
                valor_cell.number_format = '#,##0'
                row_idx += 1
            
            row_idx += 2
            emp_ws.cell(row=row_idx, column=1).value = "CONSOLIDADO MENSUAL"
            emp_ws.cell(row=row_idx, column=1).font = Font(bold=True)
            emp_ws.merge_cells(f'A{row_idx}:C{row_idx}')
            
            row_idx += 1
            headers_mensual = ["Año", "Mes", "Valor Total"]
            for col, header in enumerate(headers_mensual, start=1):
                cell = emp_ws.cell(row=row_idx, column=col)
                cell.value = header
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
                cell.alignment = Alignment(horizontal='center')
            
            monthly_data = {}
            for vale in vales_empleado:
                if vale["fecha"] is not None and isinstance(vale["fecha"], dt.datetime) and vale["valor"] is not None:
                    try:
                        year = vale["fecha"].year
                        month = vale["fecha"].month
                        month_key = f"{year}-{month:02d}"
                        
                        if month_key not in monthly_data:
                            monthly_data[month_key] = {"year": year, "month": month, "total": 0}
                        
                        monthly_data[month_key]["total"] += float(vale["valor"])
                    except Exception as e:
                        print(f"Error procesando fecha mensual: {e}")
            
            month_names = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
            
            row_idx += 1
            for month_key, data in sorted(monthly_data.items()):
                emp_ws.cell(row=row_idx, column=1).value = data["year"]
                emp_ws.cell(row=row_idx, column=2).value = month_names[data["month"] - 1]
                valor_cell = emp_ws.cell(row=row_idx, column=3)
                valor_cell.value = data["total"]
                valor_cell.number_format = '#,##0'
                row_idx += 1
            
            row_idx += 2
            emp_ws.cell(row=row_idx, column=1).value = "CONSOLIDADO ANUAL"
            emp_ws.cell(row=row_idx, column=1).font = Font(bold=True)
            emp_ws.merge_cells(f'A{row_idx}:B{row_idx}')
            
            row_idx += 1
            headers_anual = ["Año", "Valor Total"]
            for col, header in enumerate(headers_anual, start=1):
                cell = emp_ws.cell(row=row_idx, column=col)
                cell.value = header
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
                cell.alignment = Alignment(horizontal='center')
            
            yearly_data = {}
            for vale in vales_empleado:
                if vale["fecha"] is not None and isinstance(vale["fecha"], dt.datetime) and vale["valor"] is not None:
                    try:
                        year = vale["fecha"].year
                        if year not in yearly_data:
                            yearly_data[year] = 0
                        yearly_data[year] += float(vale["valor"])
                    except Exception as e:
                        print(f"Error procesando fecha anual: {e}")
            
            row_idx += 1
            for year, total in sorted(yearly_data.items()):
                emp_ws.cell(row=row_idx, column=1).value = year
                valor_cell = emp_ws.cell(row=row_idx, column=2)
                valor_cell.value = total
                valor_cell.number_format = '#,##0'
                row_idx += 1
                
        except Exception as e:
            print(f"Error creando consolidados: {e}")
    def setup_employee_management(self):
        """Carga empleados en el ComboBox, conecta el botón Registrar Vale y limpia la tabla de previsualización."""
        try:
            # --- Manejo de Archivo Excel ---
            try:
                wb = load_workbook(self.excel_path)
            except FileNotFoundError:
                print(f"Advertencia: Archivo Excel no encontrado en {self.excel_path}. Creando uno nuevo.")
                wb = Workbook()
                # Usa la hoja activa si es un libro nuevo
                if "Sheet" in wb.sheetnames and len(wb.sheetnames) == 1:
                    empleados_ws = wb.active
                    empleados_ws.title = "Empleados"
                else:
                    empleados_ws = wb.create_sheet(title="Empleados")
                # Añadir encabezados
                empleados_ws.append(["Nombre", "Cedula", "Celular", "Correo", "EmpleadoId"])
                # Añadir un empleado de ejemplo
                empleados_ws.append(["Juan Pérez (Ejemplo)", "1234567890", "3001234567", "juan@example.com", "E001"])
                wb.save(self.excel_path)
                print(f"Archivo Excel '{self.excel_path}' creado con hoja 'Empleados'.")

            if "Empleados" not in wb.sheetnames:
                print(f"Creando hoja 'Empleados' en archivo existente: {self.excel_path}")
                empleados_ws = wb.create_sheet(title="Empleados")
                empleados_ws.append(["Nombre", "Cedula", "Celular", "Correo", "EmpleadoId"])
                empleados_ws.append(["Juan Pérez (Ejemplo)", "1234567890", "3001234567", "juan@example.com", "E001"])
                wb.save(self.excel_path)
            else:
                empleados_ws = wb["Empleados"]
                # Asegurarse de que la hoja Empleados tenga las cabeceras básicas si está vacía o corrupta
                if empleados_ws.max_row == 0 or not all(empleados_ws.cell(row=1, column=c+1).value for c in range(5)):
                    empleados_ws.delete_rows(1, empleados_ws.max_row)  # Limpiar por si acaso
                    empleados_ws.append(["Nombre", "Cedula", "Celular", "Correo", "EmpleadoId"])
                    wb.save(self.excel_path)

            # --- Configuración del ComboBox ---
            if hasattr(self.ui, 'EmpleadosBox'):
                self.ui.EmpleadosBox.clear()  # Limpiar items previos
                self.ui.EmpleadosBox.setMinimumWidth(200)

                employees_loaded = False
                # Leer las 5 columnas estándar
                for row in empleados_ws.iter_rows(min_row=2, max_col=5):
                    # Asegurarse de que la fila tiene al menos las columnas de Nombre (0) y EmpleadoId (4)
                    if len(row) >= 5 and row[0].value and row[4].value:
                        name = str(row[0].value)
                        emp_id = str(row[4].value) if row[4].value else "SIN-ID"
                        self.ui.EmpleadosBox.addItem(f"{name} ({emp_id})", emp_id)
                        employees_loaded = True

                if not employees_loaded:
                    self.ui.EmpleadosBox.addItem("Sin empleados registrados", "")
                    print("No se cargaron empleados desde la hoja 'Empleados'.")
                else:
                    print(f"Se cargaron {self.ui.EmpleadosBox.count()} empleados.")
            else:
                print("ERROR: El QComboBox 'EmpleadosBox' no se encontró en la UI.")
                if hasattr(self.ui, 'btnRegisterVale'):
                    self.ui.btnRegisterVale.setEnabled(False)
                return

            # --- Limpiar la tabla de previsualización ---
            if hasattr(self.ui, 'tableViewVale') and hasattr(self, 'table_model'):
                self.table_model.clear()  # Limpiar todas las filas
                # Definir los encabezados fijos
                fixed_headers = ["Código Serial", "Número Ticket", "Referencia", "Tipo Trabajo", "Color", "Total Producido"]
                # Generar los encabezados dinámicos para los valores de trabajo
                valor_headers = [f"Valor {work_type}" for work_type in WORK_TYPE_ABBREVIATIONS.keys()]
                # Combinar encabezados fijos y dinámicos
                self.table_model.setHorizontalHeaderLabels(fixed_headers + valor_headers)
                self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                print("Tabla de previsualización 'tableViewVale' limpiada y encabezados actualizados.")
            else:
                print("Advertencia: No se pudo limpiar la tabla 'tableViewVale' porque no existe o no tiene modelo.")

            # --- Conexión del Botón Registrar Vale ---
            if hasattr(self.ui, 'btnRegisterVale'):
                if hasattr(self, 'register_vale'):
                    try:
                        self.ui.btnRegisterVale.clicked.disconnect()
                    except RuntimeError:
                        pass
                    self.ui.btnRegisterVale.clicked.connect(self.register_vale)
                    self.ui.btnRegisterVale.setEnabled(True)
                    print("Botón 'btnRegisterVale' conectado correctamente.")
                else:
                    print("ERROR: El método 'register_vale' no está definido en esta clase.")
                    self.ui.btnRegisterVale.setEnabled(False)
            else:
                print("ERROR: El QPushButton 'btnRegisterVale' no se encontró en la UI.")

        except FileNotFoundError:
            print(f"ERROR CRÍTICO: No se pudo encontrar ni crear el archivo Excel en {self.excel_path}")
        except Exception as e:
            print(f"Error inesperado durante setup_employee_management: {e}")
            traceback.print_exc()

    def _gather_and_validate_ui_data(self):
        """
        Responsabilidad: Recopilar y validar todos los datos de la interfaz.
        - Todos los campos de valor de trabajo son ahora OBLIGATORIOS.
        Retorna un diccionario con los datos o None si la validación falla.
        """
        # --- DIAGNÓSTICO DE VERSIÓN (sin cambios) ---
        print(f"\nVERSIÓN DE PYTHON EN USO: {sys.version}\n")

        # --- Validación de campos básicos (sin cambios) ---
        referencia = self.ui.CampoReferenciaTrabajo.text().strip()
        ticket_number = self.ui.CampoNumeroTicket.text().strip()
        color = self.ui.CampoColor.text().strip()
        if not all([referencia, ticket_number, color]):
            QMessageBox.warning(self, "Campos Incompletos", "Los campos Referencia, Número de Ticket y Color son obligatorios.")
            return None

        # --- SECCIÓN DE TALLAS (con mensaje de error corregido) ---
        tallas_cantidades = {}
        total_producido_calculado = 0
        for i in range(33, 49):
            field_name = "CampoTalla_{}".format(i)
            field = getattr(self.ui, field_name, None)
            if field is None:
                continue 

            cantidad_text = field.text().strip()
            if cantidad_text:
                try:
                    cantidad = int(cantidad_text)
                    if cantidad > 0:
                        tallas_cantidades[str(i)] = cantidad
                        total_producido_calculado += cantidad
                    else:
                        # Añadido para no permitir cero o negativos
                        QMessageBox.warning(self, "Entrada Inválida", f"La cantidad para Talla {i} debe ser un número positivo.")
                        field.setFocus()
                        return None
                except ValueError:
                    # CORRECCIÓN: Se añade la variable 'i' al mensaje de error.
                    QMessageBox.warning(self, "Entrada Inválida", f"La cantidad para Talla {i} debe ser un número válido.")
                    field.setFocus()
                    return None
        
        if not tallas_cantidades:
            QMessageBox.warning(self, "Campos Incompletos", "Debe ingresar cantidad para al menos una talla.")
            return None

        # --- SECCIÓN DE VALORES DE TRABAJO (MODIFICADA PARA SER OBLIGATORIA) ---
        valores_trabajo = {}
        for work_type, field_attr in CAMPOS_VALOR_TRABAJO_MAP.items():
            field = getattr(self.ui, field_attr, None)
            
            # Es poco probable, pero es una buena práctica comprobar si el campo existe en la UI
            if field is None:
                QMessageBox.critical(self, "Error de UI", f"El campo '{field_attr}' no fue encontrado en la interfaz.")
                return None

            valor_text = field.text().strip()

            # 1. ¡NUEVA VALIDACIÓN! Comprobar si el campo está vacío.
            if not valor_text:
                QMessageBox.warning(self, "Campo Obligatorio", f"Debe ingresar un valor para el campo '{work_type}'.")
                field.setFocus() # Pone el cursor en el campo vacío.
                return None # Detiene la ejecución.

            # 2. Si no está vacío, proceder con la validación numérica.
            try:
                valor_float = float(valor_text.replace(',', '.'))
                if valor_float <= 0:
                    QMessageBox.warning(self, "Entrada Inválida", f"El valor para '{work_type}' debe ser un número positivo.")
                    field.setFocus()
                    return None
                
                valores_trabajo[work_type] = valor_float

            except ValueError:
                # CORRECCIÓN: Se añade la variable 'work_type' al mensaje de error.
                QMessageBox.warning(self, "Entrada Inválida", f"El valor para '{work_type}' debe ser un número.")
                field.setFocus()
                return None

        # --- Si todo es correcto, retornar el diccionario de datos (sin cambios) ---
        return {
            "referencia": referencia,
            "ticket_number": ticket_number,
            "color": color,
            "tallas_cantidades": tallas_cantidades,
            "total_producido": total_producido_calculado,
            "valores_trabajo": valores_trabajo
        }
    def _clear_all_input_fields(self):
        """
        Limpia todos los campos de entrada del formulario, la previsualización de la imagen
        y restablece el foco para la siguiente entrada de datos.
        
        Esta función está diseñada para ser llamada después de una operación exitosa.
        """
        print("Limpiando campos del formulario...")
        
        # 1. Recopilar todos los widgets de entrada en una lista
        all_fields_to_clear = []

        # Campos de texto básicos
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            all_fields_to_clear.append(self.ui.CampoReferenciaTrabajo)
        if hasattr(self.ui, 'CampoNumeroTicket'):
            all_fields_to_clear.append(self.ui.CampoNumeroTicket)
        if hasattr(self.ui, 'CampoColor'):
            all_fields_to_clear.append(self.ui.CampoColor)

        # Campos de tallas (del 33 al 48)
        for i in range(33, 49):
            field_name = f"CampoTalla_{i}"
            if hasattr(self.ui, field_name):
                all_fields_to_clear.append(getattr(self.ui, field_name))

        # Campos de valores de trabajo
        # NOTA: Esto asume que la constante CAMPOS_VALOR_TRABAJO_MAP está disponible
        if 'CAMPOS_VALOR_TRABAJO_MAP' in globals() or hasattr(self, 'CAMPOS_VALOR_TRABAJO_MAP'):
            # Determina dónde está definida la constante
            the_map = CAMPOS_VALOR_TRABAJO_MAP if hasattr(self, 'CAMPOS_VALOR_TRABAJO_MAP') else CAMPOS_VALOR_TRABAJO_MAP
            
            for field_attr_name in the_map.values():
                if hasattr(self.ui, field_attr_name):
                    all_fields_to_clear.append(getattr(self.ui, field_attr_name))

        # 2. Iterar sobre la lista y limpiar cada widget
        for field_widget in all_fields_to_clear:
            # QLineEdit, QTextEdit, etc., tienen un método .clear()
            if hasattr(field_widget, 'clear'):
                field_widget.clear()

        # 3. Limpiar la previsualización de la imagen
        if hasattr(self.ui, 'PreviwImage') and self.ui.PreviwImage.scene() is not None:
            self.ui.PreviwImage.scene().clear()

        # 4. Poner el foco en el primer campo para facilitar la siguiente entrada
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            self.ui.CampoReferenciaTrabajo.setFocus()
            
        print("Formulario limpiado y listo para la siguiente entrada.")

    def _generate_qr_codes_for_ticket(self, ticket_number, referencia, color, tallas_cantidades, valores_trabajo, subfolder_name):
        """
        Responsabilidad: Generar todos los códigos QR para un tiquete específico.
        AHORA RECIBE TODOS LOS DATOS NECESARIOS.
        """
        barcode_paths = {}
        for work_type, abbr in WORK_TYPE_ABBREVIATIONS.items():
            if work_type in valores_trabajo:
                # LA LLAMADA CORREGIDA: Pasamos todos los argumentos que la función espera.
                # Asegúrate de que el orden aquí coincida con la definición de tu función.
                # Si tu función no usa 'color' o 'tallas_cantidades', puedes quitarlos,
                # pero el error indica que sí los necesita.
                serial_code = generate_serial_code(ticket_number, referencia, color, tallas_cantidades, abbr)
                
                barcode_path = generate_barcode(serial_code, subfolder_name=subfolder_name)
                if not barcode_path:
                    QMessageBox.critical(self, "Error de QR", f"No se pudo generar el código QR para  (Ticket: ).")
                    return None
                barcode_paths[work_type] = barcode_path
        return barcode_paths
    def _generate_serial_codes_for_ticket(self, ticket_data: dict) -> dict:
        """
        Genera los códigos seriales para todos los tipos de trabajo de un tiquete.

        Esta función NO genera los archivos de imagen QR. Solo crea los strings
        de los códigos para ser guardados en la base de datos.

        Args:
            ticket_data (dict): Un diccionario con la información del tiquete,
                                que debe incluir 'ticket_number', 'referencia',
                                'color', 'tallas_cantidades' y 'valores_trabajo'.

        Returns:
            dict: Un diccionario mapeando tipo de trabajo a su código serial.
                Ej: {'Corte': 'TKT-REF-CT-X-123456', ...}
        """
        serial_codes = {}
        
        # Itera sobre los tipos de trabajo definidos en la clase
        for work_type, abbr in WORK_TYPE_ABBREVIATIONS.items():
            # Verifica si este tiquete tiene un valor para este tipo de trabajo
            if work_type in ticket_data.get('valores_trabajo', {}):
                
                # Llama a la función importada desde generateCodes.py
                code = generate_serial_code(
                    ticket_data['ticket_number'],
                    ticket_data['referencia'],
                    ticket_data['color'],
                    ticket_data['tallas_cantidades'],
                    abbr  # Pasa la abreviatura del tipo de trabajo
                )
                serial_codes[work_type] = code
        
        return serial_codes

    def on_save_button_clicked(self):
        """
        Handler principal del botón. Guarda datos de AMBOS tiquetes en Excel,
        luego genera el PDF de vale doble y los QR.
        """
        # 1. Recopilar y validar datos de la UI (TU LÓGICA)
        base_data = self._gather_and_validate_ui_data()
        if not base_data:
            return

        # 2. Preparar datos para los dos tiquetes (TU LÓGICA)
        left_ticket_info = base_data.copy()
        # Asumimos que tienes una función para esto, ej: increment_ticket_number
        right_ticket_number = increment_ticket_number(base_data['ticket_number'])
        right_ticket_info = {**base_data, "ticket_number": right_ticket_number}

        # --- 3. GUARDAR AMBOS TIQUETES EN BD Y EXCEL (LÓGICA DE DOBLE GUARDADO) ---
            
        for ticket_data in [left_ticket_info, right_ticket_info]:
            # Preparación de datos para este tiquete (SIN CAMBIOS)
            id_vale_unico = f"VALE-{ticket_data['ticket_number']}-{uuid.uuid4().hex[:8].upper()}"
            timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado = "IMPRESO"
            serial_codes = self._generate_serial_codes_for_ticket(ticket_data) # Asumiendo que refactorizas esto a una función
            
            data_to_save = {
                "id_vale_unico": id_vale_unico,
                "timestamp": timestamp,
                "estado": estado,
                **ticket_data, # Desempaqueta el resto de los datos del tiquete
                "serial_codes": serial_codes
            }

            # --- ¡AQUÍ LA LÓGICA DE DOBLE GUARDADO! ---

            # 1. Guardar en la Base de Datos (Prioridad Principal)
            if not guardar_o_actualizar_trabajo(data_to_save):
                QMessageBox.critical(self, "Error Crítico de Base de Datos", 
                                    f"No se pudo guardar el tiquete {ticket_data['ticket_number']} en la base de datos.\n"
                                    "La operación ha sido cancelada.")
                return # Detener todo si el guardado principal falla

            # 2. Guardar en Excel (Respaldo)
            # Este código solo se ejecuta si el guardado en la BD fue exitoso.
            if not self.save_to_excel(data_to_save):
                # El dato ya está en la BD, pero informamos del fallo secundario.
                QMessageBox.warning(self, "Error de Respaldo en Excel", 
                                    f"El tiquete {ticket_data['ticket_number']} se guardó correctamente en la base de datos, "
                                    "pero falló al guardar el respaldo en el archivo Excel.\n\n"
                                    "Por favor, revisa si el archivo 'database.xlsx' está cerrado.")
                # Decidimos continuar aunque Excel falle, porque la BD es la fuente de verdad.
                # Si quisieras que fuera un fallo total, cambia 'warning' por 'critical' y añade 'return'.
        # --- 4. DEFINIR RUTAS DE SALIDA (TU LÓGICA, SIN CAMBIOS) ---
        pdf_output_dir = "codes"
        qr_folder_name = f"qr_images_tiquetes_{left_ticket_info['ticket_number']}_{right_ticket_info['ticket_number']}"
        qr_output_dir = os.path.join(pdf_output_dir, qr_folder_name)
        os.makedirs(pdf_output_dir, exist_ok=True)
        safe_ref = base_data['referencia'].replace('/', '-').replace('\\', '_')
        pdf_filename = os.path.join(pdf_output_dir, f"VALE_DOBLE_{base_data['ticket_number']}_{safe_ref}.pdf")

        # --- 5. GENERAR EL PDF Y LOS CÓDIGOS QR (TU LÓGICA, SIN CAMBIOS) ---
        # Asumimos que esta función existe y funciona como esperas
        pdf_path, first_qr_path = generar_vales_pdf(
            left_ticket_info=left_ticket_info,
            right_ticket_info=right_ticket_info,
            output_filename=pdf_filename,
            qr_output_folder=qr_output_dir
        )

        if not pdf_path:
            QMessageBox.critical(self, "Error", "Datos guardados en Excel, pero hubo un error al generar el PDF.")
            return

        # --- 6. FINALIZAR (TU LÓGICA, SIN CAMBIOS) ---
        if first_qr_path:
            display_code_image(self.ui, first_qr_path)

        QMessageBox.information(
            self, "Operación Exitosa",
            f"Vale doble generado y datos guardados.\n"
            f"Total Producido: {base_data['total_producido']} unidades por tiquete.\n"
            f"Archivos generados en la carpeta: '{pdf_output_dir}'"
        )

        self._clear_all_input_fields()
        self.autocompletado_manager.actualizar_todos_los_autocompletados()


    def setup_window(self):
        """Setup basic window properties and appearance"""
        # Remove standard title bar
        UIFunctions.removeTitleBar(True)
        
        # Set window title
        self.setWindowTitle('Gestor de Vales')
        UIFunctions.labelTitle(self, 'Thimoty')
        UIFunctions.labelDescription(self, '2025')
        
        # Set window size
        startSize = QSize(1300, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        # UIFunctions.enableMaximumSize(self, 500, 720)

    def setup_menus(self):
        """Setup menu functionality and navigation"""
        # Toggle menu size button
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        
        # Add custom menus
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Leer Vales", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        UIFunctions.addNewMenu(self, "Crear Vales", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
        UIFunctions.addNewMenu(self, "Configuracion", "btn_widgets", "url(:/16x16/icons/16x16/cil-equalizer.png)", False)
        
        # Select starting menu
        UIFunctions.selectStandardMenu(self, "btn_home")
        
        # Set starting page
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

    def setup_eliminar_todo_button(self):
        """Conecta el botón EliminarTODO con la función de eliminación"""
        self.ui.EliminarTODO.clicked.connect(self.eliminar_todo_con_backup)

    def eliminar_todo_con_backup(self):
        """
        Elimina la base de datos Excel y el directorio codes después de crear un backup
        Versión con threading para UI más responsiva
        """
        try:
            # Confirmar acción con el usuario
            reply = QMessageBox.question(
                self, 
                'Confirmar Eliminación', 
                '¿Está seguro de que desea eliminar toda la base de datos?\n\n'
                'Se creará un backup automáticamente antes de eliminar.',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
                
            # Obtener rutas usando BackupManager
            excel_path, codes_dir = BackupManager.get_paths()
            
            # Verificar si hay algo que respaldar
            has_files, excel_exists, codes_exists = BackupManager.check_files_exist(excel_path, codes_dir)
            
            if not has_files:
                QMessageBox.information(
                    self, 
                    'Información', 
                    'No hay archivos para eliminar. La base de datos ya está limpia.'
                )
                return
            
            # Deshabilitar el botón mientras se procesa
            self.ui.EliminarTODO.setEnabled(False)
            self.ui.EliminarTODO.setText("Procesando...")
            QApplication.processEvents()
            
            # Crear backup en thread separado
            self.backup_thread = BackupThread(excel_path, codes_dir)
            self.backup_thread.finished.connect(self.on_backup_finished)
            self.backup_thread.progress.connect(self.on_backup_progress)
            self.backup_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al iniciar eliminación: {str(e)}")
            self.ui.EliminarTODO.setEnabled(True)
            self.ui.EliminarTODO.setText("Eliminar TODO")
    def eliminar_todo_simple(self):
        """
        Versión simple sin threading - buena para pocos archivos
        """
        try:
            # Confirmar acción
            reply = QMessageBox.question(
                self, 
                'Confirmar Eliminación', 
                '¿Está seguro de que desea eliminar toda la base de datos?\n\n'
                'Se creará un backup automáticamente.',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply != QMessageBox.Yes:
                return
            
            # Cambiar botón para mostrar progreso
            self.ui.EliminarTODO.setEnabled(False)
            original_text = self.ui.EliminarTODO.text()
            
            def update_progress(message):
                self.ui.EliminarTODO.setText(message)
                QApplication.processEvents()
            
            # Obtener rutas
            excel_path, codes_dir = BackupManager.get_paths()
            
            # Verificar archivos
            has_files, excel_exists, codes_exists = BackupManager.check_files_exist(excel_path, codes_dir)
            
            if not has_files:
                QMessageBox.information(self, 'Información', 'No hay archivos para eliminar.')
                return
            
            # Crear backup
            update_progress("Creando backup...")
            backup_name = BackupManager.create_backup_sync(excel_path, codes_dir, update_progress)
            
            # Eliminar archivos originales
            update_progress("Eliminando archivos...")
            deleted_files = BackupManager.delete_files(excel_path, codes_dir)
            
            # Recrear estructura
            update_progress("Recreando estructura...")
            self.setup_code_generator()
            
            QMessageBox.information(
                self, 
                'Completado', 
                f'Backup creado: {backup_name}\n'
                f'Archivos eliminados: {", ".join(deleted_files)}'
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante la eliminación: {str(e)}")
        
        finally:
            # Restaurar botón
            self.ui.EliminarTODO.setEnabled(True)
            self.ui.EliminarTODO.setText("Eliminar TODO")
    
    def on_backup_progress(self, message):
        """Callback para actualizar progreso del backup"""
        self.ui.EliminarTODO.setText(message)
    
    def on_backup_finished(self, success, message):
        """Callback cuando termina el backup"""
        try:
            if success:
                # Backup exitoso, proceder con eliminación
                self.ui.EliminarTODO.setText("Eliminando archivos...")
                QApplication.processEvents()
                
                excel_path, codes_dir = BackupManager.get_paths()
                deleted_files = BackupManager.delete_files(excel_path, codes_dir)
                
                # Recrear estructura
                self.ui.EliminarTODO.setText("Recreando estructura...")
                QApplication.processEvents()
                self.setup_code_generator()
                
                QMessageBox.information(
                    self, 
                    'Completado', 
                    f'{message}\n'
                    f'Archivos eliminados: {", ".join(deleted_files)}'
                )
            else:
                # Error en backup
                QMessageBox.critical(self, "Error en Backup", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error en proceso de eliminación: {str(e)}")
        
        finally:
            # Rehabilitar botón
            self.ui.EliminarTODO.setEnabled(True)
            self.ui.EliminarTODO.setText("Eliminar TODO")

    def on_code_scanned(self):
        """
        Maneja el evento de escaneo de código, usando la base de datos como fuente.
        """
        scanned_code = self.ui.codeReaderInput.text().strip()
        if not scanned_code:
            QMessageBox.warning(self, "Entrada Vacía", "Por favor, escanee o ingrese un código válido.")
            return

        empleado_id = self.ui.EmpleadosBox.currentData()
        if not empleado_id:
            QMessageBox.warning(self, "Empleado No Seleccionado", "Por favor, seleccione un empleado.")
            self.ui.EmpleadosBox.setFocus()
            return

        # VALIDACIÓN 1: ¿Ya está en la tabla visual de la sesión actual?
        for row in range(self.table_model.rowCount()):
            item = self.table_model.item(row, 0) # Columna 0 es 'Código Serial'
            if item and item.text() == scanned_code:
                QMessageBox.warning(self, "Código Duplicado", f"El código '{scanned_code}' ya fue agregado en esta sesión.")
                self.ui.codeReaderInput.clear()
                self.ui.codeReaderInput.setFocus()
                return

        # VALIDACIÓN 2: ¿Ya existe un vale para este empleado y código en la BD?
        if vale_existe(scanned_code, empleado_id):
            QMessageBox.warning(self, "Vale Ya Registrado", f"Ya existe un vale para este empleado con el código '{scanned_code}'.")
            self.ui.codeReaderInput.clear()
            self.ui.codeReaderInput.setFocus()
            return

        # BÚSQUEDA DEL TRABAJO EN LA BASE DE DATOS
        resultado_busqueda = buscar_trabajo_por_codigo_serial(scanned_code)
        if not resultado_busqueda:
            # ... (mensaje de error) ...
            return

        trabajo_data, work_type_found_id = resultado_busqueda # ej: 'corte'

        # --- Obtener el nombre de display desde la configuración central ---
        # Es más seguro usar .get() para evitar errores si algo sale mal
        work_type_info = WORK_TYPES.get(work_type_found_id)
        if not work_type_info:
            QMessageBox.critical(self, "Error de Configuración", f"El tipo de trabajo '{work_type_found_id}' no está en config.py.")
            return
            
        work_type_display = work_type_info['display'] # ej: 'Corte'
        
        # Calcular el valor a pagar para este vale específico
        valor_columna = f'valor_{work_type_found_id}' # ej: 'valor_corte'
        valor_pagado = trabajo_data.get(valor_columna, 0.0)

        # CREACIÓN DEL VALE EN LA BASE DE DATOS
        datos_vale = {
            'empleado_id': empleado_id,
            'codigo_serial_trabajo_asociado': scanned_code,
            'work_type_detected': work_type_display,
            'valor_pagado': valor_pagado
        }
        
        if not crear_vale(datos_vale):
            QMessageBox.critical(self, "Error al Guardar", "No se pudo registrar el vale en la base de datos. Revise la consola para más detalles.")
            return

        # ACTUALIZACIÓN DE LA TABLA VISUAL
        try:
            # Los datos para la fila deben coincidir con las cabeceras definidas en setup_code_reader
            row_data = [
                scanned_code,
                str(trabajo_data.get('numero_ticket', '')),
                str(trabajo_data.get('referencia', '')),
                work_type_display,
                str(trabajo_data.get('color', '')),
                str(trabajo_data.get('total_producido', 0)),
                f"{valor_pagado:.2f}" # Formatear el valor monetario
            ]
            items = [QtGui.QStandardItem(value) for value in row_data]
            self.table_model.appendRow(items)
            
            QMessageBox.information(self, "Vale Registrado", f"Vale para '{work_type_display}' registrado exitosamente.")

        except Exception as e:
            QMessageBox.critical(self, "Error de UI", f"Error al actualizar la tabla visual: {e}")
            traceback.print_exc()

        # Limpiar para el siguiente escaneo
        self.ui.codeReaderInput.clear()
        self.ui.codeReaderInput.setFocus()



    def setup_add_employee_button(self):
        """Conecta el botón de agregar empleado (si lo tienes)"""
        if hasattr(self.ui, 'btnAgregarEmpleado'):
            self.ui.btnAgregarEmpleado.clicked.connect(self.add_employee)
            print("Botón 'btnAgregarEmpleado' conectado correctamente.")
        else:
            print("Botón 'btnAgregarEmpleado' no encontrado en la UI.")



    # Versión mejorada con validación
    def add_employee(self):
        """Agrega empleado con validaciones adicionales"""
        try:
            # Obtener valores de los campos
            nombre = self.ui.Nombre_Empleado.text().strip() if hasattr(self.ui, 'Nombre_Empleado') else ""
            cedula = self.ui.Cedula_Empleado.text().strip() if hasattr(self.ui, 'Cedula_Empleado') else ""
            celular = self.ui.Celular_Empleado.text().strip() if hasattr(self.ui, 'Celular_Empleado') else ""
            correo = self.ui.Correo_Empleado.text().strip() if hasattr(self.ui, 'Correo_Empleado') else ""
            
            # Validaciones
            if not nombre:
                QMessageBox.warning(self, "Campo Requerido", "El nombre es obligatorio.")
                self.ui.Nombre_Empleado.setFocus()
                return
                
            if not cedula:
                QMessageBox.warning(self, "Campo Requerido", "La cédula es obligatoria.")
                self.ui.Cedula_Empleado.setFocus()
                return
            
            # Validar formato de cédula
            if not validate_cedula(cedula):
                QMessageBox.warning(self, "Cédula Inválida", "La cédula debe contener solo números (6-12 dígitos).")
                self.ui.Cedula_Empleado.setFocus()
                return
            
            # Validar email si se proporciona
            if correo and "@" not in correo:
                QMessageBox.warning(self, "Email Inválido", "El formato del correo electrónico no es válido.")
                self.ui.Correo_Empleado.setFocus()
                return
            
            # Generar ID único del empleado
            unique_id = str(uuid.uuid4())[:4]
            empleado_id = f"E{cedula[-4:]}{unique_id}".upper()
            
            # Cargar Excel y verificar duplicados
            wb = load_workbook(self.excel_path)
            
            if "Empleados" not in wb.sheetnames:
                empleados_ws = wb.create_sheet(title="Empleados")
                empleados_ws.append(["Nombre", "Cedula", "Celular", "Correo", "EmpleadoId"])
            else:
                empleados_ws = wb["Empleados"]
            
            # Verificar si la cédula ya existe
            for row in empleados_ws.iter_rows(min_row=2, max_col=5):
                if row[1].value and str(row[1].value) == cedula:
                    QMessageBox.warning(self, "Empleado Existente", f"Ya existe un empleado con cédula {cedula}")
                    return
            
            # Agregar empleado
            empleados_ws.append([nombre, cedula, celular, correo, empleado_id])
            wb.save(self.excel_path)
            
            # Limpiar campos
            self.ui.Nombre_Empleado.clear()
            self.ui.Cedula_Empleado.clear()
            self.ui.Celular_Empleado.clear()
            self.ui.Correo_Empleado.clear()
            
            # Actualizar ComboBox
            if hasattr(self, 'setup_employee_management'):
                self.setup_employee_management()
            
            # Mensaje de éxito
            QMessageBox.information(self, "Empleado Agregado", f"Empleado: {nombre}\nCédula: {cedula}\nID: {empleado_id}")
            
            print(f"Empleado agregado exitosamente: {nombre} ({empleado_id})")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar empleado: {str(e)}")
            print(f"Error en add_employee_with_validation: {e}")


        #TODOok



    #TODOok
    def register_vale(self):
        """Registra los vales escaneados y limpia la tabla."""
        try:
            if not self.table_model or self.table_model.rowCount() == 0:
                QMessageBox.warning(self, "Sin Vales", "No hay vales pendientes para registrar.")
                return

            total_vales = self.table_model.rowCount()
            self.table_model.removeRows(0, total_vales)

            QMessageBox.information(
                self, "Vales Registrados",
                f"Se han limpiado {total_vales} registros de la vista previa."
            )
        except Exception as e:
            print(f"Error al registrar vales: {e}")
            QMessageBox.critical(self, "Error", f"Error al registrar vales: {str(e)}")





    def Button(self):
        """Handler for menu button clicks"""
        # Get clicked button
        btnWidget = self.sender()

        # Handle different pages
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
        elif btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
        elif btnWidget.objectName() == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.create_user)
            UIFunctions.resetStyle(self, "create_user")      
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    # Window event handlers
    def moveWindow(self, event):
        """Handle window movement"""
        # If maximized change to normal
        if UIFunctions.returStatus() == 1:
            UIFunctions.maximize_restore(self)

        # Move window
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def eventFilter(self, watched, event):
        """Event filter for double-click events"""
        if hasattr(self, 'le') and watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
        return super().eventFilter(watched, event)

    def mousePressEvent(self, event):
        """Handle mouse press events"""
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')

    def keyPressEvent(self, event):
        """Handle key press events"""
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))

    def resizeEvent(self, event):
        """Handle resize events"""
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        """Log window size on resize"""
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
## ==> GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

## ==> COUT INITIAL MENU
count = 1

class UIFunctions(MainWindow):

    ## ==> GLOBALS
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    ########################################################################
    ## START - GUI FUNCTIONS
    ########################################################################

    ## ==> MAXIMIZE/RESTORE
    ########################################################################
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

    ## ==> RETURN STATUS
    def returStatus():
        return GLOBAL_STATE

    ## ==> SET STATUS
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    ## ==> ENABLE MAXIMUM SIZE
    ########################################################################
    def enableMaximumSize(self, width, height):
        if width != '' and height != '':
            self.setMaximumSize(QSize(width, height))
            self.ui.frame_size_grip.hide()
            self.ui.btn_maximize_restore.hide()


    ## ==> TOGGLE MENU
    ########################################################################
    def toggleMenu(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    ## ==> SET TITLE BAR
    ########################################################################
    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    ## ==> HEADER TEXTS
    ########################################################################
    # LABEL TITLE
    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)

    # LABEL DESCRIPTION
    def labelDescription(self, text):
        self.ui.label_top_info_1.setText(text)

    ## ==> DYNAMIC MENUS
    ########################################################################
    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    ## ==> SELECT/DESELECT MENU
    ########################################################################
    ## ==> SELECT
    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    ## ==> START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    ## ==> CHANGE PAGE LABEL TEXT
    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.ui.label_top_info_2.setText(newText)

    ## ==> USER ICON
    ########################################################################
    # def userIcon(self, initialsTooltip, icon, showHide):
    #     if showHide:
    #         # SET TEXT
    #         self.ui.label_user_icon.setText(initialsTooltip)

    #         # SET ICON
    #         if icon:
    #             style = self.ui.label_user_icon.styleSheet()
    #             setIcon = "QLabel { background-image: " + icon + "; }"
    #             self.ui.label_user_icon.setStyleSheet(style + setIcon)
    #             self.ui.label_user_icon.setText('')
    #             self.ui.label_user_icon.setToolTip(initialsTooltip)
    #     else:
    #         self.ui.label_user_icon.hide()

    ########################################################################
    ## END - GUI FUNCTIONS
    ########################################################################


    ########################################################################
    ## START - GUI DEFINITIONS
    ########################################################################

    ## ==> UI DEFINITIONS
    ########################################################################
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        ## SHOW ==> DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())


    ########################################################################
    ## END - GUI DEFINITIONS
    ########################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()
    init_db()
    sys.exit(app.exec_())