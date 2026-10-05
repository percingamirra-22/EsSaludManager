"""
Componente reutilizable para búsqueda y filtrado.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class BusquedaFiltro(ttk.Frame):
    """Campo de búsqueda con botón de acción."""

    def __init__(
        self,
        padre: tk.Misc,
        placeholder: str,
        comando: Callable[[str], None],
    ) -> None:
        """
        Inicializa el componente de búsqueda.

        Args:
            padre: Widget contenedor.
            placeholder: Texto orientativo.
            comando: Función que recibe el texto buscado.
        """
        super().__init__(padre)

        self._comando = comando

        self._variable = tk.StringVar()

        self._entrada = ttk.Entry(
            self,
            textvariable=self._variable,
            width=40,
        )
        self._entrada.pack(side=tk.LEFT, padx=(0, 8))

        self._entrada.insert(0, placeholder)
        self._entrada.bind(
            "<FocusIn>",
            self._limpiar_placeholder,
        )

        boton = ttk.Button(
            self,
            text="Buscar",
            command=self._ejecutar_busqueda,
        )
        boton.pack(side=tk.LEFT)

    def _limpiar_placeholder(self, evento: object) -> None:
        """Limpia el texto orientativo al obtener foco."""
        if self._variable.get() == "Buscar...":
            self._entrada.delete(0, tk.END)

    def _ejecutar_busqueda(self) -> None:
        """Ejecuta la búsqueda con el texto ingresado."""
        self._comando(self._variable.get().strip())
