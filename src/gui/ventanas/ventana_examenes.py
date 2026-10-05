"""
Módulo de exámenes médicos.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioExamen
from src.servicios import ExamenMedicoService


class VentanaExamenes(ttk.Frame):
    """Módulo para consultar exámenes médicos."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = ExamenMedicoService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Exámenes médicos",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo examen",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("servicio", "ID servicio", 130),
                ("orden", "ID orden", 130),
                ("tecnico", "ID técnico", 130),
                ("tipo", "Tipo", 180),
                ("estado", "Estado", 140),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los exámenes registrados."""
        self._tabla.limpiar()
        examenes = self._servicio.listar_examenes()

        for examen in examenes:
            self._tabla.agregar_fila(
                identificador=str(examen["id"]),
                valores=(
                    examen["servicio_id"],
                    examen["orden_examen_id"],
                    examen["tecnico_id"],
                    examen["tipo_examen"],
                    examen["estado"],
                ),
                datos=examen,
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioExamen(
            self,
            self._servicio,
            self._listar,
        )
