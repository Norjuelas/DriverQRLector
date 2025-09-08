# config.py


TIPOS_DE_TRABAJO = {
    "Plantillas TERRY": "Plantillas TERRY",
    "EMPAQUE": "Empaque",
    "ENSUELADO": "Ensuelado",
    "ALISTAMIENTO PARA ENSUELADO": "Alistamiento para Ensuelado",
    "MONTAR": "Montar",
    "ENGRUDAR": "ENGRUDAR",
    "GUARNICION": "Guarnicion",
    "CORTE": "Corte"
}

# Estos son los nombres que se usarán como claves principales y en la UI.
# Usaremos las claves de este diccionario para mantener el orden y la consistencia.
WORK_TYPE_ABBREVIATIONS = {
    "Corte": "CT",
    "Guarnicion": "GU",
    "Montar": "MO",
    "ENGRUDAR": "EG",
    "Alistamiento para Ensuelado": "AE",
    "Ensuelado": "EN",
    "Plantillas TERRY": "PT",
    "Empaque": "EM",
}

CAMPOS_VALOR_TRABAJO_MAP = {
    "Corte": "CampoValorCorte",
    "Guarnicion": "CampoValorGuarnicion",
    "Montar": "CampoValorMontar",
    "ENGRUDAR": "CampoValorEngrudar",
    "Alistamiento para Ensuelado": "CampoValorAlistamiento",
    "Ensuelado": "CampoValorEnsuelado",
    "Plantillas TERRY": "CampoValorPlantillas",
    "Empaque": "CampoValorEmpaque",
}

"""
Archivo de Configuración Central para Tipos de Trabajo.
Esta es la ÚNICA FUENTE DE VERDAD para toda la información relacionada con
los tipos de trabajo en la aplicación.

Estructura de WORK_TYPES:
{
    'identificador_programatico': {
        'display': 'Nombre para mostrar en la UI',
        'abbr': 'Abreviatura para códigos seriales',
        'ui_field': 'Nombre del objeto QLineEdit en la UI para el valor'
    },
    ...
}
El 'identificador_programatico' (la clave) debe coincidir con el sufijo
de las columnas en la base de datos (ej. 'corte' para 'valor_corte' y 'codigo_corte').
El orden en este diccionario define el orden en que aparecerán en la UI.
"""

WORK_TYPES = {
    'corte': {
        'display': 'Corte',
        'abbr': 'CT',
        'ui_field': 'CampoValorCorte'
    },
    'guarnicion': {
        'display': 'Guarnición', # Mejorado para usar tilde
        'abbr': 'GU',
        'ui_field': 'CampoValorGuarnicion'
    },
    'montar': {
        'display': 'Montar',
        'abbr': 'MO',
        'ui_field': 'CampoValorMontar'
    },
    'engrudar': {
        'display': 'Engrudar', # Normalizado a minúsculas
        'abbr': 'EG',
        'ui_field': 'CampoValorEngrudar'
    },
    'alist_ensuelado': {
        'display': 'Alist. Ensuelado', # Abreviado para UI
        'abbr': 'AE',
        'ui_field': 'CampoValorAlistamiento'
    },
    'ensuelado': {
        'display': 'Ensuelado',
        'abbr': 'EN',
        'ui_field': 'CampoValorEnsuelado'
    },
    'plantillas_terry': {
        'display': 'Plantillas TERRY',
        'abbr': 'PT',
        'ui_field': 'CampoValorPlantillas'
    },
    'empaque': {
        'display': 'Empaque',
        'abbr': 'EM',
        'ui_field': 'CampoValorEmpaque'
    }
}

# --- Derivaciones útiles (no es necesario modificarlas) ---

# Lista de identificadores programáticos (para uso en la base de datos)
# Ejemplo: ['corte', 'guarnicion', ...]
WORK_TYPE_IDS = list(WORK_TYPES.keys())

# Mapeo de nombre de display a identificador (útil para conversiones)
# Ejemplo: {'Corte': 'corte', 'Guarnición': 'guarnicion', ...}
DISPLAY_NAME_TO_ID_MAP = {v['display']: k for k, v in WORK_TYPES.items()}