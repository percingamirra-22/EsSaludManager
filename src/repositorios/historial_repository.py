"""
Repositorio para gestión de historial clínico.
"""

from typing import Any

from .base_repository import BaseRepository


class HistorialRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para las entidades HistorialClinico y EntradaHistorial.

    Métodos específicos:
    - find_by_paciente(): Obtiene historial de un paciente.
    - registrar_entrada(): Agrega una entrada al historial.
    - obtener_entradas(): Obtiene entradas del historial con filtros.
    """

    def __init__(self) -> None:
        super().__init__("historial_clinico")

    def find_by_paciente(self, paciente_id: int) -> dict[str, Any] | None:
        """Obtiene el historial clínico de un paciente."""
        query = "SELECT * FROM historial_clinico WHERE paciente_id = ?"
        cursor = self._db.execute_query(query, (paciente_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def registrar_entrada(
        self,
        historial_id: int,
        tipo_entrada: str,
        contenido: str,
        usuario_registro: str,
    ) -> int:
        """
        Registra una nueva entrada en el historial clínico.

        Args:
            historial_id: ID del historial clínico.
            tipo_entrada: Tipo de entrada (nota, diagnóstico, tratamiento, etc.).
            contenido: Contenido de la entrada.
            usuario_registro: Username del usuario que registra.

        Returns:
            int: ID de la entrada creada.
        """
        data: dict[str, Any] = {
            "historial_id": historial_id,
            "tipo_entrada": tipo_entrada,
            "contenido": contenido,
            "usuario_registro": usuario_registro,
        }

        # Insertar en entrada_historial
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO entrada_historial ({columns}) VALUES ({placeholders})"

        self._db.execute_query(query, values)
        self._db.commit()

        # Obtener ID
        cursor = self._db.execute_query("SELECT last_insert_rowid()")
        return cursor.fetchone()[0]  # type: ignore[no-any-return]

    def obtener_entradas(
        self,
        historial_id: int,
        filtro: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Obtiene las entradas de un historial clínico con filtros opcionales.

        Args:
            historial_id: ID del historial clínico.
            filtro: Filtros opcionales (tipo_entrada, estado, etc.).

        Returns:
            list[dict]: Lista de entradas.
        """
        query = "SELECT * FROM entrada_historial WHERE historial_id = ?"
        params: list[Any] = [historial_id]

        if filtro:
            if "tipo_entrada" in filtro:
                query += " AND tipo_entrada = ?"
                params.append(filtro["tipo_entrada"])

            if "estado" in filtro:
                query += " AND estado = ?"
                params.append(filtro["estado"])

        query += " ORDER BY fecha_registro DESC"

        cursor = self._db.execute_query(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def actualizar_entrada(
        self,
        entrada_id: int,
        contenido: str,
        usuario_registro: str,
    ) -> bool:
        """
        Actualiza una entrada existente (crea nueva versión).

        Args:
            entrada_id: ID de la entrada a actualizar.
            contenido: Nuevo contenido.
            usuario_registro: Username del usuario que actualiza.

        Returns:
            bool: True si se actualizó, False si no existe.
        """
        # Obtener entrada actual para versionar
        entrada_actual = self._db.execute_query(
            "SELECT * FROM entrada_historial WHERE id = ?",
            (entrada_id,),
        ).fetchone()

        if entrada_actual is None:
            return False

        # Desactivar entrada anterior
        self._db.execute_query(
            "UPDATE entrada_historial SET estado = 'desactivada' WHERE id = ?",
            (entrada_id,),
        )

        # Obtener datos para nueva versión
        historial_id = entrada_actual[1]
        tipo_entrada = entrada_actual[2]
        version_anterior = entrada_actual[6]

        # Insertar nueva versión
        data: dict[str, Any] = {
            "historial_id": historial_id,
            "tipo_entrada": tipo_entrada,
            "contenido": contenido,
            "usuario_registro": usuario_registro,
            "version": version_anterior + 1,
        }

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO entrada_historial ({columns}) VALUES ({placeholders})"
        self._db.execute_query(query, values)
        self._db.commit()

        return True
