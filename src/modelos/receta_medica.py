"""
Modelo de dominio para recetas médicas.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

ESTADOS_RECETA = frozenset({"activa", "dispensada", "cancelada"})


def crear_items_receta() -> list[int]:
    """Crea una lista tipada para IDs de ítems de receta."""
    return []


@dataclass
class RecetaMedica:
    """Representa una receta emitida por un especialista."""

    paciente_id: int
    especialista_id: int
    usuario_emisor: str
    id: int | None = None
    fecha_emision: datetime | None = None
    estado: str = "activa"
    observaciones: str | None = None
    items_ids: list[int] = field(default_factory=crear_items_receta)

    def __post_init__(self) -> None:
        """Valida los datos principales de la receta."""
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.especialista_id = validar_entero_positivo(
            self.especialista_id,
            "especialista_id",
        )
        self.usuario_emisor = validar_no_vacio(
            self.usuario_emisor,
            "usuario_emisor",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_RECETA,
            "estado",
        )

        if self.observaciones is not None:
            self.observaciones = self.observaciones.strip() or None

    def agregar_item(self, item_receta_id: int) -> bool:
        """
        Agrega el ID de un ítem de receta en memoria.

        Args:
            item_receta_id: ID de ItemReceta.

        Returns:
            True si se agregó; False si ya existía.
        """
        if self.estado != "activa":
            raise ValueError("Solo se pueden agregar ítems a una receta activa.")

        item_receta_id = validar_entero_positivo(
            item_receta_id,
            "item_receta_id",
        )

        if item_receta_id in self.items_ids:
            return False

        self.items_ids.append(item_receta_id)
        return True

    def quitar_item(self, item_receta_id: int) -> bool:
        """
        Retira el ID de un ítem en memoria.

        Args:
            item_receta_id: ID de ItemReceta.

        Returns:
            True si se retiró; False si no existía.
        """
        if self.estado != "activa":
            raise ValueError("Solo se pueden quitar ítems de una receta activa.")

        if item_receta_id not in self.items_ids:
            return False

        self.items_ids.remove(item_receta_id)
        return True

    def dispensar(self) -> None:
        """Marca la receta como dispensada."""
        if self.estado != "activa":
            raise ValueError("Solo una receta activa puede dispensarse.")

        if not self.items_ids:
            raise ValueError("No se puede dispensar una receta sin ítems.")

        self.estado = "dispensada"

    def cancelar(self) -> None:
        """Cancela la receta si todavía está activa."""
        if self.estado == "dispensada":
            raise ValueError("No se puede cancelar una receta dispensada.")

        self.estado = "cancelada"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "paciente_id": self.paciente_id,
            "especialista_id": self.especialista_id,
            "estado": self.estado,
            "observaciones": self.observaciones,
            "usuario_emisor": self.usuario_emisor,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "RecetaMedica":
        """Crea una RecetaMedica desde una fila SQLite."""
        fecha_emision = fila.get("fecha_emision")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            paciente_id=int(fila["paciente_id"]),
            especialista_id=int(fila["especialista_id"]),
            fecha_emision=(
                datetime.fromisoformat(str(fecha_emision))
                if fecha_emision is not None
                else None
            ),
            estado=str(fila["estado"]),
            observaciones=(
                str(fila["observaciones"])
                if fila.get("observaciones") is not None
                else None
            ),
            usuario_emisor=str(fila["usuario_emisor"]),
        )
