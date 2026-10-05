"""
Repositorio para gestión de recetas médicas e ítems de receta.
"""

from typing import Any

from .base_repository import BaseRepository


class RecetaRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para las entidades RecetaMedica e ItemReceta.

    Métodos específicos:
    - find_by_paciente(): Lista recetas de un paciente.
    - find_by_especialista(): Lista recetas emitidas por un especialista.
    - registrar_item(): Registra un medicamento prescrito.
    - obtener_items(): Lista ítems de una receta.
    - actualizar_item(): Actualiza un ítem de receta.
    """

    def __init__(self) -> None:
        super().__init__("receta_medica")

    def find_by_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista recetas de un paciente."""
        query = """
            SELECT * FROM receta_medica
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

    def find_by_especialista(
        self,
        especialista_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista recetas emitidas por un especialista."""
        query = """
            SELECT * FROM receta_medica
            WHERE especialista_id = ?
            ORDER BY fecha_emision DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (especialista_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def registrar_item(
        self,
        receta_id: int,
        medicamento_id: int,
        dosis: str,
        frecuencia: str,
        duracion_dias: int,
    ) -> int:
        """
        Registra un ítem de receta.

        Args:
            receta_id: ID de la receta.
            medicamento_id: ID del medicamento.
            dosis: Dosis indicada.
            frecuencia: Frecuencia de consumo.
            duracion_dias: Duración del tratamiento.

        Returns:
            ID del ítem creado.
        """
        query = """
            INSERT INTO item_receta
                (receta_id, medicamento_id, dosis, frecuencia, duracion_dias)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor = self._db.execute_query(
            query,
            (
                receta_id,
                medicamento_id,
                dosis,
                frecuencia,
                duracion_dias,
            ),
        )
        self._db.commit()

        return int(cursor.lastrowid or 0)

    def obtener_items(self, receta_id: int) -> list[dict[str, Any]]:
        """Obtiene los ítems de una receta."""
        query = """
            SELECT * FROM item_receta
            WHERE receta_id = ?
            ORDER BY id ASC
        """
        cursor = self._db.execute_query(query, (receta_id,))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def actualizar_item(
        self,
        item_receta_id: int,
        data: dict[str, Any],
    ) -> bool:
        """
        Actualiza un ítem de receta.

        Args:
            item_receta_id: ID del ítem.
            data: Campos a actualizar.

        Returns:
            True si se actualizó.
        """
        if not data:
            return False

        set_clause = ", ".join(f"{campo} = ?" for campo in data)
        valores = tuple(data.values()) + (item_receta_id,)

        query = f"UPDATE item_receta SET {set_clause} WHERE id = ?"
        cursor = self._db.execute_query(query, valores)
        self._db.commit()

        return cursor.rowcount > 0

    def list_all(self) -> list[dict[str, Any]]:
        """Retorna todas las recetas registradas."""
        query = "SELECT * FROM receta_medica ORDER BY id"
        cursor = self._db.execute_query(query)
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]
