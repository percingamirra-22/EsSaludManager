"""
Módulo de coberturas.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioCobertura
from src.servicios import CoberturaService


class VentanaCoberturas(ttk.Frame):
    """Módulo para consultar coberturas."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = CoberturaService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Coberturas",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nueva cobertura",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("seguro", "ID seguro", 120),
                ("servicio", "ID servicio", 120),
                ("porcentaje", "Porcentaje", 130),
                ("maximo", "Monto máximo", 140),
                ("copago", "Copago", 120),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista las coberturas registradas."""
        self._tabla.limpiar()
        coberturas = self._servicio.listar_coberturas()
        for cobertura in coberturas:
            self._tabla.agregar_fila(
                identificador=str(cobertura.id),
                valores=(
                    cobertura.seguro_id,
                    cobertura.servicio_id,
                    cobertura.porcentaje_cobertura,
                    cobertura.monto_maximo,
                    cobertura.copago_fijo,
                ),
                datos={"id": cobertura.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioCobertura(
            self,
            self._servicio,
            self._listar,
        )
