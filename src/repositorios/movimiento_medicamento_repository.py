"""
Repositorio para gestión de movimientos de medicamentos.
"""

from typing import Any

from .base_repository import BaseRepository


class MovimientoMedicamentoRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad MovimientoMedicamento.

    Métodos específicos:
    - find_by_lote(): Lista movimientos de un lote.
    - find_by_tipo(): Lista movimientos por tipo.
    - listar_recientes(): Lista los últimos movimientos.
    """

    def __init__(self) -> None:
        super().__init__("movimiento_medicamento")

    def find_by_lote(
        self,
        lote_id: int,
        limite: int = 50,
    ) -> list[dict[str, Any]]:
        """Lista los movimientos de un lote."""
        query = """
            SELECT * FROM movimiento_medicamento
            WHERE lote_id = ?
            ORDER BY fecha_movimiento DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (lote_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_tipo(
        self,
        tipo_movimiento: str,
        limite: int = 50,
    ) -> list[dict[str, Any]]:
        """Lista movimientos por tipo: entrada, salida o ajuste."""
        query = """
            SELECT * FROM movimiento_medicamento
            WHERE tipo_movimiento = ?
            ORDER BY fecha_movimiento DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (tipo_movimiento, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def listar_recientes(self, limite: int = 20) -> list[dict[str, Any]]:
        """Lista los movimientos más recientes."""
        query = """
            SELECT * FROM movimiento_medicamento
            ORDER BY fecha_movimiento DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (limite,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]
