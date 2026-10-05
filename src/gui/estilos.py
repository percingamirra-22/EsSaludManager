"""
Estilos visuales y configuración de tema para EsSaludManager.
"""

import tkinter as tk
from tkinter import ttk


class EstilosEsSalud:
    """Define colores, tipografía y estilos ttk de la aplicación."""

    COLOR_PRINCIPAL = "#007AC9"
    COLOR_SECUNDARIO = "#3DB7E4"
    COLOR_FONDO = "#F5F7FA"
    COLOR_SUPERFICIE = "#FFFFFF"
    COLOR_TEXTO = "#1F2933"
    COLOR_TEXTO_SUAVE = "#52606D"
    COLOR_EXITO = "#00A557"
    COLOR_ADVERTENCIA = "#FFC63D"
    COLOR_ERROR = "#EF4B4A"
    COLOR_BORDE = "#CBD2D9"

    FUENTE_PRINCIPAL = "Tahoma"
    FUENTE_SECUNDARIA = "Arial"

    def __init__(self) -> None:
        """Inicializa la configuración visual de ttk."""
        self._configurar_estilos()

    def aplicar_fondo(self, ventana: tk.Tk | tk.Toplevel) -> None:
        """Aplica el fondo institucional a una ventana."""
        ventana.configure(background=self.COLOR_FONDO)

    def _configurar_estilos(self) -> None:
        """Configura los estilos disponibles para widgets ttk."""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TFrame",
            background=self.COLOR_FONDO,
        )

        estilo.configure(
            "Superficie.TFrame",
            background=self.COLOR_SUPERFICIE,
        )

        estilo.configure(
            "TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_TEXTO,
            font=(self.FUENTE_PRINCIPAL, 10),
        )

        estilo.configure(
            "Titulo.TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_PRINCIPAL,
            font=(self.FUENTE_PRINCIPAL, 16, "bold"),
        )

        estilo.configure(
            "Subtitulo.TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_TEXTO_SUAVE,
            font=(self.FUENTE_SECUNDARIA, 10),
        )

        estilo.configure(
            "Superficie.TLabel",
            background=self.COLOR_SUPERFICIE,
            foreground=self.COLOR_TEXTO,
        )

        estilo.configure(
            "TButton",
            background=self.COLOR_PRINCIPAL,
            foreground="#FFFFFF",
            font=(self.FUENTE_PRINCIPAL, 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )

        estilo.map(
            "TButton",
            background=[
                ("active", "#0069AC"),
                ("pressed", "#005A94"),
            ],
        )

        estilo.configure(
            "Secundario.TButton",
            background=self.COLOR_SECUNDARIO,
            foreground="#FFFFFF",
        )

        estilo.map(
            "Secundario.TButton",
            background=[
                ("active", "#2FA3CE"),
                ("pressed", "#278FB8"),
            ],
        )

        estilo.configure(
            "Peligro.TButton",
            background=self.COLOR_ERROR,
            foreground="#FFFFFF",
        )

        estilo.map(
            "Peligro.TButton",
            background=[
                ("active", "#D63F3E"),
                ("pressed", "#C23635"),
            ],
        )

        estilo.configure(
            "TEntry",
            padding=6,
            font=(self.FUENTE_PRINCIPAL, 10),
        )

        estilo.configure(
            "Treeview",
            background=self.COLOR_SUPERFICIE,
            foreground=self.COLOR_TEXTO,
            fieldbackground=self.COLOR_SUPERFICIE,
            rowheight=28,
            font=(self.FUENTE_SECUNDARIA, 10),
        )

        estilo.configure(
            "Treeview.Heading",
            background=self.COLOR_PRINCIPAL,
            foreground="#FFFFFF",
            font=(self.FUENTE_PRINCIPAL, 10, "bold"),
            padding=8,
        )

        estilo.configure(
            "Error.TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_ERROR,
            font=(self.FUENTE_SECUNDARIA, 9),
        )

        estilo.configure(
            "Exito.TLabel",
            background=self.COLOR_FONDO,
            foreground=self.COLOR_EXITO,
            font=(self.FUENTE_SECUNDARIA, 10, "bold"),
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", self.COLOR_SECUNDARIO),
            ],
            foreground=[
                ("selected", "#FFFFFF"),
            ],
        )
