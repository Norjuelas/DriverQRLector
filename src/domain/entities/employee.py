"""
Entidad de Dominio: Empleado
No depende de ningún framework ni de infraestructura.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Employee:
    """Representa un empleado de la fábrica."""
    cedula: str
    nombre: str
    celular: str = ""
    correo: str = ""
    empleado_id: Optional[str] = None  # None hasta que sea persistido o generado

    def __post_init__(self):
        if not self.nombre:
            raise ValueError("El nombre del empleado no puede estar vacío.")
        if not self.cedula:
            raise ValueError("La cédula del empleado no puede estar vacía.")
        cedula_clean = self.cedula.replace(" ", "").replace("-", "")
        if not cedula_clean.isdigit() or not (6 <= len(cedula_clean) <= 12):
            raise ValueError("La cédula debe contener solo números (6–12 dígitos).")
        if self.correo and "@" not in self.correo:
            raise ValueError("El formato del correo electrónico no es válido.")
