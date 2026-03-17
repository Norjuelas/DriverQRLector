"""
Bootstrap / Composición de Dependencias.

Este es el único lugar del proyecto donde las capas se conectan entre sí.
Para migrar a Electron/Atom u otro framework:
  1. Mantén dominio, aplicación e infraestructura tal como están.
  2. Crea una nueva carpeta en src/presentation/<nuevo_framework>/.
  3. En bootstrap.py, instancia el nuevo controlador en lugar de MainWindow.

Para cambiar la base de datos (ej. PostgreSQL, Firebase):
  1. Crea nuevas implementaciones de repositorio en src/infrastructure/persistence/.
  2. Actualiza solo las 3 líneas de repo_* que hay abajo.
"""
import sys

from PySide2.QtWidgets import QApplication

from db import init_db

# --- Infraestructura ---
from src.infrastructure.persistence.sqlite_work_order_repo import SQLiteWorkOrderRepository
from src.infrastructure.persistence.sqlite_voucher_repo import SQLiteVoucherRepository
from src.infrastructure.persistence.sqlite_employee_repo import SQLiteEmployeeRepository
from src.infrastructure.code_generation.qr_code_generator import QRCodeGenerator
from src.infrastructure.pdf.reportlab_pdf_generator import ReportLabPdfGenerator
from src.infrastructure.backup.zip_backup_service import ZipBackupService

# --- Casos de Uso ---
from src.application.use_cases.create_work_order import CreateWorkOrderUseCase
from src.application.use_cases.scan_code import ScanCodeUseCase
from src.application.use_cases.add_employee import AddEmployeeUseCase
from src.application.use_cases.reset_database import ResetDatabaseUseCase

# --- Presentación ---
from src.presentation.pyside2.main_window import MainWindow


def create_app() -> QApplication:
    """
    Construye toda la cadena de dependencias y retorna la aplicación lista para ejecutarse.
    """
    init_db()

    # Repositorios (puertos de dominio implementados en infraestructura)
    work_order_repo = SQLiteWorkOrderRepository()
    voucher_repo = SQLiteVoucherRepository()
    employee_repo = SQLiteEmployeeRepository()

    # Servicios de infraestructura
    code_generator = QRCodeGenerator()
    pdf_generator = ReportLabPdfGenerator()
    backup_service = ZipBackupService()

    # Casos de uso (inyección de dependencias)
    create_work_order_uc = CreateWorkOrderUseCase(
        work_order_repo=work_order_repo,
        code_generator=code_generator,
        pdf_generator=pdf_generator,
    )
    scan_code_uc = ScanCodeUseCase(
        work_order_repo=work_order_repo,
        voucher_repo=voucher_repo,
    )
    add_employee_uc = AddEmployeeUseCase(employee_repo=employee_repo)
    reset_database_uc = ResetDatabaseUseCase(backup_service=backup_service)

    # Aplicación Qt
    app = QApplication.instance() or QApplication(sys.argv)

    # Controlador delgado de UI (recibe casos de uso, no infraestructura directa)
    _window = MainWindow(
        create_work_order=create_work_order_uc,
        scan_code=scan_code_uc,
        add_employee=add_employee_uc,
        reset_database=reset_database_uc,
    )

    return app
