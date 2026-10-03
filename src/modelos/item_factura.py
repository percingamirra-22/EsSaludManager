"""
Modelo de dominio para ítems de factura.
"""

from dataclasses import dataclass
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
    validar_numero_en_rango,
)

ESTADOS_ITEM_FACTURA = frozenset({"activo", "anulado"})


@dataclass
class ItemFactura:
    """Representa un servicio facturado dentro de una factura."""

    factura_id: int
    servicio_id: int
    descripcion: str
    costo: float
    id: int | None = None
    estado: str = "activo"

    def __post_init__(self) -> None:
        """Valida los campos del ítem facturable."""
        self.factura_id = validar_entero_positivo(self.factura_id, "factura_id")
        self.servicio_id = validar_entero_positivo(
            self.servicio_id,
            "servicio_id",
        )
        self.descripcion = validar_no_vacio(self.descripcion, "descripcion")
        self.costo = validar_numero_en_rango(
            float(self.costo),
            0.0,
            float("inf"),
            "costo",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_ITEM_FACTURA,
            "estado",
        )

    def anular(self) -> None:
        """Anula lógicamente el ítem de factura."""
        self.estado = "anulado"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "factura_id": self.factura_id,
            "servicio_id": self.servicio_id,
            "descripcion": self.descripcion,
            "costo": self.costo,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "ItemFactura":
        """Crea un ItemFactura desde una fila SQLite."""
        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            factura_id=int(fila["factura_id"]),
            servicio_id=int(fila["servicio_id"]),
            descripcion=str(fila["descripcion"]),
            costo=float(fila["costo"]),
            estado=str(fila["estado"]),
        )
