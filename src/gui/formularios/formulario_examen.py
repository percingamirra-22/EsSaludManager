"""
Formulario para crear exámenes médicos.
"""

import tkinter as tk
from collections.abc import Callable

from src.gui.componentes import FormularioBase
from src.servicios import ExamenMedicoService


class FormularioExamen(FormularioBase):
    """Formulario para crear un examen médico."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: ExamenMedicoService,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nuevo examen", al_guardar)
        self._servicio = servicio

        self.agregar_campo("paciente_id", "ID del paciente")
        self.agregar_campo("especialista_id", "ID del especialista")
        self.agregar_campo("servicio_id", "ID del servicio de examen")
        self.agregar_campo("tecnico_id", "ID del técnico")
        self.agregar_campo("tipo_examen", "Tipo de examen")

    def guardar(self) -> None:
        """Crea la orden y el examen."""
        orden_id = self._servicio.crear_orden(
            paciente_id=int(self.obtener_valor("paciente_id")),
            especialista_id=int(self.obtener_valor("especialista_id")),
        )

        examen_id = self._servicio.crear_examen(
            servicio_id=int(self.obtener_valor("servicio_id")),
            orden_examen_id=orden_id,
            tecnico_id=int(self.obtener_valor("tecnico_id")),
            tipo_examen=self.obtener_valor("tipo_examen"),
        )

        self._servicio.agregar_examen_a_orden(orden_id, examen_id)
        self._notificar_guardado()
