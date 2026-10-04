"""
Repositorio para gestión de lotes de medicamentos.
"""

from typing import Any

from .base_repository import BaseRepository


class LoteMedicamentoRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad LoteMedicamento.

    Métodos específicos:
    - find_by_numero_lote(): Busca un lote por su número.
    - find_by_medicamento(): Lista lotes de un medicamento.
    - listar_activos(): Lista lotes activos.
    - actualizar_stock(): Actualiza la cantidad actual de un lote.
    """

    def __init__(self) -> None:
        super().__init__("lote_medicamento")

    def find_by_numero_lote(
        self,
        numero_lote: str,
    ) -> dict[str, Any] | None:
        """Busca un lote por su número único."""
        query = "SELECT * FROM lote_medicamento WHERE numero_lote = ?"
        cursor = self._db.execute_query(query, (numero_lote,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def find_by_medicamento(
        self,
        medicamento_id: int,
        solo_activos: bool = True,
    ) -> list[dict[str, Any]]:
        """Lista los lotes asociados a un medicamento."""
        query = """
            SELECT * FROM lote_medicamento
            WHERE medicamento_id = ?
        """
        parametros: list[Any] = [medicamento_id]

        if solo_activos:
            query += " AND estado = 'activo'"

        query += " ORDER BY fecha_vencimiento ASC"

        cursor = self._db.execute_query(query, tuple(parametros))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def listar_activos(self) -> list[dict[str, Any]]:
        """Lista todos los lotes activos."""
        query = """
            SELECT * FROM lote_medicamento
            WHERE estado = 'activo'
            ORDER BY fecha_vencimiento ASC
        """
        cursor = self._db.execute_query(query)
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def actualizar_stock(
        self,
        lote_id: int,
        nueva_cantidad: int,
    ) -> bool:
        """
        Actualiza la cantidad actual de un lote.

        Args:
            lote_id: ID del lote.
            nueva_cantidad: Nueva cantidad disponible.

        Returns:
            True si se actualizó el lote.
        """
        if nueva_cantidad < 0:
            raise ValueError("La cantidad actual no puede ser negativa.")

        data: dict[str, Any] = {
            "cantidad_actual": nueva_cantidad,
        }

        return self.update(lote_id, data)
