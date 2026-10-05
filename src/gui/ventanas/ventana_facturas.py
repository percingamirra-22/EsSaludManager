"""
Módulo de facturación.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioFactura
from src.servicios import FacturaService


class VentanaFacturas(ttk.Frame):
    """Módulo para consultar facturas."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo."""
        super().__init__(padre)
        self._servicio = FacturaService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Facturación",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nueva factura",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("numero", "Número", 160),
                ("paciente", "ID paciente", 130),
                ("estado", "Estado", 130),
                ("total", "Monto total", 130),
                ("paciente_monto", "Monto paciente", 150),
            ],
        )
        self._tabla.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 24))

        self._listar()

    def _listar(self) -> None:
        """Lista las facturas registradas."""
        self._tabla.limpiar()
        facturas = self._servicio.listar_facturas()

        for factura in facturas:
            self._tabla.agregar_fila(
                identificador=str(factura.id),
                valores=(
                    factura.numero_factura,
                    factura.paciente_id,
                    factura.estado,
                    factura.monto_total,
                    factura.monto_paciente,
                ),
                datos={"id": factura.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro."""
        FormularioFactura(
            self,
            self._servicio,
            self._listar,
        )
