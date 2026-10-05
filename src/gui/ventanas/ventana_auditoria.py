"""
Módulo de auditoría.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.servicios import AuditoriaService


class VentanaAuditoria(ttk.Frame):
    """Módulo para consultar eventos de auditoría."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = AuditoriaService()

        ttk.Label(
            self,
            text="Auditoría",
            style="Titulo.TLabel",
        ).pack(pady=(24, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("usuario", "ID usuario", 120),
                ("accion", "Acción", 140),
                ("recurso", "Recurso", 160),
                ("recurso_id", "ID recurso", 120),
                ("fecha", "Fecha", 220),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los eventos de auditoría."""
        self._tabla.limpiar()
        eventos = self._servicio.obtener_historial(limite=100)

        for evento in eventos:
            self._tabla.agregar_fila(
                identificador=str(evento["id"]),
                valores=(
                    evento["usuario_id"],
                    evento["accion"],
                    evento["recurso"],
                    evento["recurso_id"],
                    evento["fecha_accion"],
                ),
                datos=evento,
            )
