# REQUERIMIENTOS FUNCIONALES - EsSaludManager

## DOMINIO 1: GESTIÓN DE HISTORIAL CLÍNICO 
- **RF-HC-001**: Registrar, leer, actualizar y desactivar historial clínico con trazabilidad y versión.
- **RF-HC-002**: El sistema debe registrar en auditoría cada creación, lectura, actualización y desactivación del historial clínico, indicando usuario, fecha, acción y versión; y debe aplicar control de acceso basado en roles para operaciones de escritura.
- **RF-HC-003**: Asociar historial clínico con identidad del paciente y su seguro para validación de coberturas y facturación.

## DOMINIO 2: GESTIÓN DE CITAS (CONSULTAS Y EXÁMENES)
- **RF-CIE-001**: Crear, consultar, actualizar (reprogramar) y cancelar consultas y exámenes con verificación de disponibilidad.
- **RF-CIE-002**: Detectar conflictos horarios al crear o reprogramar consultas y exámenes, y permitir reprogramación con registro de motivo.
- **RF-CIE-003**: Registro de historial de citas y generación de recordatorios por teléfono al paciente.
- **RF-CIE-004**: El sistema debe verificar que el usuario tenga credenciales y permisos suficientes antes de permitir actualizaciones de citas o resultados de exámenes, y debe registrar la verificación en auditoría.

## DOMINIO 3: GESTIÓN DE MEDICAMENTOS Y STOCK
- **RF-MED-001**: Registrar y organizar medicamentos, con reglas de dispensa basadas en receta, dosis y pauta terapéutica.
- **RF-MED-002**: Monitorear stock de medicamentos, con trazabilidad por proveedor y lote, alerta de stock bajo y registro de compras.
- **RF-MED-003**: Asociar medicamentos a recetas médicas con control de verificación de dosis, vencimientos y presencia en stock.
- **RF-MED-004**: Registro de movimientos de medicamentos (entrada, salida, ajuste) con auditoría.

## DOMINIO 4: GESTIÓN DE PROVEEDORES Y TRAZABILIDAD
- **RF-PRV-001**: Registrar proveedores, datos de contacto y trazabilidad de suministro (lotes, fechas, certificados).
- **RF-PRV-002**: El sistema debe generar reportes de trazabilidad de medicamentos por lote y proveedor, mostrando origen, fechas de suministro y certificados asociados.

## DOMINIO 5: GESTIÓN DE COBERTURAS Y VERIFICACIÓN DE SEGUROS 
- **RF-COV-001**: Verificar cobertura de EsSalud o seguros privados al registrar servicios, citas y procedimientos.
- **RF-COV-002**: Calcular y mostrar directamente la cobertura restante, co-pago y límites por procedimiento.

## DOMINIO 6: MONITOREO DE PAGOS Y FACTURACIÓN
- **RF-PAY-001**: Registrar pagos pendientes y realizados por pacientes/seguro, asociando facturas a citas, exámenes y tratamientos.
- **RF-PAY-002**: Generar informes de morosidad y estado de cuentas, con filtros por fecha, paciente y tipo de servicio.
- **RF-PAY-003**: El sistema debe registrar en auditoría cada cobro y conciliación de pagos, indicando usuario, fecha, monto y estado de conciliación.

## DOMINIO 7: SEGURIDAD Y CONTROL DE ACCESOS
- **RF-SEC-001**: Gestión de credenciales y roles para actualizar información sensible; control de acceso basado en mínimo privilegio.
- **RF-SEC-002**: El sistema debe registrar cada sesión de usuario (inicio, cierre, IP de origen, duración).
- **RF-SEC-003**: Registro de auditoría de acciones (qué, quién, cuándo, desde dónde) para todos los cambios de datos sensibles.

## DOMINIO 8: INTERFAZ Y EXPERIENCIA DE USUARIO (GUI)
- **RF-GUI-001**: El sistema debe permitir búsquedas de información, registros de datos y navegación entre módulos (historial, citas, medicamentos, facturación) desde la interfaz de usuario.
- **RF-GUI-002**: Soportar búsquedas por paciente, historial, citas, medicamentos y facturación con resultados paginados y filtrados.
- **RF-GUI-003**: Acceso a funciones de reporte y exportación (PDF/CSV) para uso administrativo.

## DOMINIO 9: GESTIÓN DE EMPLEADOS Y CONTROL DE ACCESOS
- **RF-EMP-001**: Registrar empleados (Especialista, Gerente, Recepcionista, Técnico) con datos de identidad, contacto y rol asignado.
- **RF-EMP-002**: Asignar roles y permisos a empleados según sus funciones (p. ej., Recepcionista gestiona citas, Especialista emite recetas, Gerente genera reportes).
- **RF-EMP-003**: Verificar credenciales y permisos antes de permitir actualizaciones de información sensible (historial clínico, citas, resultados, medicamentos).
- **RF-EMP-004**: Registrar en auditoría cada acción realizada por empleados (qué, quién, cuándo, desde dónde) para garantizar trazabilidad.
- **RF-EMP-005**: Permitir que cada tipo de empleado realice sus funciones específicas:
  - **Recepcionista**: Registrar y gestionar citas, enviar recordatorios.
  - **Especialista**: Emitir órdenes de examen, recetas, realizar consultas.
  - **Técnico**: Realizar exámenes médicos, registrar resultados.
  - **Gerente**: Generar reportes administrativos, aprobar solicitudes.
- **RF-EMP-006**: Gestionar sesiones de usuario asociadas a empleados (inicio, cierre, IP de origen, duración).
