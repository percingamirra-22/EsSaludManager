"""
Módulo de recetas médicas.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioReceta
from src.servicios import RecetaService


class VentanaRecetas(ttk.Frame):
    """Módulo para consultar recetas médicas."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = RecetaService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Recetas médicas",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nueva receta",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("paciente", "ID paciente", 130),
                ("especialista", "ID especialista", 150),
                ("estado", "Estado", 140),
                ("emisor", "Usuario emisor", 180),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista las recetas registradas."""
        self._tabla.limpiar()
        recetas = self._servicio.listar_recetas()

        for receta in recetas:
            self._tabla.agregar_fila(
                identificador=str(receta.id),
                valores=(
                    receta.paciente_id,
                    receta.especialista_id,
                    receta.estado,
                    receta.usuario_emisor,
                ),
                datos={"id": receta.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioReceta(
            self,
            self._servicio,
            self._listar,
        )
