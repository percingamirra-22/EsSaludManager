"""
Modelo de dominio para pagos de facturas.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    METODOS_PAGO,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

ESTADOS_PAGO = frozenset({"registrado", "conciliado"})


@dataclass
class Pago:
    """Representa un pago asociado a una factura."""

    factura_id: int
    monto: float
    metodo_pago: str
    usuario_registro: str
    id: int | None = None
    fecha_pago: datetime | None = None
    estado: str = "registrado"
    numero_referencia: str | None = None

    def __post_init__(self) -> None:
        """Valida los datos principales del pago."""
        self.factura_id = validar_entero_positivo(self.factura_id, "factura_id")
        self.monto = float(self.monto)

        if self.monto <= 0:
            raise ValueError("El campo 'monto' debe ser mayor que cero.")

        self.metodo_pago = validar_dominio(
            self.metodo_pago.strip().lower(),
            METODOS_PAGO,
            "metodo_pago",
        )
        self.usuario_registro = validar_no_vacio(
            self.usuario_registro,
            "usuario_registro",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_PAGO,
            "estado",
        )

        if self.numero_referencia is not None:
            self.numero_referencia = self.numero_referencia.strip() or None

    def conciliar(self) -> None:
        """Marca el pago como conciliado."""
        if self.estado == "conciliado":
            raise ValueError("El pago ya se encuentra conciliado.")

        self.estado = "conciliado"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "factura_id": self.factura_id,
            "monto": self.monto,
            "metodo_pago": self.metodo_pago,
            "estado": self.estado,
            "usuario_registro": self.usuario_registro,
            "numero_referencia": self.numero_referencia,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Pago":
        """Crea un Pago desde una fila SQLite."""
        fecha_pago = fila.get("fecha_pago")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            factura_id=int(fila["factura_id"]),
            monto=float(fila["monto"]),
            fecha_pago=(
                datetime.fromisoformat(str(fecha_pago))
                if fecha_pago is not None
                else None
            ),
            metodo_pago=str(fila["metodo_pago"]),
            estado=str(fila["estado"]),
            usuario_registro=str(fila["usuario_registro"]),
            numero_referencia=(
                str(fila["numero_referencia"])
                if fila.get("numero_referencia") is not None
                else None
            ),
        )
