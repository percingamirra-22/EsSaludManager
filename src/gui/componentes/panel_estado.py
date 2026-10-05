"""
Componente reutilizable para mostrar el estado de una operación.
"""

import tkinter as tk
from tkinter import ttk


class PanelEstado(ttk.Label):
    """Muestra mensajes de estado al usuario."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el panel."""
        super().__init__(padre, text="", style="Subtitulo.TLabel")

    def mostrar_exito(self, mensaje: str) -> None:
        """Muestra un mensaje de éxito."""
        self.configure(text=f"✅ {mensaje}", style="Exito.TLabel")

    def mostrar_error(self, mensaje: str) -> None:
        """Muestra un mensaje de error."""
        self.configure(text=f"❌ {mensaje}", style="Error.TLabel")

    def limpiar(self) -> None:
        """Limpia el mensaje."""
        self.configure(text="")
