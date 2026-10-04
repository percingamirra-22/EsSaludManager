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
│ └── scripts/
│ ├── create_tables.sql # Esquema completo (tablas + índices)
│ ├── insert_initial_data.sql # Datos iniciales
│ ├── migrate_v1.sql # Migraciones futuras
│ └── ejecutar_schema.py # Script de inicialización
├── src/
│ ├── modelos/ # Entidades de dominio (PENDIENTE)
│ ├── repositorios/ # Acceso a datos (COMPLETADO)
│ │ ├── base_repository.py
│ │ ├── usuario_repository.py
│ │ ├── auditoria_repository.py
│ │ ├── paciente_repository.py
│ │ ├── historial_repository.py
│ │ ├── cita_repository.py
│ │ └── medicamento_repository.py
│ ├── servicios/ # Lógica de negocio (PENDIENTE)
│ ├── gui/ # Interfaz de usuario (PENDIENTE)
│ └── utils/ # Utilidades
│ ├── database.py # Singleton de conexión SQLite
│ ├── validaciones.py # Validaciones de datos (PENDIENTE)
│ ├── seguridad.py # Hash, RBAC (PENDIENTE)
│ ├── configuracion.py # Configuración global (PENDIENTE)
│ └── logger.py # Logger centralizado (PENDIENTE)
├── tests/ # Pruebas unitarias (PENDIENTE)
├── docs/ # Documentación
│ ├── requerimientos.md
│ ├── diagrama_clases.plantuml
│ ├── modelo_ere.md # Modelo ERE + relacional
│ ├── manual_usuario.md # (PENDIENTE)
│ └── manual_tecnico.md # (PENDIENTE)
├── requirements.txt
├── main.py
├── README.md
└── setup.py
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