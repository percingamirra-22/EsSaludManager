"""
Módulo de lotes y stock de medicamentos.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioLote
from src.servicios import MedicamentoService


class VentanaLotes(ttk.Frame):
    """Módulo para consultar lotes y stock."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = MedicamentoService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Lotes y stock",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo lote",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("medicamento", "ID medicamento", 140),
                ("lote", "Número lote", 180),
                ("vencimiento", "Vencimiento", 140),
                ("cantidad", "Cantidad actual", 140),
                ("estado", "Estado", 120),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los lotes registrados."""
        self._tabla.limpiar()
        lotes = self._servicio.listar_lotes_de_medicamento(1, False)

        for lote in lotes:
            self._tabla.agregar_fila(
                identificador=str(lote.id),
                valores=(
                    lote.medicamento_id,
                    lote.numero_lote,
                    lote.fecha_vencimiento,
                    lote.cantidad_actual,
                    lote.estado,
                ),
                datos={"id": lote.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioLote(
            self,
            self._servicio,
            medicamento_id=1,
            al_guardar=self._listar,
        )
