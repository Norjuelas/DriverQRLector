"""
Adaptador de Infraestructura: Repositorio SQLite para Empleados.
Implementa EmployeeRepository usando la tabla 'empleados' de SQLite.
"""
import sqlite3
from typing import Dict, List, Optional

from src.domain.entities.employee import Employee
from src.domain.repositories.employee_repository import EmployeeRepository
from db import get_conn


class SQLiteEmployeeRepository(EmployeeRepository):
    """Persiste Employee en la tabla 'empleados' de SQLite."""

    def save(self, employee: Employee) -> bool:
        try:
            sql = """
                INSERT INTO empleados (empleado_id, nombre, cedula, celular, correo)
                VALUES (:empleado_id, :nombre, :cedula, :celular, :correo)
                ON CONFLICT(empleado_id) DO UPDATE SET
                    nombre   = excluded.nombre,
                    cedula   = excluded.cedula,
                    celular  = excluded.celular,
                    correo   = excluded.correo
            """
            with get_conn() as conn:
                with conn:
                    conn.execute(sql, {
                        "empleado_id": employee.empleado_id,
                        "nombre": employee.nombre,
                        "cedula": employee.cedula,
                        "celular": employee.celular,
                        "correo": employee.correo,
                    })
            return True
        except sqlite3.IntegrityError as exc:
            print(f"[SQLiteEmployeeRepository.save] IntegrityError (duplicado?): {exc}")
            return False
        except sqlite3.Error as exc:
            print(f"[SQLiteEmployeeRepository.save] Error: {exc}")
            return False

    def find_by_cedula(self, cedula: str) -> Optional[Employee]:
        try:
            sql = "SELECT * FROM empleados WHERE cedula = ? LIMIT 1"
            with get_conn() as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(sql, (cedula,)).fetchone()
            return self._row_to_employee(dict(row)) if row else None
        except sqlite3.Error as exc:
            print(f"[SQLiteEmployeeRepository.find_by_cedula] Error: {exc}")
            return None

    def find_all(self) -> List[Employee]:
        try:
            sql = "SELECT * FROM empleados ORDER BY nombre"
            with get_conn() as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(sql).fetchall()
            return [self._row_to_employee(dict(r)) for r in rows]
        except sqlite3.Error as exc:
            print(f"[SQLiteEmployeeRepository.find_all] Error: {exc}")
            return []

    def delete_all(self) -> bool:
        try:
            with get_conn() as conn:
                with conn:
                    conn.execute("DELETE FROM empleados")
            return True
        except sqlite3.Error as exc:
            print(f"[SQLiteEmployeeRepository.delete_all] Error: {exc}")
            return False

    @staticmethod
    def _row_to_employee(row: Dict) -> Employee:
        return Employee(
            empleado_id=row.get("empleado_id"),
            nombre=row.get("nombre", ""),
            cedula=row.get("cedula", ""),
            celular=row.get("celular", ""),
            correo=row.get("correo", ""),
        )
