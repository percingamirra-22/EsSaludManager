# EsSaludManager
Sistema de gestión para establecimientos de salud (EsSalud). En este caso, para el Policlínico Juan José Rodríguez Lazo - Curso Lenguajes de Programación

## Descripción
Aplicación de escritorio para la gestión de:
- Historial clínico de pacientes
- Citas y exámenes médicos
- Medicamentos y stock
- Proveedores y trazabilidad
- Coberturas de seguros
- Facturación y pagos
- Seguridad y control de accesos

## Estado del proyecto
- [x] Estructura del proyecto
- [x] Modelado ERE y relacional
- [x] Base de datos SQLite (esquema + índices)
- [x] Repositorios (capa de datos)
- [x] Modelos
- [x] Servicios
- [ ] GUI
- [ ] Pruebas
- [ ] Documentación

## Instalación

### Requisitos
- Python 3.10 o superior
- Windows 10/11
- Git (para clonar el repositorio)

### Pasos
``` En Git Bash
# 1. Clonar el repositorio
git clone [https://github.com/percingamirra-22/EsSaludManager.git](https://github.com/percingamirra-22/EsSaludManager.git)

# 2. Entrar al directorio
cd EsSaludManager

# 3. Crear entorno virtual
python -m venv .venv

# 4. Activar entorno virtual (Windows)
.venv\Scripts\activate

# 5. Instalar dependencias
pip install -r requirements.txt
```

## Inicialización de la base de datos

Antes de ejecutar la aplicación, debes crear la base de datos:

```bash
# Con el entorno virtual activado
python data/scripts/ejecutar_schema.py
```

Esto creará:
- `data/esalud.db` (base de datos de producción)
- Todas las tablas, índices y datos iniciales (roles, permisos, usuario admin)

**Opcional**: Crear base de datos de pruebas:
```bash
python data/scripts/ejecutar_schema.py --test
```

## Ejecución
``` En Git Bash
# Con entorno virtual activado
python main.py
```

## Pruebas
``` En Git Bash
# Ejecutar todas las pruebas
python -m unittest discover tests

# Con cobertura de código
coverage run -m unittest discover tests
coverage report
```

## Estructura del proyecto
``` 
EsSaludManager/
├── data/ # Capa de datos
│ ├── esalud.db # Base de datos SQLite (producción)
│ ├── test_esalud.db # Base de datos SQLite (pruebas)
│ ├── __init__.py
│ └── scripts/
│   ├── create_tables.sql # Esquema completo (tablas + índices)
│   ├── insert_initial_data.sql # Datos iniciales
│   ├── migrate_v1.sql # Migraciones futuras
│   └── ejecutar_schema.py # Script de inicialización
├── src/
│ ├── modelos/ # Entidades de dominio (PENDIENTE)
│ │ ├── __init__.py
│ │ ├── auditoria.py
│ │ ├── cita.py
│ │ ├── cobertura.py
│ │ ├── consulta.py
│ │ ├── empleado.py
│ │ ├── entrada_historial.py
│ │ ├── especialista.py
│ │ ├── examen_medico.py
│ │ ├── factura.py
│ │ ├── gerente.py
│ │ ├── historial_clinico.py
│ │ ├── item_factura.py
│ │ ├── item_receta.py
│ │ ├── lote_medicamento.py
│ │ ├── medicamento.py
│ │ ├── movimiento_medicamento.py
│ │ ├── notificacion.py
│ │ ├── orden_examen.py
│ │ ├── paciente.py
│ │ ├── pago.py
│ │ ├── permiso.py
│ │ ├── proveedor.py
│ │ ├── recepcionista.py
│ │ ├── receta_medica.py
│ │ ├── reporte.py
│ │ ├── rol.py
│ │ ├── seguro.py
│ │ ├── servicio.py
│ │ ├── sesion.py
│ │ ├── tecnico.py
│ │ ├── usuario_rol.py
│ │ └── usuario.py
│ ├── repositorios/ # Acceso a datos (COMPLETADO)
│ │ ├── __init__.py
│ │ ├── auditoria_repository.py
│ │ ├── base_repository.py
│ │ ├── cita_repository.py
│ │ ├── cobertura_repository.py
│ │ ├── examen_medico_repository.py
│ │ ├── factura_repository.py
│ │ ├── historial_repository.py
│ │ ├── lote_medicamento_repository.py
│ │ ├── medicamento_repository.py
│ │ ├── movimiento_medicamento_repository.py
│ │ ├── notificacion_repository.py
│ │ ├── orden_examen_repository.py
│ │ ├── paciente_repository.py
│ │ ├── receta_repository.py
│ │ ├── reporte_repository.py
│ │ ├── seguro_repository.py
│ │ └── usuario_repository.py
│ ├── servicios/ # Lógica de negocio (PENDIENTE)
│ │ ├── __init__.py
│ │ ├── auditoria_service.py
│ │ ├── cita_service.py
│ │ ├── cobertura_service.py
│ │ ├── examen_medico_service.py
│ │ ├── factura_service.py
│ │ ├── historial_service.py
│ │ ├── medicamento_service.py
│ │ ├── notificacion_service.py
│ │ ├── paciente_service.py
│ │ ├── pago_service.py
│ │ ├── receta_service.py
│ │ ├── reporte_service.py
│ │ ├── seguro_service.py
│ │ └── usuario_service.py
│ ├── gui/ # Interfaz de usuario (PENDIENTE)
│ │ ├── __init__.py
│ │ ├── componentes/
│ │ │ └── __init__.py
│ │ ├── formularios/
│ │ │ └── __init__.py
│ │ └── ventanas/
│ │   ├── __init__.py
│ │   ├── ventana_citas.py
│ │   ├── ventana_historial.py
│ │   ├── ventana_medicamentos.py
│ │   └── ventana_principal.py
│ ├── utils/ # Utilidades
│ │ ├── __init__.py
│ │ ├── database.py # Singleton de conexión SQLite
│ │ ├── validaciones.py # Validaciones de datos (PENDIENTE)
│ │ ├── seguridad.py # Hash, RBAC (PENDIENTE)
│ │ ├── configuracion.py # Configuración global (PENDIENTE)
│ │ └── logger.py # Logger centralizado (PENDIENTE)
│ ├── tests/ # Pruebas unitarias (PENDIENTE)
│ │ ├── __init__.py
│ │ ├── test_backend.py
│ │ ├── test_modelos.py
│ │ ├── test_seguridad.py
│ │ ├── test_servicios.py
│ │ └── test_validaciones.py
│ ├── __init__.py
│ └── app.py
├── docs/ # Documentación
│ ├── requerimientos.md
│ ├── diagrama_clases.plantuml
│ ├── modelo_ere.md # Modelo ERE + relacional
│ ├── manual_usuario.md # (PENDIENTE)
│ └── manual_tecnico.md # (PENDIENTE)
├── .gitattributes
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
└── setup.py # (PENDIENTE)
``` 

## Equipo
- **Miembro 1**: Backend, BD, Repositorios, Integración
  - Responsable: Percing Amir Rodriguez Arce
  - Estado: COMPLETADO
  - Entregables:
    - Modelo ERE y relacional (40 tablas, 50 índices)
    - Script de inicialización (`ejecutar_schema.py`)
    - Singleton de conexión (`database.py`)
    - 7 repositorios implementados y probados

- **Miembro 2**: Modelos, Servicios
  - Responsable: Piero Garay Sarango Alexander
  - Estado: COMPLETADO
  - Entregables:
    - Modelos de dominio para pacientes, historial clínico, citas, empleados, usuarios, medicamentos, coberturas, facturación y pagos.
    - Repositorios adicionales para lotes, movimientos, recetas, coberturas, facturas, pagos, notificaciones, órdenes y exámenes médicos.
    - Servicios de negocio para pacientes, historial, usuarios, auditoría, citas, medicamentos, reportes, seguros, coberturas, recetas, facturación, pagos, notificaciones y exámenes.
    - Validaciones de negocio integradas con `src/utils/validaciones.py`.
    - Pruebas manuales integrales de modelos y servicios.

- **Miembro 3**: GUI
-> Responsable: Anderson Daniel Luque Rivera

- **Miembro 4**: Pruebas
-> Responsable: Damaris Jarumy Vilca Lingan

## Documentación técnica
- [Modelo ERE y Relacional](docs/modelo_ere.md)
- [Diagrama de Clases UML](docs/diagrama_clases.plantuml)
- [Requerimientos Funcionales](docs/requerimientos.md)

## Licencia
Licencia MIT

## Contacto
Para consultas, crear un issue en GitHub.
