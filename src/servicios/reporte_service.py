"""
Servicio de negocio para generación y exportación de reportes.
"""

import csv
import json
from pathlib import Path

from src.modelos.reporte import Reporte
from src.repositorios.reporte_repository import ReporteRepository
from src.utils.validaciones import (
    validar_entero_positivo,
    validar_no_vacio,
)


class ReporteService:
    """Coordina la creación, exportación y consulta de reportes."""

    def __init__(self) -> None:
        """Inicializa el repositorio de reportes."""
        self._repositorio = ReporteRepository()

    def crear_reporte(
        self,
        tipo_reporte: str,
        formato: str,
        usuario_solicitante_id: int,
        ruta_archivo: str,
        filtros: dict[str, object] | None = None,
    ) -> int:
        """
        Crea un reporte con una ruta de archivo destino.

        Args:
            tipo_reporte: Tipo de reporte.
            formato: PDF o CSV.
            usuario_solicitante_id: ID del usuario solicitante.
            ruta_archivo: Ruta destino del archivo.
            filtros: Filtros aplicados.

        Returns:
            ID del reporte creado.

        Raises:
            ValueError: Si la ruta o el usuario son inválidos.
        """
        usuario_solicitante_id = validar_entero_positivo(
            usuario_solicitante_id,
            "usuario_solicitante_id",
        )
        ruta_archivo = validar_no_vacio(ruta_archivo, "ruta_archivo")

        reporte = Reporte(
            tipo_reporte=tipo_reporte,
            formato=formato,
            usuario_solicitante_id=usuario_solicitante_id,
            ruta_archivo=ruta_archivo,
            filtros=filtros or {},
        )

        return self._repositorio.create(reporte.to_dict())

    def obtener_reporte(self, reporte_id: int) -> Reporte:
        """
        Obtiene un reporte por ID.

        Args:
            reporte_id: ID del reporte.

        Returns:
            Instancia de Reporte.

        Raises:
            LookupError: Si el reporte no existe.
        """
        reporte_id = validar_entero_positivo(reporte_id, "reporte_id")
        fila = self._repositorio.find_by_id(reporte_id)

        if fila is None:
            raise LookupError(f"No existe un reporte con ID {reporte_id}.")

        return Reporte.from_row(fila)

    def exportar_csv(
        self,
        reporte_id: int,
        encabezados: list[str],
        filas: list[list[object]],
        ruta_archivo: str,
    ) -> str:
        """
        Exporta un reporte a CSV.

        Args:
            reporte_id: ID del reporte.
            encabezados: Encabezados de columnas.
            filas: Filas de datos.
            ruta_archivo: Ruta destino del archivo.

        Returns:
            Ruta final del archivo generado.

        Raises:
            LookupError: Si el reporte no existe.
            ValueError: Si no hay encabezados o la ruta es inválida.
        """
        self.obtener_reporte(reporte_id)
        validar_no_vacio(ruta_archivo, "ruta_archivo")

        if not encabezados:
            raise ValueError("El reporte CSV requiere al menos un encabezado.")

        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(encabezados)
            escritor.writerows(filas)

        self._repositorio.marcar_exportado(reporte_id, str(ruta))
        return str(ruta)

    def exportar_json(
        self,
        reporte_id: int,
        datos: dict[str, object],
        ruta_archivo: str,
    ) -> str:
        """
        Exporta un reporte a JSON.

        Args:
            reporte_id: ID del reporte.
            datos: Datos a exportar.
            ruta_archivo: Ruta destino.

        Returns:
            Ruta final del archivo generado.
        """
        self.obtener_reporte(reporte_id)
        validar_no_vacio(ruta_archivo, "ruta_archivo")

        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=2)

        self._repositorio.marcar_exportado(reporte_id, str(ruta))
        return str(ruta)

    def listar_reportes_de_usuario(
        self,
        usuario_id: int,
        limite: int = 20,
    ) -> list[Reporte]:
        """Lista reportes solicitados por un usuario."""
        usuario_id = validar_entero_positivo(
            usuario_id,
            "usuario_solicitante_id",
        )

        return [
            Reporte.from_row(fila)
            for fila in self._repositorio.find_by_usuario(usuario_id, limite)
        ]
