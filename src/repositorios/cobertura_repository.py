"""
Repositorio para gestión de coberturas de seguro.
"""

from typing import Any

from .base_repository import BaseRepository


class CoberturaRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Cobertura.

    Métodos específicos:
    - find_by_seguro(): Lista coberturas de un seguro.
    - find_by_servicio(): Lista coberturas de un servicio.
    - buscar_vigente(): Busca una cobertura vigente para seguro y servicio.
    - desactivar(): Desactiva lógicamente una cobertura.
    """

    def __init__(self) -> None:
        super().__init__("cobertura")

    def find_by_seguro(
        self,
        seguro_id: int,
        solo_activas: bool = True,
    ) -> list[dict[str, Any]]:
        """Lista coberturas asociadas a un seguro."""
        query = "SELECT * FROM cobertura WHERE seguro_id = ?"
        parametros: list[Any] = [seguro_id]

        if solo_activas:
            query += " AND estado = 1"

        query += " ORDER BY fecha_inicio DESC"

        cursor = self._db.execute_query(query, tuple(parametros))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_servicio(
        self,
        servicio_id: int,
        solo_activas: bool = True,
    ) -> list[dict[str, Any]]:
        """Lista coberturas asociadas a un servicio."""
        query = "SELECT * FROM cobertura WHERE servicio_id = ?"
        parametros: list[Any] = [servicio_id]

        if solo_activas:
            query += " AND estado = 1"

        query += " ORDER BY fecha_inicio DESC"

        cursor = self._db.execute_query(query, tuple(parametros))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def buscar_vigente(
        self,
        seguro_id: int,
        servicio_id: int,
        fecha_consulta: str,
    ) -> dict[str, Any] | None:
        """
        Busca una cobertura activa y vigente.

        Args:
            seguro_id: ID del seguro.
            servicio_id: ID del servicio.
            fecha_consulta: Fecha en formato ISO.

        Returns:
            Datos de cobertura o None.
        """
        query = """
            SELECT * FROM cobertura
            WHERE seguro_id = ?
              AND servicio_id = ?
              AND estado = 1
              AND fecha_inicio <= ?
              AND (fecha_fin IS NULL OR fecha_fin >= ?)
            ORDER BY fecha_inicio DESC
            LIMIT 1
        """
        cursor = self._db.execute_query(
            query,
            (seguro_id, servicio_id, fecha_consulta, fecha_consulta),
        )
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def desactivar(self, cobertura_id: int) -> bool:
        """Desactiva lógicamente una cobertura."""
        return self.update(cobertura_id, {"estado": 0})
