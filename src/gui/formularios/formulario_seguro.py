"""
Formulario para registrar seguros médicos.
"""

import tkinter as tk
from collections.abc import Callable
from datetime import date

from src.gui.componentes import FormularioBase
from src.servicios import SeguroService


class FormularioSeguro(FormularioBase):
    """Formulario para registrar un seguro."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: SeguroService,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre, "Nuevo seguro", al_guardar)
        self._servicio = servicio

        self.agregar_campo("tipo_seguro", "Tipo (EsSalud o Privado)")
        self.agregar_campo("nombre_aseguradora", "Aseguradora")
        self.agregar_campo("codigo_plan", "Código del plan")
        self.agregar_campo("numero_poliza", "Número de póliza")
        self.agregar_campo("fecha_inicio", "Fecha inicio (AAAA-MM-DD)")

    def guardar(self) -> None:
        """Registra el seguro."""
        self._servicio.registrar_seguro(
            tipo_seguro=self.obtener_valor("tipo_seguro"),
            nombre_aseguradora=self.obtener_valor("nombre_aseguradora"),
            codigo_plan=self.obtener_valor("codigo_plan"),
            numero_poliza=self.obtener_valor("numero_poliza"),
            fecha_inicio=date.fromisoformat(self.obtener_valor("fecha_inicio")),
        )
        self._notificar_guardado()
