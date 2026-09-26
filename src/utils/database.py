"""
Módulo de conexión a base de datos SQLite
Patrón: Singleton
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional


class Database:
    """Singleton para conexión a base de datos SQLite"""

    _instancia: Optional["Database"] = None

    def __new__(cls, db_name: str = "data/esalud.db") -> "Database":
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.db_name = db_name
        return cls._instancia

    @classmethod
    def get_instance(cls, db_name: str = "data/esalud.db") -> "Database":
        """Obtener instancia única de Database"""
        if cls._instancia is None:
            cls._instancia = cls(db_name)
        return cls._instancia

    @contextmanager
    def get_connection(self):
        """Obtener conexión a la base de datos (context manager)"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def crear_tablas(self):
        """Crear tablas si no existen (llamar al inicio)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabla Paciente
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Paciente (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigoPaciente TEXT UNIQUE NOT NULL,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    tipoDocumento TEXT CHECK(tipoDocumento IN ('DNI', 'CE', 'PAS')),
                    numeroDocumento TEXT NOT NULL,
                    fechaNacimiento DATE,
                    sexo TEXT CHECK(sexo IN ('M', 'F', 'O')),
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    estado BOOLEAN DEFAULT 1,
                    fechaRegistro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    usuarioRegistro TEXT
                )
            """)

            # Tabla Usuario
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    empleadoId INTEGER,
                    username TEXT UNIQUE NOT NULL,
                    passwordHash TEXT NOT NULL,
                    email TEXT,
                    estado BOOLEAN DEFAULT 1,
                    fechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    fechaUltimoAcceso DATETIME
                )
            """)

            # Índices para búsquedas rápidas
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_paciente_documento ON Paciente(numeroDocumento)"
            )
            cursor.execute(
                "CREATE INDEX IF NOT EXISTS idx_usuario_username ON Usuario(username)"
            )
