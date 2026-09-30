"""
Repositorio para gestión de medicamentos y stock.
"""

from typing import Any

from .base_repository import BaseRepository


class MedicamentoRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Medicamento.

    Métodos específicos:
    - find_by_codigo(): Busca por código de medicamento.
    - find_by_nombre(): Busca por nombre genérico o comercial.
    - obtener_stock(): Obtiene stock total de un medicamento.
    - verificar_vencimientos(): Obtiene lotes próximos a vencer.
    """

    def __init__(self) -> None:
        super().__init__("medicamento")

    def find_by_codigo(self, codigo_medicamento: str) -> dict[str, Any] | None:
        """Busca medicamento por código."""
        query = "SELECT * FROM medicamento WHERE codigo_medicamento = ?"
        cursor = self._db.execute_query(query, (codigo_medicamento,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def find_by_nombre(
        self,
        nombre: str,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Busca medicamentos por nombre (genérico o comercial).

        Args:
            nombre: Texto a buscar.
            limite: Número máximo de resultados.
        """
        query = """
            SELECT * FROM medicamento 
            WHERE nombre_generico LIKE ? OR nombre_comercial LIKE ?
            ORDER BY nombre_generico
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (f"%{nombre}%", f"%{nombre}%", limite))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def obtener_stock(self, medicamento_id: int) -> int:
        """
        Obtiene el stock total de un medicamento (suma de lotes activos).

        Args:
            medicamento_id: ID del medicamento.

        Returns:
            int: Stock total.
        """
        query = """
            SELECT COALESCE(SUM(cantidad_actual), 0) 
            FROM lote_medicamento 
            WHERE medicamento_id = ? AND estado = 'activo'
        """
        cursor = self._db.execute_query(query, (medicamento_id,))
        return cursor.fetchone()[0]  # type: ignore[no-any-return]

    def verificar_vencimientos(
        self,
        dias_limite: int = 30,
    ) -> list[dict[str, Any]]:
        """
        Obtiene lotes próximos a vencer.

        Args:
            dias_limite: Días límite para considerar vencimiento próximo.

        Returns:
            list[dict]: Lista de lotes próximos a vencer.
        """
        query = """
            SELECT lm.*, m.nombre_generico, m.nombre_comercial
            FROM lote_medicamento lm
            INNER JOIN medicamento m ON lm.medicamento_id = m.id
            WHERE lm.estado = 'activo'
            AND lm.fecha_vencimiento <= date('now', '+' || ? || ' days')
            AND lm.fecha_vencimiento >= date('now')
            ORDER BY lm.fecha_vencimiento ASC
        """
        cursor = self._db.execute_query(query, (dias_limite,))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def registrar_movimiento(
        self,
        lote_id: int,
        tipo_movimiento: str,
        cantidad: int,
        usuario_responsable: str,
        motivo: str | None = None,
        documento_referencia: str | None = None,
    ) -> int:
        """
        Registra un movimiento de medicamento (entrada, salida, ajuste).

        Args:
            lote_id: ID del lote.
            tipo_movimiento: Tipo de movimiento (entrada, salida, ajuste).
            cantidad: Cantidad del movimiento.
            usuario_responsable: Username del responsable.
            motivo: Motivo del movimiento (opcional).
            documento_referencia: Documento de referencia (opcional).

        Returns:
            int: ID del movimiento creado.
        """
        data: dict[str, Any] = {
            "lote_id": lote_id,
            "tipo_movimiento": tipo_movimiento,
            "cantidad": cantidad,
            "usuario_responsable": usuario_responsable,
            "motivo": motivo,
            "documento_referencia": documento_referencia,
        }

        # Insertar movimiento
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        query = (
            f"INSERT INTO movimiento_medicamento ({columns}) VALUES ({placeholders})"
        )

        self._db.execute_query(query, values)
        self._db.commit()

        # Obtener ID
        cursor = self._db.execute_query("SELECT last_insert_rowid()")
        movimiento_id = cursor.fetchone()[0]

        # Actualizar cantidad_actual del lote (trigger lo hace, pero por seguridad)
        if tipo_movimiento == "entrada":
            self._db.execute_query(
                "UPDATE lote_medicamento SET cantidad_actual = cantidad_actual + ? WHERE id = ?",
                (cantidad, lote_id),
            )
        elif tipo_movimiento == "salida":
            self._db.execute_query(
                "UPDATE lote_medicamento SET cantidad_actual = cantidad_actual - ? WHERE id = ?",
                (cantidad, lote_id),
            )

        self._db.commit()

        return movimiento_id  # type: ignore[no-any-return]
