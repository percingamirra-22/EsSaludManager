"""
Repositorio para gestión de seguros y asignaciones a pacientes.
"""

from typing import Any

from .base_repository import BaseRepository


class SeguroRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para las entidades Seguro y PacienteSeguro.

    Métodos específicos:
    - find_by_poliza(): Busca seguro por número de póliza.
    - asignar_a_paciente(): Asigna un seguro a un paciente.
    - obtener_seguro_de_paciente(): Obtiene el seguro activo de un paciente.
    - desasignar_de_paciente(): Desactiva la asignación paciente-seguro.
    """

    def __init__(self) -> None:
        super().__init__("seguro")

    def find_by_poliza(self, numero_poliza: str) -> dict[str, Any] | None:
        """Busca un seguro por número de póliza."""
        query = "SELECT * FROM seguro WHERE numero_poliza = ?"
        cursor = self._db.execute_query(query, (numero_poliza,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def asignar_a_paciente(
        self,
        paciente_id: int,
        seguro_id: int,
    ) -> int:
        """Asigna un seguro a un paciente."""
        query = """
            INSERT INTO paciente_seguro (paciente_id, seguro_id)
            VALUES (?, ?)
        """
        cursor = self._db.execute_query(query, (paciente_id, seguro_id))
        self._db.commit()

        return int(cursor.lastrowid or 0)

    def obtener_seguro_de_paciente(
        self,
        paciente_id: int,
    ) -> dict[str, Any] | None:
        """Obtiene el seguro activo de un paciente."""
        query = """
            SELECT s.*
            FROM seguro s
            INNER JOIN paciente_seguro ps ON s.id = ps.seguro_id
            WHERE ps.paciente_id = ?
              AND ps.estado = 1
              AND s.estado = 1
            LIMIT 1
        """
        cursor = self._db.execute_query(query, (paciente_id,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def desasignar_de_paciente(
        self,
        paciente_id: int,
        seguro_id: int,
    ) -> bool:
        """Desactiva la asignación de un seguro a un paciente."""
        query = """
            UPDATE paciente_seguro
            SET estado = 0
            WHERE paciente_id = ? AND seguro_id = ?
        """
        cursor = self._db.execute_query(query, (paciente_id, seguro_id))
        self._db.commit()

        return cursor.rowcount > 0
