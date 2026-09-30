# Modelo Entidad-Relación Extendido (ERE) - EsSaludManager

## Descripción

Este documento describe el modelo conceptual ERE del sistema EsSaludManager, derivado del diagrama de clases UML 2.5.1+. El modelo fue normalizado hasta 3NF y transformado al modelo relacional implementado en SQLite.

**Nota**: En el modelo ERE no se especifican tipos de datos, solo nombres de atributos y dominios.

---

## Entidades

### Dominio 1: Pacientes y seguros

#### Entidad: Paciente
- **Clave primaria**: `id`
- **Atributos**:
  - `codigoPaciente` (único)
  - `nombres`
  - `apellidos`
  - `tipoDocumento` (dominio: {DNI, CE, PAS})
  - `numeroDocumento` (único)
  - `fechaNacimiento`
  - `sexo` (dominio: {M, F, O})
  - `telefono`
  - `email`
  - `direccion`
  - `estado` (default: activo)
  - `fechaRegistro`
  - `usuarioRegistro`

#### Entidad: Seguro
- **Clave primaria**: `id`
- **Atributos**:
  - `tipoSeguro` (dominio: {EsSalud, Privado})
  - `nombreAseguradora`
  - `codigoPlan`
  - `numeroPoliza` (único)
  - `estado` (default: activo)
  - `fechaInicio`
  - `fechaFin`

---

### Dominio 2: Historial clínico

#### Entidad: HistorialClinico
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente
- **Atributos**:
  - `numeroHistoria` (único)
  - `fechaApertura`
  - `estado` (dominio: {activo, cerrado, desactivado})
  - `version`
  - `fechaUltimaModificacion`
  - `usuarioUltimaModificacion`

#### Entidad: EntradaHistorial
- **Clave primaria**: `id`
- **Claves foráneas**: `historialId` → HistorialClinico
- **Atributos**:
  - `tipoEntrada` (dominio: {nota, diagnóstico, tratamiento, examen, receta})
  - `contenido`
  - `fechaRegistro`
  - `usuarioRegistro`
  - `version`
  - `estado` (dominio: {activa, desactivada})

#### Entidad: Auditoria
- **Clave primaria**: `id`
- **Claves foráneas**: `usuarioId` → Usuario, `empleadoId` → Empleado
- **Atributos**:
  - `accion`
  - `recurso`
  - `recursoId`
  - `fechaAccion`
  - `ipOrigen`
  - `detalles`
  - `estado` (default: activo)

---

### Dominio 3: Servicios, citas y exámenes

#### Entidad: Servicio
- **Clave primaria**: `id`
- **Atributos**:
  - `codigoServicio` (único)
  - `nombreServicio`
  - `tipoServicio` (dominio: {consulta, examen, procedimiento})
  - `costoBase`
  - `estado` (default: activo)
  - `fechaRegistro`

#### Entidad: Consulta
- **Clave primaria**: `id` (también FK a Servicio)
- **Claves foráneas**: `servicioId` → Servicio, `especialistaId` → Especialista
- **Atributos**:
  - `duracion` (minutos)
  - `requierePreparacion`

#### Entidad: OrdenExamen
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente, `especialistaId` → Especialista
- **Atributos**:
  - `fechaOrden`
  - `estado` (dominio: {pendiente, completada, cancelada})
  - `observaciones`

#### Entidad: ExamenSolicitado (entidad asociativa)
- **Clave primaria**: `id`
- **Claves foráneas**: `ordenExamenId` → OrdenExamen, `examenId` → ExamenMedico
- **Atributos**:
  - `fechaSolicitud`

#### Entidad: ExamenMedico
- **Clave primaria**: `id` (también FK a Servicio)
- **Claves foráneas**: `servicioId` → Servicio, `ordenExamenId` → OrdenExamen, `tecnicoId` → Tecnico
- **Atributos**:
  - `tipoExamen`
  - `fechaRealizacion`
  - `resultado`
  - `archivoResultado`
  - `estado` (dominio: {programado, en proceso, completado, cancelado})

#### Entidad: Cita
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente, `recepcionistaId` → Recepcionista, `servicioId` → Servicio
- **Atributos**:
  - `fechaInicio`
  - `fechaFin`
  - `estado` (dominio: {programada, completada, cancelada, reprogramada})
  - `motivo`
  - `observaciones`
  - `fechaCreacion`
  - `usuarioCreacion`
  - `fechaUltimaModificacion`
  - `usuarioUltimaModificacion`

#### Entidad: Notificacion
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente, `citaId` → Cita
- **Atributos**:
  - `tipoNotificacion` (dominio: {recordatorio_cita, recordatorio_examen})
  - `mensaje`
  - `fechaEnvio`
  - `estado` (dominio: {pendiente, enviada, fallida})
  - `canal` (dominio: {sms, email})

---

### Dominio 4: Empleados y roles

#### Entidad: Empleado
- **Clave primaria**: `id`
- **Atributos**:
  - `codigoEmpleado` (único)
  - `nombres`
  - `apellidos`
  - `tipoDocumento` (dominio: {DNI, CE, PAS})
  - `numeroDocumento` (único)
  - `telefono`
  - `email`
  - `direccion`
  - `fechaContratacion`
  - `estado` (default: activo)
  - `fechaRegistro`
  - `fechaDespido`
  - `usuarioRegistro`

#### Entidad: Especialista
- **Clave primaria**: `id` (también FK a Empleado)
- **Claves foráneas**: `empleadoId` → Empleado
- **Atributos**:
  - `especialidad`
  - `numeroColegiatura` (único)

#### Entidad: HorarioEspecialista (atributo multivaluado convertido)
- **Clave primaria**: `id`
- **Claves foráneas**: `especialistaId` → Especialista
- **Atributos**:
  - `diaSemana` (dominio: 0-6)
  - `horaInicio`
  - `horaFin`
  - `estado` (default: activo)

#### Entidad: Gerente
- **Clave primaria**: `id` (también FK a Empleado)
- **Claves foráneas**: `empleadoId` → Empleado
- **Atributos**:
  - `area`
  - `nivelGerencial`

#### Entidad: Recepcionista
- **Clave primaria**: `id` (también FK a Empleado)
- **Claves foráneas**: `empleadoId` → Empleado
- **Atributos**:
  - `turno` (dominio: {Mañana, Tarde, Noche})
  - `moduloAtencion`

#### Entidad: Tecnico
- **Clave primaria**: `id` (también FK a Empleado)
- **Claves foráneas**: `empleadoId` → Empleado
- **Atributos**:
  - `especialidadTecnica`
  - `areaTrabajo`

#### Entidad: CertificacionTecnico (atributo multivaluado convertido)
- **Clave primaria**: `id`
- **Claves foráneas**: `tecnicoId` → Tecnico
- **Atributos**:
  - `nombreCertificacion`
  - `entidadEmisora`
  - `fechaObtencion`
  - `fechaVencimiento`
  - `estado` (default: activo)

#### Entidad: Usuario
- **Clave primaria**: `id`
- **Claves foráneas**: `empleadoId` → Empleado (único)
- **Atributos**:
  - `username` (único)
  - `passwordHash`
  - `email` (único)
  - `estado` (default: activo)
  - `fechaCreacion`
  - `fechaUltimoAcceso`

#### Entidad: Rol
- **Clave primaria**: `id`
- **Atributos**:
  - `nombreRol` (único)
  - `descripcion`
  - `estado` (default: activo)

#### Entidad: Permiso
- **Clave primaria**: `id`
- **Atributos**:
  - `codigoPermiso` (único)
  - `descripcion`
  - `recurso`
  - `accion` (dominio: {crear, leer, actualizar, eliminar, aprobar})
  - `estado` (default: activo)

#### Entidad: RolPermiso (entidad asociativa)
- **Clave primaria**: `id`
- **Claves foráneas**: `rolId` → Rol, `permisoId` → Permiso
- **Atributos**:
  - `fechaAsignacion`

#### Entidad: UsuarioRol
- **Clave primaria**: `id`
- **Claves foráneas**: `usuarioId` → Usuario, `rolId` → Rol
- **Atributos**:
  - `fechaAsignacion`
  - `estado` (default: activo)
  - `usuarioQueAsigno`

#### Entidad: Sesion
- **Clave primaria**: `id`
- **Claves foráneas**: `usuarioId` → Usuario
- **Atributos**:
  - `fechaInicio`
  - `fechaFin`
  - `ipOrigen`
  - `estado` (dominio: {activa, cerrada, expirada})

---

### Dominio 5: Medicamentos y stock

#### Entidad: Medicamento
- **Clave primaria**: `id`
- **Atributos**:
  - `codigoMedicamento` (único)
  - `nombreGenerico`
  - `nombreComercial`
  - `formaFarmaceutica`
  - `concentracion`
  - `unidadMedida`
  - `requiereReceta`
  - `stockMinimo` (default: 0)
  - `estado` (default: activo)
  - `fechaRegistro`

#### Entidad: LoteMedicamento
- **Clave primaria**: `id`
- **Claves foráneas**: `medicamentoId` → Medicamento, `proveedorId` → Proveedor
- **Atributos**:
  - `numeroLote` (único)
  - `fechaFabricacion`
  - `fechaVencimiento`
  - `cantidadInicial`
  - `cantidadActual`
  - `estado` (dominio: {activo, agotado, vencido})
  - `fechaRegistro`

#### Entidad: MovimientoMedicamento
- **Clave primaria**: `id`
- **Claves foráneas**: `loteId` → LoteMedicamento
- **Atributos**:
  - `tipoMovimiento` (dominio: {entrada, salida, ajuste})
  - `cantidad`
  - `fechaMovimiento`
  - `usuarioResponsable`
  - `motivo`
  - `documentoReferencia`

#### Entidad: Proveedor
- **Clave primaria**: `id`
- **Atributos**:
  - `razonSocial`
  - `ruc` (único)
  - `direccion`
  - `telefono`
  - `email` (único)
  - `contactoNombre`
  - `contactoTelefono`
  - `estado` (default: activo)
  - `fechaRegistro`

#### Entidad: CertificadoProveedor (atributo multivaluado convertido)
- **Clave primaria**: `id`
- **Claves foráneas**: `proveedorId` → Proveedor
- **Atributos**:
  - `tipoCertificado`
  - `numeroCertificado` (único)
  - `entidadEmisora`
  - `fechaEmision`
  - `fechaVencimiento`
  - `archivoCertificado`
  - `estado` (default: activo)

#### Entidad: RecetaMedica
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente, `especialistaId` → Especialista
- **Atributos**:
  - `fechaEmision`
  - `estado` (dominio: {activa, dispensada, cancelada})
  - `observaciones`
  - `usuarioEmisor`

#### Entidad: ItemReceta
- **Clave primaria**: `id`
- **Claves foráneas**: `recetaId` → RecetaMedica, `medicamentoId` → Medicamento
- **Atributos**:
  - `dosis`
  - `frecuencia`
  - `duracionDias`
  - `cantidadDispensada` (default: 0)
  - `estado` (dominio: {pendiente, dispensado, cancelado})

---

### Dominio 6: Coberturas

#### Entidad: Cobertura
- **Clave primaria**: `id`
- **Claves foráneas**: `seguroId` → Seguro, `servicioId` → Servicio
- **Atributos**:
  - `porcentajeCobertura` (dominio: 0.0–100.0)
  - `montoMaximo`
  - `copagoFijo`
  - `estado` (default: activo)
  - `fechaInicio`
  - `fechaFin`

---

### Dominio 7: Facturación y pagos

#### Entidad: Factura
- **Clave primaria**: `id`
- **Claves foráneas**: `pacienteId` → Paciente
- **Atributos**:
  - `numeroFactura` (único)
  - `fechaEmision`
  - `estado` (dominio: {pendiente, pagada, anulada})
  - `montoTotal` (derivado)
  - `montoCubierto` (derivado)
  - `montoPaciente` (derivado)
  - `usuarioEmisor`

#### Entidad: ItemFactura
- **Clave primaria**: `id`
- **Claves foráneas**: `facturaId` → Factura, `servicioId` → Servicio
- **Atributos**:
  - `descripcion`
  - `costo`
  - `estado` (dominio: {activo, anulado})

#### Entidad: Pago
- **Clave primaria**: `id`
- **Claves foráneas**: `facturaId` → Factura
- **Atributos**:
  - `monto`
  - `fechaPago`
  - `metodoPago` (dominio: {efectivo, tarjeta, transferencia})
  - `estado` (dominio: {registrado, conciliado})
  - `usuarioRegistro`
  - `numeroReferencia`

---

### Dominio 8: Reportes e infraestructura

#### Entidad: Reporte
- **Clave primaria**: `id`
- **Claves foráneas**: `usuarioSolicitanteId` → Usuario
- **Atributos**:
  - `tipoReporte`
  - `filtros` (formato JSON)
  - `fechaGeneracion`
  - `formato` (dominio: {PDF, CSV})
  - `rutaArchivo`

#### Entidad: Configuracion
- **Clave primaria**: `id`
- **Atributos**:
  - `clave` (único)
  - `valor`
  - `descripcion`
  - `fechaActualizacion`

#### Entidad: LogSistema
- **Clave primaria**: `id`
- **Atributos**:
  - `nivel` (dominio: {INFO, WARNING, ERROR})
  - `mensaje`
  - `fechaRegistro`
  - `modulo`

---

## Relaciones ERE

| Relación | Entidad Origen | Entidad Destino | Cardinalidad | Tipo |
|----------|----------------|-----------------|--------------|------|
| `tiene` | Paciente | Seguro | 0..* — 0..1 | Asociación opcional |
| `tiene` | Paciente | HistorialClinico | 1 — 1..* | Entidad débil |
| `contiene` | HistorialClinico | EntradaHistorial | 1 — 0..* | Entidad débil |
| `audita` | HistorialClinico | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | EntradaHistorial | Auditoria | 0..* — 0..* | Auditoría transversal |
| `es_un` | Servicio | Consulta | 1 — 0..* | Especialización total |
| `es_un` | Servicio | ExamenMedico | 1 — 0..* | Especialización total |
| `solicita` | OrdenExamen | ExamenSolicitado | 1 — 0..* | Entidad asociativa |
| `es_solicitado_en` | ExamenMedico | ExamenSolicitado | 0..* — 1 | Entidad asociativa |
| `pertenece` | Cita | Paciente | 0..* — 1 | FK |
| `requiere` | Cita | Servicio | 0..* — 1 | FK |
| `genera` | Cita | Notificacion | 1 — 0..* | Composición |
| `audita` | Cita | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | Notificacion | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | OrdenExamen | Auditoria | 0..* — 0..* | Auditoría transversal |
| `emite` | OrdenExamen | Especialista | 0..* — 1 | FK |
| `realiza` | ExamenMedico | Tecnico | 0..* — 1 | FK |
| `audita` | ExamenMedico | Auditoria | 0..* — 0..* | Auditoría transversal |
| `atiende` | Especialista | Consulta | 1 — 0..* | FK |
| `es_un` | Empleado | Especialista | 1 — 0..* | Especialización parcial, disjoint |
| `es_un` | Empleado | Gerente | 1 — 0..* | Especialización parcial, disjoint |
| `es_un` | Empleado | Recepcionista | 1 — 0..* | Especialización parcial, disjoint |
| `es_un` | Empleado | Tecnico | 1 — 0..* | Especialización parcial, disjoint |
| `pertenece` | Usuario | Empleado | 0..1 — 1 | 1:1 |
| `asigna` | UsuarioRol | Usuario | 0..* — 1 | Entidad asociativa |
| `asigna` | UsuarioRol | Rol | 0..* — 1 | Entidad asociativa |
| `contiene` | Rol | RolPermiso | 1 — 0..* | Entidad asociativa |
| `tiene` | Permiso | RolPermiso | 1 — 0..* | Entidad asociativa |
| `tiene` | Usuario | Sesion | 1 — 0..* | Composición |
| `audita` | Usuario | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | Empleado | Auditoria | 0..* — 0..* | Auditoría transversal |
| `tiene` | Especialista | HorarioEspecialista | 1 — 0..* | Atributo multivaluado |
| `tiene` | Tecnico | CertificacionTecnico | 1 — 0..* | Atributo multivaluado |
| `tiene` | Medicamento | LoteMedicamento | 1 — 0..* | Entidad débil |
| `proviene` | LoteMedicamento | Proveedor | 0..* — 1 | FK |
| `registra` | LoteMedicamento | MovimientoMedicamento | 1 — 0..* | Entidad débil |
| `tiene` | Proveedor | CertificadoProveedor | 1 — 0..* | Atributo multivaluado |
| `pertenece` | RecetaMedica | Paciente | 0..* — 1 | FK |
| `emite` | RecetaMedica | Especialista | 0..* — 1 | FK |
| `contiene` | RecetaMedica | ItemReceta | 1 — 1..* | Entidad débil |
| `referencia` | ItemReceta | Medicamento | 0..* — 1 | FK |
| `audita` | RecetaMedica | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | MovimientoMedicamento | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | LoteMedicamento | Auditoria | 0..* — 0..* | Auditoría transversal |
| `pertenece` | Cobertura | Seguro | 0..* — 1 | FK |
| `aplica` | Cobertura | Servicio | 0..* — 1 | FK |
| `pertenece` | Factura | Paciente | 0..* — 1 | FK |
| `contiene` | Factura | ItemFactura | 1 — 1..* | Entidad débil |
| `referencia` | ItemFactura | Servicio | 0..* — 1 | FK |
| `tiene` | Factura | Pago | 1 — 0..* | Composición |
| `audita` | Factura | Auditoria | 0..* — 0..* | Auditoría transversal |
| `audita` | Pago | Auditoria | 0..* — 0..* | Auditoría transversal |
| `solicitado_por` | Reporte | Usuario | 0..* — 1 | FK |
| `audita` | Reporte | Auditoria | 0..* — 0..* | Auditoría transversal |
| `usa` | LogSistema | Configuracion | 0..* — 0..* | Dependencia lógica |
| `audita` | LogSistema | Auditoria | 0..* — 0..* | Auditoría transversal |

---

## Decisiones de modelado

### 1. Entidades débiles
- `HistorialClinico` es débil respecto a `Paciente` (no existe sin paciente).
- `EntradaHistorial`, `ItemReceta`, `ItemFactura`, `MovimientoMedicamento`, `LoteMedicamento` son entidades débiles de sus padres.

### 2. Especialización/Generalización
- **Servicio → Consulta, ExamenMedico**: Especialización total (todo servicio es consulta o examen).
- **Empleado → Especialista, Gerente, Recepcionista, Tecnico**: Especialización parcial y disjoint (un empleado tiene un solo rol específico).

### 3. Atributos multivaluados convertidos a entidades
- `certificaciones` de `Tecnico` → `CertificacionTecnico`.
- `examenesSolicitados` de `OrdenExamen` → `ExamenSolicitado`.
- `horariosDisponibles` de `Especialista` → `HorarioEspecialista`.
- `certificados` de `Proveedor` → `CertificadoProveedor`.

### 4. Relaciones N:M resueltas
- `Rol` ↔ `Permiso` → `RolPermiso`.
- `Usuario` ↔ `Rol` → `UsuarioRol`.
- `OrdenExamen` ↔ `ExamenMedico` → `ExamenSolicitado`.

### 5. Atributos derivados marcados
- `montoTotal`, `montoCubierto`, `montoPaciente` en `Factura` se marcaron como derivados (se calculan desde `ItemFactura` y `Cobertura`).

---

## Modelo relacional (SQLite)
El modelo ERE fue transformado a 40 tablas SQLite con 50 índices, aplicando normalización 3NF. Ver:
- `data/scripts/create_tables.sql` (esquema completo)
- `data/scripts/insert_initial_data.sql` (datos iniciales)

---

## Referencias
- Diagrama de clases UML: `docs/diagrama_clases.plantuml`
- Requerimientos funcionales: `docs/requerimientos.md`