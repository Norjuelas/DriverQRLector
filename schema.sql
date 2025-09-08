-- schema.sql

-- Almacena la información de los empleados de la fábrica.
CREATE TABLE IF NOT EXISTS empleados (
  empleado_id TEXT PRIMARY KEY,
  nombre      TEXT NOT NULL,
  cedula      TEXT UNIQUE,
  celular     TEXT,
  correo      TEXT
);
CREATE INDEX IF NOT EXISTS idx_empleados_cedula ON empleados(cedula);

-- Almacena la información detallada de cada lote de producción (trabajo).
-- Cada fila representa un trabajo específico identificado por un código serial único.
CREATE TABLE IF NOT EXISTS trabajos (
  codigo_serial TEXT PRIMARY KEY,
  numero_ticket TEXT,
  referencia    TEXT,
  color         TEXT,
  -- Cantidades por talla
  cant_t33 INTEGER DEFAULT 0, cant_t34 INTEGER DEFAULT 0, cant_t35 INTEGER DEFAULT 0,
  cant_t36 INTEGER DEFAULT 0, cant_t37 INTEGER DEFAULT 0, cant_t38 INTEGER DEFAULT 0,
  cant_t39 INTEGER DEFAULT 0, cant_t40 INTEGER DEFAULT 0, cant_t41 INTEGER DEFAULT 0,
  cant_t42 INTEGER DEFAULT 0, cant_t43 INTEGER DEFAULT 0, cant_t44 INTEGER DEFAULT 0,
  cant_t45 INTEGER DEFAULT 0, cant_t46 INTEGER DEFAULT 0, cant_t47 INTEGER DEFAULT 0,
  cant_t48 INTEGER DEFAULT 0,
  total_producido INTEGER DEFAULT 0,
  -- Valores monetarios por etapa/tipo de trabajo
  valor_corte             REAL DEFAULT 0,
  valor_guarnicion        REAL DEFAULT 0,
  valor_montar            REAL DEFAULT 0,
  valor_engrudar          REAL DEFAULT 0,
  valor_alist_ensuelado   REAL DEFAULT 0,
  valor_ensuelado         REAL DEFAULT 0,
  valor_plantillas_terry  REAL DEFAULT 0,
  valor_empaque           REAL DEFAULT 0,
  -- Códigos seriales específicos para cada etapa (si aplica)
  codigo_corte            TEXT,
  codigo_guarnicion       TEXT,
  codigo_montar           TEXT,
  codigo_engrudar         TEXT,
  codigo_alist_ensuelado  TEXT,
  codigo_ensuelado        TEXT,
  codigo_plantillas_terry TEXT,
  codigo_empaque          TEXT,
  -- Metadatos
  ruta_imagen TEXT
);
CREATE INDEX IF NOT EXISTS idx_trabajos_ticket ON trabajos(numero_ticket);

-- Registra cada "lectura" o "escaneo" de un código de trabajo por parte de un empleado.
-- Cada fila es un "vale" que certifica que un empleado realizó una tarea.
CREATE TABLE IF NOT EXISTS vales (
  id_vale         TEXT PRIMARY KEY,
  empleado_id     TEXT NOT NULL,
  codigo_serial_trabajo_asociado TEXT NOT NULL,
  fecha_hora      TEXT NOT NULL,  -- Formato ISO: "YYYY-MM-DD HH:MM:SS"
  work_type_detected TEXT, -- El tipo de trabajo detectado en esta lectura específica (Corte, Guarnición, etc.)
  valor_pagado    REAL DEFAULT 0, -- El valor específico de este vale (ej. valor_corte del trabajo asociado)
  estado          TEXT DEFAULT 'pendiente', -- pendiente, pagado, anulado

  FOREIGN KEY (empleado_id) REFERENCES empleados(empleado_id),
  FOREIGN KEY (codigo_serial_trabajo_asociado) REFERENCES trabajos(codigo_serial),
  -- Evita que un empleado escanee el mismo código de trabajo dos veces.
  UNIQUE(empleado_id, codigo_serial_trabajo_asociado)
);
CREATE INDEX IF NOT EXISTS idx_vales_empleado ON vales(empleado_id);
CREATE INDEX IF NOT EXISTS idx_vales_fecha    ON vales(fecha_hora);
CREATE INDEX IF NOT EXISTS idx_vales_codigo   ON vales(codigo_serial_trabajo_asociado);