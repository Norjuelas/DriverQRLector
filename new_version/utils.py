
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMessageBox, QGraphicsScene
from PySide2.QtCore import Qt

def validate_cedula(cedula):
    """Valida que la cédula tenga formato correcto"""
    # Remover espacios y guiones
    cedula_clean = cedula.replace(" ", "").replace("-", "")
    
    # Verificar que solo contenga números y tenga longitud apropiada
    if not cedula_clean.isdigit() or len(cedula_clean) < 6 or len(cedula_clean) > 12:
        return False
    
    return True

def display_code_image(ui,image_path):
    """Display the code image in the QGraphicsView"""
    try:
        if not hasattr(ui, 'PreviwImage'):
            print("Error: PreviwImage not found in UI")
            return False
            
        # Load image
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: No se pudo cargar la imagen en {image_path}")
            return False
        
        # Get scene from QGraphicsView
        scene = ui.PreviwImage.scene()
        if scene is None:
            scene = QGraphicsScene()
            ui.PreviwImage.setScene(scene)
        else:
            scene.clear()
        
        # Add image to scene
        scene.addPixmap(pixmap)
        
        # Fit view
        ui.PreviwImage.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)
        
        return True
    except Exception as e:
        print(f"Error al mostrar la imagen: {str(e)}")
        QMessageBox.critical("Error", f"Error al mostrar la imagen: {str(e)}")
        return False