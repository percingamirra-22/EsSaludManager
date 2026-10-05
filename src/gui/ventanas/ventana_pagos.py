"""
Módulo de pagos.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioPago
from src.servicios import PagoService


class VentanaPagos(ttk.Frame):
    """Módulo para consultar pagos."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = PagoService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Pagos",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo pago",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("factura", "ID factura", 130),
                ("monto", "Monto", 130),
                ("metodo", "Método", 160),
                ("estado", "Estado", 140),
                ("usuario", "Usuario", 180),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista los pagos registrados."""
        self._tabla.limpiar()
        pagos = self._servicio.obtener_pagos(1)

        for pago in pagos:
            self._tabla.agregar_fila(
                identificador=str(pago.id),
                valores=(
                    pago.factura_id,
                    pago.monto,
                    pago.metodo_pago,
                    pago.estado,
                    pago.usuario_registro,
                ),
                datos={"id": pago.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioPago(
            self,
            self._servicio,
            factura_id=1,
            al_guardar=self._listar,
        )
