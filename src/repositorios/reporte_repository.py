"""
Repositorio para gestión de reportes.
"""

from typing import Any

from .base_repository import BaseRepository


class ReporteRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Reporte.

    Métodos específicos:
    - find_by_usuario(): Lista reportes solicitados por un usuario.
    - find_by_tipo(): Lista reportes por tipo.
    - marcar_exportado(): Actualiza la ruta del archivo generado.
    """

    def __init__(self) -> None:
        super().__init__("reporte")

    def find_by_usuario(
        self,
        usuario_id: int,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista reportes solicitados por un usuario."""
        query = """
            SELECT * FROM reporte
            WHERE usuario_solicitante_id = ?
            ORDER BY fecha_generacion DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (usuario_id, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def find_by_tipo(
        self,
        tipo_reporte: str,
        limite: int = 20,
    ) -> list[dict[str, Any]]:
        """Lista reportes por tipo."""
        query = """
            SELECT * FROM reporte
            WHERE tipo_reporte = ?
            ORDER BY fecha_generacion DESC
            LIMIT ?
        """
        cursor = self._db.execute_query(query, (tipo_reporte, limite))
        filas = cursor.fetchall()

        if not filas:
            return []

        columnas = [descripcion[0] for descripcion in cursor.description]
        return [dict(zip(columnas, fila)) for fila in filas]  # type: ignore[return-value]

    def marcar_exportado(
        self,
        reporte_id: int,
        ruta_archivo: str,
    ) -> bool:
        """Actualiza la ruta del archivo exportado."""
        return self.update(
            reporte_id,
            {"ruta_archivo": ruta_archivo},
        )
