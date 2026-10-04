"""
Servicio de negocio para pagos de facturas.
"""

from src.modelos.pago import Pago
from src.repositorios.factura_repository import FacturaRepository
from src.utils.validaciones import (
    METODOS_PAGO,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
    validar_numero_en_rango,
)


class PagoService:
    """Coordina pagos y cierre de facturas."""

    def __init__(self) -> None:
        """Inicializa el repositorio de facturas y pagos."""
        self._factura_repository = FacturaRepository()

    def registrar_pago(
        self,
        factura_id: int,
        monto: float,
        metodo_pago: str,
        usuario_registro: str,
        numero_referencia: str | None = None,
    ) -> int:
        """
        Registra un pago para una factura pendiente.

        Args:
            factura_id: ID de la factura.
            monto: Monto pagado.
            metodo_pago: efectivo, tarjeta o transferencia.
            usuario_registro: Usuario que registra el pago.
            numero_referencia: Referencia opcional.

        Returns:
            ID del pago creado.

        Raises:
            LookupError: Si la factura no existe.
            RuntimeError: Si la factura está anulada.
            ValueError: Si el monto o método son inválidos.
        """
        factura_id = validar_entero_positivo(factura_id, "factura_id")
        monto = validar_numero_en_rango(
            float(monto),
            0.0,
            float("inf"),
            "monto",
        )

        if monto <= 0:
            raise ValueError("El monto del pago debe ser mayor que cero.")

        metodo_pago = validar_dominio(
            metodo_pago.strip().lower(),
            METODOS_PAGO,
            "metodo_pago",
        )
        usuario_registro = validar_no_vacio(
            usuario_registro,
            "usuario_registro",
        )

        factura_fila = self._factura_repository.find_by_id(factura_id)

        if factura_fila is None:
            raise LookupError(f"No existe una factura con ID {factura_id}.")

        if factura_fila["estado"] == "anulada":
            raise RuntimeError("No se puede pagar una factura anulada.")

        pago = Pago(
            factura_id=factura_id,
            monto=monto,
            metodo_pago=metodo_pago,
            usuario_registro=usuario_registro,
            numero_referencia=numero_referencia,
        )

        return self._factura_repository.registrar_pago(
            factura_id,
            float(pago.monto),
            pago.metodo_pago,
            pago.usuario_registro,
            pago.numero_referencia,
        )

    def obtener_pagos(self, factura_id: int) -> list[Pago]:
        """Obtiene los pagos de una factura."""
        factura_id = validar_entero_positivo(factura_id, "factura_id")

        return [
            Pago.from_row(fila)
            for fila in self._factura_repository.obtener_pagos(factura_id)
        ]

    def calcular_total_pagado(self, factura_id: int) -> float:
        """Calcula el total pagado de una factura."""
        factura_id = validar_entero_positivo(factura_id, "factura_id")
        return self._factura_repository.calcular_total_pagado(factura_id)

    def marcar_factura_pagada(self, factura_id: int) -> bool:
        """
        Marca una factura como pagada si cubre el monto del paciente.

        Args:
            factura_id: ID de la factura.

        Returns:
            True si se marcó como pagada.

        Raises:
            LookupError: Si la factura no existe.
            RuntimeError: Si el pago no cubre el monto pendiente.
        """
        factura = self._factura_repository.find_by_id(factura_id)

        if factura is None:
            raise LookupError(f"No existe una factura con ID {factura_id}.")

        total_pagado = self._factura_repository.calcular_total_pagado(factura_id)
        monto_paciente = float(factura["monto_paciente"])

        if total_pagado < monto_paciente:
            raise RuntimeError(
                "El total pagado no cubre el monto pendiente del paciente."
            )

        return self._factura_repository.update(
            factura_id,
            {"estado": "pagada"},
        )
