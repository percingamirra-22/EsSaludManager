"""
Módulo de utilidades transversales de EsSaludManager.

Contiene:
- database: Singleton de conexión SQLite.
- validaciones: Validaciones de datos (DNI, email, etc.).
- seguridad: Hash de passwords, RBAC.
- configuracion: Configuración global (Singleton).
- logger: Logger centralizado (Singleton).
"""

from .configuracion import Configuracion, configuracion
from .database import Database, db
from .logger import LogSistema, logger

__all__ = [
    "Configuracion",
    "Database",
    "LogSistema",
    "configuracion",
    "db",
    "logger",
]
