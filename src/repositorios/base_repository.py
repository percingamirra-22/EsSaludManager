"""
Repositorio base con operaciones CRUD genéricas.

Todas las clases repository heredarán de esta para evitar
código repetido en cada repositorio específico.
"""

from abc import ABC
from typing import Any, Generic, TypeVar

from src.utils.database import db

# Tipo genérico para entidades (diccionarios con estructura definida)
EntityT = TypeVar("EntityT", bound=dict[str, Any])


class BaseRepository(ABC, Generic[EntityT]):
    """
    Clase base abstracta para repositorios.

    Proporciona métodos CRUD genéricos que pueden ser
    reutilizados por todos los repositorios específicos.

    Uso:
        class PacienteRepository(BaseRepository[Paciente]):
            def __init__(self):
                super().__init__("paciente")
    """

    def __init__(self, table_name: str) -> None:
        """
        Inicializa el repositorio.

        Args:
            table_name: Nombre de la tabla en la base de datos.
        """
        self._table_name = table_name
        self._db = db

    @property
    def table_name(self) -> str:
        """Retorna el nombre de la tabla."""
        return self._table_name

    def create(self, data: EntityT) -> int:
        """
        Crea un nuevo registro en la tabla.

        Args:
            data: Diccionario con los datos del registro.

        Returns:
            int: ID del registro creado.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO {self._table_name} ({columns}) VALUES ({placeholders})"

        self._db.execute_query(query, values)
        self._db.commit()

        # Obtener el ID del registro creado
        cursor = self._db.execute_query("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]  # type: ignore[no-any-return]

    def read(self, record_id: int) -> EntityT | None:
        """
        Lee un registro por su ID.

        Args:
            record_id: ID del registro a leer.

        Returns:
            EntityT | None: Diccionario con los datos o None si no existe.
        """
        query = f"SELECT * FROM {self._table_name} WHERE id = ?"
        cursor = self._db.execute_query(query, (record_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        # Convertir fila a diccionario
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def update(self, record_id: int, data: EntityT) -> bool:
        """
        Actualiza un registro existente.

        Args:
            record_id: ID del registro a actualizar.
            data: Diccionario con los datos a actualizar.

        Returns:
            bool: True si se actualizó, False si no existe.
        """
        if not data:
            return False

        set_clause = ", ".join([f"{key} = ?" for key in data])
        values = tuple(data.values()) + (record_id,)

        query = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"

        cursor = self._db.execute_query(query, values)
        self._db.commit()

        return cursor.rowcount > 0

    def delete(self, record_id: int) -> bool:
        """
        Elimina un registro por su ID.

        Args:
            record_id: ID del registro a eliminar.

        Returns:
            bool: True si se eliminó, False si no existe.
        """
        query = f"DELETE FROM {self._table_name} WHERE id = ?"

        cursor = self._db.execute_query(query, (record_id,))
        self._db.commit()

        return cursor.rowcount > 0

    def list_all(self) -> list[EntityT]:
        """
        Lista todos los registros de la tabla.

        Returns:
            list[EntityT]: Lista de diccionarios con los datos.
        """
        query = f"SELECT * FROM {self._table_name} ORDER BY id"
        cursor = self._db.execute_query(query)
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def find_by_id(self, record_id: int) -> EntityT | None:
        """
        Busca un registro por su ID (alias de read).

        Args:
            record_id: ID del registro a buscar.

        Returns:
            EntityT | None: Diccionario con los datos o None si no existe.
        """
        return self.read(record_id)

    def count(self) -> int:
        """
        Cuenta el número total de registros en la tabla.

        Returns:
            int: Número de registros.
        """
        query = f"SELECT COUNT(*) FROM {self._table_name}"
        cursor = self._db.execute_query(query)
        return cursor.fetchone()[0]  # type: ignore[no-any-return]

    def exists(self, record_id: int) -> bool:
        """
        Verifica si un registro existe.

        Args:
            record_id: ID del registro a verificar.

        Returns:
            bool: True si existe, False si no.
        """
        query = f"SELECT 1 FROM {self._table_name} WHERE id = ? LIMIT 1"
        cursor = self._db.execute_query(query, (record_id,))
        return cursor.fetchone() is not None
