# EsSaludManager
Sistema de gestión para establecimientos de salud (EsSalud), desarrollado para el Policlínico Juan José Rodríguez Lazo en el curso **Lenguajes de Programación**.

## Descripción
EsSaludManager es una aplicación de escritorio desarrollada en Python y Tkinter para la gestión integral de un establecimiento de salud. Permite administrar pacientes, historias clínicas, citas, medicamentos, lotes, recetas, seguros, coberturas, exámenes, facturación, pagos, usuarios y auditoría.

### Módulos principales
- Gestión de pacientes.
- Historial clínico.
- Citas médicas.
- Medicamentos, lotes y control de stock.
- Proveedores y trazabilidad de medicamentos.
- Recetas médicas y dispensación.
- Seguros médicos y coberturas.
- Exámenes médicos y órdenes de examen.
- Facturación, ítems facturables y pagos.
- Notificaciones.
- Reportes en PDF.
- Usuarios, roles, permisos y auditoría.

## Estado del proyecto
- [x] Estructura del proyecto.
- [x] Modelado ERE y relacional.
- [x] Base de datos SQLite: esquema, índices y datos iniciales.
- [x] Capa de modelos de dominio.
- [x] Capa de repositorios.
- [x] Capa de servicios de negocio.
- [x] Utilidades: conexión a base de datos, validaciones, seguridad y auditoría.
- [x] Interfaz gráfica con Tkinter.
- [x] Módulos navegables desde la ventana principal.
- [x] Pruebas unitarias y de integración.
- [x] Documentación técnica.
- [x] Empaquetado y distribución con PyInstaller.

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

La aplicación crea automáticamente la base de datos si no existe al ejecutar `main.py`.

También puedes inicializarla manualmente:

```bash
python data/scripts/ejecutar_schema.py
```

Esto crea:

- `data/esalud.db`: base de datos de producción.
- Tablas, índices y restricciones.
- Datos iniciales de roles, permisos y usuario administrador.

Para reiniciar completamente la base de datos:

```bash
python data/scripts/ejecutar_schema.py --reset
```

Para crear una base de datos de pruebas:

```bash
python data/scripts/ejecutar_schema.py --test
```

## Ejecución

Con el entorno virtual activado:

```bash
python main.py
```

La aplicación iniciará mostrando la ventana de login. Después de autenticarse, se abrirá la ventana principal con acceso a los módulos del sistema.

## Pruebas

El proyecto utiliza `pytest` para pruebas unitarias y de integración.

### Instalar dependencias de prueba

```bash
python -m pip install pytest pytest-cov
```

### Ejecutar todas las pruebas

```bash
python -m pytest tests -v
```

### Ejecutar pruebas por módulo

```bash
python -m pytest tests/test_utils.py -v
python -m pytest tests/test_modelos.py -v
python -m pytest tests/test_data.py -v
python -m pytest tests/test_repositorios.py -v
python -m pytest tests/test_servicios.py -v
```

### Cobertura de código

```bash
python -m pytest tests --cov=src --cov-report=term-missing
```

## Verificación de calidad

Antes de generar el ejecutable final, ejecuta:

```bash
python -m ruff check .
python -m ruff check . --fix
python -m ruff check .
python -m compileall src tests
python -m pytest tests -v
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
│ ├── modelos/ # Entidades de dominio
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
│ ├── repositorios/ # Acceso a datos
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
│ ├── servicios/ # Lógica de negocio
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
│ ├── gui/
│ │ ├── __init__.py
│ │ ├── app.py
│ │ ├── estilos.py
│ │ ├── componentes/
│ │ │ ├── __init__.py
│ │ │ ├── boton_accion.py
│ │ │ ├── busqueda_filtro.py
│ │ │ ├── campo_formulario.py
│ │ │ ├── formulario_base.py
│ │ │ ├── panel_estado.py
│ │ │ └── tabla_datos.py
│ │ ├── formularios/
│ │ │ ├── __init__.py
│ │ │ ├── formulario_cita.py
│ │ │ ├── formulario_cobertura.py
│ │ │ ├── formulario_examen.py
│ │ │ ├── formulario_factura.py
│ │ │ ├── formulario_lote.py
│ │ │ ├── formulario_medicamento.py
│ │ │ ├── formulario_pago.py
│ │ │ ├── formulario_paciente.py
│ │ │ ├── formulario_receta.py
│ │ │ └── formulario_seguro.py
│ │ └── ventanas/
│ │   ├── __init__.py
│ │   ├── ventana_auditoria.py
│ │   ├── ventana_citas.py
│ │   ├── ventana_coberturas.py
│ │   ├── ventana_examenes.py
│ │   ├── ventana_facturas.py
│ │   ├── ventana_historial.py
│ │   ├── ventana_login.py
│ │   ├── ventana_lotes.py
│ │   ├── ventana_medicamentos.py
│ │   ├── ventana_notificaciones.py
│ │   ├── ventana_pagos.py
│ │   ├── ventana_pacientes.py
│ │   ├── ventana_principal.py
│ │   ├── ventana_recetas.py
│ │   ├── ventana_reportes.py
│ │   ├── ventana_seguros.py
│ │   └── ventana_usuarios.py
│ ├── utils/ # Utilidades
│ │ ├── __init__.py
│ │ ├── database.py # Singleton de conexión SQLite
│ │ ├── validaciones.py # Validaciones de datos
│ │ ├── seguridad.py # Hash, RBAC
│ │ ├── configuracion.py # Configuración global
│ │ └── logger.py # Logger centralizado
│ ├── tests/ # Pruebas unitarias
│ │ ├── __init__.py
│ │ ├── test_data.py
│ │ ├── test_modelos.py
│ │ ├── test_repositorios.py
│ │ ├── test_servicios.py
│ │└── test_utils.py
│ ├── __init__.py
│ └── app.py
├── docs/ # Documentación
│ ├── requerimientos.md
│ ├── diagrama_clases.plantuml
│ ├── modelo_ere.md # Modelo ERE + relacional
│ ├── manual_usuario.md
│ └── manual_tecnico.md
├── .gitattributes
├── .gitignore
├── LICENSE
├── main.py
├── README.md
└── requirements.txt
``` 

## Arquitectura

El proyecto sigue una arquitectura en capas:

| Capa | Responsabilidad |
|---|---|
| `src/gui` | Presentación, ventanas, formularios y componentes reutilizables. |
| `src/servicios` | Reglas de negocio, validaciones y coordinación de operaciones. |
| `src/repositorios` | Acceso a datos y consultas SQL. |
| `src/modelos` | Entidades de dominio y transformación entre filas y objetos. |
| `src/utils` | Conexión a base de datos, validaciones, seguridad y utilidades comunes. |
| `tests` | Pruebas unitarias y de integración. |

La interfaz gráfica no accede directamente a repositorios ni ejecuta consultas SQL. Toda operación pasa por la capa de servicios.

## Empaquetado y distribución

### Generar ejecutable en carpeta

Esta es la opción recomendada para distribución y pruebas:

```bash
python -m PyInstaller --name EsSaludManager --onedir --noconsole --clean --add-data "data;data" main.py
```

El ejecutable se genera en:

```text
dist/EsSaludManager/EsSaludManager.exe
```

### Generar ejecutable único

```bash
python -m PyInstaller --name EsSaludManager --onefile --noconsole --clean --add-data "data;data" main.py
```

El ejecutable se genera en:

```text
dist/EsSaludManager.exe
```

La primera vez que se ejecute, la aplicación creará automáticamente `data/esalud.db` junto al ejecutable si la base de datos no existe.

## Uso básico

1. Ejecutar `main.py` o `EsSaludManager.exe`.
2. Iniciar sesión con un usuario válido.
3. Navegar por los módulos desde el menú lateral.
4. Registrar y consultar pacientes, citas, medicamentos, seguros, facturas y otros recursos.
5. Generar reportes PDF desde el módulo de reportes.
6. Cerrar sesión o salir desde la ventana principal.

## Equipo

- **Miembro 1**: Backend, base de datos, repositorios e integración.  
  Responsable: Percing Amir Rodriguez Arce.  
  Estado: completado.  
  Entregables: modelo ERE y relacional, script de inicialización, singleton de conexión, repositorios y base de datos SQLite.

- **Miembro 2**: Modelos y servicios de negocio.  
  Responsable: Piero Garay Sarango Alexander.  
  Estado: completado.  
  Entregables: modelos de dominio, servicios de negocio, validaciones, integración de repositorios y pruebas manuales.

- **Miembro 3**: Interfaz gráfica.  
  Responsable: Anderson Daniel Luque Rivera.  
  Estado: completado.  
  Entregables: ventana de login, ventana principal, módulos navegables, formularios, componentes reutilizables, estilos visuales e integración con servicios.

- **Miembro 4**: Pruebas y calidad.  
  Responsable: Damaris Jarumy Vilca Lingan.  
  Estado: completado.  
  Entregables: pruebas unitarias, pruebas de integración, validación de servicios, repositorios, modelos, utilidades y recursos de datos.

## Documentación técnica

- [Modelo ERE y Relacional](docs/modelo_ere.md)
- [Diagrama de Clases UML](docs/diagrama_clases.plantuml)
- [Requerimientos Funcionales](docs/requerimientos.md)
- [Manual de Usuario](docs/manual_usuario.md)
- [Manual Técnico](docs/manual_tecnico.md)

## Licencia

Este proyecto se distribuye bajo la licencia MIT.

## Contacto

Para consultas, reportes de errores o sugerencias, crear un issue en el repositorio de GitHub.
