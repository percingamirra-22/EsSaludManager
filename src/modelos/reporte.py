"""
Modelo de dominio para reportes generados por el sistema.
"""

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

FORMATOS_REPORTE = frozenset({"PDF", "CSV"})


def crear_diccionario_filtros() -> dict[str, Any]:
    """Crea un diccionario vacío tipado para filtros del reporte."""
    return {}


@dataclass
class Reporte:
    """Representa un reporte solicitado y generado por un usuario."""

    tipo_reporte: str
    formato: str
    usuario_solicitante_id: int
    id: int | None = None
    filtros: dict[str, Any] = field(default_factory=crear_diccionario_filtros)
    fecha_generacion: datetime | None = None
    ruta_archivo: str | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos principales del reporte."""
        self.tipo_reporte = validar_no_vacio(
            self.tipo_reporte,
            "tipo_reporte",
        )
        self.formato = validar_dominio(
            self.formato.strip().upper(),
            FORMATOS_REPORTE,
            "formato",
        )
        self.usuario_solicitante_id = validar_entero_positivo(
            self.usuario_solicitante_id,
            "usuario_solicitante_id",
        )

        if self.ruta_archivo is not None:
            self.ruta_archivo = str(Path(self.ruta_archivo))

    def establecer_ruta_archivo(self, ruta_archivo: str) -> None:
        """
        Asigna la ruta del archivo generado.

        Args:
            ruta_archivo: Ruta al archivo PDF o CSV.
        """
        self.ruta_archivo = str(Path(validar_no_vacio(ruta_archivo, "ruta_archivo")))

    def exportado(self) -> bool:
        """
        Determina si el reporte tiene una ruta asignada.

        Returns:
            True si existe una ruta de archivo registrada.
        """
        return self.ruta_archivo is not None

    def to_dict(self) -> dict[str, object]:
        """
        Convierte el modelo a columnas de la tabla reporte.

        Raises:
            ValueError: Si aún no se asignó una ruta de archivo.
        """
        if self.ruta_archivo is None:
            raise ValueError("No se puede persistir un reporte sin ruta_archivo.")

        return {
            "tipo_reporte": self.tipo_reporte,
            "filtros": json.dumps(
                self.filtros,
                ensure_ascii=False,
                sort_keys=True,
            ),
            "formato": self.formato,
            "ruta_archivo": self.ruta_archivo,
            "usuario_solicitante_id": self.usuario_solicitante_id,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Reporte":
        """Crea un Reporte desde una fila SQLite."""
        filtros_guardados = fila.get("filtros")
        fecha_generacion = fila.get("fecha_generacion")
        filtros: dict[str, Any] = {}

        if filtros_guardados:
            filtros_cargados = json.loads(str(filtros_guardados))

            if not isinstance(filtros_cargados, dict):
                raise ValueError(
                    "El campo 'filtros' del reporte debe contener un objeto JSON."
                )

            filtros = cast(dict[str, Any], filtros_cargados)

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            tipo_reporte=str(fila["tipo_reporte"]),
            filtros=filtros,
            fecha_generacion=(
                datetime.fromisoformat(str(fecha_generacion))
                if fecha_generacion is not None
                else None
            ),
            formato=str(fila["formato"]),
            ruta_archivo=str(fila["ruta_archivo"]),
            usuario_solicitante_id=int(fila["usuario_solicitante_id"]),
        )
