"""
Presentación PySide2: MainWindow (controlador delgado)

Esta clase es SOLO UI:
  - Lee inputs de los widgets.
  - Llama a los casos de uso con datos primitivos.
  - Interpreta el resultado y actualiza los widgets.

No contiene lógica de negocio. Si mañana se migra a Atom/Electron u otro
framework, solo se reemplaza este archivo manteniendo intactos dominio,
aplicación e infraestructura.
"""
from __future__ import annotations

import os
import traceback

from PySide2.QtCore import QSize, Qt
from PySide2.QtGui import QPixmap, QStandardItemModel
from PySide2 import QtGui, QtWidgets
from PySide2.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableView,
    QVBoxLayout,
)

from ui_main import Ui_MainWindow
from ui_styles import Style

from src.application.use_cases.create_work_order import CreateWorkOrderUseCase
from src.application.use_cases.scan_code import ScanCodeUseCase
from src.application.use_cases.add_employee import AddEmployeeUseCase
from src.application.use_cases.reset_database import ResetDatabaseUseCase
from config import CAMPOS_VALOR_TRABAJO_MAP, WORK_TYPE_ABBREVIATIONS

# Importamos las funciones de UI auxiliares del archivo original
from ui_main import Ui_MainWindow


class MainWindow(QMainWindow):
    """
    Controlador delgado de la ventana principal.
    Depende de los casos de uso mediante inyección de dependencias en __init__.
    """

    def __init__(
        self,
        create_work_order: CreateWorkOrderUseCase,
        scan_code: ScanCodeUseCase,
        add_employee: AddEmployeeUseCase,
        reset_database: ResetDatabaseUseCase,
    ):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dragPos = None

        # Inyección de casos de uso
        self._create_work_order = create_work_order
        self._scan_code = scan_code
        self._add_employee = add_employee
        self._reset_database = reset_database

        self._setup_table()
        self._connect_signals()
        self.show()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_table(self) -> None:
        """Configura la tabla de previsualización de vales escaneados."""
        if not hasattr(self.ui, "WidgetTabla"):
            return

        layout = self.ui.WidgetTabla.layout() or QVBoxLayout(self.ui.WidgetTabla)
        self.ui.WidgetTabla.setLayout(layout)

        if not hasattr(self.ui, "tableViewVale"):
            self.ui.tableViewVale = QTableView()
            layout.addWidget(self.ui.tableViewVale)
            self._table_model = QStandardItemModel()
            self.ui.tableViewVale.setModel(self._table_model)
        else:
            self._table_model = self.ui.tableViewVale.model() or QStandardItemModel()
            self.ui.tableViewVale.setModel(self._table_model)

        self._table_model.setHorizontalHeaderLabels([
            "Código Serial", "N° Ticket", "Referencia",
            "Tipo Trabajo", "Color", "Total Pares", "Valor Pagado",
        ])
        self.ui.tableViewVale.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _connect_signals(self) -> None:
        """Conecta todos los botones y eventos de la UI a sus handlers."""
        if hasattr(self.ui, "pushButtonGuardar"):
            self.ui.pushButtonGuardar.clicked.connect(self._on_save_clicked)

        if hasattr(self.ui, "codeReaderInput"):
            self.ui.codeReaderInput.returnPressed.connect(self._on_code_scanned)

        if hasattr(self.ui, "btnAgregarEmpleado"):
            self.ui.btnAgregarEmpleado.clicked.connect(self._on_add_employee_clicked)

        if hasattr(self.ui, "EliminarTODO"):
            self.ui.EliminarTODO.clicked.connect(self._on_reset_database_clicked)

        if hasattr(self.ui, "btnRegisterVale"):
            self.ui.btnRegisterVale.clicked.connect(self._on_register_vale_clicked)

    # ------------------------------------------------------------------
    # Handlers de UI — solo leen/escriben widgets y llaman casos de uso
    # ------------------------------------------------------------------

    def _on_save_clicked(self) -> None:
        """Recoge los datos del formulario y ejecuta CreateWorkOrderUseCase."""
        data = self._collect_form_data()
        if data is None:
            return

        result = self._create_work_order.execute(
            ticket_number=data["ticket_number"],
            referencia=data["referencia"],
            color=data["color"],
            tallas_cantidades=data["tallas_cantidades"],
            valores_trabajo=data["valores_trabajo"],
        )

        if not result.success:
            QMessageBox.critical(self, "Error", result.error_message or "Error desconocido.")
            return

        if result.first_qr_path:
            self._display_image(result.first_qr_path)

        QMessageBox.information(
            self,
            "Operación Exitosa",
            f"Vale doble generado.\n"
            f"Total Producido: {result.left_order.total_producido} unidades por tiquete.\n"
            f"PDF: {result.pdf_path}",
        )
        self._clear_form()

    def _on_code_scanned(self) -> None:
        """Lee el código escaneado y ejecuta ScanCodeUseCase."""
        scanned_code = self.ui.codeReaderInput.text().strip()
        empleado_id = (
            self.ui.EmpleadosBox.currentData()
            if hasattr(self.ui, "EmpleadosBox")
            else None
        )

        result = self._scan_code.execute(
            scanned_code=scanned_code,
            empleado_id=empleado_id or "",
        )

        if not result.success:
            QMessageBox.warning(self, "Error de Escaneo", result.error_message)
            if result.error_code == "NO_EMPLOYEE" and hasattr(self.ui, "EmpleadosBox"):
                self.ui.EmpleadosBox.setFocus()
            else:
                self.ui.codeReaderInput.clear()
                self.ui.codeReaderInput.setFocus()
            return

        # Agregar fila a la tabla de previsualización
        v = result.voucher
        wo = result.work_order
        row = [
            v.codigo_serial_trabajo_asociado,
            wo.ticket_number,
            wo.referencia,
            result.work_type_display,
            wo.color,
            str(wo.total_producido),
            f"{v.valor_pagado:.2f}",
        ]
        self._table_model.appendRow(
            [QtGui.QStandardItem(cell) for cell in row]
        )
        QMessageBox.information(
            self,
            "Vale Registrado",
            f"Vale para '{result.work_type_display}' registrado exitosamente.",
        )
        self.ui.codeReaderInput.clear()
        self.ui.codeReaderInput.setFocus()

    def _on_add_employee_clicked(self) -> None:
        """Recoge datos del formulario de empleado y ejecuta AddEmployeeUseCase."""
        nombre = self._get_field_text("Nombre_Empleado")
        cedula = self._get_field_text("Cedula_Empleado")
        celular = self._get_field_text("Celular_Empleado")
        correo = self._get_field_text("Correo_Empleado")

        result = self._add_employee.execute(
            nombre=nombre, cedula=cedula, celular=celular, correo=correo
        )

        if not result.success:
            QMessageBox.warning(self, "Error al Agregar Empleado", result.error_message)
            return

        emp = result.employee
        QMessageBox.information(
            self,
            "Empleado Agregado",
            f"Empleado: {emp.nombre}\nCédula: {emp.cedula}\nID: {emp.empleado_id}",
        )
        for field_name in ("Nombre_Empleado", "Cedula_Empleado", "Celular_Empleado", "Correo_Empleado"):
            widget = getattr(self.ui, field_name, None)
            if widget:
                widget.clear()

    def _on_reset_database_clicked(self) -> None:
        """Solicita confirmación y ejecuta ResetDatabaseUseCase con threading."""
        reply = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Está seguro de que desea eliminar toda la base de datos?\n\n"
            "Se creará un backup automáticamente antes de eliminar.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return

        self.ui.EliminarTODO.setEnabled(False)
        self.ui.EliminarTODO.setText("Procesando...")

        def progress(msg: str) -> None:
            self.ui.EliminarTODO.setText(msg)
            QApplication.processEvents()

        try:
            result = self._reset_database.execute(progress_callback=progress)
            if result.success:
                QMessageBox.information(
                    self,
                    "Completado",
                    f"Backup: {result.backup_path}\n"
                    + "\n".join(result.deleted_items),
                )
            else:
                QMessageBox.warning(self, "Advertencia", result.error_message)
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"Error durante la eliminación: {exc}")
        finally:
            self.ui.EliminarTODO.setEnabled(True)
            self.ui.EliminarTODO.setText("Eliminar TODO")

    def _on_register_vale_clicked(self) -> None:
        """Limpia la tabla y registra los vales escaneados en la sesión."""
        if not self._table_model or self._table_model.rowCount() == 0:
            QMessageBox.warning(self, "Sin Vales", "No hay vales pendientes para registrar.")
            return
        total = self._table_model.rowCount()
        self._table_model.removeRows(0, total)
        self._scan_code.clear_session()
        QMessageBox.information(
            self, "Vales Registrados",
            f"Se han limpiado {total} registros de la vista previa.",
        )

    # ------------------------------------------------------------------
    # Helpers de UI
    # ------------------------------------------------------------------

    def _collect_form_data(self) -> dict | None:
        """
        Lee y valida los datos del formulario de creación de tiquetes.
        Retorna un diccionario con los datos, o None si la validación falla.
        """
        referencia = self._get_field_text("CampoReferenciaTrabajo")
        ticket_number = self._get_field_text("CampoNumeroTicket")
        color = self._get_field_text("CampoColor")

        if not all([referencia, ticket_number, color]):
            QMessageBox.warning(
                self, "Campos Incompletos",
                "Los campos Referencia, Número de Ticket y Color son obligatorios.",
            )
            return None

        tallas_cantidades: dict = {}
        for i in range(33, 49):
            field = getattr(self.ui, f"CampoTalla_{i}", None)
            if field is None:
                continue
            text = field.text().strip()
            if not text:
                continue
            try:
                cant = int(text)
                if cant <= 0:
                    QMessageBox.warning(self, "Entrada Inválida", f"Talla {i}: debe ser un número positivo.")
                    field.setFocus()
                    return None
                tallas_cantidades[str(i)] = cant
            except ValueError:
                QMessageBox.warning(self, "Entrada Inválida", f"Talla {i}: ingrese un número válido.")
                field.setFocus()
                return None

        if not tallas_cantidades:
            QMessageBox.warning(self, "Campos Incompletos", "Debe ingresar cantidad para al menos una talla.")
            return None

        valores_trabajo: dict = {}
        for work_type, field_attr in CAMPOS_VALOR_TRABAJO_MAP.items():
            field = getattr(self.ui, field_attr, None)
            if field is None:
                QMessageBox.critical(self, "Error de UI", f"Campo '{field_attr}' no encontrado.")
                return None
            text = field.text().strip()
            if not text:
                QMessageBox.warning(self, "Campo Obligatorio", f"Ingrese un valor para '{work_type}'.")
                field.setFocus()
                return None
            try:
                valor = float(text.replace(",", "."))
                if valor <= 0:
                    QMessageBox.warning(self, "Entrada Inválida", f"Valor para '{work_type}' debe ser positivo.")
                    field.setFocus()
                    return None
                valores_trabajo[work_type] = valor
            except ValueError:
                QMessageBox.warning(self, "Entrada Inválida", f"Valor para '{work_type}': ingrese un número.")
                field.setFocus()
                return None

        return {
            "referencia": referencia,
            "ticket_number": ticket_number,
            "color": color,
            "tallas_cantidades": tallas_cantidades,
            "valores_trabajo": valores_trabajo,
        }

    def _clear_form(self) -> None:
        for name in ("CampoReferenciaTrabajo", "CampoNumeroTicket", "CampoColor"):
            widget = getattr(self.ui, name, None)
            if widget:
                widget.clear()
        for i in range(33, 49):
            widget = getattr(self.ui, f"CampoTalla_{i}", None)
            if widget:
                widget.clear()
        for field_attr in CAMPOS_VALOR_TRABAJO_MAP.values():
            widget = getattr(self.ui, field_attr, None)
            if widget:
                widget.clear()
        if hasattr(self.ui, "PreviwImage") and self.ui.PreviwImage.scene():
            self.ui.PreviwImage.scene().clear()
        if hasattr(self.ui, "CampoReferenciaTrabajo"):
            self.ui.CampoReferenciaTrabajo.setFocus()

    def _display_image(self, image_path: str) -> None:
        if not hasattr(self.ui, "PreviwImage"):
            return
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return
        scene = self.ui.PreviwImage.scene() or QGraphicsScene()
        self.ui.PreviwImage.setScene(scene)
        scene.clear()
        scene.addPixmap(pixmap)
        self.ui.PreviwImage.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)

    def _get_field_text(self, field_name: str) -> str:
        widget = getattr(self.ui, field_name, None)
        return widget.text().strip() if widget else ""
