"""
Modelo de dominio para facturas.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
    validar_numero_en_rango,
)

ESTADOS_FACTURA = frozenset({"pendiente", "pagada", "anulada"})


def crear_items_factura() -> list[int]:
    """Crea una lista tipada para IDs de ítems de factura."""
    return []


@dataclass
class Factura:
    """Representa una factura de servicios médicos."""

    numero_factura: str
    paciente_id: int
    usuario_emisor: str
    id: int | None = None
    fecha_emision: datetime | None = None
    estado: str = "pendiente"
    monto_total: float = 0.0
    monto_cubierto: float = 0.0
    monto_paciente: float = 0.0
    items_ids: list[int] = field(default_factory=crear_items_factura)

    def __post_init__(self) -> None:
        """Valida los datos principales de la factura."""
        self.numero_factura = validar_no_vacio(
            self.numero_factura,
            "numero_factura",
        ).upper()
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.usuario_emisor = validar_no_vacio(
            self.usuario_emisor,
            "usuario_emisor",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_FACTURA,
            "estado",
        )
        self.monto_total = validar_numero_en_rango(
            float(self.monto_total),
            0.0,
            float("inf"),
            "monto_total",
        )
        self.monto_cubierto = validar_numero_en_rango(
            float(self.monto_cubierto),
            0.0,
            float("inf"),
            "monto_cubierto",
        )
        self.monto_paciente = validar_numero_en_rango(
            float(self.monto_paciente),
            0.0,
            float("inf"),
            "monto_paciente",
        )

    def agregar_item(self, item_factura_id: int) -> bool:
        """
        Agrega el ID de un ítem de factura en memoria.

        Args:
            item_factura_id: ID de ItemFactura.

        Returns:
            True si se agregó; False si ya existía.
        """
        if self.estado != "pendiente":
            raise ValueError("Solo se pueden agregar ítems a una factura pendiente.")

        item_factura_id = validar_entero_positivo(
            item_factura_id,
            "item_factura_id",
        )

        if item_factura_id in self.items_ids:
            return False

        self.items_ids.append(item_factura_id)
        return True

    def quitar_item(self, item_factura_id: int) -> bool:
        """
        Retira un ítem de factura en memoria.

        Args:
            item_factura_id: ID de ItemFactura.

        Returns:
            True si se retiró; False si no estaba asociado.
        """
        if self.estado != "pendiente":
            raise ValueError("Solo se pueden quitar ítems de una factura pendiente.")

        if item_factura_id not in self.items_ids:
            return False

        self.items_ids.remove(item_factura_id)
        return True

    def aplicar_cobertura(
        self,
        monto_cubierto: float,
        copago: float,
    ) -> None:
        """
        Aplica los montos calculados por una cobertura.

        Args:
            monto_cubierto: Monto cubierto por seguro.
            copago: Copago fijo asumido por el paciente.
        """
        monto_cubierto = validar_numero_en_rango(
            float(monto_cubierto),
            0.0,
            self.monto_total,
            "monto_cubierto",
        )
        copago = validar_numero_en_rango(
            float(copago),
            0.0,
            float("inf"),
            "copago",
        )

        self.monto_cubierto = monto_cubierto
        self.monto_paciente = round(
            max(self.monto_total - monto_cubierto + copago, 0.0),
            2,
        )

    def recalcular_montos(self, costos_activos: list[float]) -> None:
        """
        Recalcula el monto total desde los costos activos.

        Args:
            costos_activos: Costos de ítems activos.

        Raises:
            ValueError: Si algún costo es negativo.
        """
        for costo in costos_activos:
            validar_numero_en_rango(
                float(costo),
                0.0,
                float("inf"),
                "costo",
            )

        self.monto_total = round(sum(costos_activos), 2)

        self.monto_cubierto = min(self.monto_cubierto, self.monto_total)

        self.monto_paciente = round(
            self.monto_total - self.monto_cubierto,
            2,
        )

    def marcar_pagada(self) -> None:
        """Marca la factura como pagada."""
        if self.estado == "anulada":
            raise ValueError("No se puede pagar una factura anulada.")

        self.estado = "pagada"

    def anular(self) -> None:
        """Anula la factura si no fue pagada."""
        if self.estado == "pagada":
            raise ValueError("No se puede anular una factura pagada.")

        self.estado = "anulada"

    def generar_estado_cuenta(self, total_pagado: float) -> dict[str, float | str]:
        """
        Genera el estado de cuenta de la factura.

        Args:
            total_pagado: Total de pagos registrados.

        Returns:
            Resumen de montos y estado.
        """
        total_pagado = validar_numero_en_rango(
            float(total_pagado),
            0.0,
            float("inf"),
            "total_pagado",
        )
        saldo_pendiente = max(self.monto_paciente - total_pagado, 0.0)

        return {
            "estado": self.estado,
            "monto_total": self.monto_total,
            "monto_cubierto": self.monto_cubierto,
            "monto_paciente": self.monto_paciente,
            "total_pagado": round(total_pagado, 2),
            "saldo_pendiente": round(saldo_pendiente, 2),
        }

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "numero_factura": self.numero_factura,
            "paciente_id": self.paciente_id,
            "estado": self.estado,
            "monto_total": self.monto_total,
            "monto_cubierto": self.monto_cubierto,
            "monto_paciente": self.monto_paciente,
            "usuario_emisor": self.usuario_emisor,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Factura":
        """Crea una Factura desde una fila SQLite."""
        fecha_emision = fila.get("fecha_emision")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            numero_factura=str(fila["numero_factura"]),
            paciente_id=int(fila["paciente_id"]),
            fecha_emision=(
                datetime.fromisoformat(str(fecha_emision))
                if fecha_emision is not None
                else None
            ),
            estado=str(fila["estado"]),
            monto_total=float(fila["monto_total"]),
            monto_cubierto=float(fila["monto_cubierto"]),
            monto_paciente=float(fila["monto_paciente"]),
            usuario_emisor=str(fila["usuario_emisor"]),
        )
