"""
Módulo de utilidades transversales de EsSaludManager.

Contiene:
- database: Singleton de conexión SQLite.
- validaciones: Validaciones de datos (DNI, email, etc.).
- seguridad: Hash de passwords, RBAC.
- configuracion: Configuración global (Singleton).
- logger: Logger centralizado (Singleton).
"""

from .database import Database, db

__all__ = ["Database", "db"]
