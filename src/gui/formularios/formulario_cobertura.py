"""
Formulario para registrar coberturas.
"""

import tkinter as tk
from collections.abc import Callable
from datetime import date

from src.gui.componentes import FormularioBase
from src.servicios import CoberturaService


class FormularioCobertura(FormularioBase):
    """Formulario para registrar una cobertura."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: CoberturaService,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nueva cobertura", al_guardar)
        self._servicio = servicio

        self.agregar_campo("seguro_id", "ID del seguro")
        self.agregar_campo("servicio_id", "ID del servicio")
        self.agregar_campo("porcentaje", "Porcentaje de cobertura")
        self.agregar_campo("monto_maximo", "Monto máximo")
        self.agregar_campo("copago", "Copago fijo")
        self.agregar_campo("fecha_inicio", "Fecha inicio (AAAA-MM-DD)")

    def guardar(self) -> None:
        """Registra la cobertura."""
        self._servicio.registrar_cobertura(
            seguro_id=int(self.obtener_valor("seguro_id")),
            servicio_id=int(self.obtener_valor("servicio_id")),
            porcentaje_cobertura=float(self.obtener_valor("porcentaje")),
            monto_maximo=float(self.obtener_valor("monto_maximo")),
            copago_fijo=float(self.obtener_valor("copago")),
            fecha_inicio=date.fromisoformat(self.obtener_valor("fecha_inicio")),
        )
        self._notificar_guardado()
