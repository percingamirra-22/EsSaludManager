"""
Componente reutilizable para campos de formulario.
"""

import tkinter as tk
from tkinter import ttk


class CampoFormulario(ttk.Frame):
    """Campo de formulario con etiqueta, entrada y mensaje de error."""

    def __init__(
        self,
        padre: tk.Misc,
        etiqueta: str,
        ancho: int = 32,
        es_password: bool = False,
    ) -> None:
        """Inicializa el campo."""
        super().__init__(padre)

        self._variable = tk.StringVar()

        ttk.Label(
            self,
            text=etiqueta,
            style="Subtitulo.TLabel",
        ).pack(anchor=tk.W)

        self._entrada = ttk.Entry(
            self,
            textvariable=self._variable,
            width=ancho,
            show="*" if es_password else "",
        )
        self._entrada.pack(fill=tk.X, pady=(4, 2))

        self._mensaje = ttk.Label(
            self,
            text="",
            style="Error.TLabel",
        )
        self._mensaje.pack(anchor=tk.W)

    def obtener_valor(self) -> str:
        """Retorna el valor ingresado."""
        return self._variable.get().strip()

    def establecer_valor(self, valor: str) -> None:
        """Establece el valor del campo."""
        self._variable.set(valor)

    def mostrar_error(self, mensaje: str) -> None:
        """Muestra un mensaje de error."""
        self._mensaje.configure(text=mensaje)

    def limpiar_error(self) -> None:
        """Limpia el mensaje de error."""
        self._mensaje.configure(text="")
