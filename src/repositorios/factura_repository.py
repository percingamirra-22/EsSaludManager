"""
Repositorio para gestión de facturas, ítems y pagos.
"""

from typing import Any

from .base_repository import BaseRepository


class FacturaRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para las entidades Factura, ItemFactura y Pago.

    Métodos específicos:
    - find_by_numero(): Busca factura por número.
    - find_by_paciente(): Lista facturas de un paciente.
    - registrar_item(): Registra un ítem facturable.
    - obtener_items(): Lista ítems de una factura.
    - actualizar_item(): Actualiza un ítem de factura.
    - registrar_pago(): Registra un pago.
    - obtener_pagos(): Lista pagos de una factura.
    - calcular_total_pagado(): Suma pagos registrados o conciliados.
    """

    def __init__(self) -> None:
        super().__init__("factura")

    def find_by_numero(self, numero_factura: str) -> dict[str, Any] | None:
        """Busca una factura por su número único."""
        query = "SELECT * FROM factura WHERE numero_factura = ?"
        cursor = self._db.execute_query(query, (numero_factura,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def find_by_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista facturas de un paciente."""
        query = """
            SELECT * FROM factura
            WHERE paciente_id = ?
            ORDER BY fecha_emision DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (paciente_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def registrar_item(
        self,
        factura_id: int,
        servicio_id: int,
        descripcion: str,
        costo: float,
    ) -> int:
        """Registra un ítem facturable."""
        query = """
            INSERT INTO item_factura
                (factura_id, servicio_id, descripcion, costo)
            VALUES (?, ?, ?, ?)
        """
        cursor = self._db.execute_query(
            query,
            (factura_id, servicio_id, descripcion, costo),
        )
        self._db.commit()

        return int(cursor.lastrowid or 0)

    def obtener_items(self, factura_id: int) -> list[dict[str, Any]]:
        """Obtiene los ítems de una factura."""
        query = """
            SELECT * FROM item_factura
            WHERE factura_id = ?
            ORDER BY id ASC
        """
        cursor = self._db.execute_query(query, (factura_id,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def actualizar_item(
        self,
        item_factura_id: int,
        data: dict[str, Any],
    ) -> bool:
        """Actualiza un ítem de factura."""
        if not data:
            return False

        set_clause = ", ".join(f"{campo} = ?" for campo in data)
        valores = tuple(data.values()) + (item_factura_id,)

        query = f"UPDATE item_factura SET {set_clause} WHERE id = ?"
        cursor = self._db.execute_query(query, valores)
        self._db.commit()

        return cursor.rowcount > 0

    def registrar_pago(
        self,
        factura_id: int,
        monto: float,
        metodo_pago: str,
        usuario_registro: str,
        numero_referencia: str | None = None,
    ) -> int:
        """Registra un pago asociado a una factura."""
        query = """
            INSERT INTO pago
                (factura_id, monto, metodo_pago, usuario_registro, numero_referencia)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self._db.execute_query(
            query,
            (factura_id, monto, metodo_pago, usuario_registro, numero_referencia),
        )
        self._db.commit()

        return int(cursor.lastrowid or 0)

    def obtener_pagos(self, factura_id: int) -> list[dict[str, Any]]:
        """Obtiene los pagos de una factura."""
        query = """
            SELECT * FROM pago
            WHERE factura_id = ?
            ORDER BY fecha_pago ASC
        """
        cursor = self._db.execute_query(query, (factura_id,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def calcular_total_pagado(self, factura_id: int) -> float:
        """Calcula el total pagado de una factura."""
        query = """
            SELECT COALESCE(SUM(monto), 0.0)
            FROM pago
            WHERE factura_id = ?
        """
        cursor = self._db.execute_query(query, (factura_id,))
        resultado = cursor.fetchone()[0]

        return float(resultado)  # type: ignore[no-any-return]

    def list_all(self) -> list[dict[str, Any]]:
        """Retorna todas las facturas registradas."""
        query = "SELECT * FROM factura ORDER BY id"
        cursor = self._db.execute_query(query)
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]
