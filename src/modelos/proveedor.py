"""
Modelo de dominio para proveedores.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_email,
    validar_no_vacio,
    validar_ruc,
    validar_telefono,
)


@dataclass
class Proveedor:
    """Representa un proveedor de medicamentos e insumos."""

    razon_social: str
    ruc: str
    direccion: str
    id: int | None = None
    telefono: str | None = None
    email: str | None = None
    contacto_nombre: str | None = None
    contacto_telefono: str | None = None
    estado: bool = True
    fecha_registro: datetime | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del proveedor."""
        self.razon_social = validar_no_vacio(
            self.razon_social,
            "razon_social",
        )
        self.ruc = validar_ruc(self.ruc)
        self.direccion = validar_no_vacio(self.direccion, "direccion")
        self.telefono = validar_telefono(self.telefono)
        self.email = validar_email(self.email)

        if self.contacto_nombre is not None:
            self.contacto_nombre = self.contacto_nombre.strip() or None

        self.contacto_telefono = validar_telefono(self.contacto_telefono)

    def actualizar(self, datos: dict[str, Any]) -> None:
        """Actualiza atributos permitidos del proveedor."""
        campos_permitidos = {
            "razon_social",
            "direccion",
            "telefono",
            "email",
            "contacto_nombre",
            "contacto_telefono",
            "estado",
        }
        campos_invalidos = set(datos) - campos_permitidos

        if campos_invalidos:
            campos = ", ".join(sorted(campos_invalidos))
            raise ValueError(f"Campos no actualizables para proveedor: {campos}.")

        for campo, valor in datos.items():
            setattr(self, campo, valor)

        self.__post_init__()

    def desactivar(self) -> None:
        """Desactiva lógicamente al proveedor."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato de columnas SQLite."""
        return {
            "razon_social": self.razon_social,
            "ruc": self.ruc,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email,
            "contacto_nombre": self.contacto_nombre,
            "contacto_telefono": self.contacto_telefono,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Proveedor":
        """Crea un Proveedor desde una fila SQLite."""
        fecha_registro = fila.get("fecha_registro")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            razon_social=str(fila["razon_social"]),
            ruc=str(fila["ruc"]),
            direccion=str(fila["direccion"]),
            telefono=(
                str(fila["telefono"]) if fila.get("telefono") is not None else None
            ),
            email=str(fila["email"]) if fila.get("email") is not None else None,
            contacto_nombre=(
                str(fila["contacto_nombre"])
                if fila.get("contacto_nombre") is not None
                else None
            ),
            contacto_telefono=(
                str(fila["contacto_telefono"])
                if fila.get("contacto_telefono") is not None
                else None
            ),
            estado=bool(fila.get("estado", 1)),
            fecha_registro=(
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
        )
