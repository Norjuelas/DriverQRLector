"""
Adaptador de Infraestructura: Repositorio SQLite para Vales.
Implementa VoucherRepository usando la tabla 'vales' de SQLite.
"""
import sqlite3
import time
import uuid
import datetime as dt
from typing import Dict, List, Optional, Tuple

from src.domain.entities.voucher import Voucher
from src.domain.repositories.voucher_repository import VoucherRepository
from db import get_conn

_VALID_VALE_COLUMNS = [
    "id_vale", "empleado_id", "codigo_serial_trabajo_asociado",
    "fecha_hora", "work_type_detected", "valor_pagado", "estado",
]


def _build_upsert_sql(table: str, pk: str, data: Dict, valid_cols) -> Tuple[str, Dict]:
    filtered = {k: v for k, v in data.items() if k in valid_cols}
    cols = ", ".join(filtered.keys())
    placeholders = ", ".join(f":{k}" for k in filtered.keys())
    updates = ", ".join(f"{k} = excluded.{k}" for k in filtered.keys() if k != pk)
    sql = (
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
        f"ON CONFLICT({pk}) DO UPDATE SET {updates}"
    )
    return sql, filtered


class SQLiteVoucherRepository(VoucherRepository):
    """Persiste Voucher en la tabla 'vales' de SQLite."""

    def save(self, voucher: Voucher) -> bool:
        try:
            data = {
                "id_vale": voucher.id_vale or f"V{int(time.time())}{str(uuid.uuid4())[:4]}",
                "empleado_id": voucher.empleado_id,
                "codigo_serial_trabajo_asociado": voucher.codigo_serial_trabajo_asociado,
                "fecha_hora": voucher.fecha_hora or dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "work_type_detected": voucher.work_type_detected,
                "valor_pagado": voucher.valor_pagado,
                "estado": voucher.estado,
            }
            sql, params = _build_upsert_sql("vales", "id_vale", data, _VALID_VALE_COLUMNS)
            with get_conn() as conn:
                with conn:
                    conn.execute(sql, params)
            return True
        except sqlite3.IntegrityError as exc:
            print(f"[SQLiteVoucherRepository.save] IntegrityError (duplicado?): {exc}")
            return False
        except sqlite3.Error as exc:
            print(f"[SQLiteVoucherRepository.save] Error: {exc}")
            return False

    def exists(self, codigo_serial_trabajo: str, empleado_id: str) -> bool:
        try:
            sql = (
                "SELECT EXISTS(SELECT 1 FROM vales "
                "WHERE codigo_serial_trabajo_asociado = ? AND empleado_id = ? LIMIT 1)"
            )
            with get_conn() as conn:
                result = conn.execute(sql, (codigo_serial_trabajo, empleado_id)).fetchone()
            return bool(result and result[0] == 1)
        except sqlite3.Error as exc:
            print(f"[SQLiteVoucherRepository.exists] Error: {exc}")
            return False

    def find_by_employee(self, empleado_id: str) -> List[Voucher]:
        try:
            sql = "SELECT * FROM vales WHERE empleado_id = ?"
            with get_conn() as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(sql, (empleado_id,)).fetchall()
            return [self._row_to_voucher(dict(r)) for r in rows]
        except sqlite3.Error as exc:
            print(f"[SQLiteVoucherRepository.find_by_employee] Error: {exc}")
            return []

    def delete_all(self) -> bool:
        try:
            with get_conn() as conn:
                with conn:
                    conn.execute("DELETE FROM vales")
            return True
        except sqlite3.Error as exc:
            print(f"[SQLiteVoucherRepository.delete_all] Error: {exc}")
            return False

    @staticmethod
    def _row_to_voucher(row: Dict) -> Voucher:
        return Voucher(
            id_vale=row.get("id_vale"),
            empleado_id=row.get("empleado_id", ""),
            codigo_serial_trabajo_asociado=row.get("codigo_serial_trabajo_asociado", ""),
            work_type_detected=row.get("work_type_detected", ""),
            valor_pagado=float(row.get("valor_pagado", 0)),
            fecha_hora=row.get("fecha_hora"),
            estado=row.get("estado", "pendiente"),
        )
