"""
Componente reutilizable para botones de acción.
"""

from collections.abc import Callable
from tkinter import ttk


class BotonAccion(ttk.Button):
    """Botón con estilo y comando tipado."""

    def __init__(
        self,
        padre: ttk.Widget,
        texto: str,
        comando: Callable[[], None],
        estilo: str = "TButton",
    ) -> None:
        """Inicializa el botón."""
        super().__init__(
            padre,
            text=texto,
            command=comando,
            style=estilo,
        )
