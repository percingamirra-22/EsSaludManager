"""
Repositorio para gestión de exámenes médicos.
"""

from typing import Any

from .base_repository import BaseRepository


class ExamenMedicoRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad ExamenMedico.

    Métodos específicos:
    - find_by_servicio(): Busca examen por servicio asociado.
    - find_by_tecnico(): Lista exámenes asignados a un técnico.
    - find_by_estado(): Lista exámenes por estado.
    - registrar_resultado(): Registra resultado y archivo.
    - cambiar_estado(): Actualiza el estado del examen.
    """

    def __init__(self) -> None:
        super().__init__("examen_medico")

    def find_by_servicio(self, servicio_id: int) -> dict[str, Any] | None:
        """Busca un examen por su servicio asociado."""
        query = "SELECT * FROM examen_medico WHERE servicio_id = ?"
        cursor = self._db.execute_query(query, (servicio_id,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        columnas = [descripcion[0] for descripcion in cursor.description]
        return dict(zip(columnas, fila))  # type: ignore[return-value]

    def find_by_tecnico(
        self,
        tecnico_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista exámenes asignados a un técnico."""
        query = """
            SELECT * FROM examen_medico
            WHERE tecnico_id = ?
            ORDER BY id DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (tecnico_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_estado(
        self,
        estado: str,
        limite: int = 50,
    ) -> list[dict[str, Any]]:
        """Lista exámenes por estado."""
        query = """
            SELECT * FROM examen_medico
            WHERE estado = ?
            ORDER BY id DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (estado, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def registrar_resultado(
        self,
        examen_id: int,
        resultado: str,
        archivo_resultado: str | None,
    ) -> bool:
        """Registra el resultado de un examen."""
        data: dict[str, Any] = {
            "resultado": resultado,
            "archivo_resultado": archivo_resultado,
            "estado": "completado",
        }

        return self.update(examen_id, data)

    def cambiar_estado(
        self,
        examen_id: int,
        estado: str,
    ) -> bool:
        """Actualiza el estado de un examen."""
        return self.update(examen_id, {"estado": estado})
