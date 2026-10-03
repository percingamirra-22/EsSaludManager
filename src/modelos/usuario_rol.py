"""
Modelo de dominio para la relación Usuario-Rol.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import validar_entero_positivo, validar_no_vacio


@dataclass
class UsuarioRol:
    """Representa la asignación de un rol a un usuario."""

    usuario_id: int
    rol_id: int
    usuario_que_asigno: str
    id: int | None = None
    fecha_asignacion: datetime | None = None
    estado: bool = True

    def __post_init__(self) -> None:
        """Valida los datos de la asignación."""
        self.usuario_id = validar_entero_positivo(self.usuario_id, "usuario_id")
        self.rol_id = validar_entero_positivo(self.rol_id, "rol_id")
        self.usuario_que_asigno = validar_no_vacio(
            self.usuario_que_asigno,
            "usuario_que_asigno",
        )

    def revocar(self) -> None:
        """Desactiva lógicamente la asignación del rol."""
        self.estado = False

    def reactivar(self) -> None:
        """Reactiva la asignación del rol."""
        self.estado = True

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "usuario_id": self.usuario_id,
            "rol_id": self.rol_id,
            "estado": int(self.estado),
            "usuario_que_asigno": self.usuario_que_asigno,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "UsuarioRol":
        """Crea un UsuarioRol desde una fila SQLite."""
        fecha_asignacion = fila.get("fecha_asignacion")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            usuario_id=int(fila["usuario_id"]),
            rol_id=int(fila["rol_id"]),
            fecha_asignacion=(
                datetime.fromisoformat(str(fecha_asignacion))
                if fecha_asignacion is not None
                else None
            ),
            estado=bool(fila.get("estado", 1)),
            usuario_que_asigno=str(fila["usuario_que_asigno"]),
        )
