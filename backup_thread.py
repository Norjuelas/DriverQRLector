"""
Utilidades para backup y eliminación de base de datos (Migrado a PySide2)
"""
import os
import sys
import shutil
import zipfile
from datetime import datetime
from PySide2.QtWidgets import QMessageBox, QApplication 
from PySide2.QtCore import QThread, Signal # Cambiado pyqtSignal a Signal


class BackupThread(QThread):
    """Thread para crear backup sin bloquear la UI"""
    # Cambio aquí: pyqtSignal a Signal
    finished = Signal(bool, str)  # success, message
    progress = Signal(str)  # progress message
    
    def __init__(self, excel_path, codes_dir):
        super().__init__()
        self.excel_path = excel_path
        self.codes_dir = codes_dir
        
    def run(self):
        try:
            # Crear nombre del backup con fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Determinar la ruta del backup en el directorio del script o ejecutable
            if getattr(sys, 'frozen', False):
                application_path = os.path.dirname(sys.executable)
            else:
                # __file__ podría no estar definido si se ejecuta en ciertos entornos interactivos,
                # pero es estándar para scripts.
                try:
                    application_path = os.path.dirname(os.path.abspath(__file__))
                except NameError: # En caso de que __file__ no esté definido
                    application_path = os.getcwd() # Usar el directorio de trabajo actual como fallback

            backup_folder = os.path.join(application_path, "backups_eliminados")
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            
            backup_name_with_path = os.path.join(backup_folder, f"version_eliminada_{timestamp}.zip")
            
            self.progress.emit("Creando archivo ZIP...")
            
            with zipfile.ZipFile(backup_name_with_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Agregar archivo Excel si existe
                if os.path.exists(self.excel_path):
                    self.progress.emit(f"Respaldando base de datos: {self.excel_path}...")
                    zipf.write(self.excel_path, os.path.basename(self.excel_path))
                
                # Agregar directorio codes si existe
                if os.path.exists(self.codes_dir):
                    self.progress.emit(f"Respaldando directorio de códigos: {self.codes_dir}...")
                    files_list = []
                    for root, dirs, files in os.walk(self.codes_dir):
                        for file in files:
                            files_list.append(os.path.join(root, file))
                    
                    total_files = len(files_list)
                    if total_files == 0:
                        self.progress.emit("Directorio de códigos está vacío, nada que respaldar de allí.")
                    else:
                        for i, file_path in enumerate(files_list):
                            # Crear un path relativo dentro del zip para la carpeta codes
                            # Por ejemplo, si codes_dir es '.../app/codes', y file_path es '.../app/codes/img/code1.png',
                            # arcname será 'codes/img/code1.png'
                            arcname = os.path.relpath(file_path, os.path.dirname(self.codes_dir))
                            zipf.write(file_path, arcname)
                            
                            if i % 10 == 0 or i == total_files - 1:
                                self.progress.emit(f"Respaldando códigos... {i+1}/{total_files}")
            
            self.finished.emit(True, f"Backup creado con éxito en: {backup_name_with_path}")
            
        except Exception as e:
            self.finished.emit(False, f"Error al crear backup: {str(e)}")


class BackupManager:
    """Clase para manejar operaciones de backup de forma estática"""
    
    @staticmethod
    def get_paths():
        """Obtiene las rutas del Excel y directorio codes"""
        # Definir la ruta base de la aplicación
        if getattr(sys, 'frozen', False): # Si la aplicación está empaquetada (ej. PyInstaller)
            application_path = os.path.dirname(sys.executable)
        else: # Si se ejecuta como script .py
            try:
                # __file__ es la ruta del script actual.
                application_path = os.path.dirname(os.path.abspath(__file__))
            except NameError: # Fallback si __file__ no está definido (ej. en algunos REPLs)
                 application_path = os.getcwd()

        excel_path = os.path.join(application_path, "trabajos_database.xlsx")
        codes_dir = os.path.join(application_path, "codes")
        
        return excel_path, codes_dir
    
    @staticmethod
    def check_files_exist(excel_path, codes_dir):
        """Verifica si existen archivos para respaldar usando get_paths"""
        excel_exists = os.path.exists(excel_path)
        
        codes_content_exists = False
        if os.path.exists(codes_dir) and os.path.isdir(codes_dir):
            if len(os.listdir(codes_dir)) > 0: # Verifica si el directorio no está vacío
                 codes_content_exists = True
        
        return excel_exists or codes_content_exists, excel_exists, codes_content_exists
    
    @staticmethod
    def create_backup_sync(excel_path, codes_dir,progress_callback=None):
        """Crea backup de forma síncrona (puede bloquear UI)"""
        
        # Verificar si hay algo que respaldar
        can_backup, excel_exists, codes_exist = BackupManager.check_files_exist()
        if not can_backup:
            if progress_callback:
                progress_callback("No hay archivos (Excel o directorio 'codes' con contenido) para respaldar.")
            return None # O lanzar una excepción, o devolver un mensaje indicando que no hay nada

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ruta base para guardar backups
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            try:
                application_path = os.path.dirname(os.path.abspath(__file__))
            except NameError:
                application_path = os.getcwd()

        backup_folder = os.path.join(application_path, "backups_eliminados")
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)
            if progress_callback:
                progress_callback(f"Carpeta de backups creada en: {backup_folder}")

        backup_name = f"version_eliminada_{timestamp}.zip"
        backup_name_with_path = os.path.join(backup_folder, backup_name)
        
        if progress_callback:
            progress_callback(f"Iniciando creación de backup: {backup_name_with_path}")

        with zipfile.ZipFile(backup_name_with_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if excel_exists: # Usar la variable de check_files_exist
                if progress_callback:
                    progress_callback(f"Respaldando base de datos: {excel_path}...")
                zipf.write(excel_path, os.path.basename(excel_path))
            
            if codes_exist: # Usar la variable de check_files_exist
                if progress_callback:
                    progress_callback(f"Respaldando directorio de códigos: {codes_dir}...")
                
                files_list = []
                for root, dirs, files in os.walk(codes_dir):
                    for file in files:
                        files_list.append(os.path.join(root, file))
                
                total_files = len(files_list)
                if total_files == 0:
                    if progress_callback:
                        progress_callback("Directorio de códigos está vacío.")
                else:
                    for i, file_path in enumerate(files_list):
                        arcname = os.path.relpath(file_path, os.path.dirname(codes_dir))
                        zipf.write(file_path, arcname)
                        
                        if progress_callback and (i % 10 == 0 or i == total_files - 1):
                            progress_callback(f"Respaldando códigos... {i+1}/{total_files}")
        
        if progress_callback:
            progress_callback(f"Backup síncrono completado: {backup_name_with_path}")
        return backup_name_with_path
    
    @staticmethod
    def delete_files(excel_path, codes_dir):
        """Elimina los archivos Excel y el directorio codes"""
        deleted_items_info = []
        
        if os.path.exists(excel_path):
            try:
                os.remove(excel_path)
                deleted_items_info.append(f"Archivo Excel eliminado: {excel_path}")
            except Exception as e:
                deleted_items_info.append(f"Error al eliminar Excel {excel_path}: {e}")
        else:
            deleted_items_info.append(f"Archivo Excel no encontrado en {excel_path}, no se eliminó.")
            
        if os.path.exists(codes_dir):
            try:
                shutil.rmtree(codes_dir)
                deleted_items_info.append(f"Directorio de códigos eliminado: {codes_dir}")
            except Exception as e:
                deleted_items_info.append(f"Error al eliminar directorio {codes_dir}: {e}")
        else:
            deleted_items_info.append(f"Directorio de códigos no encontrado en {codes_dir}, no se eliminó.")
            
        return deleted_items_info