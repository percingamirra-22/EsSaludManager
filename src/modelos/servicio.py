"""
Modelo base para servicios médicos.
"""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Any, TypedDict

from src.utils.validaciones import (
    validar_dominio,
    validar_no_vacio,
    validar_numero_en_rango,
)

TIPOS_SERVICIO = frozenset({"consulta", "examen", "procedimiento"})


class DatosServicio(TypedDict):
    """Datos comunes de un servicio obtenidos desde SQLite."""

    id: int | None
    codigo_servicio: str
    nombre_servicio: str
    tipo_servicio: str
    costo_base: float
    estado: bool
    fecha_registro: datetime | None


@dataclass
class Servicio(ABC):
    """
    Representa el catálogo base de servicios médicos.

    Consulta y ExamenMedico se relacionan con servicio mediante servicio_id.
    La persistencia y creación coordinada se implementa en los servicios
    de negocio.
    """

    codigo_servicio: str
    nombre_servicio: str
    tipo_servicio: str
    costo_base: float
    id: int | None = None
    estado: bool = True
    fecha_registro: datetime | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos comunes de un servicio."""
        self.codigo_servicio = validar_no_vacio(
            self.codigo_servicio,
            "codigo_servicio",
        ).upper()
        self.nombre_servicio = validar_no_vacio(
            self.nombre_servicio,
            "nombre_servicio",
        )
        self.tipo_servicio = validar_dominio(
            self.tipo_servicio.strip().lower(),
            TIPOS_SERVICIO,
            "tipo_servicio",
        )
        self.costo_base = validar_numero_en_rango(
            float(self.costo_base),
            0.0,
            float("inf"),
            "costo_base",
        )

    def actualizar(self, datos: dict[str, Any]) -> None:
        """
        Actualiza atributos permitidos del servicio.

        Args:
            datos: Campos y valores a modificar.
        """
        campos_permitidos = {
            "codigo_servicio",
            "nombre_servicio",
            "costo_base",
            "estado",
        }
        campos_invalidos = set(datos) - campos_permitidos

        if campos_invalidos:
            campos = ", ".join(sorted(campos_invalidos))
            raise ValueError(f"Campos no actualizables para servicio: {campos}.")

        for campo, valor in datos.items():
            setattr(self, campo, valor)

        self.__post_init__()

    def desactivar(self) -> None:
        """Desactiva lógicamente el servicio."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte atributos comunes al formato SQLite."""
        return {
            "codigo_servicio": self.codigo_servicio,
            "nombre_servicio": self.nombre_servicio,
            "tipo_servicio": self.tipo_servicio,
            "costo_base": self.costo_base,
            "estado": int(self.estado),
        }

    @classmethod
    def datos_comunes_desde_fila(cls, fila: dict[str, Any]) -> DatosServicio:
        """
        Convierte una fila SQLite en datos comunes de Servicio.

        Args:
            fila: Fila de la tabla servicio.

        Returns:
            Datos tipados de Servicio.
        """
        fecha_registro = fila.get("fecha_registro")

        return {
            "id": int(fila["id"]) if fila.get("id") is not None else None,
            "codigo_servicio": str(fila["codigo_servicio"]),
            "nombre_servicio": str(fila["nombre_servicio"]),
            "tipo_servicio": str(fila["tipo_servicio"]),
            "costo_base": float(fila["costo_base"]),
            "estado": bool(fila.get("estado", 1)),
            "fecha_registro": (
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
        }
