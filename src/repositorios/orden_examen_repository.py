"""
Repositorio para órdenes de examen y exámenes solicitados.
"""

from typing import Any

from .base_repository import BaseRepository


class OrdenExamenRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para las entidades OrdenExamen y ExamenSolicitado.

    Métodos específicos:
    - find_by_paciente(): Lista órdenes de un paciente.
    - find_by_especialista(): Lista órdenes emitidas por un especialista.
    - agregar_examen_solicitado(): Asocia un examen a una orden.
    - obtener_examenes_solicitados(): Lista exámenes de una orden.
    - cambiar_estado(): Actualiza el estado de una orden.
    """

    def __init__(self) -> None:
        super().__init__("orden_examen")

    def find_by_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista órdenes de examen de un paciente."""
        query = """
            SELECT * FROM orden_examen
            WHERE paciente_id = ?
            ORDER BY fecha_orden DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (paciente_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_especialista(
        self,
        especialista_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista órdenes emitidas por un especialista."""
        query = """
            SELECT * FROM orden_examen
            WHERE especialista_id = ?
            ORDER BY fecha_orden DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (especialista_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def agregar_examen_solicitado(
        self,
        orden_examen_id: int,
        examen_id: int,
    ) -> int:
        """Asocia un examen médico a una orden."""
        query = """
            INSERT INTO examen_solicitado (orden_examen_id, examen_id)
            VALUES (?, ?)
        """
        cursor = self._db.execute_query(
            query,
            (orden_examen_id, examen_id),
        )
        self._db.commit()

        return int(cursor.lastrowid or 0)

    def obtener_examenes_solicitados(
        self,
        orden_examen_id: int,
    ) -> list[dict[str, Any]]:
        """Lista los exámenes solicitados en una orden."""
        query = """
            SELECT em.*
            FROM examen_medico em
            INNER JOIN examen_solicitado es ON em.id = es.examen_id
            WHERE es.orden_examen_id = ?
            ORDER BY es.fecha_solicitud ASC
        """
        cursor = self._db.execute_query(query, (orden_examen_id,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def cambiar_estado(
        self,
        orden_examen_id: int,
        estado: str,
    ) -> bool:
        """Actualiza el estado de una orden de examen."""
        return self.update(
            orden_examen_id,
            {"estado": estado},
        )
