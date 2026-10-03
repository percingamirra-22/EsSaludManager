"""
Modelo de dominio para seguros de pacientes.
"""

from dataclasses import dataclass
from datetime import date
from typing import Any

from src.utils.validaciones import (
    TIPOS_SEGURO,
    validar_dominio,
    validar_no_vacio,
    validar_rango_fechas,
)


@dataclass
class Seguro:
    """Representa un seguro EsSalud o privado."""

    tipo_seguro: str
    nombre_aseguradora: str
    codigo_plan: str
    numero_poliza: str
    fecha_inicio: date
    id: int | None = None
    fecha_fin: date | None = None
    estado: bool = True

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del seguro."""
        self.tipo_seguro = validar_dominio(
            self.tipo_seguro.strip(),
            TIPOS_SEGURO,
            "tipo_seguro",
        )
        self.nombre_aseguradora = validar_no_vacio(
            self.nombre_aseguradora,
            "nombre_aseguradora",
        )
        self.codigo_plan = validar_no_vacio(self.codigo_plan, "codigo_plan").upper()
        self.numero_poliza = validar_no_vacio(
            self.numero_poliza,
            "numero_poliza",
        ).upper()
        validar_rango_fechas(
            self.fecha_inicio,
            self.fecha_fin,
            "fecha_inicio",
            "fecha_fin",
        )

    def verificar_vigencia(self, fecha_consulta: date) -> bool:
        """
        Determina si el seguro está activo y vigente para una fecha.

        Args:
            fecha_consulta: Fecha sobre la que se consulta vigencia.

        Returns:
            True si el seguro está vigente.
        """
        if not self.estado or fecha_consulta < self.fecha_inicio:
            return False

        return self.fecha_fin is None or fecha_consulta <= self.fecha_fin

    def renovar(self, nueva_fecha_fin: date) -> None:
        """
        Renueva la vigencia del seguro.

        Args:
            nueva_fecha_fin: Nueva fecha final de cobertura.
        """
        validar_rango_fechas(
            self.fecha_inicio,
            nueva_fecha_fin,
            "fecha_inicio",
            "fecha_fin",
        )
        self.fecha_fin = nueva_fecha_fin
        self.estado = True

    def cancelar(self) -> None:
        """Desactiva lógicamente el seguro."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo a columnas de la tabla seguro."""
        return {
            "tipo_seguro": self.tipo_seguro,
            "nombre_aseguradora": self.nombre_aseguradora,
            "codigo_plan": self.codigo_plan,
            "numero_poliza": self.numero_poliza,
            "estado": int(self.estado),
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": (
                self.fecha_fin.isoformat() if self.fecha_fin is not None else None
            ),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Seguro":
        """Crea un Seguro desde una fila SQLite."""
        fecha_fin = fila.get("fecha_fin")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            tipo_seguro=str(fila["tipo_seguro"]),
            nombre_aseguradora=str(fila["nombre_aseguradora"]),
            codigo_plan=str(fila["codigo_plan"]),
            numero_poliza=str(fila["numero_poliza"]),
            estado=bool(fila.get("estado", 1)),
            fecha_inicio=date.fromisoformat(str(fila["fecha_inicio"])),
            fecha_fin=(
                date.fromisoformat(str(fecha_fin)) if fecha_fin is not None else None
            ),
        )
