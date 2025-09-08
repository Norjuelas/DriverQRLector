import sqlite3
from typing import Dict, Any, List

# Dependencias de Qt (no cambian)
from PySide2.QtWidgets import QCompleter
from PySide2.QtCore import Qt

# Importamos la función para obtener la conexión a la base de datos
from db import get_conn 
# Importamos la lista de columnas válidas para validación
from dao import VALID_TRABAJO_COLUMNS, VALID_VALE_COLUMNS#, VALID_EMPLEADO_COLUMNS # Asumo que VALID_EMPLEADO_COLUMNS existe o la creamos

# --- Listas blancas de columnas para validación de seguridad ---
# Esto previene inyección SQL al construir consultas dinámicamente.
# El manager solo podrá consultar tablas y columnas definidas aquí.
VALID_COLUMNS_BY_TABLE = {
    "trabajos": VALID_TRABAJO_COLUMNS,
    "vales": VALID_VALE_COLUMNS,
    # "empleados": VALID_EMPLEADO_COLUMNS, # Necesitarás añadir esta lista en dao.py
}


class AutocompletadoManager:
    """
    Clase para manejar el autocompletado de QLineEdit basado en datos 
    de una base de datos SQLite.
    """

    def __init__(self):
        """
        Inicializar el manager de autocompletado.
        No necesita argumentos ya que la conexión a la BD se obtiene a demanda.
        """
        # Almacena las configuraciones para poder actualizarlas todas a la vez.
        # Formato: { 'campo_id': {'line_edit': QLineEdit, 'tabla': str, 'columna': str} }
        self.campos_configurados: Dict[str, Dict[str, Any]] = {}

    def obtener_valores_unicos(self, tabla: str, columna: str) -> List[str]:
        """
        Obtiene valores únicos de una columna y tabla específicas de la base de datos.

        Args:
            tabla (str): Nombre de la tabla a consultar (ej. "trabajos").
            columna (str): Nombre de la columna (ej. "referencia").

        Returns:
            list: Lista de valores únicos como strings.
        """
        # --- Validación de seguridad ---
        if tabla not in VALID_COLUMNS_BY_TABLE:
            print(f"Error de seguridad: La tabla '{tabla}' no está permitida para consultas.")
            return []
        if columna not in VALID_COLUMNS_BY_TABLE[tabla]:
            print(f"Error de seguridad: La columna '{columna}' no está permitida en la tabla '{tabla}'.")
            return []

        try:
            # Construcción segura de la consulta
            sql = f"SELECT DISTINCT {columna} FROM {tabla} WHERE {columna} IS NOT NULL AND {columna} != ''"
            
            with get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                # fetchall() devuelve una lista de tuplas, ej: [('valor1',), ('valor2',)]
                # La convertimos a una lista plana de strings.
                valores = [str(row[0]).strip() for row in cursor.fetchall()]
            
            return valores

        except sqlite3.Error as e:
            print(f"Error de base de datos al obtener valores para '{tabla}.{columna}': {e}")
            return []

    def configurar_autocompletado(self, line_edit, tabla: str, columna: str, campo_id: str = None):
        """
        Configura el autocompletado para un QLineEdit específico.

        Args:
            line_edit: Widget QLineEdit a configurar.
            tabla (str): Nombre de la tabla en la base de datos.
            columna (str): Nombre de la columna en la base de datos.
            campo_id (str, optional): ID único para el campo. Si es None, se usa el nombre de la columna.
        """
        if campo_id is None:
            campo_id = columna
        
        # Guardar la configuración para futuras actualizaciones
        self.campos_configurados[campo_id] = {
            'line_edit': line_edit,
            'tabla': tabla,
            'columna': columna
        }
            
        valores = self.obtener_valores_unicos(tabla, columna)

        # Usar el método de actualización, que es más robusto y evita duplicar código
        self.actualizar_autocompletado(line_edit, tabla, columna, valores_precalculados=valores)
        
        # --- Conexión al evento focusInEvent para auto-actualización ---
        # Sobrescribir el método de evento es arriesgado y puede causar problemas.
        # Es mucho más seguro y robusto conectarse a una señal si el widget la tuviera
        # o, en este caso, usar un event filter en la ventana principal.
        # Sin embargo, para mantener la lógica original, la adaptamos de forma más segura.
        
        original_focus_in_event = line_edit.focusInEvent
        
        def new_focus_in_event(event):
            # Llama al manejador original si existía
            original_focus_in_event(event)
            # Luego, ejecuta nuestra lógica de actualización
            self.actualizar_autocompletado(line_edit, tabla, columna)
        
        # Reemplaza el manejador de eventos del widget
        line_edit.focusInEvent = new_focus_in_event

    def actualizar_autocompletado(self, line_edit, tabla: str, columna: str, valores_precalculados: List[str] = None):
        """
        Actualiza la lista de sugerencias para un QLineEdit específico.
        Es más eficiente que re-crear el completer cada vez.

        Args:
            line_edit: Widget QLineEdit a actualizar.
            tabla (str): Nombre de la tabla.
            columna (str): Nombre de la columna.
            valores_precalculados (List[str], optional): Si ya se tienen los valores, se usan estos.
                                                          Si no, se consultan de la BD.
        """
        if valores_precalculados is not None:
            nuevos_valores = valores_precalculados
        else:
            nuevos_valores = self.obtener_valores_unicos(tabla, columna)

        completer = line_edit.completer()
        if completer:
            # Si ya existe, solo actualizamos el modelo (la lista de palabras)
            model = completer.model()
            model.setStringList(nuevos_valores)
        else:
            # Si no existe, lo creamos y configuramos desde cero
            if not nuevos_valores:
                return # No crear un completer si no hay valores iniciales
                
            completer = QCompleter(nuevos_valores)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchContains)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            line_edit.setCompleter(completer)

    def actualizar_todos_los_autocompletados(self):
        """
        Actualiza las listas de sugerencias para todos los campos configurados.
        Ideal para llamar después de guardar un nuevo registro que podría
        contener nuevos valores para autocompletar.
        """
        print("Actualizando todas las listas de autocompletado...")
        for campo_id, config in self.campos_configurados.items():
            print(f" -> Actualizando '{campo_id}' ({config['tabla']}.{config['columna']})")
            self.actualizar_autocompletado(
                line_edit=config['line_edit'],
                tabla=config['tabla'],
                columna=config['columna']
            )
        print("Actualización completada.")

    def configurar_multiples_campos(self, campos_config: Dict[str, Dict[str, Any]]):
        """
        Configura múltiples campos de autocompletado de una vez.

        Args:
            campos_config (dict): Diccionario con la configuración.
                Formato: {
                    'id_campo': {'line_edit': widget, 'tabla': 'nombre_tabla', 'columna': 'nombre_columna'}
                }
        """
        for campo_id, config in campos_config.items():
            line_edit = config.get('line_edit')
            tabla = config.get('tabla')
            columna = config.get('columna')
            
            if not all([line_edit, tabla, columna]):
                print(f"Advertencia: Configuración incompleta para '{campo_id}'. Se omitió.")
                continue
            
            self.configurar_autocompletado(line_edit, tabla, columna, campo_id)

    def obtener_todos_los_trabajos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los registros de la tabla 'trabajos' como una lista de diccionarios.

        Returns:
            list: Lista de diccionarios, donde cada uno es un trabajo.
        """
        try:
            with get_conn() as conn:
                # Usar Row Factory para obtener resultados como diccionarios
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM trabajos ORDER BY numero_ticket DESC")
                
                # Convertir cada objeto `sqlite3.Row` a un diccionario estándar
                trabajos = [dict(row) for row in cursor.fetchall()]
            return trabajos
        except sqlite3.Error as e:
            print(f"Error de base de datos al obtener todos los trabajos: {e}")
            return []
