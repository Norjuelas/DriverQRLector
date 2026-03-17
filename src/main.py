"""
Nuevo punto de entrada de la aplicación (Clean Architecture).
El main.py original queda intacto para no romper nada mientras la migración
se completa de forma incremental.
"""
import sys
from src.bootstrap import create_app

if __name__ == "__main__":
    app = create_app()
    sys.exit(app.exec_())
