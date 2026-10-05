"""
Formulario para registrar medicamentos.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from src.servicios import MedicamentoService


class FormularioMedicamento(tk.Toplevel):
    """Ventana modal para registrar un medicamento."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: MedicamentoService,
        al_guardar: Callable[[], None],
    ) -> None:
        """
        Inicializa el formulario.

        Args:
            padre: Ventana principal.
            servicio: Servicio de medicamentos.
            al_guardar: Acción posterior al guardado.
        """
        super().__init__(padre)
        self.title("Registrar medicamento")
        self.geometry("520x520")
        self.resizable(False, False)
        self.configure(background="#F5F7FA")
        self.grab_set()

        self._servicio = servicio
        self._al_guardar = al_guardar

        ttk.Label(
            self,
            text="Registrar medicamento",
            style="Titulo.TLabel",
        ).pack(pady=(20, 5))

        formulario = ttk.Frame(self)
        formulario.pack(fill=tk.BOTH, expand=True, padx=24)

        self._codigo = self._crear_campo(formulario, "Código", 0)
        self._generico = self._crear_campo(formulario, "Nombre genérico", 1)
        self._comercial = self._crear_campo(formulario, "Nombre comercial", 2)
        self._forma = self._crear_campo(formulario, "Forma farmacéutica", 3)
        self._concentracion = self._crear_campo(formulario, "Concentración", 4)
        self._unidad = self._crear_campo(formulario, "Unidad de medida", 5)
        self._stock_minimo = self._crear_campo(formulario, "Stock mínimo", 6)

        botones = ttk.Frame(self)
        botones.pack(pady=20)

        ttk.Button(
            botones,
            text="Guardar",
            command=self._guardar,
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            botones,
            text="Cancelar",
            style="Secundario.TButton",
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=6)

    def _crear_campo(
        self,
        contenedor: ttk.Frame,
        etiqueta: str,
        fila: int,
    ) -> ttk.Entry:
        """Crea una etiqueta y un campo de texto."""
        ttk.Label(contenedor, text=etiqueta).grid(
            row=fila,
            column=0,
            sticky=tk.W,
            pady=6,
        )

        entrada = ttk.Entry(contenedor, width=28)
        entrada.grid(row=fila, column=1, sticky=tk.EW, pady=6)

        return entrada

    def _guardar(self) -> None:
        """Valida y registra el medicamento."""
        try:
            self._servicio.registrar_medicamento(
                codigo_medicamento=self._codigo.get().strip(),
                nombre_generico=self._generico.get().strip(),
                nombre_comercial=self._comercial.get().strip(),
                forma_farmaceutica=self._forma.get().strip(),
                concentracion=self._concentracion.get().strip(),
                unidad_medida=self._unidad.get().strip(),
                stock_minimo=int(self._stock_minimo.get() or 0),
            )

            messagebox.showinfo(
                "Medicamento registrado",
                "El medicamento fue registrado correctamente.",
            )
            self._al_guardar()
            self.destroy()

        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))
        except RuntimeError as error:
            messagebox.showerror("No se pudo registrar", str(error))
