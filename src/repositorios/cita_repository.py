"""
Repositorio para gestión de citas médicas.
"""

from typing import Any

from .base_repository import BaseRepository


class CitaRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Cita.

    Métodos específicos:
    - find_by_paciente(): Obtiene citas de un paciente.
    - find_by_fecha(): Obtiene citas en un rango de fechas.
    - verificar_colisiones(): Verifica si hay conflicto de horarios.
    - reprogramar(): Reprograma una cita existente.
    """

    def __init__(self) -> None:
        super().__init__("cita")

    def find_by_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Obtiene citas de un paciente."""
        query = """
            SELECT * FROM cita 
            WHERE paciente_id = ? 
            ORDER BY fecha_inicio DESC 
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (paciente_id, limite))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def find_by_fecha(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        especialista_id: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Obtiene citas en un rango de fechas.

        Args:
            fecha_inicio: Fecha inicio (YYYY-MM-DD).
            fecha_fin: Fecha fin (YYYY-MM-DD).
            especialista_id: Filtrar por especialista (opcional).
        """
        query = """
            SELECT * FROM cita 
            WHERE fecha_inicio >= ? AND fecha_inicio <= ?
        """
        params: list[Any] = [fecha_inicio, fecha_fin]

        if especialista_id is not None:
            query += " AND servicio_id IN (SELECT id FROM consulta WHERE especialista_id = ?)"
            params.append(especialista_id)

        query += " ORDER BY fecha_inicio"

        cursor = self._db.execute_query(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def verificar_colisiones(
        self,
        servicio_id: int,
        fecha_inicio: str,
        fecha_fin: str,
        cita_id_excluida: int | None = None,
    ) -> bool:
        """
        Verifica si hay colisión de horarios para un servicio.

        Args:
            servicio_id: ID del servicio (especialista).
            fecha_inicio: Fecha inicio de la cita.
            fecha_fin: Fecha fin de la cita.
            cita_id_excluida: ID de cita a excluir (para reprogramación).

        Returns:
            bool: True si hay colisión, False si está disponible.
        """
        query = """
            SELECT COUNT(*) FROM cita 
            WHERE servicio_id = ? 
            AND estado IN ('programada', 'reprogramada')
            AND (
                (fecha_inicio >= ? AND fecha_inicio < ?)
                OR (fecha_fin > ? AND fecha_fin <= ?)
                OR (fecha_inicio <= ? AND fecha_fin >= ?)
            )
        """
        params: list[Any] = [
            servicio_id,
            fecha_inicio,
            fecha_fin,
            fecha_inicio,
            fecha_fin,
            fecha_inicio,
            fecha_fin,
        ]

        if cita_id_excluida is not None:
            query += " AND id != ?"
            params.append(cita_id_excluida)

        cursor = self._db.execute_query(query, tuple(params))
        count = cursor.fetchone()[0]

        return count > 0  # type: ignore[no-any-return]

    def reprogramar(
        self,
        cita_id: int,
        nueva_fecha_inicio: str,
        nueva_fecha_fin: str,
        motivo: str,
        usuario_modificacion: str,
    ) -> bool:
        """
        Reprograma una cita existente.

        Args:
            cita_id: ID de la cita a reprogramar.
            nueva_fecha_inicio: Nueva fecha de inicio.
            nueva_fecha_fin: Nueva fecha de fin.
            motivo: Motivo de la reprogramación.
            usuario_modificacion: Username del usuario que reprograma.

        Returns:
            bool: True si se reprogramó, False si no existe o hay colisión.
        """
        # Verificar colisiones
        cita_actual = self.read(cita_id)
        if cita_actual is None:
            return False

        servicio_id = cita_actual["servicio_id"]

        if self.verificar_colisiones(
            servicio_id,
            nueva_fecha_inicio,
            nueva_fecha_fin,
            cita_id_excluida=cita_id,
        ):
            return False

        # Actualizar cita
        data: dict[str, Any] = {
            "fecha_inicio": nueva_fecha_inicio,
            "fecha_fin": nueva_fecha_fin,
            "motivo": motivo,
            "estado": "reprogramada",
            "fecha_ultima_modificacion": "CURRENT_TIMESTAMP",
            "usuario_ultima_modificacion": usuario_modificacion,
        }

        return self.update(cita_id, data)

    def cancelar(
        self,
        cita_id: int,
        motivo: str,
        usuario_modificacion: str,
    ) -> bool:
        """
        Cancela una cita.

        Args:
            cita_id: ID de la cita.
            motivo: Motivo de la cancelación.
            usuario_modificacion: Username del usuario que cancela.

        Returns:
            bool: True si se canceló, False si no existe.
        """
        data: dict[str, Any] = {
            "motivo": motivo,
            "estado": "cancelada",
            "fecha_ultima_modificacion": "CURRENT_TIMESTAMP",
            "usuario_ultima_modificacion": usuario_modificacion,
        }

        return self.update(cita_id, data)
