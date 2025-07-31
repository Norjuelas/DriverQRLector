# -*- coding: utf-8 -*-
"""
Módulo para la tarjeta de visualización de Vales (Kanban) con Drag & Drop.
Compatible con PySide2.
"""
from PySide2.QtWidgets import QFrame, QLabel, QVBoxLayout, QApplication
from PySide2.QtCore import Qt, QMimeData
from PySide2.QtGui import QDrag, QPixmap


import sys
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QGridLayout, QGroupBox, QScrollArea
)
from PySide2.QtCore import Qt, Signal

# --- 1. IMPORTA LA NUEVA CLASE ValeCard ---

class ValeCard(QFrame):
    """
    Una tarjeta personalizable y arrastrable para mostrar la información de un vale.
    """
    def __init__(self, vale_data, parent=None):
        super(ValeCard, self).__init__(parent)
        
        # Guardamos el ticket_id para identificar la tarjeta durante el Drag & Drop
        self.ticket_id = vale_data.get('ticket', 'N/A')
        self.vale_data = vale_data # Guardamos todos los datos

        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setMinimumWidth(200)
        self.setMaximumHeight(120)
        self.setStyleSheet("""
            ValeCard {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 8px;
                padding: 8px;
            }
            QLabel {
                font-size: 13px;
                background-color: transparent; /* Importante para el drag pixmap */
            }
            .LabelTitulo {
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout(self)
        
        ticket_label = QLabel(f"Ticket: {self.ticket_id}")
        ticket_label.setObjectName("LabelTitulo")
        layout.addWidget(ticket_label)

        ref = vale_data.get('referencia', 'N/A')
        color = vale_data.get('color', 'N/A')
        total = vale_data.get('total', 0)
        
        layout.addWidget(QLabel(f"Ref: {ref} - Color: {color}"))
        layout.addWidget(QLabel(f"Total: {total}"))
        
        es_satelite = vale_data.get('Satelite', False)
        tipo = "Satélite" if es_satelite else "Empleado"
        
        tipo_label = QLabel(tipo)
        tipo_label.setAlignment(Qt.AlignRight)
        tipo_label.setStyleSheet("font-style: italic; color: #606060;")
        layout.addWidget(tipo_label)

    def mouseMoveEvent(self, event):
        """ Inicia la operación de arrastre (Drag). """
        if event.buttons() != Qt.LeftButton:
            return

        # Preparamos los datos a transferir (el ID del ticket)
        mime_data = QMimeData()
        # Usamos setText para enviar información simple como el ID
        mime_data.setText(self.ticket_id)

        # Creamos el objeto QDrag
        drag = QDrag(self)
        drag.setMimeData(mime_data)

        # Creamos una imagen de la tarjeta para que se vea mientras se arrastra
        pixmap = QPixmap(self.size())
        self.render(pixmap)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos()) # El punto del cursor sobre la imagen

        # Ocultamos la tarjeta original mientras se arrastra
        self.hide()

        # Ejecutamos el arrastre y esperamos a que termine
        # Qt.MoveAction indica que estamos moviendo el item
        drag.exec_(Qt.MoveAction)
        
        # Mostramos la tarjeta de nuevo si el drop no fue aceptado en otro lugar.
        # La lógica de actualización la manejará la ventana principal, que la borrará
        # y la creará en el nuevo lugar. Si el drop falla, simplemente reaparece.
        self.show()

class DropColumnWidget(QWidget):
    """
    Un QWidget que actúa como zona de destino (drop target).
    Emite una señal cuando una tarjeta es soltada sobre él.
    """
    # Señal que emitirá el ID del ticket y el nuevo estado de la columna
    card_dropped = Signal(str, str)

    def __init__(self, estado, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.estado = estado # El estado que esta columna representa
        
        # El layout interno para las tarjetas
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(10)

    def dragEnterEvent(self, event):
        """ Acepta el evento si contiene texto (nuestro ticket_id). """
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """ Se activa cuando la tarjeta es soltada. """
        ticket_id = event.mimeData().text()
        # Emitimos la señal para que la ventana principal maneje la lógica
        self.card_dropped.emit(ticket_id, self.estado)
        event.acceptProposedAction()

    def add_card(self, card):
        """ Método para añadir una tarjeta al layout de esta columna. """
        self.layout.addWidget(card)

    def clear(self):
        """ Limpia todas las tarjetas de la columna. """
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
