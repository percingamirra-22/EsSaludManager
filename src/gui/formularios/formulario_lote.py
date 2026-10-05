"""
Formulario para registrar lotes de medicamentos.
"""

import tkinter as tk
from collections.abc import Callable
from datetime import date

from src.gui.componentes import FormularioBase
from src.servicios import MedicamentoService


class FormularioLote(FormularioBase):
    """Formulario para registrar un lote de medicamento."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: MedicamentoService,
        medicamento_id: int,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nuevo lote", al_guardar)
        self._servicio = servicio
        self._medicamento_id = medicamento_id

        self.agregar_campo("numero_lote", "Número de lote")
        self.agregar_campo("fecha_fabricacion", "Fecha fabricación (AAAA-MM-DD)")
        self.agregar_campo("fecha_vencimiento", "Fecha vencimiento (AAAA-MM-DD)")
        self.agregar_campo("cantidad_inicial", "Cantidad inicial")

    def guardar(self) -> None:
        """Registra el lote."""
        self._servicio.registrar_lote(
            medicamento_id=self._medicamento_id,
            proveedor_id=1,
            numero_lote=self.obtener_valor("numero_lote"),
            fecha_fabricacion=date.fromisoformat(
                self.obtener_valor("fecha_fabricacion")
            ),
            fecha_vencimiento=date.fromisoformat(
                self.obtener_valor("fecha_vencimiento")
            ),
            cantidad_inicial=int(self.obtener_valor("cantidad_inicial")),
        )
        self._notificar_guardado()
