"""
Módulo de usuarios.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.servicios import UsuarioService


class VentanaUsuarios(ttk.Frame):
    """Módulo para consultar usuarios."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = UsuarioService()

        ttk.Label(
            self,
            text="Usuarios",
            style="Titulo.TLabel",
        ).pack(pady=(24, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("empleado", "ID empleado", 140),
                ("username", "Usuario", 180),
                ("email", "Correo", 260),
                ("estado", "Estado", 110),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los usuarios registrados."""
        self._tabla.limpiar()
        usuarios = self._servicio.listar_usuarios()

        for usuario in usuarios:
            self._tabla.agregar_fila(
                identificador=str(usuario["id"]),
                valores=(
                    usuario["empleado_id"],
                    usuario["username"],
                    usuario["email"],
                    usuario["estado"],
                ),
                datos=usuario,
            )
