"""
Modelo de dominio para ítems de receta médica.
"""

from dataclasses import dataclass
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_no_negativo,
    validar_entero_positivo,
    validar_no_vacio,
)

ESTADOS_ITEM_RECETA = frozenset({"pendiente", "dispensado", "cancelado"})


@dataclass
class ItemReceta:
    """Representa un medicamento prescrito dentro de una receta."""

    receta_id: int
    medicamento_id: int
    dosis: str
    frecuencia: str
    duracion_dias: int
    id: int | None = None
    cantidad_dispensada: int = 0
    estado: str = "pendiente"

    def __post_init__(self) -> None:
        """Valida los datos del ítem de receta."""
        self.receta_id = validar_entero_positivo(self.receta_id, "receta_id")
        self.medicamento_id = validar_entero_positivo(
            self.medicamento_id,
            "medicamento_id",
        )
        self.dosis = validar_no_vacio(self.dosis, "dosis")
        self.frecuencia = validar_no_vacio(self.frecuencia, "frecuencia")
        self.duracion_dias = validar_entero_positivo(
            self.duracion_dias,
            "duracion_dias",
        )
        self.cantidad_dispensada = validar_entero_no_negativo(
            self.cantidad_dispensada,
            "cantidad_dispensada",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_ITEM_RECETA,
            "estado",
        )

    def dispensar(self, cantidad: int) -> None:
        """
        Registra la dispensación del ítem.

        Args:
            cantidad: Cantidad dispensada.

        Raises:
            ValueError: Si el ítem está cancelado o la cantidad es inválida.
        """
        if self.estado == "cancelado":
            raise ValueError("No se puede dispensar un ítem cancelado.")

        cantidad = validar_entero_positivo(cantidad, "cantidad")
        self.cantidad_dispensada += cantidad
        self.estado = "dispensado"

    def cancelar(self) -> None:
        """Cancela el ítem si no se ha dispensado."""
        if self.estado == "dispensado":
            raise ValueError("No se puede cancelar un ítem ya dispensado.")

        self.estado = "cancelado"

    def verificar_stock(self, stock_disponible: int, cantidad_requerida: int) -> bool:
        """
        Verifica si existe stock suficiente para una cantidad requerida.

        Args:
            stock_disponible: Stock existente.
            cantidad_requerida: Cantidad solicitada.

        Returns:
            True si el stock es suficiente.
        """
        stock_disponible = validar_entero_no_negativo(
            stock_disponible,
            "stock_disponible",
        )
        cantidad_requerida = validar_entero_positivo(
            cantidad_requerida,
            "cantidad_requerida",
        )
        return stock_disponible >= cantidad_requerida

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "receta_id": self.receta_id,
            "medicamento_id": self.medicamento_id,
            "dosis": self.dosis,
            "frecuencia": self.frecuencia,
            "duracion_dias": self.duracion_dias,
            "cantidad_dispensada": self.cantidad_dispensada,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "ItemReceta":
        """Crea un ItemReceta desde una fila SQLite."""
        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            receta_id=int(fila["receta_id"]),
            medicamento_id=int(fila["medicamento_id"]),
            dosis=str(fila["dosis"]),
            frecuencia=str(fila["frecuencia"]),
            duracion_dias=int(fila["duracion_dias"]),
            cantidad_dispensada=int(fila.get("cantidad_dispensada", 0)),
            estado=str(fila["estado"]),
        )
