# ui_manager.py
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QPropertyAnimation, QSize, Qt
from PySide2.QtGui import QFont, QIcon, QColor, QStandardItemModel, QStandardItem
from PySide2.QtWidgets import (
    QPushButton, QSizePolicy, QGraphicsDropShadowEffect, QSizeGrip,
    QHeaderView, QVBoxLayout, QTableView
)

# Puedes importar tus estilos si los tienes en un archivo separado
from ui_styles import Style 

class UIManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        
        # Las variables globales ahora son atributos de la instancia
        self.global_state = 0
        self.animation = None # Para evitar errores si se llama varias veces

    # --- MÉTODOS DE CONFIGURACIÓN DE ALTO NIVEL (Tu código original) ---

    def setup_window_and_ui(self):
        """Método único para toda la configuración inicial de la UI."""
        # Configuración de la ventana sin bordes, sombra, etc.
        self._uiDefinitions() 
        
        # Propiedades de la ventana (título, tamaño)
        self.main_window.setWindowTitle('Gestor de Vales')
        self.labelTitle('Thimoty') # Llama al método local
        # self.labelDescription('2025') # Si tienes este método, muévelo aquí también
        
        startSize = QSize(1300, 720)
        self.main_window.resize(startSize)
        self.main_window.setMinimumSize(startSize)

class UIManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.ui = main_window.ui
        self.global_state = 0
        self.animation = None

    # --- MÉTODOS DE CONFIGURACIÓN PRINCIPALES ---

    def setup_window_and_ui(self):
        """Método único que configura toda la apariencia inicial de la UI."""
        self._uiDefinitions()  # Configura ventana sin bordes, sombra, etc.
        
        self.main_window.setWindowTitle('Gestor de Vales')
        self.labelTitle('Thimoty') # Llama al método de ESTA MISMA clase
        # self.labelDescription('2025') # Si tienes este método, llámalo aquí también

        startSize = QSize(1300, 720)
        self.main_window.resize(startSize)
        self.main_window.setMinimumSize(startSize)

    def setup_menus_and_buttons(self):
        """Configura los menús de navegación y los botones de acción."""
        self.ui.btn_toggle_menu.clicked.connect(lambda: self.toggleMenu(220, True))
        self.ui.stackedWidget.setMinimumWidth(20)

        # Usamos el método de esta clase para crear los menús
        self.addNewMenu("Leer Vales", "btn_home", "url(:/16x16/icons/16x16/cil-home.png)", True)
        self.addNewMenu("Crear Vales", "btn_new_user", "url(:/16x16/icons/16x16/cil-user-follow.png)", True)
        self.addNewMenu("Configuracion", "btn_widgets", "url(:/16x16/icons/16x16/cil-equalizer.png)", False)
        
        self.selectStandardMenu("btn_home")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        
        # Conexiones de botones (esta parte ya estaba bien)
        if hasattr(self.ui, 'pushButtonGuardar'):
            self.ui.pushButtonGuardar.clicked.connect(self.main_window.on_save_button_clicked)
        # ... resto del método ...

    # --- MÉTODOS DE MANIPULACIÓN DE UI (Movidos desde ui_functions.py) ---

    def maximize_restore(self):
        """Maximiza o restaura la ventana."""
        status = self.global_state
        if status == 0:
            self.main_window.showMaximized()
            self.global_state = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_size_grip.hide()
        else:
            self.global_state = 0
            self.main_window.showNormal()
            self.main_window.resize(self.main_window.width()+1, self.main_window.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_size_grip.show()

    def get_status(self):
        return self.global_state

    def toggleMenu(self, maxWidth, enable):
        """Anima el menú lateral para expandirlo o contraerlo."""
        if enable:
            width = self.ui.frame_left_menu.width()
            widthExtended = maxWidth if width == 70 else 70
            
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def labelTitle(self, text):
        """Establece el texto de la barra de título."""
        self.ui.label_title_bar_top.setText(text)

    def addNewMenu(self, name, objName, icon_path, isTopMenu):
        """Crea y añade un nuevo botón al menú lateral."""
        button = QPushButton(name, self.main_window)
        button.setObjectName(objName)
        button.setMinimumSize(QSize(0, 70))
        # Asumiendo que `Style` no existe, usamos un stylesheet simple. Reemplázalo si tienes tu clase `Style`.
        style = f"""
        QPushButton {{
            background-image: url({icon_path});
            background-position: left center;
            background-repeat: no-repeat;
            border: none;
            border-left: 28px solid rgb(27, 29, 35);
            background-color: rgb(27, 29, 35);
            text-align: left;
            padding-left: 45px;
        }}
        """
        button.setStyleSheet(style)
        button.clicked.connect(self.main_window.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)
            
    def selectMenu(self, getStyle):
        return getStyle + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"

    def deselectMenu(self, getStyle):
        return getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
    
    def resetStyle(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.deselectMenu(w.styleSheet()))

    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(self.selectMenu(w.styleSheet()))

    def _uiDefinitions(self):
        """Configuraciones privadas de la UI (sombra, ventana sin bordes, etc.)."""
        def dobleClickMaximizeRestore(event):
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: self.maximize_restore())

        self.main_window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        
        shadow = QGraphicsDropShadowEffect(self.main_window)
        shadow.setBlurRadius(17)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(shadow)

        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin: 0px; padding: 0px;")

        self.ui.btn_minimize.clicked.connect(lambda: self.main_window.showMinimized())
        self.ui.btn_maximize_restore.clicked.connect(lambda: self.maximize_restore())
        self.ui.btn_close.clicked.connect(lambda: self.main_window.close())

    def populate_employee_combobox(self, employees):
        """Llena el ComboBox de empleados."""
        self.ui.EmpleadosBox.clear()
        if not employees:
            self.ui.EmpleadosBox.addItem("Sin empleados registrados", "")
            return
        for emp in employees:
            self.ui.EmpleadosBox.addItem(f"{emp['nombre']} ({emp['id']})", emp['id'])

    def add_row_to_vale_table(self, row_data):
        """Añade una fila a la tabla de previsualización de vales."""
        items = [QStandardItem(str(value) if value is not None else "") for value in row_data]
        self.main_window.table_model.appendRow(items)
    
    def clear_vale_table(self):
        """Limpia la tabla de previsualización de vales."""
        if hasattr(self.main_window, 'table_model'):
            self.main_window.table_model.removeRows(0, self.main_window.table_model.rowCount())

    def clear_employee_form(self):
        """Limpia los campos del formulario de agregar empleado."""
        self.ui.Nombre_Empleado.clear()
        self.ui.Cedula_Empleado.clear()
        self.ui.Celular_Empleado.clear()
        self.ui.Correo_Empleado.clear()