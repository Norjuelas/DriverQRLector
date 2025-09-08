#dao.py
import sqlite3
import os
import datetime as dt
# En dao.py (añadir estas funciones y dependencias)

import time
import uuid
from typing import Dict, Any, List, Tuple, Optional
from config import WORK_TYPE_IDS 


# Asumimos que esta constante está definida en algún lugar central

# Asumimos que tienes estas dependencias y configuraciones en otros archivos
from db import get_conn  # Tu módulo para obtener la conexión a la BD
# from my_utils import display_code_image, increment_ticket_number, generate_serial_code, WORK_TYPE_ABBREVIATIONS, generar_vales_pdf

# --- Columnas Válidas para Evitar Inyección SQL ---
# Lista blanca de columnas permitidas para cada tabla.
VALID_TRABAJO_COLUMNS = [
    'codigo_serial', 'numero_ticket', 'referencia', 'color', 'total_producido', 'ruta_imagen',
    'cant_t33', 'cant_t34', 'cant_t35', 'cant_t36', 'cant_t37', 'cant_t38', 'cant_t39',
    'cant_t40', 'cant_t41', 'cant_t42', 'cant_t43', 'cant_t44', 'cant_t45', 'cant_t46',
    'cant_t47', 'cant_t48', 'valor_corte', 'valor_guarnicion', 'valor_montar',
    'valor_engrudar', 'valor_alist_ensuelado', 'valor_ensuelado', 'valor_plantillas_terry',
    'valor_empaque', 'codigo_corte', 'codigo_guarnicion', 'codigo_montar', 'codigo_engrudar',
    'codigo_alist_ensuelado', 'codigo_ensuelado', 'codigo_plantillas_terry', 'codigo_empaque'
]

VALID_VALE_COLUMNS = [
    'id_vale', 'empleado_id', 'codigo_serial_trabajo_asociado', 'fecha_hora',
    'work_type_detected', 'valor_pagado', 'estado'
]


def _build_upsert_sql(table: str, pk: str, data: Dict[str, Any], valid_cols: List[str]) -> Tuple[str, Dict[str, Any]]:
    """
    Construye una sentencia SQL de tipo INSERT ... ON CONFLICT (UPSERT) de forma segura.

    Valida las columnas contra una lista blanca para prevenir inyección SQL.

    Args:
        table (str): El nombre de la tabla.
        pk (str): El nombre de la columna que es clave primaria.
        data (Dict[str, Any]): El diccionario con los datos a insertar/actualizar.
        valid_cols (List[str]): La lista de columnas permitidas para la tabla.

    Returns:
        Tuple[str, Dict[str, Any]]: Una tupla con la sentencia SQL y el diccionario
                                     de parámetros filtrado y listo para ejecutar.
    """
    # 1. Filtrar solo los datos que corresponden a columnas válidas
    filtered_data = {k: v for k, v in data.items() if k in valid_cols}
    
    # 2. Construir las partes de la sentencia SQL
    cols = ", ".join(filtered_data.keys())
    
    # --- LÍNEA CORREGIDA ---
    # Crea placeholders nombrados como :columna1, :columna2, etc.
    placeholders = ", ".join([f":{k}" for k in filtered_data.keys()])
    
    # 3. Construir la parte de la actualización (UPDATE)
    update_cols = [f"{k} = excluded.{k}" for k in filtered_data.keys() if k != pk]
    assignments = ", ".join(update_cols)
    
    # 4. Ensamblar la sentencia SQL final
    sql = (f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
           f"ON CONFLICT({pk}) DO UPDATE SET {assignments}")
           
    return sql, filtered_data

def guardar_o_actualizar_trabajo(data_to_save: Dict[str, Any]) -> bool:
    """
    Guarda o actualiza un registro en la tabla 'trabajos' de forma atómica.

    Esta función mapea el diccionario de datos de la aplicación a las columnas
    de la tabla 'trabajos' y ejecuta una operación de tipo "UPSERT" (INSERT ON CONFLICT).

    Args:
        data_to_save (dict): Diccionario con todos los datos del tiquete a guardar.
                             Debe contener llaves como 'id_vale_unico', 'ticket_number',
                             'tallas_cantidades', 'valores_trabajo', 'serial_codes', etc.

    Returns:
        bool: True si la operación fue exitosa, False en caso contrario.
    """
    try:
        # 1. Mapear el diccionario de entrada a los nombres de las columnas de la BD.
        #    Este es el "traductor" entre tu lógica de aplicación y el esquema de la BD.
        datos_trabajo = {
            'codigo_serial': data_to_save.get('id_vale_unico'),
            'numero_ticket': data_to_save.get('ticket_number'),
            'referencia': data_to_save.get('referencia'),
            'color': data_to_save.get('color'),
            'total_producido': data_to_save.get('total_producido')
        }

        # Añadir cantidades por talla (cant_t33, cant_t34, ...)
        for i in range(33, 49):
            talla_str = str(i)
            col_name = f'cant_t{talla_str}'
            datos_trabajo[col_name] = data_to_save.get('tallas_cantidades', {}).get(talla_str, 0)

        # Añadir valores por tipo de trabajo (valor_corte, valor_guarnicion, ...)
        for work_type, value in data_to_save.get('valores_trabajo', {}).items():
            col_name = f'valor_{work_type.lower().replace(" ", "_")}'
            if col_name in VALID_TRABAJO_COLUMNS:
                datos_trabajo[col_name] = value

        # Añadir códigos seriales por tipo de trabajo (codigo_corte, ...)
        for work_type, code in data_to_save.get('serial_codes', {}).items():
            col_name = f'codigo_{work_type.lower().replace(" ", "_")}'
            if col_name in VALID_TRABAJO_COLUMNS:
                datos_trabajo[col_name] = code

        # 2. Usar una transacción para garantizar la atomicidad de la operación.
        with get_conn() as conn:
            with conn: # Inicia la transacción
                cursor = conn.cursor()

                # 3. Construir y ejecutar la sentencia SQL de forma segura.
                #    La clave primaria es 'codigo_serial'.
                sql, params = _build_upsert_sql('trabajos', 'codigo_serial', datos_trabajo, VALID_TRABAJO_COLUMNS)
                
                cursor.execute(sql, params)
        
        return True

    except sqlite3.Error as e:
        print(f"Error en la base de datos al guardar el trabajo: {e}")
        # En una aplicación real, aquí registrarías el error en un log.
        # print("Datos que fallaron:", datos_trabajo) # Descomenta para depurar
        return False



def buscar_trabajo_por_codigo_serial(codigo_serial: str) -> Optional[Tuple[Dict[str, Any], str]]:
    """
    Busca un trabajo en la BD usando uno de sus códigos de etapa (ej. codigo_corte).

    Utiliza una sentencia CASE en SQL para identificar qué tipo de trabajo 
    coincidió con el código escaneado.

    Args:
        codigo_serial (str): El código de trabajo escaneado.

    Returns:
        Optional[Tuple[Dict[str, Any], str]]: Una tupla conteniendo:
            - Un diccionario con todos los datos del trabajo encontrado.
            - Una cadena con el tipo de trabajo que coincidió (ej. "corte").
        Retorna None si no se encuentra ningún trabajo.
    """
    try:
        # Construcción dinámica USANDO LA CONFIGURACIÓN CENTRAL
        case_statement = " ".join([f"WHEN codigo_{wt_id} = :codigo THEN '{wt_id}'" for wt_id in WORK_TYPE_IDS])
        where_clauses = " OR ".join([f"codigo_{wt_id} = :codigo" for wt_id in WORK_TYPE_IDS])

        sql = f"""
            SELECT *,
                   CASE {case_statement} ELSE 'desconocido' END as work_type_found
            FROM trabajos
            WHERE {where_clauses}
            LIMIT 1
        """
        
        with get_conn() as conn:
            conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
            cursor = conn.cursor()
            cursor.execute(sql, {'codigo': codigo_serial})
            row = cursor.fetchone()

            if row:
                return dict(row), row['work_type_found']
            return None

    except sqlite3.Error as e:
        print(f"Error de base de datos al buscar trabajo por código serial: {e}")
        return None

def vale_existe(codigo_serial_trabajo: str, empleado_id: str) -> bool:
    """
    Verifica si ya existe un vale para una combinación de empleado y código de trabajo.
    Usa la restricción UNIQUE(empleado_id, codigo_serial_trabajo_asociado) de la BD.

    Args:
        codigo_serial_trabajo (str): El código de trabajo escaneado.
        empleado_id (str): El ID del empleado.

    Returns:
        bool: True si ya existe un vale, False en caso contrario.
    """
    try:
        sql = "SELECT EXISTS(SELECT 1 FROM vales WHERE codigo_serial_trabajo_asociado = ? AND empleado_id = ? LIMIT 1)"
        with get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (codigo_serial_trabajo, empleado_id))
            return cursor.fetchone()[0] == 1
            
    except sqlite3.Error as e:
        print(f"Error de base de datos al verificar existencia de vale: {e}")
        return False # Es más seguro asumir que no existe si hay un error

def crear_vale(datos_vale: Dict[str, Any]) -> bool:
    """
    Crea un nuevo registro en la tabla 'vales'.

    Args:
        datos_vale (Dict[str, Any]): Un diccionario con los datos del vale.
                                     Debe contener las llaves: 'empleado_id',
                                     'codigo_serial_trabajo_asociado', 'work_type_detected',
                                     y 'valor_pagado'.

    Returns:
        bool: True si la creación fue exitosa, False en caso contrario.
    """
    try:
        # Generar ID único para el vale y la fecha/hora actual
        datos_vale['id_vale'] = f"V{int(time.time())}{str(uuid.uuid4())[:4]}"
        datos_vale['fecha_hora'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos_vale['estado'] = 'pendiente' # Estado por defecto
        
        # Usar la función de construcción de SQL para seguridad
        sql, params = _build_upsert_sql('vales', 'id_vale', datos_vale, VALID_VALE_COLUMNS)
        
        with get_conn() as conn:
            with conn: # Iniciar transacción
                cursor = conn.cursor()
                cursor.execute(sql, params)
        
        print(f"Vale {datos_vale['id_vale']} creado exitosamente.")
        return True

    except sqlite3.IntegrityError as e:
        # Esto puede ocurrir si se viola la restricción UNIQUE, por ejemplo.
        print(f"Error de integridad al crear el vale: {e}. ¿Quizás un vale duplicado?")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos al crear el vale: {e}")
        return False
