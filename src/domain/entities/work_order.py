"""
Entidad de Dominio: Orden de Trabajo (Trabajo / Tiquete)
Contiene los datos de producción y los códigos seriales por etapa.
No depende de ningún framework ni de infraestructura.
"""
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class WorkOrder:
    """
    Representa una orden de trabajo completa.

    Cada orden tiene un número de tiquete, referencia, color, cantidades por talla
    y los valores monetarios y códigos seriales para cada etapa de producción.
    """
    ticket_number: str
    referencia: str
    color: str
    tallas_cantidades: Dict[str, int]           # {"33": 5, "34": 3, ...}
    valores_trabajo: Dict[str, float]           # {"corte": 1200.0, "guarnicion": 800.0, ...}
    serial_codes: Dict[str, str] = field(default_factory=dict)   # {"corte": "001-RE-CT-X-abc123", ...}
    codigo_serial: Optional[str] = None         # ID único de la orden en BD
    ruta_imagen: Optional[str] = None

    @property
    def total_producido(self) -> int:
        return sum(self.tallas_cantidades.values())

    def __post_init__(self):
        if not self.ticket_number:
            raise ValueError("El número de tiquete no puede estar vacío.")
        if not self.referencia:
            raise ValueError("La referencia no puede estar vacía.")
        if not self.color:
            raise ValueError("El color no puede estar vacío.")
        if not self.tallas_cantidades:
            raise ValueError("Debe ingresar cantidad para al menos una talla.")
        for talla, cant in self.tallas_cantidades.items():
            if cant <= 0:
                raise ValueError(f"La cantidad para talla {talla} debe ser positiva.")
        for tipo, valor in self.valores_trabajo.items():
            if valor <= 0:
                raise ValueError(f"El valor para '{tipo}' debe ser un número positivo.")
