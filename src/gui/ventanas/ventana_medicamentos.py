"""
Módulo de gestión de medicamentos.
"""

import tkinter as tk
from tkinter import ttk

from src.gui.componentes import BusquedaFiltro, TablaDatos
from src.gui.formularios import FormularioMedicamento
from src.servicios import MedicamentoService


class VentanaMedicamentos(ttk.Frame):
    """Módulo para buscar y registrar medicamentos."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo de medicamentos."""
        super().__init__(padre)

        self._servicio = MedicamentoService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Medicamentos",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo medicamento",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        busqueda = BusquedaFiltro(
            self,
            "Buscar por nombre...",
            self._buscar,
        )
        busqueda.pack(fill=tk.X, padx=24, pady=(0, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("codigo", "Código", 130),
                ("generico", "Nombre genérico", 200),
                ("comercial", "Nombre comercial", 180),
                ("forma", "Forma", 140),
                ("concentracion", "Concentración", 130),
                ("stock", "Stock mínimo", 120),
            ],
        )
        self._tabla.pack(
            fill=tk.BOTH,
            expand=True,
            padx=24,
            pady=(0, 24),
        )

        self._listar_medicamentos()

    def _listar_medicamentos(self) -> None:
        """Muestra los medicamentos registrados."""
        self._tabla.limpiar()

        medicamentos = self._servicio.buscar_por_nombre("")

        for medicamento in medicamentos:
            self._tabla.agregar_fila(
                identificador=str(medicamento.id),
                valores=(
                    medicamento.codigo_medicamento,
                    medicamento.nombre_generico,
                    medicamento.nombre_comercial,
                    medicamento.forma_farmaceutica,
                    medicamento.concentracion,
                    medicamento.stock_minimo,
                ),
                datos={"id": medicamento.id},
            )

    def _buscar(self, texto: str) -> None:
        """Busca medicamentos por nombre."""
        self._tabla.limpiar()

        if not texto:
            self._listar_medicamentos()
            return

        medicamentos = self._servicio.buscar_por_nombre(texto)

        for medicamento in medicamentos:
            self._tabla.agregar_fila(
                identificador=str(medicamento.id),
                valores=(
                    medicamento.codigo_medicamento,
                    medicamento.nombre_generico,
                    medicamento.nombre_comercial,
                    medicamento.forma_farmaceutica,
                    medicamento.concentracion,
                    medicamento.stock_minimo,
                ),
                datos={"id": medicamento.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro de medicamento."""
        FormularioMedicamento(
            self,
            self._servicio,
            self._listar_medicamentos,
        )
