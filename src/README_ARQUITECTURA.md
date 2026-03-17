# Clean Architecture — DriverQRLector

## Estructura del proyecto

```
src/
├── domain/                          # Reglas de Negocio Empresariales
│   ├── entities/                    # Objetos del dominio (sin dependencias)
│   │   ├── employee.py              #   Empleado
│   │   ├── work_order.py            #   Orden de Trabajo (Tiquete)
│   │   └── voucher.py               #   Vale de Trabajo
│   └── repositories/                # Puertos de entrada (interfaces abstractas)
│       ├── work_order_repository.py
│       ├── voucher_repository.py
│       └── employee_repository.py
│
├── application/                     # Reglas de Negocio de la Aplicación
│   ├── ports/                       # Puertos de salida (interfaces para infra)
│   │   ├── code_generator_port.py
│   │   ├── pdf_generator_port.py
│   │   └── backup_service_port.py
│   └── use_cases/                   # Casos de Uso (orquestadores)
│       ├── create_work_order.py     #   Crear tiquete doble + PDF + QR
│       ├── scan_code.py             #   Escanear código → crear vale
│       ├── add_employee.py          #   Registrar empleado
│       └── reset_database.py        #   Backup + borrar datos
│
├── infrastructure/                  # Adaptadores (implementan los puertos)
│   ├── persistence/
│   │   ├── sqlite_work_order_repo.py
│   │   ├── sqlite_voucher_repo.py
│   │   └── sqlite_employee_repo.py
│   ├── code_generation/
│   │   └── qr_code_generator.py     #   qrcode library
│   ├── pdf/
│   │   └── reportlab_pdf_generator.py  # reportlab / generate_pdf.py
│   └── backup/
│       └── zip_backup_service.py    #   zipfile + shutil
│
├── presentation/                    # Interfaz de usuario (intercambiable)
│   └── pyside2/
│       └── main_window.py           #   Controlador delgado PySide2
│
├── bootstrap.py                     # Composición de dependencias (único lugar)
└── main.py                          # Punto de entrada
```

## Reglas de dependencia

```
presentation  →  application  →  domain
infrastructure  →  application  →  domain
```

- **domain**: Python puro, cero imports externos.
- **application**: depende solo de `domain` y define los puertos.
- **infrastructure**: implementa los puertos; puede usar SQLite, qrcode, reportlab, etc.
- **presentation**: usa los casos de uso mediante inyección de dependencias.
- **bootstrap.py**: el único lugar donde todas las capas se conectan.

## Migrar la UI a Atom / Electron / otro framework

1. Crea `src/presentation/<nuevo_framework>/main_window.py`.
2. Implementa la misma interfaz de llamadas a los casos de uso.
3. En `bootstrap.py`, cambia la línea que instancia `MainWindow`.

No toques dominio, aplicación ni infraestructura.

## Cambiar la base de datos (SQLite → PostgreSQL, Firebase, etc.)

1. Crea nuevas implementaciones en `src/infrastructure/persistence/`.
2. En `bootstrap.py`, sustituye las 3 líneas de `*_repo = SQLite*`.

## Añadir un nuevo Caso de Uso

1. Crea el archivo en `src/application/use_cases/`.
2. Si necesita un servicio externo nuevo, define el puerto en `src/application/ports/`.
3. Implementa el adaptador en `src/infrastructure/`.
4. Registra en `bootstrap.py`.
5. Conecta al handler de UI en `src/presentation/pyside2/main_window.py`.
