"""
Modelo de dominio para registros de auditoría.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_entero_positivo,
    validar_no_vacio,
)


@dataclass
class Auditoria:
    """
    Representa una acción auditada sobre un recurso sensible.

    Es un modelo inmutable en la práctica: no se incluyen métodos de
    actualización ni eliminación.
    """

    usuario_id: int
    empleado_id: int
    accion: str
    recurso: str
    recurso_id: int
    ip_origen: str
    id: int | None = None
    fecha_accion: datetime | None = None
    detalles: str | None = None
    estado: bool = True

    def __post_init__(self) -> None:
        """Valida los campos obligatorios de auditoría."""
        self.usuario_id = validar_entero_positivo(
            self.usuario_id,
            "usuario_id",
        )
        self.empleado_id = validar_entero_positivo(
            self.empleado_id,
            "empleado_id",
        )
        self.recurso_id = validar_entero_positivo(
            self.recurso_id,
            "recurso_id",
        )
        self.accion = validar_no_vacio(self.accion, "accion").lower()
        self.recurso = validar_no_vacio(self.recurso, "recurso").lower()
        self.ip_origen = validar_no_vacio(self.ip_origen, "ip_origen")

        if self.detalles is not None:
            self.detalles = self.detalles.strip() or None

    def to_dict(self) -> dict[str, object]:
        """
        Convierte el modelo a columnas de auditoria.

        No incluye fecha_accion porque SQLite la asigna con CURRENT_TIMESTAMP.
        """
        return {
            "usuario_id": self.usuario_id,
            "empleado_id": self.empleado_id,
            "accion": self.accion,
            "recurso": self.recurso,
            "recurso_id": self.recurso_id,
            "ip_origen": self.ip_origen,
            "detalles": self.detalles,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Auditoria":
        """Crea una Auditoria desde una fila SQLite."""
        fecha_accion = fila.get("fecha_accion")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            usuario_id=int(fila["usuario_id"]),
            empleado_id=int(fila["empleado_id"]),
            accion=str(fila["accion"]),
            recurso=str(fila["recurso"]),
            recurso_id=int(fila["recurso_id"]),
            fecha_accion=(
                datetime.fromisoformat(str(fecha_accion))
                if fecha_accion is not None
                else None
            ),
            ip_origen=str(fila["ip_origen"]),
            detalles=(
                str(fila["detalles"]) if fila.get("detalles") is not None else None
            ),
            estado=bool(fila.get("estado", 1)),
        )
