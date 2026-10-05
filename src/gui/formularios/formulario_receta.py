"""
Formulario para crear recetas médicas.
"""

import tkinter as tk
from collections.abc import Callable

from src.gui.componentes import FormularioBase
from src.servicios import RecetaService


class FormularioReceta(FormularioBase):
    """Formulario para crear una receta médica."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: RecetaService,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nueva receta", al_guardar)
        self._servicio = servicio

        self.agregar_campo("paciente_id", "ID del paciente")
        self.agregar_campo("especialista_id", "ID del especialista")
        self.agregar_campo("usuario_emisor", "Usuario emisor")
        self.agregar_campo("observaciones", "Observaciones")

    def guardar(self) -> None:
        """Crea la receta."""
        self._servicio.crear_receta(
            paciente_id=int(self.obtener_valor("paciente_id")),
            especialista_id=int(self.obtener_valor("especialista_id")),
            usuario_emisor=self.obtener_valor("usuario_emisor"),
            observaciones=self.obtener_valor("observaciones") or None,
        )
        self._notificar_guardado()
