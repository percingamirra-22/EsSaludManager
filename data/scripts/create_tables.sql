-- ============================================
-- EsSaludManager - Esquema de Base de Datos
-- ============================================
-- Descripción: Creación de todas las tablas e índices del sistema.
-- Versión: 1.0.0
-- Fecha: 2026-09-29
-- ============================================

-- Habilitar foreign keys (SQLite no las activa por defecto)
PRAGMA foreign_keys = ON;

-- ============================================
-- Dominio 1: Pacientes y seguros
-- ============================================

CREATE TABLE IF NOT EXISTS paciente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_paciente TEXT NOT NULL UNIQUE,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    tipo_documento TEXT NOT NULL CHECK (tipo_documento IN ('DNI', 'CE', 'PAS')),
    numero_documento TEXT NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    sexo TEXT NOT NULL CHECK (sexo IN ('M', 'F', 'O')),
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_registro TEXT
);

CREATE TABLE IF NOT EXISTS seguro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_seguro TEXT NOT NULL CHECK (tipo_seguro IN ('EsSalud', 'Privado')),
    nombre_aseguradora TEXT NOT NULL,
    codigo_plan TEXT NOT NULL,
    numero_poliza TEXT NOT NULL UNIQUE,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);

CREATE TABLE IF NOT EXISTS paciente_seguro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL UNIQUE,
    seguro_id INTEGER NOT NULL,
    fecha_asignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (seguro_id) REFERENCES seguro(id) ON DELETE RESTRICT,
    UNIQUE (paciente_id, seguro_id)
);

-- ============================================
-- Dominio 2: Historial clínico
-- ============================================

CREATE TABLE IF NOT EXISTS historial_clinico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    numero_historia TEXT NOT NULL UNIQUE,
    fecha_apertura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'cerrado', 'desactivado')),
    version INTEGER NOT NULL DEFAULT 1,
    fecha_ultima_modificacion DATETIME,
    usuario_ultima_modificacion TEXT,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS entrada_historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    historial_id INTEGER NOT NULL,
    tipo_entrada TEXT NOT NULL CHECK (tipo_entrada IN ('nota', 'diagnóstico', 'tratamiento', 'examen', 'receta')),
    contenido TEXT NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_registro TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'desactivada')),
    FOREIGN KEY (historial_id) REFERENCES historial_clinico(id) ON DELETE CASCADE
);

-- ============================================
-- Dominio 3: Auditoría
-- ============================================

CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    accion TEXT NOT NULL,
    recurso TEXT NOT NULL,
    recurso_id INTEGER NOT NULL,
    fecha_accion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_origen TEXT NOT NULL,
    detalles TEXT,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE RESTRICT,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE RESTRICT
);

-- ============================================
-- Dominio 4: Servicios, citas y exámenes
-- ============================================

CREATE TABLE IF NOT EXISTS servicio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_servicio TEXT NOT NULL UNIQUE,
    nombre_servicio TEXT NOT NULL,
    tipo_servicio TEXT NOT NULL CHECK (tipo_servicio IN ('consulta', 'examen', 'procedimiento')),
    costo_base REAL NOT NULL DEFAULT 0.0 CHECK (costo_base >= 0),
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consulta (
    id INTEGER PRIMARY KEY,
    servicio_id INTEGER NOT NULL UNIQUE,
    especialista_id INTEGER NOT NULL,
    duracion INTEGER NOT NULL CHECK (duracion > 0),
    requiere_preparacion INTEGER NOT NULL DEFAULT 0 CHECK (requiere_preparacion IN (0, 1)),
    FOREIGN KEY (id) REFERENCES servicio(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicio(id) ON DELETE CASCADE,
    FOREIGN KEY (especialista_id) REFERENCES especialista(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS orden_examen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    especialista_id INTEGER NOT NULL,
    fecha_orden DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'completada', 'cancelada')),
    observaciones TEXT,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (especialista_id) REFERENCES especialista(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS examen_solicitado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orden_examen_id INTEGER NOT NULL,
    examen_id INTEGER NOT NULL,
    fecha_solicitud DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (orden_examen_id) REFERENCES orden_examen(id) ON DELETE CASCADE,
    FOREIGN KEY (examen_id) REFERENCES examen_medico(id) ON DELETE CASCADE,
    UNIQUE (orden_examen_id, examen_id)
);

CREATE TABLE IF NOT EXISTS examen_medico (
    id INTEGER PRIMARY KEY,
    servicio_id INTEGER NOT NULL UNIQUE,
    orden_examen_id INTEGER NOT NULL,
    tecnico_id INTEGER NOT NULL,
    tipo_examen TEXT NOT NULL,
    fecha_realizacion DATETIME,
    resultado TEXT,
    archivo_resultado TEXT,
    estado TEXT NOT NULL DEFAULT 'programado' CHECK (estado IN ('programado', 'en proceso', 'completado', 'cancelado')),
    FOREIGN KEY (id) REFERENCES servicio(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicio(id) ON DELETE CASCADE,
    FOREIGN KEY (orden_examen_id) REFERENCES orden_examen(id) ON DELETE CASCADE,
    FOREIGN KEY (tecnico_id) REFERENCES tecnico(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS cita (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    recepcionista_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    estado TEXT NOT NULL DEFAULT 'programada' CHECK (estado IN ('programada', 'completada', 'cancelada', 'reprogramada')),
    motivo TEXT,
    observaciones TEXT,
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion TEXT NOT NULL,
    fecha_ultima_modificacion DATETIME,
    usuario_ultima_modificacion TEXT,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (recepcionista_id) REFERENCES recepcionista(id) ON DELETE RESTRICT,
    FOREIGN KEY (servicio_id) REFERENCES servicio(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS notificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    cita_id INTEGER NOT NULL,
    tipo_notificacion TEXT NOT NULL CHECK (tipo_notificacion IN ('recordatorio_cita', 'recordatorio_examen')),
    mensaje TEXT NOT NULL,
    fecha_envio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'enviada', 'fallida')),
    canal TEXT NOT NULL CHECK (canal IN ('sms', 'email')),
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (cita_id) REFERENCES cita(id) ON DELETE CASCADE
);

-- ============================================
-- Dominio 5: Empleados y roles
-- ============================================

CREATE TABLE IF NOT EXISTS empleado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_empleado TEXT NOT NULL UNIQUE,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    tipo_documento TEXT NOT NULL CHECK (tipo_documento IN ('DNI', 'CE', 'PAS')),
    numero_documento TEXT NOT NULL UNIQUE,
    telefono TEXT,
    email TEXT,
    direccion TEXT,
    fecha_contratacion DATE NOT NULL,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_despido DATE,
    usuario_registro TEXT
);

CREATE TABLE IF NOT EXISTS especialista (
    id INTEGER PRIMARY KEY,
    empleado_id INTEGER NOT NULL UNIQUE,
    especialidad TEXT NOT NULL,
    numero_colegiatura TEXT NOT NULL UNIQUE,
    FOREIGN KEY (id) REFERENCES empleado(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS horario_especialista (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especialista_id INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL CHECK (hora_fin > hora_inicio),
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    FOREIGN KEY (especialista_id) REFERENCES especialista(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gerente (
    id INTEGER PRIMARY KEY,
    empleado_id INTEGER NOT NULL UNIQUE,
    area TEXT NOT NULL,
    nivel_gerencial TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES empleado(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recepcionista (
    id INTEGER PRIMARY KEY,
    empleado_id INTEGER NOT NULL UNIQUE,
    turno TEXT NOT NULL CHECK (turno IN ('Mañana', 'Tarde', 'Noche')),
    modulo_atencion TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES empleado(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tecnico (
    id INTEGER PRIMARY KEY,
    empleado_id INTEGER NOT NULL UNIQUE,
    especialidad_tecnica TEXT NOT NULL,
    area_trabajo TEXT NOT NULL,
    FOREIGN KEY (id) REFERENCES empleado(id) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS certificacion_tecnico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tecnico_id INTEGER NOT NULL,
    nombre_certificacion TEXT NOT NULL,
    entidad_emisora TEXT NOT NULL,
    fecha_obtencion DATE NOT NULL,
    fecha_vencimiento DATE,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    FOREIGN KEY (tecnico_id) REFERENCES tecnico(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_ultimo_acceso DATETIME,
    FOREIGN KEY (empleado_id) REFERENCES empleado(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_rol TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS permiso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_permiso TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    recurso TEXT NOT NULL,
    accion TEXT NOT NULL CHECK (accion IN ('crear', 'leer', 'actualizar', 'eliminar', 'aprobar')),
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1))
);

CREATE TABLE IF NOT EXISTS rol_permiso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rol_id INTEGER NOT NULL,
    permiso_id INTEGER NOT NULL,
    fecha_asignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE,
    FOREIGN KEY (permiso_id) REFERENCES permiso(id) ON DELETE CASCADE,
    UNIQUE (rol_id, permiso_id)
);

CREATE TABLE IF NOT EXISTS usuario_rol (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    rol_id INTEGER NOT NULL,
    fecha_asignacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    usuario_que_asigno TEXT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE,
    FOREIGN KEY (rol_id) REFERENCES rol(id) ON DELETE CASCADE,
    UNIQUE (usuario_id, rol_id)
);

CREATE TABLE IF NOT EXISTS sesion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    fecha_inicio DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_fin DATETIME,
    ip_origen TEXT,
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'cerrada', 'expirada')),
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
);

-- ============================================
-- Dominio 6: Medicamentos y stock
-- ============================================

CREATE TABLE IF NOT EXISTS medicamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_medicamento TEXT NOT NULL UNIQUE,
    nombre_generico TEXT NOT NULL,
    nombre_comercial TEXT NOT NULL,
    forma_farmaceutica TEXT NOT NULL,
    concentracion TEXT NOT NULL,
    unidad_medida TEXT NOT NULL,
    requiere_receta INTEGER NOT NULL DEFAULT 0 CHECK (requiere_receta IN (0, 1)),
    stock_minimo INTEGER NOT NULL DEFAULT 0 CHECK (stock_minimo >= 0),
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS lote_medicamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicamento_id INTEGER NOT NULL,
    proveedor_id INTEGER NOT NULL,
    numero_lote TEXT NOT NULL UNIQUE,
    fecha_fabricacion DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    cantidad_inicial INTEGER NOT NULL CHECK (cantidad_inicial >= 0),
    cantidad_actual INTEGER NOT NULL DEFAULT 0 CHECK (cantidad_actual >= 0),
    estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'agotado', 'vencido')),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicamento_id) REFERENCES medicamento(id) ON DELETE CASCADE,
    FOREIGN KEY (proveedor_id) REFERENCES proveedor(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS movimiento_medicamento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id INTEGER NOT NULL,
    tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('entrada', 'salida', 'ajuste')),
    cantidad INTEGER NOT NULL,
    fecha_movimiento DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario_responsable TEXT NOT NULL,
    motivo TEXT,
    documento_referencia TEXT,
    FOREIGN KEY (lote_id) REFERENCES lote_medicamento(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS proveedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    razon_social TEXT NOT NULL,
    ruc TEXT NOT NULL UNIQUE,
    direccion TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE,
    contacto_nombre TEXT,
    contacto_telefono TEXT,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS certificado_proveedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proveedor_id INTEGER NOT NULL,
    tipo_certificado TEXT NOT NULL,
    numero_certificado TEXT NOT NULL UNIQUE,
    entidad_emisora TEXT NOT NULL,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE,
    archivo_certificado TEXT,
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    FOREIGN KEY (proveedor_id) REFERENCES proveedor(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS receta_medica (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER NOT NULL,
    especialista_id INTEGER NOT NULL,
    fecha_emision DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'activa' CHECK (estado IN ('activa', 'dispensada', 'cancelada')),
    observaciones TEXT,
    usuario_emisor TEXT NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE,
    FOREIGN KEY (especialista_id) REFERENCES especialista(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS item_receta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receta_id INTEGER NOT NULL,
    medicamento_id INTEGER NOT NULL,
    dosis TEXT NOT NULL,
    frecuencia TEXT NOT NULL,
    duracion_dias INTEGER NOT NULL CHECK (duracion_dias > 0),
    cantidad_dispensada INTEGER NOT NULL DEFAULT 0 CHECK (cantidad_dispensada >= 0),
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'dispensado', 'cancelado')),
    FOREIGN KEY (receta_id) REFERENCES receta_medica(id) ON DELETE CASCADE,
    FOREIGN KEY (medicamento_id) REFERENCES medicamento(id) ON DELETE RESTRICT
);

-- ============================================
-- Dominio 7: Coberturas
-- ============================================

CREATE TABLE IF NOT EXISTS cobertura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seguro_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    porcentaje_cobertura REAL NOT NULL CHECK (porcentaje_cobertura BETWEEN 0.0 AND 100.0),
    monto_maximo REAL NOT NULL DEFAULT 0.0 CHECK (monto_maximo >= 0),
    copago_fijo REAL NOT NULL DEFAULT 0.0 CHECK (copago_fijo >= 0),
    estado INTEGER NOT NULL DEFAULT 1 CHECK (estado IN (0, 1)),
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,
    FOREIGN KEY (seguro_id) REFERENCES seguro(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicio(id) ON DELETE CASCADE,
    UNIQUE (seguro_id, servicio_id, fecha_inicio)
);

-- ============================================
-- Dominio 8: Facturación y pagos
-- ============================================

CREATE TABLE IF NOT EXISTS factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_factura TEXT NOT NULL UNIQUE,
    paciente_id INTEGER NOT NULL,
    fecha_emision DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado TEXT NOT NULL DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'pagada', 'anulada')),
    monto_total REAL NOT NULL DEFAULT 0.0 CHECK (monto_total >= 0),
    monto_cubierto REAL NOT NULL DEFAULT 0.0 CHECK (monto_cubierto >= 0),
    monto_paciente REAL NOT NULL DEFAULT 0.0 CHECK (monto_paciente >= 0),
    usuario_emisor TEXT NOT NULL,
    FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS item_factura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    servicio_id INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    costo REAL NOT NULL CHECK (costo >= 0),
    estado TEXT NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'anulado')),
    FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE,
    FOREIGN KEY (servicio_id) REFERENCES servicio(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS pago (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    factura_id INTEGER NOT NULL,
    monto REAL NOT NULL CHECK (monto > 0),
    fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    metodo_pago TEXT NOT NULL CHECK (metodo_pago IN ('efectivo', 'tarjeta', 'transferencia')),
    estado TEXT NOT NULL DEFAULT 'registrado' CHECK (estado IN ('registrado', 'conciliado')),
    usuario_registro TEXT NOT NULL,
    numero_referencia TEXT,
    FOREIGN KEY (factura_id) REFERENCES factura(id) ON DELETE CASCADE
);

-- ============================================
-- Dominio 9: Reportes e infraestructura
-- ============================================

CREATE TABLE IF NOT EXISTS reporte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo_reporte TEXT NOT NULL,
    filtros TEXT,
    fecha_generacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    formato TEXT NOT NULL CHECK (formato IN ('PDF', 'CSV')),
    ruta_archivo TEXT NOT NULL,
    usuario_solicitante_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_solicitante_id) REFERENCES usuario(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS configuracion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave TEXT NOT NULL UNIQUE,
    valor TEXT NOT NULL,
    descripcion TEXT,
    fecha_actualizacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS log_sistema (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nivel TEXT NOT NULL CHECK (nivel IN ('INFO', 'WARNING', 'ERROR')),
    mensaje TEXT NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modulo TEXT
);

-- ============================================
-- ÍNDICES
-- ============================================

-- Dominio 1: Pacientes
CREATE INDEX IF NOT EXISTS idx_paciente_numero_documento ON paciente(numero_documento);
CREATE INDEX IF NOT EXISTS idx_paciente_apellidos ON paciente(apellidos);
CREATE INDEX IF NOT EXISTS idx_paciente_estado ON paciente(estado);

-- Dominio 2: Historial clínico
CREATE INDEX IF NOT EXISTS idx_entrada_historial_historial ON entrada_historial(historial_id);
CREATE INDEX IF NOT EXISTS idx_entrada_historial_fecha ON entrada_historial(fecha_registro);
CREATE INDEX IF NOT EXISTS idx_historial_clinico_paciente ON historial_clinico(paciente_id);
CREATE INDEX IF NOT EXISTS idx_historial_clinico_numero ON historial_clinico(numero_historia);
CREATE INDEX IF NOT EXISTS idx_historial_clinico_estado ON historial_clinico(estado);

-- Dominio 3: Citas y exámenes
CREATE INDEX IF NOT EXISTS idx_cita_paciente ON cita(paciente_id);
CREATE INDEX IF NOT EXISTS idx_cita_fecha_inicio ON cita(fecha_inicio);
CREATE INDEX IF NOT EXISTS idx_cita_estado ON cita(estado);
CREATE INDEX IF NOT EXISTS idx_cita_servicio ON cita(servicio_id);
CREATE INDEX IF NOT EXISTS idx_consulta_especialista ON consulta(especialista_id);
CREATE INDEX IF NOT EXISTS idx_examen_medico_tecnico ON examen_medico(tecnico_id);
CREATE INDEX IF NOT EXISTS idx_cita_fecha_creacion ON cita(fecha_creacion);

-- Dominio 4: Empleados y usuarios
CREATE INDEX IF NOT EXISTS idx_usuario_username ON usuario(username);
CREATE INDEX IF NOT EXISTS idx_usuario_empleado ON usuario(empleado_id);
CREATE INDEX IF NOT EXISTS idx_usuario_estado ON usuario(estado);
CREATE INDEX IF NOT EXISTS idx_empleado_numero_documento ON empleado(numero_documento);
CREATE INDEX IF NOT EXISTS idx_empleado_apellidos ON empleado(apellidos);
CREATE INDEX IF NOT EXISTS idx_empleado_estado ON empleado(estado);
CREATE INDEX IF NOT EXISTS idx_sesion_usuario ON sesion(usuario_id);
CREATE INDEX IF NOT EXISTS idx_sesion_estado ON sesion(estado);
CREATE INDEX IF NOT EXISTS idx_sesion_fecha_inicio ON sesion(fecha_inicio);

-- Dominio 5: Medicamentos
CREATE INDEX IF NOT EXISTS idx_medicamento_codigo ON medicamento(codigo_medicamento);
CREATE INDEX IF NOT EXISTS idx_medicamento_nombre_generico ON medicamento(nombre_generico);
CREATE INDEX IF NOT EXISTS idx_medicamento_estado ON medicamento(estado);
CREATE INDEX IF NOT EXISTS idx_lote_medicamento_estado ON lote_medicamento(estado);
CREATE INDEX IF NOT EXISTS idx_lote_medicamento_vencimiento ON lote_medicamento(fecha_vencimiento);
CREATE INDEX IF NOT EXISTS idx_lote_medicamento_medicamento ON lote_medicamento(medicamento_id);
CREATE INDEX IF NOT EXISTS idx_movimiento_medicamento_lote ON movimiento_medicamento(lote_id);
CREATE INDEX IF NOT EXISTS idx_movimiento_medicamento_fecha ON movimiento_medicamento(fecha_movimiento);

-- Dominio 6: Coberturas
CREATE INDEX IF NOT EXISTS idx_cobertura_seguro ON cobertura(seguro_id);
CREATE INDEX IF NOT EXISTS idx_cobertura_servicio ON cobertura(servicio_id);
CREATE INDEX IF NOT EXISTS idx_cobertura_estado ON cobertura(estado);

-- Dominio 7: Facturación
CREATE INDEX IF NOT EXISTS idx_factura_paciente ON factura(paciente_id);
CREATE INDEX IF NOT EXISTS idx_factura_numero ON factura(numero_factura);
CREATE INDEX IF NOT EXISTS idx_factura_estado ON factura(estado);
CREATE INDEX IF NOT EXISTS idx_factura_fecha ON factura(fecha_emision);
CREATE INDEX IF NOT EXISTS idx_pago_factura ON pago(factura_id);
CREATE INDEX IF NOT EXISTS idx_pago_estado ON pago(estado);
CREATE INDEX IF NOT EXISTS idx_pago_fecha ON pago(fecha_pago);
CREATE INDEX IF NOT EXISTS idx_item_factura_factura ON item_factura(factura_id);

-- Dominio 8: Auditoría
CREATE INDEX IF NOT EXISTS idx_auditoria_fecha ON auditoria(fecha_accion);
CREATE INDEX IF NOT EXISTS idx_auditoria_usuario ON auditoria(usuario_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_empleado ON auditoria(empleado_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_recurso ON auditoria(recurso, recurso_id);
CREATE INDEX IF NOT EXISTS idx_auditoria_estado ON auditoria(estado);

-- ============================================
-- FIN DEL ESQUEMA
-- ============================================