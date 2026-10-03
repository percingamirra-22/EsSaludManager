"""
Modelo de dominio para sesiones de usuario.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import validar_dominio, validar_entero_positivo

ESTADOS_SESION = frozenset({"activa", "cerrada", "expirada"})


@dataclass
class Sesion:
    """Representa una sesión de acceso al sistema."""

    usuario_id: int
    fecha_inicio: datetime
    ip_origen: str | None = None
    id: int | None = None
    fecha_fin: datetime | None = None
    estado: str = "activa"

    def __post_init__(self) -> None:
        """Valida los datos de sesión."""
        self.usuario_id = validar_entero_positivo(self.usuario_id, "usuario_id")
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_SESION,
            "estado",
        )

        if self.fecha_fin is not None and self.fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha de fin de sesión no puede ser anterior al inicio."
            )

    def cerrar(self, fecha_fin: datetime) -> None:
        """
        Cierra una sesión activa.

        Args:
            fecha_fin: Fecha y hora de cierre.
        """
        if fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha de fin de sesión no puede ser anterior al inicio."
            )

        self.fecha_fin = fecha_fin
        self.estado = "cerrada"

    def expirar(self, fecha_fin: datetime) -> None:
        """
        Marca la sesión como expirada.

        Args:
            fecha_fin: Fecha y hora de expiración.
        """
        if fecha_fin < self.fecha_inicio:
            raise ValueError(
                "La fecha de fin de sesión no puede ser anterior al inicio."
            )

        self.fecha_fin = fecha_fin
        self.estado = "expirada"

    def esta_activa(self) -> bool:
        """Indica si la sesión se encuentra activa."""
        return self.estado == "activa"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "usuario_id": self.usuario_id,
            "fecha_inicio": self.fecha_inicio.isoformat(sep=" "),
            "fecha_fin": (
                self.fecha_fin.isoformat(sep=" ")
                if self.fecha_fin is not None
                else None
            ),
            "ip_origen": self.ip_origen,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Sesion":
        """Crea una Sesion desde una fila SQLite."""
        fecha_fin = fila.get("fecha_fin")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            usuario_id=int(fila["usuario_id"]),
            fecha_inicio=datetime.fromisoformat(str(fila["fecha_inicio"])),
            fecha_fin=(
                datetime.fromisoformat(str(fecha_fin))
                if fecha_fin is not None
                else None
            ),
            ip_origen=(
                str(fila["ip_origen"]) if fila.get("ip_origen") is not None else None
            ),
            estado=str(fila["estado"]),
        )
