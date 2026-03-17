"""
Entidad de Dominio: Vale de Trabajo
Registra que un empleado completó una etapa de una orden de trabajo.
No depende de ningún framework ni de infraestructura.
"""
from dataclasses import dataclass, field
from typing import Optional
import datetime


@dataclass
class Voucher:
    """
    Representa el vale que acredita el trabajo de un empleado
    en una etapa específica de una orden de trabajo.
    """
    empleado_id: str
    codigo_serial_trabajo_asociado: str
    work_type_detected: str      # Nombre de display, ej. "Corte"
    valor_pagado: float
    id_vale: Optional[str] = None
    fecha_hora: Optional[str] = None
    estado: str = "pendiente"

    def __post_init__(self):
        if not self.empleado_id:
            raise ValueError("El empleado_id no puede estar vacío.")
        if not self.codigo_serial_trabajo_asociado:
            raise ValueError("El código serial del trabajo no puede estar vacío.")
        if not self.work_type_detected:
            raise ValueError("El tipo de trabajo no puede estar vacío.")
        if self.valor_pagado < 0:
            raise ValueError("El valor pagado no puede ser negativo.")
