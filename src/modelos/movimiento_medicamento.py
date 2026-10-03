"""
Modelo de dominio para movimientos de medicamentos.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    TIPOS_MOVIMIENTO_MEDICAMENTO,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)


@dataclass
class MovimientoMedicamento:
    """Representa una entrada, salida o ajuste de un lote."""

    lote_id: int
    tipo_movimiento: str
    cantidad: int
    usuario_responsable: str
    id: int | None = None
    fecha_movimiento: datetime | None = None
    motivo: str | None = None
    documento_referencia: str | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del movimiento."""
        self.lote_id = validar_entero_positivo(self.lote_id, "lote_id")
        self.tipo_movimiento = validar_dominio(
            self.tipo_movimiento.strip().lower(),
            TIPOS_MOVIMIENTO_MEDICAMENTO,
            "tipo_movimiento",
        )
        self.cantidad = validar_entero_positivo(self.cantidad, "cantidad")
        self.usuario_responsable = validar_no_vacio(
            self.usuario_responsable,
            "usuario_responsable",
        )

        if self.motivo is not None:
            self.motivo = self.motivo.strip() or None

        if self.documento_referencia is not None:
            self.documento_referencia = self.documento_referencia.strip() or None

    def es_entrada(self) -> bool:
        """Indica si el movimiento es una entrada."""
        return self.tipo_movimiento == "entrada"

    def es_salida(self) -> bool:
        """Indica si el movimiento es una salida."""
        return self.tipo_movimiento == "salida"

    def es_ajuste(self) -> bool:
        """Indica si el movimiento es un ajuste."""
        return self.tipo_movimiento == "ajuste"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "lote_id": self.lote_id,
            "tipo_movimiento": self.tipo_movimiento,
            "cantidad": self.cantidad,
            "usuario_responsable": self.usuario_responsable,
            "motivo": self.motivo,
            "documento_referencia": self.documento_referencia,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "MovimientoMedicamento":
        """Crea un MovimientoMedicamento desde una fila SQLite."""
        fecha_movimiento = fila.get("fecha_movimiento")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            lote_id=int(fila["lote_id"]),
            tipo_movimiento=str(fila["tipo_movimiento"]),
            cantidad=int(fila["cantidad"]),
            fecha_movimiento=(
                datetime.fromisoformat(str(fecha_movimiento))
                if fecha_movimiento is not None
                else None
            ),
            usuario_responsable=str(fila["usuario_responsable"]),
            motivo=(str(fila["motivo"]) if fila.get("motivo") is not None else None),
            documento_referencia=(
                str(fila["documento_referencia"])
                if fila.get("documento_referencia") is not None
                else None
            ),
        )
