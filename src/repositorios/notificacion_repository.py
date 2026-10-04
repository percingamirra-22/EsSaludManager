"""
Repositorio para gestión de notificaciones.
"""

from typing import Any

from .base_repository import BaseRepository


class NotificacionRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Notificacion.

    Métodos específicos:
    - find_by_paciente(): Lista notificaciones de un paciente.
    - find_by_cita(): Lista notificaciones de una cita.
    - marcar_enviada(): Marca una notificación como enviada.
    - marcar_fallida(): Marca una notificación como fallida.
    """

    def __init__(self) -> None:
        super().__init__("notificacion")

    def find_by_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista notificaciones de un paciente."""
        query = """
            SELECT * FROM notificacion
            WHERE paciente_id = ?
            ORDER BY fecha_envio DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (paciente_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_cita(self, cita_id: int) -> list[dict[str, Any]]:
        """Lista notificaciones asociadas a una cita."""
        query = """
            SELECT * FROM notificacion
            WHERE cita_id = ?
            ORDER BY fecha_envio DESC
        """
        cursor = self._db.execute_query(query, (cita_id,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def marcar_enviada(self, notificacion_id: int) -> bool:
        """Marca una notificación como enviada."""
        return self.update(
            notificacion_id,
            {"estado": "enviada"},
        )

    def marcar_fallida(self, notificacion_id: int) -> bool:
        """Marca una notificación como fallida."""
        return self.update(
            notificacion_id,
            {"estado": "fallida"},
        )
