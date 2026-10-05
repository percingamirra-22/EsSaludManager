"""
Módulo de seguros médicos.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioSeguro
from src.servicios import SeguroService


class VentanaSeguros(ttk.Frame):
    """Módulo para consultar seguros."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = SeguroService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Seguros",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo seguro",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("tipo", "Tipo", 130),
                ("aseguradora", "Aseguradora", 200),
                ("plan", "Plan", 160),
                ("poliza", "Póliza", 160),
                ("inicio", "Inicio", 130),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los seguros registrados."""
        self._tabla.limpiar()
        seguros = self._servicio.listar_seguros()

        for seguro in seguros:
            self._tabla.agregar_fila(
                identificador=str(seguro.id),
                valores=(
                    seguro.tipo_seguro,
                    seguro.nombre_aseguradora,
                    seguro.codigo_plan,
                    seguro.numero_poliza,
                    seguro.fecha_inicio,
                ),
                datos={"id": seguro.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioSeguro(
            self,
            self._servicio,
            self._listar,
        )
