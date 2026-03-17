"""
Adaptador de Infraestructura: Repositorio SQLite para Órdenes de Trabajo.
Implementa WorkOrderRepository usando la base de datos SQLite existente (dao.py / db.py).
"""
import sqlite3
from typing import Dict, Optional, Tuple

from src.domain.entities.work_order import WorkOrder
from src.domain.repositories.work_order_repository import WorkOrderRepository
from config import WORK_TYPE_IDS
from db import get_conn

# Lista blanca de columnas (reutilizada del dao.py original)
_VALID_TRABAJO_COLUMNS = [
    "codigo_serial", "numero_ticket", "referencia", "color", "total_producido", "ruta_imagen",
    "cant_t33", "cant_t34", "cant_t35", "cant_t36", "cant_t37", "cant_t38", "cant_t39",
    "cant_t40", "cant_t41", "cant_t42", "cant_t43", "cant_t44", "cant_t45", "cant_t46",
    "cant_t47", "cant_t48", "valor_corte", "valor_guarnicion", "valor_montar",
    "valor_engrudar", "valor_alist_ensuelado", "valor_ensuelado", "valor_plantillas_terry",
    "valor_empaque", "codigo_corte", "codigo_guarnicion", "codigo_montar", "codigo_engrudar",
    "codigo_alist_ensuelado", "codigo_ensuelado", "codigo_plantillas_terry", "codigo_empaque",
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


class SQLiteWorkOrderRepository(WorkOrderRepository):
    """Persiste WorkOrder en la tabla 'trabajos' de SQLite."""

    def save(self, work_order: WorkOrder) -> bool:
        try:
            data: Dict = {
                "codigo_serial": work_order.codigo_serial,
                "numero_ticket": work_order.ticket_number,
                "referencia": work_order.referencia,
                "color": work_order.color,
                "total_producido": work_order.total_producido,
            }
            # Cantidades por talla
            for i in range(33, 49):
                data[f"cant_t{i}"] = work_order.tallas_cantidades.get(str(i), 0)

            # Valores por tipo de trabajo
            for work_type, value in work_order.valores_trabajo.items():
                col = f"valor_{work_type.lower().replace(' ', '_')}"
                if col in _VALID_TRABAJO_COLUMNS:
                    data[col] = value

            # Códigos seriales por tipo de trabajo
            for work_type, code in work_order.serial_codes.items():
                col = f"codigo_{work_type.lower().replace(' ', '_')}"
                if col in _VALID_TRABAJO_COLUMNS:
                    data[col] = code

            sql, params = _build_upsert_sql("trabajos", "codigo_serial", data, _VALID_TRABAJO_COLUMNS)
            with get_conn() as conn:
                with conn:
                    conn.execute(sql, params)
            return True
        except sqlite3.Error as exc:
            print(f"[SQLiteWorkOrderRepository.save] Error: {exc}")
            return False

    def find_by_stage_code(self, stage_code: str) -> Optional[Tuple[WorkOrder, str]]:
        try:
            case_stmt = " ".join(
                f"WHEN codigo_{wt_id} = :codigo THEN '{wt_id}'" for wt_id in WORK_TYPE_IDS
            )
            where_clauses = " OR ".join(f"codigo_{wt_id} = :codigo" for wt_id in WORK_TYPE_IDS)
            sql = f"""
                SELECT *, CASE {case_stmt} ELSE 'desconocido' END AS work_type_found
                FROM trabajos
                WHERE {where_clauses}
                LIMIT 1
            """
            with get_conn() as conn:
                conn.row_factory = sqlite3.Row
                row = conn.execute(sql, {"codigo": stage_code}).fetchone()

            if not row:
                return None

            row_dict = dict(row)
            work_type_id = row_dict.pop("work_type_found")

            tallas = {
                str(i): row_dict.get(f"cant_t{i}", 0) for i in range(33, 49)
                if row_dict.get(f"cant_t{i}", 0)
            }
            valores = {}
            for wt_id in WORK_TYPE_IDS:
                val = row_dict.get(f"valor_{wt_id}")
                if val is not None:
                    valores[wt_id] = float(val)

            serial_codes = {}
            for wt_id in WORK_TYPE_IDS:
                code = row_dict.get(f"codigo_{wt_id}")
                if code:
                    serial_codes[wt_id] = code

            order = WorkOrder(
                ticket_number=str(row_dict.get("numero_ticket", "")),
                referencia=str(row_dict.get("referencia", "")),
                color=str(row_dict.get("color", "")),
                tallas_cantidades=tallas,
                valores_trabajo=valores,
                serial_codes=serial_codes,
                codigo_serial=str(row_dict.get("codigo_serial", "")),
            )
            return order, work_type_id

        except sqlite3.Error as exc:
            print(f"[SQLiteWorkOrderRepository.find_by_stage_code] Error: {exc}")
            return None

    def delete_all(self) -> bool:
        try:
            with get_conn() as conn:
                with conn:
                    conn.execute("DELETE FROM trabajos")
            return True
        except sqlite3.Error as exc:
            print(f"[SQLiteWorkOrderRepository.delete_all] Error: {exc}")
            return False
