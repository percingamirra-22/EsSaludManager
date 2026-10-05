"""
Ventana principal de EsSaludManager.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from src.gui.estilos import EstilosEsSalud
from src.gui.ventanas.ventana_citas import VentanaCitas
from src.gui.ventanas.ventana_medicamentos import VentanaMedicamentos
from src.gui.ventanas.ventana_pacientes import VentanaPacientes
from src.gui.ventanas.ventana_reportes import VentanaReportes


class VentanaPrincipal(tk.Tk):
    """Ventana principal con navegación por módulos."""

    def __init__(self, usuario: dict[str, object]) -> None:
        """
        Inicializa la ventana principal.

        Args:
            usuario: Datos del usuario autenticado.
        """
        super().__init__()

        self.title("EsSaludManager")
        self.geometry("1100x680")
        self.minsize(960, 620)

        estilos = EstilosEsSalud()
        estilos.aplicar_fondo(self)

        self._usuario = usuario

        encabezado = tk.Frame(
            self,
            background=EstilosEsSalud.COLOR_PRINCIPAL,
            height=70,
        )
        encabezado.pack(fill=tk.X)

        tk.Label(
            encabezado,
            text="EsSaludManager",
            background=EstilosEsSalud.COLOR_PRINCIPAL,
            foreground="#FFFFFF",
            font=(EstilosEsSalud.FUENTE_PRINCIPAL, 18, "bold"),
        ).pack(side=tk.LEFT, padx=24)

        tk.Label(
            encabezado,
            text=f"Usuario: {usuario.get('username', '')}",
            background=EstilosEsSalud.COLOR_PRINCIPAL,
            foreground="#FFFFFF",
            font=(EstilosEsSalud.FUENTE_SECUNDARIA, 10),
        ).pack(side=tk.RIGHT, padx=24)

        contenedor = ttk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True)

        menu = ttk.Frame(contenedor, width=220)
        menu.pack(side=tk.LEFT, fill=tk.Y)

        contenido = ttk.Frame(contenedor)
        contenido.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
        )

        self._contenido = contenido

        self._crear_boton_menu(menu, "Pacientes", self._mostrar_pacientes)
        self._crear_boton_menu(menu, "Citas", self._mostrar_citas)
        self._crear_boton_menu(menu, "Medicamentos", self._mostrar_medicamentos)
        self._crear_boton_menu(menu, "Reportes", self._mostrar_reportes)

        self._mostrar_pacientes()

    def _crear_boton_menu(
        self,
        menu: ttk.Frame,
        texto: str,
        comando: Callable[[], None],
    ) -> None:
        """Crea un botón del menú lateral."""
        ttk.Button(
            menu,
            text=texto,
            style="Secundario.TButton",
            command=comando,
        ).pack(fill=tk.X, padx=16, pady=10)

    def _limpiar_contenido(self) -> None:
        """Elimina los módulos mostrados actualmente."""
        for widget in self._contenido.winfo_children():
            widget.destroy()

    def _mostrar_pacientes(self) -> None:
        """Muestra el módulo de pacientes."""
        self._limpiar_contenido()
        VentanaPacientes(self._contenido).pack(
            fill=tk.BOTH,
            expand=True,
        )

    def _mostrar_citas(self) -> None:
        """Muestra el módulo de citas."""
        self._limpiar_contenido()
        VentanaCitas(self._contenido).pack(
            fill=tk.BOTH,
            expand=True,
        )

    def _mostrar_medicamentos(self) -> None:
        """Muestra el módulo de medicamentos."""
        self._limpiar_contenido()
        VentanaMedicamentos(self._contenido).pack(
            fill=tk.BOTH,
            expand=True,
        )

    def _mostrar_reportes(self) -> None:
        """Muestra el módulo de reportes."""
        self._limpiar_contenido()
        VentanaReportes(self._contenido).pack(
            fill=tk.BOTH,
            expand=True,
        )
