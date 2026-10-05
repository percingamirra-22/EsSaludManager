"""
Módulo de notificaciones.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.servicios import NotificacionService


class VentanaNotificaciones(ttk.Frame):
    """Módulo para consultar notificaciones."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = NotificacionService()

        ttk.Label(
            self,
            text="Notificaciones",
            style="Titulo.TLabel",
        ).pack(pady=(24, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("paciente", "ID paciente", 130),
                ("cita", "ID cita", 120),
                ("tipo", "Tipo", 200),
                ("estado", "Estado", 130),
                ("canal", "Canal", 120),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista las notificaciones registradas."""
        self._tabla.limpiar()
        notificaciones = self._servicio.listar_notificaciones()

        for notificacion in notificaciones:
            self._tabla.agregar_fila(
                identificador=str(notificacion["id"]),
                valores=(
                    notificacion["paciente_id"],
                    notificacion["cita_id"],
                    notificacion["tipo_notificacion"],
                    notificacion["estado"],
                    notificacion["canal"],
                ),
                datos=notificacion,
            )
