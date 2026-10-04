-- ============================================
-- EsSaludManager - Datos Iniciales (Seed Data)
-- ============================================
-- Descripción: Inserta roles, permisos, usuario admin y configuraciones básicas.
-- Versión: 1.0.0
-- Fecha: 2026-09-29
-- ============================================

-- Habilitar foreign keys
PRAGMA foreign_keys = ON;

-- ============================================
-- Configuración del sistema
-- ============================================

INSERT INTO configuracion (clave, valor, descripcion) VALUES
    ('version_sistema', '1.0.0', 'Versión actual del sistema'),
    ('nombre_clinica', 'EsSalud Manager', 'Nombre de la clínica/hospital'),
    ('timezone', 'America/Lima', 'Zona horaria del sistema'),
    ('sesion_timeout_minutos', '30', 'Tiempo de inactividad antes de cerrar sesión'),
    ('stock_minimo_alerta', '10', 'Cantidad mínima para alertas de stock');

-- ============================================
-- Roles del sistema
-- ============================================

INSERT INTO rol (nombre_rol, descripcion, estado) VALUES
    ('ADMIN', 'Administrador del sistema con acceso total', 1),
    ('GERENTE', 'Gerente con acceso a reportes y aprobaciones', 1),
    ('ESPECIALISTA', 'Médico especialista con acceso a historial y recetas', 1),
    ('RECEPCIONISTA', 'Recepcionista con acceso a citas y pacientes', 1),
    ('TECNICO', 'Técnico con acceso a exámenes y resultados', 1);

-- ============================================
-- Permisos del sistema
-- ============================================

-- Permisos para Paciente
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('PACIENTE_CREAR', 'Crear nuevos pacientes', 'paciente', 'crear', 1),
    ('PACIENTE_LEER', 'Leer información de pacientes', 'paciente', 'leer', 1),
    ('PACIENTE_ACTUALIZAR', 'Actualizar información de pacientes', 'paciente', 'actualizar', 1),
    ('PACIENTE_ELIMINAR', 'Eliminar/desactivar pacientes', 'paciente', 'eliminar', 1);

-- Permisos para Historial Clínico
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('HISTORIAL_CREAR', 'Crear historial clínico', 'historial_clinico', 'crear', 1),
    ('HISTORIAL_LEER', 'Leer historial clínico', 'historial_clinico', 'leer', 1),
    ('HISTORIAL_ACTUALIZAR', 'Actualizar historial clínico', 'historial_clinico', 'actualizar', 1),
    ('HISTORIAL_ELIMINAR', 'Desactivar historial clínico', 'historial_clinico', 'eliminar', 1);

-- Permisos para Citas
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('CITA_CREAR', 'Crear citas', 'cita', 'crear', 1),
    ('CITA_LEER', 'Leer citas', 'cita', 'leer', 1),
    ('CITA_ACTUALIZAR', 'Actualizar/reprogramar citas', 'cita', 'actualizar', 1),
    ('CITA_ELIMINAR', 'Cancelar citas', 'cita', 'eliminar', 1);

-- Permisos para Medicamentos
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('MEDICAMENTO_CREAR', 'Crear medicamentos', 'medicamento', 'crear', 1),
    ('MEDICAMENTO_LEER', 'Leer medicamentos', 'medicamento', 'leer', 1),
    ('MEDICAMENTO_ACTUALIZAR', 'Actualizar medicamentos', 'medicamento', 'actualizar', 1),
    ('MEDICAMENTO_ELIMINAR', 'Eliminar medicamentos', 'medicamento', 'eliminar', 1);

-- Permisos para Usuarios y Roles
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('USUARIO_CREAR', 'Crear usuarios', 'usuario', 'crear', 1),
    ('USUARIO_LEER', 'Leer usuarios', 'usuario', 'leer', 1),
    ('USUARIO_ACTUALIZAR', 'Actualizar usuarios', 'usuario', 'actualizar', 1),
    ('USUARIO_ELIMINAR', 'Eliminar usuarios', 'usuario', 'eliminar', 1),
    ('ROL_ASIGNAR', 'Asignar roles a usuarios', 'rol', 'aprobar', 1);

-- Permisos para Reportes
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('REPORTE_GENERAR', 'Generar reportes', 'reporte', 'leer', 1),
    ('REPORTE_EXPORTAR', 'Exportar reportes', 'reporte', 'leer', 1);

-- Permisos para Auditoría
INSERT INTO permiso (codigo_permiso, descripcion, recurso, accion, estado) VALUES
    ('AUDITORIA_LEER', 'Leer logs de auditoría', 'auditoria', 'leer', 1);

-- ============================================
-- Asignar permisos a roles
-- ============================================

-- ADMIN: Todos los permisos
INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM rol r, permiso p WHERE r.nombre_rol = 'ADMIN';

-- GERENTE: Reportes, auditoría, usuarios (lectura)
INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM rol r, permiso p 
WHERE r.nombre_rol = 'GERENTE' 
AND p.codigo_permiso IN ('REPORTE_GENERAR', 'REPORTE_EXPORTAR', 'AUDITORIA_LEER', 'USUARIO_LEER', 'PACIENTE_LEER', 'CITA_LEER');

-- ESPECIALISTA: Pacientes, historial, citas, medicamentos (lectura/escritura limitada)
INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM rol r, permiso p 
WHERE r.nombre_rol = 'ESPECIALISTA' 
AND p.codigo_permiso IN ('PACIENTE_LEER', 'PACIENTE_CREAR', 'HISTORIAL_CREAR', 'HISTORIAL_LEER', 'HISTORIAL_ACTUALIZAR', 'CITA_LEER', 'MEDICAMENTO_LEER', 'MEDICAMENTO_CREAR');

-- RECEPCIONISTA: Pacientes, citas (gestión completa)
INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM rol r, permiso p 
WHERE r.nombre_rol = 'RECEPCIONISTA' 
AND p.codigo_permiso IN ('PACIENTE_CREAR', 'PACIENTE_LEER', 'PACIENTE_ACTUALIZAR', 'CITA_CREAR', 'CITA_LEER', 'CITA_ACTUALIZAR', 'CITA_ELIMINAR');

-- TECNICO: Exámenes, resultados
INSERT INTO rol_permiso (rol_id, permiso_id)
SELECT r.id, p.id FROM rol r, permiso p 
WHERE r.nombre_rol = 'TECNICO' 
AND p.codigo_permiso IN ('PACIENTE_LEER', 'CITA_LEER');

-- ============================================
-- Empleado base (ADMIN)
-- ============================================

INSERT INTO empleado (codigo_empleado, nombres, apellidos, tipo_documento, numero_documento, fecha_contratacion, estado, usuario_registro) VALUES
    ('EMP001', 'Administrador', 'Sistema', 'DNI', '00000000', '2026-01-01', 1, 'SYSTEM');

-- ============================================
-- Usuario ADMIN
-- ============================================

-- Password: admin123 (hash SHA-256 para producción, aquí usamos hash simple para demo)
-- En producción, usar bcrypt o argon2 desde Python
INSERT INTO usuario (empleado_id, username, password_hash, email, estado, fecha_creacion) VALUES
    (1, 'admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'admin@esalud.com', 1, CURRENT_TIMESTAMP);

-- Asignar rol ADMIN al usuario
INSERT INTO usuario_rol (usuario_id, rol_id, usuario_que_asigno)
SELECT u.id, r.id, 'SYSTEM' FROM usuario u, rol r WHERE u.username = 'admin' AND r.nombre_rol = 'ADMIN';

-- ============================================
-- Empleados de ejemplo (para pruebas)
-- ============================================

INSERT INTO empleado (codigo_empleado, nombres, apellidos, tipo_documento, numero_documento, telefono, email, fecha_contratacion, estado, usuario_registro) VALUES
    ('EMP002', 'María', 'Rodriguez', 'DNI', '12345678', '987654321', 'maria.rodriguez@esalud.com', '2026-01-15', 1, 'admin'),
    ('EMP003', 'Juan', 'Perez', 'DNI', '87654321', '912345678', 'juan.perez@esalud.com', '2026-02-01', 1, 'admin'),
    ('EMP004', 'Ana', 'Gomez', 'DNI', '11223344', '998877665', 'ana.gomez@esalud.com', '2026-02-15', 1, 'admin'),
    ('EMP005', 'Carlos', 'Lopez', 'DNI', '44332211', '955667788', 'carlos.lopez@esalud.com', '2026-03-01', 1, 'admin');

-- Empleado adicional sin usuario, para pruebas de registro de usuario
INSERT INTO empleado (
    codigo_empleado,
    nombres,
    apellidos,
    tipo_documento,
    numero_documento,
    telefono,
    email,
    fecha_contratacion,
    estado,
    usuario_registro
) VALUES
    (
        'EMP006',
        'Prueba',
        'Usuario',
        'DNI',
        '99999999',
        '900000001',
        'prueba.usuario@esalud.com',
        '2026-01-01',
        1,
        'admin'
    );

-- ============================================
-- Especialidades para los empleados de ejemplo
-- ============================================

INSERT INTO especialista (empleado_id, especialidad, numero_colegiatura) VALUES
    (2, 'Medicina General', 'CMP-12345'),
    (3, 'Cardiología', 'CMP-67890');

INSERT INTO recepcionista (empleado_id, turno, modulo_atencion) VALUES
    (4, 'Mañana', 'Módulo 1');

INSERT INTO tecnico (empleado_id, especialidad_tecnica, area_trabajo) VALUES
    (5, 'Laboratorio Clínico', 'Análisis Clínicos');

-- ============================================
-- Usuarios para empleados de ejemplo
-- ============================================

INSERT INTO usuario (empleado_id, username, password_hash, email, estado) VALUES
    (2, 'mrodriguez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'maria.rodriguez@esalud.com', 1),
    (3, 'jperez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'juan.perez@esalud.com', 1),
    (4, 'agomez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'ana.gomez@esalud.com', 1),
    (5, 'clopez', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'carlos.lopez@esalud.com', 1);

-- Asignar roles
INSERT INTO usuario_rol (usuario_id, rol_id, usuario_que_asigno)
SELECT u.id, r.id, 'admin' FROM usuario u, rol r WHERE u.username = 'mrodriguez' AND r.nombre_rol = 'ESPECIALISTA';

INSERT INTO usuario_rol (usuario_id, rol_id, usuario_que_asigno)
SELECT u.id, r.id, 'admin' FROM usuario u, rol r WHERE u.username = 'jperez' AND r.nombre_rol = 'ESPECIALISTA';

INSERT INTO usuario_rol (usuario_id, rol_id, usuario_que_asigno)
SELECT u.id, r.id, 'admin' FROM usuario u, rol r WHERE u.username = 'agomez' AND r.nombre_rol = 'RECEPCIONISTA';

INSERT INTO usuario_rol (usuario_id, rol_id, usuario_que_asigno)
SELECT u.id, r.id, 'admin' FROM usuario u, rol r WHERE u.username = 'clopez' AND r.nombre_rol = 'TECNICO';

-- ============================================
-- Servicios básicos
-- ============================================

INSERT INTO servicio (codigo_servicio, nombre_servicio, tipo_servicio, costo_base, estado) VALUES
    ('SERV001', 'Consulta Medicina General', 'consulta', 50.00, 1),
    ('SERV002', 'Consulta Cardiología', 'consulta', 80.00, 1),
    ('SERV003', 'Examen de Sangre', 'examen', 30.00, 1),
    ('SERV004', 'Radiografía', 'examen', 40.00, 1),
    ('SERV005', 'Electrocardiograma', 'examen', 35.00, 1);

-- ============================================
-- Proveedores básicos
-- ============================================

INSERT INTO proveedor (
    razon_social,
    ruc,
    direccion,
    telefono,
    email,
    contacto_nombre,
    contacto_telefono,
    estado
) VALUES
    (
        'Distribuidora Médica SAC',
        '20100070970',
        'Av. Salud 123, Lima',
        '987654321',
        'ventas@distribuidoramedica.pe',
        'Carlos Ramírez',
        '987654322',
        1
    ),
    (
        'Farmacéutica Nacional S.A.',
        '20512345678',
        'Jr. Medicina 456, Lima',
        '912345678',
        'contacto@farmaceuticanacional.pe',
        'Lucía Torres',
        '912345679',
        1
    );

-- ============================================
-- Seguros
-- ============================================

INSERT INTO seguro (tipo_seguro, nombre_aseguradora, codigo_plan, numero_poliza, estado, fecha_inicio) VALUES
    ('EsSalud', 'EsSalud', 'ESSALUD-BASICO', 'ESS-001', 1, '2026-01-01'),
    ('Privado', 'Rímac Seguros', 'RIMAC-SALUD', 'RIM-001', 1, '2026-01-01'),
    ('Privado', 'Pacífico Seguros', 'PACIFICO-VITAL', 'PAC-001', 1, '2026-01-01');

-- ============================================
-- Coberturas de ejemplo
-- ============================================

INSERT INTO cobertura (seguro_id, servicio_id, porcentaje_cobertura, monto_maximo, copago_fijo, estado, fecha_inicio) VALUES
    (1, 1, 100.0, 0.0, 0.0, 1, '2026-01-01'),  -- EsSalud cubre 100% consulta general
    (1, 2, 80.0, 500.0, 10.0, 1, '2026-01-01'), -- EsSalud cubre 80% cardiología
    (2, 1, 90.0, 0.0, 5.0, 1, '2026-01-01'),   -- Rímac cubre 90% consulta general
    (2, 3, 85.0, 200.0, 8.0, 1, '2026-01-01'); -- Rímac cubre 85% examen de sangre

-- ============================================
-- FIN DE DATOS INICIALES
-- ============================================