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
- [ ] Modelos de datos
- [ ] Repositorios
- [ ] Servicios
- [ ] GUI
- [ ] Pruebas
- [ ] Documentación

## Instalación

### Requisitos
- Python 3.9 o superior
- Windows 10/11

### Pasos
``` En Git Bash
# 1. Clonar el repositorio
git clone https://github.com/percingamirra-22/EsSaludManager.git
Se refiere a https://github.com/percingamirra-22/EsSaludManager.git

# 2. Entrar al directorio
cd EsSaludManager

# 3. Crear entorno virtual
python -m venv .venv

# 4. Activar entorno virtual (Windows)
.venv\Scripts\activate

# 5. Instalar dependencias
pip install -r requirements.txt
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
EsSaludManager/
-> data/ # Base de datos SQLite
-> src/
--> modelos/ # Entidades de dominio
--> repositorios/ # Acceso a datos (SQL)
--> servicios/ # Lógica de negocio
--> gui/ # Interfaz de usuario
--> utils/ # Utilidades
-> tests/ # Pruebas unitarias
-> docs/ # Documentación

## Equipo
- **Persona 1**: Backend, BD, Repositorios, Integración
-> Responsable: 
- **Persona 2**: Modelos, Servicios
-> Responsable: 
- **Persona 3**: GUI
-> Responsable: 
- **Persona 4**: Pruebas
-> Responsable: 

## Licencia
Sin Licencia

## Contacto
Para consultas, crear un issue en GitHub.