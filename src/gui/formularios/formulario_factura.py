"""
Formulario para crear facturas.
"""

import tkinter as tk
from collections.abc import Callable

from src.gui.componentes import FormularioBase
from src.servicios import FacturaService


class FormularioFactura(FormularioBase):
    """Formulario para crear una factura."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: FacturaService,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nueva factura", al_guardar)
        self._servicio = servicio

        self.agregar_campo("numero_factura", "Número de factura")
        self.agregar_campo("paciente_id", "ID del paciente")
        self.agregar_campo("usuario_emisor", "Usuario emisor")

    def guardar(self) -> None:
        """Crea la factura."""
        self._servicio.crear_factura(
            numero_factura=self.obtener_valor("numero_factura"),
            paciente_id=int(self.obtener_valor("paciente_id")),
            usuario_emisor=self.obtener_valor("usuario_emisor"),
        )
        self._notificar_guardado()
