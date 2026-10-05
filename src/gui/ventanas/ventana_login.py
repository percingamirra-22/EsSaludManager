"""
Ventana de inicio de sesión.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from src.gui.estilos import EstilosEsSalud
from src.servicios import UsuarioService


class VentanaLogin(tk.Tk):
    """Ventana inicial de autenticación."""

    def __init__(
        self,
        al_iniciar_sesion: Callable[[dict[str, object]], None],
    ) -> None:
        """
        Inicializa la ventana de login.

        Args:
            al_iniciar_sesion: Acción al autenticar correctamente.
        """
        super().__init__()

        self.title("EsSaludManager - Iniciar sesión")
        self.geometry("420x420")
        self.resizable(False, False)

        estilos = EstilosEsSalud()
        estilos.aplicar_fondo(self)

        self._usuario_service = UsuarioService()
        self._al_iniciar_sesion = al_iniciar_sesion

        encabezado = tk.Frame(
            self,
            background=EstilosEsSalud.COLOR_PRINCIPAL,
            height=90,
        )
        encabezado.pack(fill=tk.X)

        tk.Label(
            encabezado,
            text="EsSaludManager",
            background=EstilosEsSalud.COLOR_PRINCIPAL,
            foreground="#FFFFFF",
            font=(EstilosEsSalud.FUENTE_PRINCIPAL, 18, "bold"),
        ).pack(expand=True)

        formulario = ttk.Frame(self, padding=30)
        formulario.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            formulario,
            text="Inicio de sesión",
            style="Titulo.TLabel",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(formulario, text="Usuario").grid(
            row=1,
            column=0,
            sticky=tk.W,
            pady=8,
        )

        self._usuario = ttk.Entry(formulario, width=28)
        self._usuario.grid(row=1, column=1, sticky=tk.EW, pady=8)

        ttk.Label(formulario, text="Contraseña").grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=8,
        )

        self._password = ttk.Entry(
            formulario,
            width=28,
            show="•",
        )
        self._password.grid(row=2, column=1, sticky=tk.EW, pady=8)

        ttk.Button(
            formulario,
            text="Iniciar sesión",
            command=self._autenticar,
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            sticky=tk.EW,
            pady=(25, 0),
        )

        self._usuario.focus_set()
        self.bind("<Return>", lambda evento: self._autenticar())

    def _autenticar(self) -> None:
        """Valida las credenciales e inicia la sesión."""
        usuario = self._usuario.get().strip()
        password = self._password.get()

        if not usuario or not password:
            messagebox.showwarning(
                "Campos incompletos",
                "Ingrese usuario y contraseña.",
            )
            return

        resultado = self._usuario_service.autenticar(usuario, password)

        if resultado is None:
            messagebox.showerror(
                "Credenciales inválidas",
                "El usuario o la contraseña son incorrectos.",
            )
            return

        self._al_iniciar_sesion(resultado)
        self.destroy()
