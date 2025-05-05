from cx_Freeze import setup, Executable
import os
import sys

# Asegura que se usa el GUI base solo en Windows
base = "Win32GUI" if sys.platform == "win64" else None

# Archivos y carpetas que deseas incluir
include_files = [
    ("app/fonts", "app/fonts"),
    ("app/icons", "app/icons"),
    ("trabajos_database.xlsx", "trabajos_database.xlsx"),
    ("app/GUI_BASE.ui", "app/GUI_BASE.ui"),
    ("app/GenerarCodigos.ui", "app/GenerarCodigos.ui")
]

# Opciones de compilación
build_exe_options = {
    "packages": ["os", "PyQt5"],
    "excludes": [],
    "include_files": include_files,
    "include_msvcr": True  # Incluye runtime de MSVC si es necesario
}

# Ejecutable principal
executables = [
    Executable("app/main.py", base=base, target_name="DriverQRLector.exe", icon=None)
]

# Setup final
setup(
    name="DriverQRLector",
    version="1.0",
    description="Lector y generador de QR para tareas y productos",
    options={"build_exe": build_exe_options},
    executables=executables
)
