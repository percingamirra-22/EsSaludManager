"""
Módulo de conexión a base de datos SQLite.

Implementa el patrón Singleton para garantizar una única conexión
global en toda la aplicación.
"""

import sqlite3
from pathlib import Path
from typing import Any, Self


class Database:
    """
    Singleton de conexión a SQLite.

    Uso:
        db = Database.get_instance()
        conn = db.get_connection()
        cursor = conn.execute("SELECT * FROM paciente")
    """

    _instance: Self | None = None
    _connection: sqlite3.Connection | None = None

    def __new__(cls) -> Self:
        """Crea o retorna la única instancia de Database."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Inicializa la conexión si no existe."""
        if self._connection is None:
            self._db_path = self._obtener_ruta_db()
            self._conectar()

    def _obtener_ruta_db(self) -> Path:
        """
        Obtiene la ruta absoluta a la base de datos.

        Busca en este orden:
        1. data/esalud.db (producción)
        2. data/test_esalud.db (pruebas)
        3. Lanza error si ninguna existe
        """
        # Ruta relativa desde src/utils/
        base_dir = Path(__file__).parent.parent.parent  # EsSaludManager/
        db_produccion = base_dir / "data" / "esalud.db"
        db_test = base_dir / "data" / "test_esalud.db"

        # Priorizar producción, fallback a test
        if db_produccion.exists():
            return db_produccion

        if db_test.exists():
            return db_test

        # Si ninguna existe, usar producción (se creará al conectar)
        return db_produccion

    def _conectar(self) -> None:
        """
        Establece la conexión SQLite y aplica configuraciones necesarias.

        Raises:
            RuntimeError: Si SQLite no puede abrir o configurar la conexión.
        """
        try:
            self._connection = sqlite3.connect(
                str(self._db_path),
                check_same_thread=False,  # Necesario para Tkinter (hilos)
                isolation_level=None,  # Autocommit (para triggers)
            )

            # Habilitar foreign keys (SQLite no las activa por defecto)
            self._connection.execute("PRAGMA foreign_keys = ON;")

            # Optimizaciones de rendimiento
            self._connection.execute("PRAGMA journal_mode = WAL;")
            self._connection.execute("PRAGMA synchronous = NORMAL;")
            self._connection.execute("PRAGMA cache_size = 10000;")

        except sqlite3.Error as error:
            raise RuntimeError(f"Error al conectar a SQLite: {error}") from error

    def get_connection(self) -> sqlite3.Connection:
        """
        Retorna la conexión SQLite activa.

        Returns:
            Conexión activa de SQLite.

        Raises:
            RuntimeError: Si no se puede crear la conexión.
        """
        if self._connection is None:
            self._conectar()

        if self._connection is None:
            raise RuntimeError("No se pudo establecer la conexión SQLite.")

        return self._connection

    def execute_query(self, query: str, params: tuple[Any, ...] = ()) -> sqlite3.Cursor:
        """
        Ejecuta una consulta SQL (SELECT).

        Args:
            query: Consulta SQL con placeholders (?).
            params: Parámetros para la consulta.

        Returns:
            sqlite3.Cursor: Cursor con los resultados.
        """
        conn = self.get_connection()
        cursor = conn.execute(query, params)
        return cursor

    def execute_many(self, query: str, params_list: list[tuple[Any, ...]]) -> None:
        """
        Ejecuta una consulta SQL múltiple (INSERT, UPDATE, DELETE).

        Args:
            query: Consulta SQL con placeholders (?).
            params_list: Lista de tuplas con parámetros.
        """
        conn = self.get_connection()
        conn.executemany(query, params_list)

    def commit(self) -> None:
        """Confirma la transacción actual."""
        conn = self.get_connection()
        conn.commit()

    def rollback(self) -> None:
        """Revierte la transacción actual."""
        conn = self.get_connection()
        conn.rollback()

    def close(self) -> None:
        """Cierra la conexión (solo para shutdown de la aplicación)."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @classmethod
    def reset_instance(cls) -> None:
        """
        Reinicia el singleton (útil para pruebas unitarias).

        Uso en tests:
            Database.reset_instance()
        """
        if cls._instance is not None and cls._instance._connection is not None:
            cls._instance._connection.close()
        cls._instance = None
        cls._connection = None


# Instancia global (lazy initialization)
db: Database = Database()
