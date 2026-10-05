"""
Servicio de negocio para generación y exportación de reportes.
"""

import csv
import json
from collections.abc import Sequence
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.modelos.reporte import Reporte
from src.repositorios.reporte_repository import ReporteRepository
from src.utils.validaciones import validar_entero_positivo, validar_no_vacio


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
        encabezados: Sequence[str],
        filas: Sequence[Sequence[object]],
        ruta_archivo: str,
        separador: str = ",",
    ) -> str:
        """
        Exporta un reporte a CSV.

        Args:
            reporte_id: ID del reporte.
            encabezados: Encabezados de columnas.
            filas: Filas de datos.
            ruta_archivo: Ruta destino del archivo.
            separador: Separador de columnas; coma o punto y coma.

        Returns:
            Ruta final del archivo generado.

        Raises:
            LookupError: Si el reporte no existe.
            ValueError: Si los datos o el separador son inválidos.
        """
        self.obtener_reporte(reporte_id)
        validar_no_vacio(ruta_archivo, "ruta_archivo")

        if separador not in {",", ";"}:
            raise ValueError("El separador debe ser ',' o ';'.")

        if not encabezados:
            raise ValueError("El reporte CSV requiere al menos un encabezado.")

        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.writer(archivo, delimiter=separador)
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

    def exportar_pdf(
        self,
        reporte_id: int,
        titulo: str,
        encabezados: Sequence[str],
        filas: Sequence[Sequence[object]],
        ruta_archivo: str,
    ) -> str:
        """
        Exporta un reporte a PDF.

        Args:
            reporte_id: ID del reporte.
            titulo: Título del reporte.
            encabezados: Encabezados de columnas.
            filas: Filas de datos.
            ruta_archivo: Ruta destino del archivo.

        Returns:
            Ruta final del archivo generado.
        """
        self.obtener_reporte(reporte_id)
        titulo = validar_no_vacio(titulo, "titulo")
        validar_no_vacio(ruta_archivo, "ruta_archivo")

        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)

        documento = SimpleDocTemplate(
            str(ruta),
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        estilos = getSampleStyleSheet()
        parrafo_titulo = Paragraph(titulo, estilos["Title"])

        datos_tabla: list[list[object]] = [list(encabezados)]
        datos_tabla.extend(list(fila) for fila in filas)

        tabla = Table(datos_tabla)
        tabla.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), "#007AC9"),
                    ("TEXTCOLOR", (0, 0), (-1, 0), "#FFFFFF"),
                    ("GRID", (0, 0), (-1, -1), 0.5, "#CBD2D9"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), ["#FFFFFF", "#F5F7FA"]),
                ]
            )
        )

        documento.build(
            [
                parrafo_titulo,
                Spacer(1, 12),
                tabla,
            ]
        )

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
