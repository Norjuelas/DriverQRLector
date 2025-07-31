import time
import uuid
import datetime as dt
from PySide2.QtWidgets import QMessageBox

class ValeManager:
    def __init__(self, excel_handler, ui_manager):
        self.excel_handler = excel_handler
        self.ui_manager = ui_manager

    def process_scanned_code(self, scanned_code, empleado_id, current_table_codes, work_type_columns):
        """
        Procesa un código escaneado: valida, busca, y si es válido, lo registra y actualiza la UI.
        """
        if not scanned_code:
            QMessageBox.warning(None, "Entrada Vacía", "Por favor, ingrese un código.")
            return

        if not empleado_id:
            QMessageBox.warning(None, "Empleado No Seleccionado", "Por favor, seleccione un empleado.")
            return

        # 1. Validar si ya está en la tabla de la UI
        if scanned_code in current_table_codes:
            QMessageBox.warning(None, "Vale Duplicado", f"El código '{scanned_code}' ya está en la lista actual.")
            return
        
        # 2. Validar si ya está registrado en la hoja "Vales"
        # ... Aquí iría una llamada a self.excel_handler.is_vale_already_registered(scanned_code) ...

        # 3. Buscar el código en la hoja "Trabajos"
        trabajo_data, work_type_found = self.excel_handler.buscar_trabajo_por_codigo(scanned_code, work_type_columns)

        if not trabajo_data:
            QMessageBox.warning(None, "Código No Encontrado", f"El código '{scanned_code}' no se encontró en la base de datos de trabajos.")
            return
            
        # 4. Extraer datos y crear la fila para la hoja "Vales"
        id_vale = f"V{int(time.time())}{str(uuid.uuid4())[:4]}"
        fecha_hora = dt.datetime.now()
        
        # Simplificando la extracción de datos
        ticket_number = trabajo_data.get("Número Ticket")
        referencia = trabajo_data.get("Referencia")
        color = trabajo_data.get("Color")
        total_producido = trabajo_data.get("Total Producido")
        valor_trabajo = trabajo_data.get(f"Valor {work_type_found}")

        vale_row_to_save = [
            id_vale, empleado_id, fecha_hora, ticket_number, referencia,
            color, "resumen_tallas_aqui", total_producido, valor_trabajo,
            scanned_code, work_type_found
        ]
        
        # 5. Guardar en Excel
        if self.excel_handler.guardar_vale(vale_row_to_save):
            # 6. Actualizar la tabla de la UI si se guardó correctamente
            row_for_ui = [scanned_code, ticket_number, referencia, work_type_found, color, total_producido, valor_trabajo]
            self.ui_manager.add_row_to_vale_table(row_for_ui)
            QMessageBox.information(None, "Vale Registrado", f"Vale para '{work_type_found}' registrado exitosamente.")
        else:
            QMessageBox.critical(None, "Error", "No se pudo guardar el vale en la base de datos.")

    def register_pending_vales(self):
        """Limpia la tabla visual. La lógica de guardado ya ocurrió en process_scanned_code."""
        self.ui_manager.clear_vale_table()
        QMessageBox.information(None, "Vista Limpiada", "La lista de previsualización ha sido limpiada.")
