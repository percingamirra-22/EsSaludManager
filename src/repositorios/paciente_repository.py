"""
Repositorio para gestión de pacientes.
"""

from typing import Any

from .base_repository import BaseRepository


class PacienteRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Paciente.

    Métodos específicos:
    - find_by_documento(): Busca por número de documento.
    - find_by_apellidos(): Busca por apellidos (LIKE).
    - list_activos(): Lista solo pacientes activos.
    """

    def __init__(self) -> None:
        super().__init__("paciente")

    def find_by_documento(self, numero_documento: str) -> dict[str, Any] | None:
        """Busca paciente por número de documento."""
        query = "SELECT * FROM paciente WHERE numero_documento = ?"
        cursor = self._db.execute_query(query, (numero_documento,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def find_by_apellidos(
        self,
        apellidos: str,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Busca pacientes por apellidos (búsqueda parcial).

        Args:
            apellidos: Texto a buscar (ej. "Rodriguez").
            limite: Número máximo de resultados.
        """
        query = """
            SELECT * FROM paciente 
            WHERE apellidos LIKE ? 
            ORDER BY apellidos, nombres
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (f"%{apellidos}%", limite))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def list_activos(self) -> list[dict[str, Any]]:
        """Lista solo pacientes activos."""
        query = "SELECT * FROM paciente WHERE estado = 1 ORDER BY apellidos, nombres"
        cursor = self._db.execute_query(query)
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def find_by_codigo(self, codigo_paciente: str) -> dict[str, Any] | None:
        """Busca paciente por código único."""
        query = "SELECT * FROM paciente WHERE codigo_paciente = ?"
        cursor = self._db.execute_query(query, (codigo_paciente,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]
