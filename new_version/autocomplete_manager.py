# autocompletado.py

from PySide2.QtWidgets import QCompleter  # MODIFICADO
from PySide2.QtCore import Qt             # MODIFICADO
import pandas as pd
import os

class AutocompletadoManager:
    """
    Clase para manejar el autocompletado de QLineEdit basado en datos de Excel
    """
    
    def __init__(self, excel_path, sheet_name="Trabajos"):
        """
        Inicializar el manager de autocompletado
        
        Args:
            excel_path (str): Ruta al archivo Excel
            sheet_name (str): Nombre de la hoja de Excel
        """
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.completers = {}  # Diccionario para almacenar los completers por campo
        
    def obtener_valores_unicos(self, columna):
        """
        Obtener valores únicos de una columna específica del Excel
        
        Args:
            columna (str): Nombre de la columna
            
        Returns:
            list: Lista de valores únicos
        """
        try:
            if not os.path.exists(self.excel_path):
                print(f"Advertencia: El archivo Excel no se encuentra en {self.excel_path}")
                return []
            
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            
            if columna not in df.columns:
                print(f"Advertencia: La columna '{columna}' no se encuentra en la hoja '{self.sheet_name}'.")
                return []
                
            # Obtener valores únicos, filtrar nulos y convertir a string
            valores = df[columna].dropna().unique()
            return [str(valor).strip() for valor in valores if str(valor).strip()]
            
        except Exception as e:
            print(f"Error al obtener valores de {columna}: {e}")
            return []
    
    def configurar_autocompletado(self, line_edit, columna, campo_id=None):
        """
        Configurar autocompletado para un QLineEdit específico
        
        Args:
            line_edit: Widget QLineEdit (debe ser PySide2.QtWidgets.QLineEdit)
            columna (str): Nombre de la columna en Excel
            campo_id (str): ID único para el campo (opcional)
        """
        if campo_id is None:
            campo_id = columna
            
        valores = self.obtener_valores_unicos(columna)
        
        if not valores:
            # print(f"No se encontraron valores para autocompletar en la columna '{columna}'.")
            # Es normal que no haya valores a veces, así que un print puede ser mucho log.
            # Considera si quieres un log aquí o no.
            # Si el QLineEdit ya tiene un completer, podríamos querer limpiarlo
            # o dejarlo como está si los valores estaban vacíos previamente.
            # Por ahora, si no hay valores, no se asigna ni actualiza el completer.
            # Si se desea limpiar un completer existente si no hay nuevos valores:
            # current_completer = line_edit.completer()
            # if current_completer:
            #     line_edit.setCompleter(None) # o un QCompleter([]) vacío
            return
            
        # Crear completer (ahora será un PySide2.QtWidgets.QCompleter)
        completer = QCompleter(valores)
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # No distingue mayúsculas/minúsculas
        completer.setFilterMode(Qt.MatchContains)  # Sugerencias si contiene, no solo si empieza igual
        completer.setCompletionMode(QCompleter.PopupCompletion)
        
        # Asignar completer al line_edit
        line_edit.setCompleter(completer)
        
        self.completers[campo_id] = completer
        
        # Guardar el método original de focusInEvent si existe, para no sobreescribir otros comportamientos
        original_focus_in_event = line_edit.focusInEvent
        
        # Conectar evento de focus para actualizar automáticamente
        # Es importante que 'original_focus_in_event' y 'line_edit' se capturen correctamente en el lambda
        line_edit.focusInEvent = lambda event, captured_original_event=original_focus_in_event, captured_line_edit=line_edit, captured_columna=columna, captured_campo_id=campo_id: \
                                 self._on_focus_in(event, captured_original_event, captured_line_edit, captured_columna, captured_campo_id)
    
    def _on_focus_in(self, event, original_event_handler, line_edit, columna, campo_id):
        """
        Evento que se ejecuta cuando el QLineEdit recibe focus
        """
        # Ejecutar el evento original si existe
        if callable(original_event_handler):
            original_event_handler(event)
        
        # Actualizar autocompletado
        self.actualizar_autocompletado(line_edit, columna, campo_id)
    
    def actualizar_autocompletado(self, line_edit, columna, campo_id=None):
        """
        Actualizar el autocompletado de un campo específico
        
        Args:
            line_edit: Widget QLineEdit
            columna (str): Nombre de la columna en Excel
            campo_id (str): ID único para el campo (opcional)
        """
        if campo_id is None:
            campo_id = columna
            
        nuevos_valores = self.obtener_valores_unicos(columna)
        
        if not nuevos_valores:
            # Si no hay nuevos valores, podríamos optar por limpiar el completer actual
            # o mantener las sugerencias anteriores si es preferible.
            # Para limpiar:
            # current_completer = line_edit.completer()
            # if current_completer:
            #    current_completer.model().setStringList([]) # Vaciar la lista del modelo actual
            # O simplemente no hacer nada si no hay nuevos valores y se quiere mantener el estado.
            # print(f"No se encontraron nuevos valores para actualizar autocompletado de '{columna}'.")
            return
            
        # Obtener el completer existente o crear uno nuevo
        completer = line_edit.completer()
        if completer:
            # Si ya existe un completer, simplemente actualizamos su modelo (la lista de strings)
            # Esto es más eficiente que crear un nuevo QCompleter cada vez.
            model = completer.model()
            model.setStringList(nuevos_valores)
        else:
            # Si no hay completer, creamos uno nuevo y lo asignamos
            completer = QCompleter(nuevos_valores)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            line_edit.setCompleter(completer)
        
        # Actualizar referencia (si es que esto es necesario fuera de la asignación inicial)
        self.completers[campo_id] = completer # Asegura que self.completers tenga el completer más reciente
    
    def actualizar_todos_los_autocompletados(self):
        """
        Actualizar todos los autocompletados configurados.
        Esto requiere que guardemos la información de line_edit y columna asociada a cada campo_id
        si queremos llamar a actualizar_autocompletado.
        Por ahora, esta función no está completamente implementada para una actualización general
        sin tener las referencias directas a los line_edits y sus columnas asociadas.
        """
        # Para implementar esto correctamente, necesitarías almacenar el line_edit y la columna
        # junto con el completer, o tener una forma de recuperarlos a partir de campo_id.
        # Ejemplo de cómo podría ser si guardaras más info:
        # for campo_id, data in self.completer_info.items(): # Suponiendo que completer_info guarda {'line_edit': ..., 'columna': ...}
        #     self.actualizar_autocompletado(data['line_edit'], data['columna'], campo_id)
        print("La función 'actualizar_todos_los_autocompletados' necesita ser expandida para ser funcional.")
        pass # Implementación pendiente si es necesaria
    
    def configurar_multiples_campos(self, campos_config):
        """
        Configurar múltiples campos de autocompletado de una vez
        
        Args:
            campos_config (dict): Diccionario con configuración de campos
                                  Formato: {campo_id: {'line_edit': widget, 'columna': 'nombre_columna'}}
        """
        for campo_id, config in campos_config.items():
            line_edit = config.get('line_edit')
            columna = config.get('columna')
            
            if not line_edit or not columna:
                print(f"Advertencia: Configuración incompleta para el campo_id '{campo_id}'. Faltan 'line_edit' o 'columna'.")
                continue
                
            self.configurar_autocompletado(line_edit, columna, campo_id)
            
    def obtener_todos_los_trabajos(self):
        """
        Obtener información completa de todos los trabajos
        
        Returns:
            list: Lista de diccionarios con información de trabajos
        """
        try:
            if not os.path.exists(self.excel_path):
                print(f"Advertencia: El archivo Excel no se encuentra en {self.excel_path} al intentar obtener todos los trabajos.")
                return []
            
            df = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)
            return df.to_dict('records')
            
        except Exception as e:
            print(f"Error al obtener trabajos: {e}")
            return []