import uuid
from PySide2.QtWidgets import QMessageBox
from utils import validate_cedula # Asumiendo que esta función está en utils.py

class EmployeeManager:
    def __init__(self, excel_handler, ui_manager):
        self.excel_handler = excel_handler
        self.ui_manager = ui_manager

    def add_employee(self, nombre, cedula, celular, correo):
        """Valida y agrega un nuevo empleado a la base de datos."""
        # Validaciones
        if not nombre or not cedula:
            QMessageBox.warning(None, "Campos Requeridos", "Nombre y Cédula son obligatorios.")
            return False
        if not validate_cedula(cedula):
            QMessageBox.warning(None, "Cédula Inválida", "La cédula debe contener solo números (6-12 dígitos).")
            return False
        
        # TODO: Añadir lógica para verificar si la cédula ya existe usando self.excel_handler
        
        unique_id = str(uuid.uuid4())[:4]
        empleado_id = f"E{cedula[-4:]}{unique_id}".upper()
        
        empleado_data = [nombre, cedula, celular, correo, empleado_id]
        if self.excel_handler.guardar_empleado(empleado_data):
            QMessageBox.information(None, "Éxito", f"Empleado '{nombre}' agregado con ID: {empleado_id}")
            self.load_employees_to_ui() # Recargar la lista
            self.ui_manager.clear_employee_form()
            return True
        return False

    def load_employees_to_ui(self):
        """Carga la lista de empleados y la muestra en el ComboBox."""
        employees = self.excel_handler.leer_empleados()
        self.ui_manager.populate_employee_combobox(employees)

    def generate_and_update_reports(self):
        """Orquesta la generación de reportes."""
        # 1. Leer datos de vales y empleados desde Excel
        # vales_data = self.excel_handler.get_all_vales()
        # empleados_data = self.excel_handler.get_all_employees()
        
        # 2. Procesar los datos para generar los reportes (lógica de 'update_employee_reports')
        # report_data = self._process_report_data(vales_data, empleados_data)

        # 3. Actualizar la tabla en la UI
        # self.ui_manager.update_report_table(report_data['consolidado'])

        # 4. Escribir las hojas individuales en Excel
        # self.excel_handler.write_employee_report_sheets(report_data['individuales'])
        
        print("Lógica de reportes debe ser implementada aquí.")
        QMessageBox.information(None, "En Construcción", "La generación de reportes está pendiente de refactorizar.")