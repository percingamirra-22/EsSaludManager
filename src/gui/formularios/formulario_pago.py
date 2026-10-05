"""
Formulario para registrar pagos.
"""

import tkinter as tk
from collections.abc import Callable

from src.gui.componentes import FormularioBase
from src.servicios import PagoService


class FormularioPago(FormularioBase):
    """Formulario para registrar un pago."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: PagoService,
        factura_id: int,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nuevo pago", al_guardar)
        self._servicio = servicio
        self._factura_id = factura_id

        self.agregar_campo("monto", "Monto")
        self.agregar_campo("metodo_pago", "Método (efectivo, tarjeta, transferencia)")
        self.agregar_campo("usuario_registro", "Usuario que registra")
        self.agregar_campo("numero_referencia", "Referencia")

    def guardar(self) -> None:
        """Registra el pago."""
        self._servicio.registrar_pago(
            factura_id=self._factura_id,
            monto=float(self.obtener_valor("monto")),
            metodo_pago=self.obtener_valor("metodo_pago"),
            usuario_registro=self.obtener_valor("usuario_registro"),
            numero_referencia=self.obtener_valor("numero_referencia") or None,
        )
        self._notificar_guardado()
