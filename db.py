# db.py
import os, sys, sqlite3

def app_dir():
    # Soporta ejecución normal y empaquetada (PyInstaller)
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(app_dir(), "app.db")
SCHEMA_PATH = os.path.join(app_dir(), "schema.sql")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    print(f"Inicializando base de datos en: {DB_PATH}")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        ddl = f.read()
    with get_conn() as c:
        for stmt in [s.strip() for s in ddl.split(";") if s.strip()]:
            c.execute(stmt)
