"""
Utilidades para backup y eliminación de base de datos
"""
import os
import sys
import shutil
import zipfile
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QThread, pyqtSignal


class BackupThread(QThread):
    """Thread para crear backup sin bloquear la UI"""
    finished = pyqtSignal(bool, str)  # success, message
    progress = pyqtSignal(str)  # progress message
    
    def __init__(self, excel_path, codes_dir):
        super().__init__()
        self.excel_path = excel_path
        self.codes_dir = codes_dir
        
    def run(self):
        try:
            # Crear nombre del backup con fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"version_eliminada_{timestamp}.zip"
            
            self.progress.emit("Creando archivo ZIP...")
            
            with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Agregar archivo Excel si existe
                if os.path.exists(self.excel_path):
                    self.progress.emit("Respaldando base de datos...")
                    zipf.write(self.excel_path, os.path.basename(self.excel_path))
                
                # Agregar directorio codes si existe
                if os.path.exists(self.codes_dir):
                    self.progress.emit("Respaldando códigos...")
                    files_list = []
                    for root, dirs, files in os.walk(self.codes_dir):
                        for file in files:
                            files_list.append(os.path.join(root, file))
                    
                    total_files = len(files_list)
                    for i, file_path in enumerate(files_list):
                        arcname = os.path.relpath(file_path, os.path.dirname(self.codes_dir))
                        zipf.write(file_path, arcname)
                        
                        if i % 10 == 0 or i == total_files - 1:
                            self.progress.emit(f"Respaldando códigos... {i+1}/{total_files}")
            
            self.finished.emit(True, f"Backup creado: {backup_name}")
            
        except Exception as e:
            self.finished.emit(False, f"Error al crear backup: {str(e)}")


class BackupManager:
    """Clase para manejar operaciones de backup de forma estática"""
    
    @staticmethod
    def get_paths():
        """Obtiene las rutas del Excel y directorio codes"""
        excel_path = "trabajos_database.xlsx"
        
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        codes_dir = os.path.join(application_path, "codes")
        
        return excel_path, codes_dir
    
    @staticmethod
    def check_files_exist(excel_path, codes_dir):
        """Verifica si existen archivos para respaldar"""
        excel_exists = os.path.exists(excel_path)
        codes_exists = os.path.exists(codes_dir) and bool(os.listdir(codes_dir)) if os.path.exists(codes_dir) else False
        return excel_exists or codes_exists, excel_exists, codes_exists
    
    @staticmethod
    def create_backup_sync(excel_path, codes_dir, progress_callback=None):
        """Crea backup de forma síncrona (puede bloquear UI)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"version_eliminada_{timestamp}.zip"
        
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if os.path.exists(excel_path):
                if progress_callback:
                    progress_callback("Respaldando base de datos...")
                zipf.write(excel_path, os.path.basename(excel_path))
            
            if os.path.exists(codes_dir):
                if progress_callback:
                    progress_callback("Respaldando códigos...")
                
                files_list = []
                for root, dirs, files in os.walk(codes_dir):
                    for file in files:
                        files_list.append(os.path.join(root, file))
                
                total_files = len(files_list)
                for i, file_path in enumerate(files_list):
                    arcname = os.path.relpath(file_path, os.path.dirname(codes_dir))
                    zipf.write(file_path, arcname)
                    
                    if progress_callback and (i % 10 == 0 or i == total_files - 1):
                        progress_callback(f"Respaldando códigos... {i+1}/{total_files}")
        
        return backup_name
    
    @staticmethod
    def delete_files(excel_path, codes_dir):
        """Elimina los archivos especificados"""
        deleted_files = []
        
        if os.path.exists(excel_path):
            os.remove(excel_path)
            deleted_files.append("Base de datos Excel")
        
        if os.path.exists(codes_dir):
            shutil.rmtree(codes_dir)
            deleted_files.append("Directorio de códigos")
        
        return deleted_files