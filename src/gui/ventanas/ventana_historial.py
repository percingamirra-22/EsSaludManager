"""
Módulo de historial clínico.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.servicios import HistorialService


class VentanaHistorial(ttk.Frame):
    """Módulo para consultar historiales clínicos."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = HistorialService()

        ttk.Label(
            self,
            text="Historial clínico",
            style="Titulo.TLabel",
        ).pack(pady=(24, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("paciente", "ID paciente", 120),
                ("historia", "Número historia", 180),
                ("estado", "Estado", 120),
                ("version", "Versión", 100),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Muestra los historiales registrados."""
        self._tabla.limpiar()
        historiales = self._servicio.listar_historiales()

        for historial in historiales:
            self._tabla.agregar_fila(
                identificador=str(historial.id),
                valores=(
                    historial.paciente_id,
                    historial.numero_historia,
                    historial.estado,
                    historial.version,
                ),
                datos={"id": historial.id},
            )
