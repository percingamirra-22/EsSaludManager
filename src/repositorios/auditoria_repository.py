"""
Repositorio para gestión de auditoría y trazabilidad.
"""

from typing import Any

from .base_repository import BaseRepository


class AuditoriaRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Auditoria.

    Métodos específicos:
    - registrar(): Registra una acción en auditoría.
    - obtener_historial(): Obtiene logs de auditoría con filtros.
    - obtener_por_usuario(): Obtiene acciones de un usuario específico.
    - obtener_por_recurso(): Obtiene acciones sobre un recurso específico.
    """

    def __init__(self) -> None:
        super().__init__("auditoria")

    def registrar(
        self,
        usuario_id: int,
        empleado_id: int,
        accion: str,
        recurso: str,
        recurso_id: int,
        ip_origen: str,
        detalles: str | None = None,
    ) -> int:
        """
        Registra una acción en la tabla de auditoría.

        Args:
            usuario_id: ID del usuario que realiza la acción.
            empleado_id: ID del empleado asociado.
            accion: Tipo de acción (crear, leer, actualizar, eliminar).
            recurso: Nombre del recurso (tabla/entidad).
            recurso_id: ID del recurso afectado.
            ip_origen: IP de origen.
            detalles: Detalles adicionales (opcional).

        Returns:
            int: ID del registro de auditoría creado.
        """
        data: dict[str, Any] = {
            "usuario_id": usuario_id,
            "empleado_id": empleado_id,
            "accion": accion,
            "recurso": recurso,
            "recurso_id": recurso_id,
            "ip_origen": ip_origen,
            "detalles": detalles,
        }

        return self.create(data)

    def obtener_historial(
        self,
        filtro: dict[str, Any] | None = None,
        limite: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Obtiene el historial de auditoría con filtros opcionales.

        Args:
            filtro: Diccionario con filtros (usuario_id, recurso, fecha_desde, etc.).
            limite: Número máximo de registros a retornar.

        Returns:
            list[dict]: Lista de registros de auditoría.
        """
        query = "SELECT * FROM auditoria WHERE 1=1"
        params: list[Any] = []

        if filtro:
            if "usuario_id" in filtro:
                query += " AND usuario_id = ?"
                params.append(filtro["usuario_id"])

            if "empleado_id" in filtro:
                query += " AND empleado_id = ?"
                params.append(filtro["empleado_id"])

            if "recurso" in filtro:
                query += " AND recurso = ?"
                params.append(filtro["recurso"])

            if "fecha_desde" in filtro:
                query += " AND fecha_accion >= ?"
                params.append(filtro["fecha_desde"])

            if "fecha_hasta" in filtro:
                query += " AND fecha_accion <= ?"
                params.append(filtro["fecha_hasta"])

        query += " ORDER BY fecha_accion DESC LIMIT ?"
        params.append(limite)

        cursor = self._db.execute_query(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def obtener_por_usuario(
        self,
        usuario_id: int,
        limite: int = 50,
    ) -> list[dict[str, Any]]:
        """Obtiene acciones de un usuario específico."""
        return self.obtener_historial(
            filtro={"usuario_id": usuario_id},
            limite=limite,
        )

    def obtener_por_recurso(
        self,
        recurso: str,
        recurso_id: int | None = None,
        limite: int = 50,
    ) -> list[dict[str, Any]]:
        """
        Obtiene acciones sobre un recurso específico.

        Args:
            recurso: Nombre del recurso (ej. "paciente", "cita").
            recurso_id: ID del recurso (opcional).
            limite: Número máximo de registros.
        """
        filtro: dict[str, Any] = {"recurso": recurso}
        if recurso_id is not None:
            filtro["recurso_id"] = recurso_id

        return self.obtener_historial(filtro=filtro, limite=limite)
