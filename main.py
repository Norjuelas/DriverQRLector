################################################################################
## V: 1.0.0
################################################################################

import sys
import os
import platform
import uuid
import traceback
from datetime import datetime
import time
import datetime

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

# GUI FILE
from app_modules import *


class MainWindow(QMainWindow):
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

        self.autocompletado_manager = AutocompletadoManager(excel_path=self.excel_path, sheet_name="Trabajos")
        self.setup_autocompletado_fields()

        # Show the window
        self.show()

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
    #TODOok

    def setup_code_generator(self):
        """
        Configura la funcionalidad del generador de códigos y el archivo Excel.
        """
        # Definir la ruta del Excel y el nombre de la hoja de vales
        self.excel_path = "trabajos_database.xlsx"
        self.vales_sheet_name = "Vales"  # Nombre de la hoja para los datos de los vales

        # Crear el directorio "codes" si no existe para guardar las imágenes de los códigos
        if not os.path.exists("codes"):
            os.makedirs("codes")

        # Definir las cabeceras para la hoja "Trabajos"
        trabajos_headers = ["Código Serial", "Número Ticket", "Referencia", "Color"]
        # Añadir cabeceras para las cantidades de cada talla (33 a 48)
        for i in range(33, 49):
            trabajos_headers.append(f"Cant_T{i}")
        # Añadir el resto de las cabeceras para "Trabajos"
        trabajos_headers.extend([
            "Total Producido", "Valor Corte", "Valor Empaque", "Valor Guarnecedor",
            "Valor Montador", "Valor Plantillas", "Valor Soldador",
            "Tipo Código", "Ruta Imagen"
        ])
        # Añadir columnas para los códigos seriales por tipo de trabajo
        work_type_abbreviations = {
            'Corte': 'C', 'Empaque': 'E', 'Guarnecedor': 'G',
            'Montador': 'M', 'Plantillas': 'P', 'Soldador': 'S'
        }
        for work_type, abbr in work_type_abbreviations.items():
            trabajos_headers.append(f"Código_{work_type}")

        # Definir las cabeceras para la hoja "Vales"
        vales_headers = [
            "ID_Vale", "EmpleadoID", "FechaHora_Generacion", "Numero_Ticket_Asociado",
            "Referencia_Asociada", "Color_Trabajo", "Resumen_Tallas_Cantidades",
            "Total_Producido_Trabajo", "Suma_Valores_Trabajos", "Codigo_Serial_Trabajo_Asociado"
        ]

        # Crear el archivo Excel si no existe y añadir las hojas con sus cabeceras
        if not os.path.exists(self.excel_path):
            wb = Workbook()
            
            # Configurar la hoja "Trabajos"
            ws_trabajos = wb.active
            ws_trabajos.title = "Trabajos"
            ws_trabajos.append(trabajos_headers)
            
            # Configurar la hoja "Vales"
            ws_vales = wb.create_sheet(title=self.vales_sheet_name)
            ws_vales.append(vales_headers)
            
            wb.save(self.excel_path)
        else:
            # Si el archivo Excel ya existe, cargar el libro de trabajo
            wb = load_workbook(self.excel_path)
            
            # Verificar si las cabeceras de "Trabajos" necesitan actualización
            ws_trabajos = wb["Trabajos"]
            current_headers = [cell.value for cell in ws_trabajos[1]]
            if current_headers != trabajos_headers:
                print("Actualizando cabeceras de la hoja 'Trabajos'...")
                ws_trabajos.delete_rows(1)  # Eliminar la fila de cabeceras antigua
                ws_trabajos.insert_rows(1)  # Insertar una nueva fila para las cabeceras
                for col_idx, header in enumerate(trabajos_headers, 1):
                    ws_trabajos.cell(row=1, column=col_idx).value = header
                wb.save(self.excel_path)

            # Verificar si la hoja "Vales" existe; si no, crearla con sus cabeceras
            if self.vales_sheet_name not in wb.sheetnames:
                ws_vales = wb.create_sheet(title=self.vales_sheet_name)
                ws_vales.append(vales_headers)
                wb.save(self.excel_path)

        # Conectar el botón de guardar a la función correspondiente
        if hasattr(self.ui, 'pushButtonGuardar'):
            self.ui.pushButtonGuardar.clicked.connect(self.on_save_button_clicked)
        else:
            print("Advertencia: self.ui.pushButtonGuardar no encontrado.")
            
        # # Configurar el selector de tipo de código (radio buttons, etc.)
        # self.setup_code_type_selector()
        
        # Asegurar que el QGraphicsView para la previsualización de la imagen tenga una escena
        if hasattr(self.ui, 'PreviwImage'):  # Corregir el nombre si es necesario
            if self.ui.PreviwImage.scene() is None:
                self.ui.PreviwImage.setScene(QtWidgets.QGraphicsScene(self))
        else:
            print("Advertencia: self.ui.PreviwImage no encontrado.")
    
    def setup_code_reader(self):
        """Setup the code reader functionality and TableView inside WidgetTabla"""
        
        # El codeReaderInput YA existe en tu UI, solo necesitamos conectar el signal
        if hasattr(self.ui, 'codeReaderInput'):
            print("codeReaderInput encontrado en UI")
            # Configurar el input existente
            self.ui.codeReaderInput.setPlaceholderText("Escanear o ingresar código aquí...")
            self.ui.codeReaderInput.setMinimumWidth(250)
            
            # IMPORTANTE: Conectar el signal returnPressed
            self.ui.codeReaderInput.returnPressed.connect(self.on_code_scanned)
            print("Signal returnPressed conectado")
        else:
            print("ERROR: codeReaderInput no encontrado en UI")
            return
        
        # Access the WidgetTabla from UI and setup table
        if hasattr(self.ui, 'WidgetTabla'):
            print("WidgetTabla encontrado")
            
            # Solo crear el layout si WidgetTabla no tiene uno
            if self.ui.WidgetTabla.layout() is None:
                table_layout = QVBoxLayout(self.ui.WidgetTabla)
                self.ui.WidgetTabla.setLayout(table_layout)
                print("Layout creado para WidgetTabla")
            else:
                table_layout = self.ui.WidgetTabla.layout()
                print("Usando layout existente de WidgetTabla")
            
            # Solo crear la tabla si no existe
            if not hasattr(self.ui, 'tableViewVale'):
                print("Creando tableViewVale")
                # Create TableView
                self.ui.tableViewVale = QTableView(self.ui.WidgetTabla)
                self.ui.tableViewVale.setMinimumHeight(200)
                
                # Create the model for the table
                self.table_model = QtGui.QStandardItemModel()
                self.table_model.setHorizontalHeaderLabels([
                    "Código Serial", "Número Ticket", "Referencia", "Color", 
                    "Total Producido", "Valor Corte", "Valor Empaque",
                    "Valor Guarnecedor", "Valor Montador", "Valor Plantillas",
                    "Valor Soldador"
                ])
                
                # Set model and adjust view
                self.ui.tableViewVale.setModel(self.table_model)
                self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
                # Add TableView to WidgetTabla's layout
                table_layout.addWidget(self.ui.tableViewVale)
                print("tableViewVale creado y agregado")
            else:
                print("tableViewVale ya existe")
        else:
            print("Warning: WidgetTabla not found in UI")



    def setup_add_employee_button(self):
        """Conecta el botón de agregar empleado (si lo tienes)"""
        if hasattr(self.ui, 'btnAgregarEmpleado'):
            self.ui.btnAgregarEmpleado.clicked.connect(self.add_employee)
            print("Botón 'btnAgregarEmpleado' conectado correctamente.")
        else:
            print("Botón 'btnAgregarEmpleado' no encontrado en la UI.")

    # Función adicional para validar cédula (opcional)
    def validate_cedula(self, cedula):
        """Valida que la cédula tenga formato correcto"""
        # Remover espacios y guiones
        cedula_clean = cedula.replace(" ", "").replace("-", "")
        
        # Verificar que solo contenga números y tenga longitud apropiada
        if not cedula_clean.isdigit() or len(cedula_clean) < 6 or len(cedula_clean) > 12:
            return False
        
        return True

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
            if not self.validate_cedula(cedula):
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

            # --- Configuración del ComboBox ---
            if hasattr(self.ui, 'EmpleadosBox'):
                self.ui.EmpleadosBox.clear()  # Limpiar items previos
                self.ui.EmpleadosBox.setMinimumWidth(200)

                employees_loaded = False
                for row in empleados_ws.iter_rows(min_row=2, max_col=5):
                    if len(row) >= 5 and row[0].value:
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
                self.table_model.setHorizontalHeaderLabels([
                    "Código Serial", "Número Ticket", "Referencia", "Color",
                    "Total Producido", "Valor Corte", "Valor Empaque",
                    "Valor Guarnecedor", "Valor Montador", "Valor Plantillas",
                    "Valor Soldador"
                ])
                self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                print("Tabla de previsualización 'tableViewVale' limpiada.")
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
            
    def update_employee_reports(self):
        """Genera un reporte de empleados basado en los datos de la hoja 'Vales' y lo muestra en tableViewVale."""
        try:
            # Cargar el archivo Excel
            wb = load_workbook(self.excel_path)
            ws_vales = wb[self.vales_sheet_name]
            ws_empleados = wb["Empleados"]

            # Obtener información de empleados
            empleados = {}
            for row in ws_empleados.iter_rows(min_row=2, max_col=5, values_only=True):
                if len(row) >= 5 and row[4]:
                    empleados[row[4]] = {
                        "Nombre": row[0] or "Sin Nombre",
                        "Cedula": row[1] or "",
                        "Celular": row[2] or "",
                        "Correo": row[3] or ""
                    }

            # Procesar datos de vales
            report_data = {}
            for emp_id in empleados:
                report_data[emp_id] = {
                    "Nombre": empleados[emp_id]["Nombre"],
                    "Total_Vales": 0,
                    "Total_Valor": 0.0,
                    "Trabajos": {
                        'Corte': 0, 'Empaque': 0, 'Guarnecedor': 0,
                        'Montador': 0, 'Plantillas': 0, 'Soldador': 0
                    }
                }

            # Mapa de códigos a tipos de trabajo
            work_type_abbreviations = {
                'C': 'Corte', 'E': 'Empaque', 'G': 'Guarnecedor',
                'M': 'Montador', 'P': 'Plantillas', 'S': 'Soldador'
            }

            # Analizar vales
            for row in ws_vales.iter_rows(min_row=2, values_only=True):
                if len(row) >= 10 and row[1] in empleados:  # row[1] es EmpleadoID
                    emp_id = row[1]
                    valor = float(row[8]) if row[8] else 0.0  # Suma_Valores_Trabajos
                    codigo = row[9]  # Codigo_Serial_Trabajo_Asociado
                    work_type = None
                    for abbr, full_name in work_type_abbreviations.items():
                        if codigo and abbr in codigo:
                            work_type = full_name
                            break
                    if work_type:
                        report_data[emp_id]["Total_Vales"] += 1
                        report_data[emp_id]["Total_Valor"] += valor
                        report_data[emp_id]["Trabajos"][work_type] += 1

            # Actualizar la tabla de previsualización
            if hasattr(self.ui, 'tableViewVale') and hasattr(self, 'table_model'):
                self.table_model.clear()
                self.table_model.setHorizontalHeaderLabels([
                    "EmpleadoID", "Nombre", "Total Vales", "Total Valor",
                    "Corte", "Empaque", "Guarnecedor", "Montador", "Plantillas", "Soldador"
                ])
                for emp_id, data in report_data.items():
                    row_data = [
                        emp_id,
                        data["Nombre"],
                        data["Total_Vales"],
                        round(data["Total_Valor"], 2),
                        data["Trabajos"]["Corte"],
                        data["Trabajos"]["Empaque"],
                        data["Trabajos"]["Guarnecedor"],
                        data["Trabajos"]["Montador"],
                        data["Trabajos"]["Plantillas"],
                        data["Trabajos"]["Soldador"]
                    ]
                    items = [QtGui.QStandardItem(str(value)) for value in row_data]
                    self.table_model.appendRow(items)
                self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                print("Reporte de empleados generado y mostrado en 'tableViewVale'.")
            else:
                print("Advertencia: No se pudo actualizar la tabla 'tableViewVale' porque no existe o no tiene modelo.")
                QMessageBox.critical(self, "Error", "No se pudo mostrar el reporte porque la tabla de previsualización no está configurada.")

            QMessageBox.information(self, "Reporte Generado", "El reporte de empleados ha sido generado y mostrado en la tabla.")

        except Exception as e:
            print(f"Error al generar el reporte de empleados: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"No se pudo generar el reporte: {e}")
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
        Configura el autocompletado para los campos QLineEdit relevantes.
        """
        # Define los campos QLineEdit de la UI y las columnas de Excel correspondientes
        # Formato: 'identificador_unico': {'line_edit': self.ui.NombreLineEdit, 'columna': 'NombreColumnaEnExcel'}
        campos_a_configurar = {}

        # Campos de texto obligatorios según on_save_button_clicked
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            campos_a_configurar['referencia'] = {
                'line_edit': self.ui.CampoReferenciaTrabajo,
                'columna': 'Referencia'
            }
        if hasattr(self.ui, 'CampoNumeroTicket'):
            campos_a_configurar['numero_ticket'] = {
                'line_edit': self.ui.CampoNumeroTicket,
                'columna': 'Número Ticket'
            }
        if hasattr(self.ui, 'CampoColor'):
            campos_a_configurar['color'] = {
                'line_edit': self.ui.CampoColor,
                'columna': 'Color'
            }

        # Opcional: Configurar autocompletado para tallas individuales
        # Asumimos que las tallas están en columnas separadas (Cant_T33 a Cant_T48) en el Excel
        for i in range(33, 49):  # Tallas de 33 a 48
            field_name = f'CampoTalla_{i}'
            if hasattr(self.ui, field_name):
                campos_a_configurar[f'talla_{i}'] = {
                    'line_edit': getattr(self.ui, field_name),
                    'columna': f'Cant_T{i}'  # Nombre de columna en el Excel (Cant_T33, Cant_T34, etc.)
                }

        # Opcional: Configurar autocompletado para valores (poco común para campos numéricos)
        # Descomenta si necesitas autocompletado para estos campos
        
        campos_valor_trabajo = [
            ('CampoValorCorte', 'Valor Corte'), ('CampoValorEmpaque', 'Valor Empaque'),
            ('CampoValorGuarnecedor', 'Valor Guarnecedor'), ('CampoValorMontador', 'Valor Montador'),
            ('CampoValorPlantillas', 'Valor Plantillas'), ('CampoValorSoldador', 'Valor Soldador')
        ]
        for field_attr_name, columna in campos_valor_trabajo:
            if hasattr(self.ui, field_attr_name):
                campos_a_configurar[field_attr_name.lower()] = {
                    'line_edit': getattr(self.ui, field_attr_name),
                    'columna': columna
                }
        

        if campos_a_configurar:
            self.autocompletado_manager.configurar_multiples_campos(campos_a_configurar)
            print("Autocompletado configurado para los campos.")
        else:
            print("No se encontraron campos para configurar el autocompletado.")
    
    def display_code_image(self, image_path):
        """Display the code image in the QGraphicsView"""
        try:
            if not hasattr(self.ui, 'PreviwImage'):
                print("Error: PreviwImage not found in UI")
                return False
                
            # Load image
            pixmap = QPixmap(image_path)
            
            # Get scene from QGraphicsView
            scene = self.ui.PreviwImage.scene()
            if scene is None:
                scene = QtWidgets.QGraphicsScene()
                self.ui.PreviwImage.setScene(scene)
            else:
                scene.clear()
            
            # Add image to scene
            scene.addPixmap(pixmap)
            
            # Fit view
            self.ui.PreviwImage.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
            
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al mostrar la imagen: {str(e)}")
            return False
    #TODOok

    def save_to_excel(self, serial_codes, code_path, ticket_number, referencia, color, tallas_cantidades, total_producido_calculado, valores_trabajo):
        """
        Guarda los datos en la hoja 'Trabajos' del archivo Excel.
        """
        try:
            wb = load_workbook(self.excel_path)
            ws_trabajos = wb["Trabajos"]

            # Crear una nueva fila con los datos
            row_data = [
                list(serial_codes.values())[0] if serial_codes else "",  # Código Serial (primer código generado)
                ticket_number,
                referencia,
                color
            ]
            # Añadir cantidades por talla (33 a 48)
            for i in range(33, 49):
                row_data.append(tallas_cantidades.get(str(i), 0))
            # Añadir total producido y valores por tipo de trabajo
            row_data.extend([
                total_producido_calculado,
                valores_trabajo.get("Corte", 0),
                valores_trabajo.get("Empaque", 0),
                valores_trabajo.get("Guarnecedor", 0),
                valores_trabajo.get("Montador", 0),
                valores_trabajo.get("Plantillas", 0),
                valores_trabajo.get("Soldador", 0),
                self.current_code_type.upper(),  # Tipo Código
                code_path  # Ruta Imagen
            ])
            # Añadir códigos seriales por tipo de trabajo
            work_type_abbreviations = {
                'Corte': 'C', 'Empaque': 'E', 'Guarnecedor': 'G',
                'Montador': 'M', 'Plantillas': 'P', 'Soldador': 'S'
            }
            for work_type in work_type_abbreviations.keys():
                row_data.append(serial_codes.get(work_type, ""))

            # Añadir la fila a la hoja "Trabajos"
            ws_trabajos.append(row_data)
            wb.save(self.excel_path)
            return True
        except Exception as e:
            print(f"Error al guardar en Excel: {e}")
            return False
        
    #TODOok

    def find_code_data(self, serial_code):
        """Find data related to a specific serial code in the Excel file"""
        try:
            # Load Excel file
            wb = load_workbook(self.excel_path)
            ws = wb.active
            
            # Search for the serial code in the first column
            for row in ws.iter_rows(min_row=2):  # Start from row 2 to skip header
                if row[0].value == serial_code:
                    # Return all data for this row
                    return {
                        "serial_code": row[0].value,
                        "num_ticket": row[1].value,
                        "referencia": row[2].value,
                        "color": row[3].value,
                        "total_producido": row[16].value,  # Índice 16 para Total Producido
                        "valor_corte": row[17].value,
                        "valor_empaque": row[18].value,
                        "valor_guarnecedor": row[19].value,
                        "valor_montador": row[20].value,
                        "valor_plantillas": row[21].value,
                        "valor_soldador": row[22].value
                    }
            
            return None
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar datos: {str(e)}")
            return None
        #TODOok

    def on_code_scanned(self):
        """Maneja el evento cuando se escanea o ingresa un código."""
        if not hasattr(self.ui, 'codeReaderInput'):
            print("ERROR: codeReaderInput no encontrado en UI")
            return

        scanned_code = self.ui.codeReaderInput.text().strip()
        if not scanned_code:
            QMessageBox.warning(self, "Entrada Vacía", "Por favor, escanee o ingrese un código válido.")
            return

        # Cargar el archivo Excel
        try:
            wb = load_workbook(self.excel_path)
            ws_trabajos = wb["Trabajos"]
            ws_vales = wb[self.vales_sheet_name]
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo Excel: {e}")
            return

        # Buscar el código en las columnas de códigos seriales por tipo de trabajo
        work_type_abbreviations = {
            'Corte': 'C', 'Empaque': 'E', 'Guarnecedor': 'G',
            'Montador': 'M', 'Plantillas': 'P', 'Soldador': 'S'
        }
        work_type_columns = {work_type: f"Código_{work_type}" for work_type in work_type_abbreviations.keys()}
        found_row = None
        work_type_found = None

        # Obtener los índices de las columnas
        headers = [cell.value for cell in ws_trabajos[1]]
        for row in ws_trabajos.iter_rows(min_row=2, values_only=True):
            for work_type, column_name in work_type_columns.items():
                col_idx = headers.index(column_name) if column_name in headers else -1
                if col_idx != -1 and row[col_idx] == scanned_code:
                    found_row = row
                    work_type_found = work_type
                    break
            if found_row:
                break

        if not found_row:
            QMessageBox.warning(self, "Código No Encontrado", f"El código '{scanned_code}' no se encontró en la hoja 'Trabajos'.")
            self.ui.codeReaderInput.clear()
            return

        # Obtener datos de la fila encontrada
        try:
            ticket_number = found_row[headers.index("Número Ticket")]
            referencia = found_row[headers.index("Referencia")]
            color = found_row[headers.index("Color")]
            total_producido = found_row[headers.index("Total Producido")]
            valor_trabajo = found_row[headers.index(f"Valor {work_type_found}")]
            tallas_cantidades = {}
            for i in range(33, 49):
                cantidad = found_row[headers.index(f"Cant_T{i}")]
                if cantidad and cantidad > 0:
                    tallas_cantidades[str(i)] = cantidad
            resumen_tallas = "; ".join([f"Talla {k}: {v}" for k, v in tallas_cantidades.items()])
        except ValueError as e:
            QMessageBox.critical(self, "Error", f"Error al procesar los datos de la hoja 'Trabajos': {e}")
            return

        # Obtener el empleado seleccionado
        if not hasattr(self.ui, 'EmpleadosBox'):
            QMessageBox.critical(self, "Error", "No se encontró el ComboBox de empleados.")
            return
        empleado_id = self.ui.EmpleadosBox.currentData()
        if not empleado_id:
            QMessageBox.warning(self, "Empleado No Seleccionado", "Por favor, seleccione un empleado.")
            return

        # Generar un ID único para el vale
        id_vale = f"V{int(time.time())}"  # ID basado en timestamp
        fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        suma_valores = valor_trabajo  # Solo el valor del trabajo escaneado

        # Crear la fila para la hoja "Vales"
        vale_row = [
            id_vale,
            empleado_id,
            fecha_hora,
            ticket_number,
            referencia,
            color,
            resumen_tallas,
            total_producido,
            suma_valores,
            scanned_code
        ]

        # Guardar en la hoja "Vales"
        try:
            ws_vales.append(vale_row)
            wb.save(self.excel_path)
            QMessageBox.information(self, "Vale Registrado", f"Vale {id_vale} registrado exitosamente para {work_type_found}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el vale en Excel: {e}")
            return

        # Actualizar la tabla visual
        if hasattr(self.ui, 'tableViewVale'):
            row_data = [
                scanned_code, ticket_number, referencia, color, total_producido,
                found_row[headers.index("Valor Corte")],
                found_row[headers.index("Valor Empaque")],
                found_row[headers.index("Valor Guarnecedor")],
                found_row[headers.index("Valor Montador")],
                found_row[headers.index("Valor Plantillas")],
                found_row[headers.index("Valor Soldador")]
            ]
            items = [QtGui.QStandardItem(str(value) if value is not None else "") for value in row_data]
            self.table_model.appendRow(items)

        # Limpiar el campo de entrada
        self.ui.codeReaderInput.clear()
    #TODOok
    def register_vale(self):
        """Register the scanned vales to Excel"""
        if not hasattr(self, 'pending_vales') or not self.pending_vales:
            QMessageBox.warning(self, "Sin Vales", "No hay vales pendientes para registrar.")
            return
        
        try:
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            wb = load_workbook(self.excel_path)
            if self.vales_sheet_name in wb.sheetnames:
                ws = wb[self.vales_sheet_name]
            else:
                ws = wb.create_sheet(title=self.vales_sheet_name)
                ws.append([
                    "ID", "EmpleadoID", "Fecha", "Código Serial", "Número Ticket",
                    "Referencia", "Color", "Total Producido", "Valor Corte",
                    "Valor Empaque", "Valor Guarnecedor", "Valor Montador",
                    "Valor Plantillas", "Valor Soldador"
                ])
            
            for vale in self.pending_vales:
                ws.append([
                    vale["vale_id"],
                    vale["employee_id"],
                    current_date,
                    vale["serial_code"],
                    vale["num_ticket"],
                    vale["referencia"],
                    vale["color"],
                    vale["total_producido"],
                    vale["valor_corte"],
                    vale["valor_empaque"],
                    vale["valor_guarnecedor"],
                    vale["valor_montador"],
                    vale["valor_plantillas"],
                    vale["valor_soldador"]
                ])
            
            wb.save(self.excel_path)
            self.pending_vales = []
            if self.table_model:
                self.table_model.removeRows(0, self.table_model.rowCount())
            
            QMessageBox.information(self, "Vales Registrados",
                                    f"Se han registrado {len(self.pending_vales)} vales correctamente.")
        
        except Exception as e:
            print(f"Error al registrar vales: {e}")
            QMessageBox.critical(self, "Error", f"Error al registrar vales: {str(e)}")
    #TODOok
    def on_save_button_clicked(self):
        """Handler for save button click"""
        # --- 1. Definición de Campos y Recolección Inicial ---
        required_core_fields = []
        all_fields_to_clear = []

        # Campos básicos obligatorios
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            required_core_fields.append((self.ui.CampoReferenciaTrabajo, "Referencia"))
            all_fields_to_clear.append(self.ui.CampoReferenciaTrabajo)
        if hasattr(self.ui, 'CampoNumeroTicket'):
            required_core_fields.append((self.ui.CampoNumeroTicket, "Número de Ticket"))
            all_fields_to_clear.append(self.ui.CampoNumeroTicket)
        if hasattr(self.ui, 'CampoColor'):
            required_core_fields.append((self.ui.CampoColor, "Color"))
            all_fields_to_clear.append(self.ui.CampoColor)

        # --- 2. Validación de Campos Básicos ---
        for field, name in required_core_fields:
            if not field.text().strip():
                QMessageBox.warning(self, "Campos Incompletos", f"El campo '{name}' es obligatorio.")
                field.setFocus()
                return

        # --- 3. Recolección de Datos Específicos ---
        referencia = getattr(self.ui, 'CampoReferenciaTrabajo').text().strip() if hasattr(self.ui, 'CampoReferenciaTrabajo') else ""
        ticket_number = getattr(self.ui, 'CampoNumeroTicket').text().strip() if hasattr(self.ui, 'CampoNumeroTicket') else ""
        color = getattr(self.ui, 'CampoColor').text().strip() if hasattr(self.ui, 'CampoColor') else ""

        # Recolectar Tallas y Cantidades
        tallas_cantidades = {}
        total_producido_calculado = 0
        has_any_talla = False
        for i in range(33, 49):
            field_name = f"CampoTalla_{i}"
            if hasattr(self.ui, field_name):
                talla_field = getattr(self.ui, field_name)
                all_fields_to_clear.append(talla_field)
                cantidad_text = talla_field.text().strip()
                if cantidad_text:
                    if cantidad_text.isdigit() and int(cantidad_text) > 0:
                        cantidad = int(cantidad_text)
                        tallas_cantidades[str(i)] = cantidad
                        total_producido_calculado += cantidad
                        has_any_talla = True
                    else:
                        QMessageBox.warning(self, "Entrada Inválida",
                                            f"La cantidad para la Talla {i} ('{cantidad_text}') debe ser un número entero positivo.")
                        talla_field.setFocus()
                        return
        
        if not has_any_talla:
            QMessageBox.warning(self, "Campos Incompletos", "Debe ingresar la cantidad para al menos una talla.")
            if hasattr(self.ui, "CampoTalla_33"):
                getattr(self.ui, "CampoTalla_33").setFocus()
            return

        # Recolectar Valores por Tipo de Trabajo
        valores_trabajo = {}
        work_type_abbreviations = {
            'Corte': 'C', 'Empaque': 'E', 'Guarnecedor': 'G',
            'Montador': 'M', 'Plantillas': 'P', 'Soldador': 'S'
        }
        campos_valor_trabajo_nombres = [
            ('CampoValorCorte', "Corte"), ('CampoValorEmpaque', "Empaque"),
            ('CampoValorGuarnecedor', "Guarnecedor"), ('CampoValorMontador', "Montador"),
            ('CampoValorPlantillas', "Plantillas"), ('CampoValorSoldador', "Soldador")
        ]

        for field_attr_name, readable_name in campos_valor_trabajo_nombres:
            if hasattr(self.ui, field_attr_name):
                valor_field = getattr(self.ui, field_attr_name)
                all_fields_to_clear.append(valor_field)
                valor_text = valor_field.text().strip()
                if valor_text:
                    try:
                        valor_float = float(valor_text.replace(',', '.'))
                        valores_trabajo[readable_name] = valor_float
                    except ValueError:
                        QMessageBox.warning(self, "Entrada Inválida",
                                            f"El valor para '{readable_name}' ('{valor_text}') debe ser un número.")
                        valor_field.setFocus()
                        return

        # --- 4. Generación de Códigos Serial y Barcodes ---
        serial_codes = {}
        barcode_paths = {}
        for work_type, abbr in work_type_abbreviations.items():
            if work_type in valores_trabajo:  # Only generate for work types with values
                serial_code = generate_serial_code(ticket_number, referencia, color, tallas_cantidades, abbr)
                barcode_path = generate_barcode(serial_code)
                if not barcode_path:
                    QMessageBox.critical(self, "Error", f"Error al generar el código de barras para {work_type}.")
                    return
                serial_codes[work_type] = serial_code
                barcode_paths[work_type] = barcode_path

        # --- 5. Guardado en Excel (Trabajos) ---
        first_work_type = next(iter(valores_trabajo), None)
        if first_work_type:
            if not self.save_to_excel(
                serial_codes=serial_codes,
                code_path=barcode_paths[first_work_type] if first_work_type else "",
                ticket_number=ticket_number,
                referencia=referencia,
                color=color,
                tallas_cantidades=tallas_cantidades,
                total_producido_calculado=total_producido_calculado,
                valores_trabajo=valores_trabajo
            ):
                QMessageBox.critical(self, "Error de Guardado", "No se pudieron guardar los datos en Excel (Trabajos).")
                return

        # --- 6. Generación de PDF ---
        pdf_path = generate_vale_pdf(
            ticket_number, referencia, tallas_cantidades, color,
            total_producido_calculado, barcode_paths, valores_trabajo
        )

        if not pdf_path:
            QMessageBox.critical(self, "Error", "Datos guardados en Excel, pero hubo un error al generar el PDF.")
            return

        QMessageBox.information(
            self,
            "Operación Exitosa",
            f"Códigos generados: {', '.join(serial_codes.values())}\n"
            f"Tipo: {self.current_code_type.upper()}\n"
            f"Total Producido: {total_producido_calculado} unidades.\n"
            f"Los datos se han guardado correctamente.\n"
            f"PDF generado en: {pdf_path}"
        )

        # --- 7. Limpieza de Campos ---
        for field_widget in all_fields_to_clear:
            field_widget.clear()
        
        if hasattr(self.ui, 'CampoReferenciaTrabajo'):
            self.ui.CampoReferenciaTrabajo.setFocus()


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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeui.ttf')
    QtGui.QFontDatabase.addApplicationFont('fonts/segoeuib.ttf')
    window = MainWindow()

    sys.exit(app.exec_())