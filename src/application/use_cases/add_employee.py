"""
Caso de Uso: Agregar Empleado

  1. Valida que la cédula no esté registrada.
  2. Construye la entidad Employee (la validación de formato ocurre en el constructor).
  3. Genera el ID único.
  4. Persiste el empleado.

Sin dependencias de UI.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Optional

from src.domain.entities.employee import Employee
from src.domain.repositories.employee_repository import EmployeeRepository


@dataclass
class AddEmployeeResult:
    success: bool
    employee: Optional[Employee] = None
    error_code: Optional[str] = None   # "DUPLICATE", "VALIDATION", "SAVE_ERROR"
    error_message: Optional[str] = None


class AddEmployeeUseCase:
    """Registra un nuevo empleado evitando duplicados por cédula."""

    def __init__(self, employee_repo: EmployeeRepository):
        self._repo = employee_repo

    def execute(
        self,
        nombre: str,
        cedula: str,
        celular: str = "",
        correo: str = "",
    ) -> AddEmployeeResult:
        """
        Args:
            nombre:   Nombre completo del empleado.
            cedula:   Número de identificación (6–12 dígitos).
            celular:  Número de celular (opcional).
            correo:   Correo electrónico (opcional).

        Returns:
            AddEmployeeResult con el resultado de la operación.
        """
        # 1. Verificar duplicado
        if self._repo.find_by_cedula(cedula) is not None:
            return AddEmployeeResult(
                success=False,
                error_code="DUPLICATE",
                error_message=f"Ya existe un empleado con cédula {cedula}.",
            )

        # 2. Construir entidad (validación de dominio en __post_init__)
        try:
            employee = Employee(
                cedula=cedula,
                nombre=nombre,
                celular=celular,
                correo=correo,
                empleado_id=self._generate_id(cedula),
            )
        except ValueError as exc:
            return AddEmployeeResult(
                success=False,
                error_code="VALIDATION",
                error_message=str(exc),
            )

        # 3. Persistir
        if not self._repo.save(employee):
            return AddEmployeeResult(
                success=False,
                error_code="SAVE_ERROR",
                error_message="No se pudo guardar el empleado en la base de datos.",
            )

        return AddEmployeeResult(success=True, employee=employee)

    @staticmethod
    def _generate_id(cedula: str) -> str:
        suffix = str(uuid.uuid4())[:4]
        return f"E{cedula[-4:]}{suffix}".upper()
