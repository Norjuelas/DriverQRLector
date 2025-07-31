import sys
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import Qt, QEvent
# GUI FILE
from ui_main import Ui_MainWindow

## ==> APP FUNCTIONS
from backup_thread import BackupThread, BackupManager

from autocomplete_manager import *

from generate_pdf import *
from ui_manager import UIManager
from generateCodes import *
# Importaciones de los nuevos módulos
from excel_handler import ExcelHandler
from employee_manager import EmployeeManager
from vale_manager import ValeManager
# from code_manager import CodeManager # Si decides crearlo
from autocomplete_manager import AutocompletadoManager
from config import TIPOS_DE_TRABAJO, WORK_TYPE_ABBREVIATIONS, CAMPOS_VALOR_TRABAJO_MAP

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dragPos = None
        self.table_model = None # El modelo de la tabla de vales vivirá aquí

        # --- INICIALIZACIÓN DE GESTORES ---
        self.excel_handler = ExcelHandler()
        self.ui_manager = UIManager(self)
        self.employee_manager = EmployeeManager(self.excel_handler, self.ui_manager)
        self.vale_manager = ValeManager(self.excel_handler, self.ui_manager)
        self.autocompletado_manager = AutocompletadoManager(excel_path=self.excel_handler.excel_path, sheet_name="Trabajos")

        # --- CONFIGURACIÓN INICIAL ---
        self.setup_application()
        self.ui_manager.setup_window_and_ui() 

        self.show()

    def setup_application(self):
        """Método central para configurar toda la aplicación."""
        # 1. Configurar la ventana y menús
        self.ui_manager.setup_window()
        self.ui_manager.setup_menus_and_buttons()

        # 2. Inicializar la base de datos Excel
        # Define tus cabeceras aquí o impórtalas desde config.py
        trabajos_headers = ["Código Serial", "Número Ticket", "Referencia", "Color", ...]
        vales_headers = ["ID_Vale", "EmpleadoID", "FechaHora_Generacion", ...]
        empleados_headers = ["Nombre", "Cedula", "Celular", "Correo", "EmpleadoId"]
        self.excel_handler.inicializar_database(trabajos_headers, vales_headers, empleados_headers)

        # 3. Configurar la vista del lector de códigos
        vale_table_headers = ["Código", "Ticket", "Referencia", "Trabajo", "Color", "Producido", "Valor"]
        self.ui_manager.setup_code_reader_view(vale_table_headers)
        
        # 4. Cargar empleados en el ComboBox
        self.employee_manager.load_employees_to_ui()
        
        # 5. Configurar autocompletado
        self.setup_autocompletado_fields()
        
    # --- HANDLERS DE EVENTOS (DELEGAN A LOS GESTORES) ---

    def on_save_button_clicked(self):
        """Se activa al pulsar 'Guardar' en la pestaña de creación."""
        # Aquí iría la lógica para recolectar datos de la UI y llamar al
        # code_manager para generar códigos y PDF, y al excel_handler para guardar.
        print("Lógica para crear vales (on_save_button_clicked) pendiente de refactorizar.")
        # Ejemplo:
        # ticket_data = self.ui_manager.collect_ticket_data()
        # if ticket_data:
        #     self.code_manager.generate_codes_and_pdf(ticket_data)
        #     self.excel_handler.guardar_trabajo(...)

    def on_code_scanned(self):
        """Se activa al presionar Enter en el campo de escaneo."""
        scanned_code = self.ui.codeReaderInput.text().strip()
        empleado_id = self.ui.EmpleadosBox.currentData()
        
        # Obtener códigos ya en la tabla para evitar duplicados
        current_codes = [self.table_model.item(row, 0).text() for row in range(self.table_model.rowCount())]
        
        # Definir las columnas donde buscar (deberían venir de config.py)
        work_type_columns = {wt: f"Código_{abbr}" for wt, abbr in WORK_TYPE_ABBREVIATIONS.items()}

        self.vale_manager.process_scanned_code(scanned_code, empleado_id, current_codes, work_type_columns)
        self.ui.codeReaderInput.clear()
        self.ui.codeReaderInput.setFocus()

    def add_employee(self):
        """Se activa al pulsar 'Agregar Empleado'."""
        nombre = self.ui.Nombre_Empleado.text().strip()
        cedula = self.ui.Cedula_Empleado.text().strip()
        celular = self.ui.Celular_Empleado.text().strip()
        correo = self.ui.Correo_Empleado.text().strip()
        self.employee_manager.add_employee(nombre, cedula, celular, correo)

    def register_vale(self):
        """Se activa al pulsar 'Registrar Vale'."""
        self.vale_manager.register_pending_vales()

    def update_employee_reports(self):
        """Se activa al pulsar 'Actualizar DB'."""
        self.employee_manager.generate_and_update_reports()

    def eliminar_todo_con_backup(self):
        """Lógica para eliminar la base de datos con backup."""
        # Esta lógica puede ir en un módulo 'backup_manager.py'
        print("Lógica de backup pendiente de refactorizar.")
    
    def setup_autocompletado_fields(self):
        """Configura los campos que usarán autocompletado."""
        # La lógica de este método no cambia mucho, solo llama al manager.
        campos = { ... } # Tu diccionario de campos
        self.autocompletado_manager.configurar_multiples_campos(campos)
        
    # --- Eventos de la ventana (sin cambios) ---
    def Button(self):
        """Maneja los clics de los botones del menú lateral."""
        btnWidget = self.sender()
        
        # La lógica de estilos se delega completamente al manager
        self.ui_manager.resetStyle(btnWidget.objectName())
        btnWidget.setStyleSheet(self.ui_manager.selectMenu(btnWidget.styleSheet()))

        # La lógica de navegación se queda aquí
        if btnWidget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        elif btnWidget.objectName() == "btn_new_user":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_widgets)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def moveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Cargar fuentes si es necesario
    window = MainWindow()
    sys.exit(app.exec_())