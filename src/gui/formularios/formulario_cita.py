"""
Formulario para programar citas médicas.
"""

import tkinter as tk
from collections.abc import Callable
from datetime import datetime
from tkinter import messagebox, ttk
from zoneinfo import ZoneInfo

from src.servicios import CitaService

ZONA_LIMA = ZoneInfo("America/Lima")


class FormularioCita(tk.Toplevel):
    """Ventana modal para programar una cita."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: CitaService,
        paciente_id: int,
        al_guardar: Callable[[], None],
    ) -> None:
        """
        Inicializa el formulario.

        Args:
            padre: Ventana principal.
            servicio: Servicio de citas.
            paciente_id: ID del paciente seleccionado.
            al_guardar: Acción posterior al guardado.
        """
        super().__init__(padre)
        self.title("Programar cita")
        self.geometry("520x360")
        self.resizable(False, False)
        self.configure(background="#F5F7FA")
        self.grab_set()

        self._servicio = servicio
        self._paciente_id = paciente_id
        self._al_guardar = al_guardar

        ttk.Label(
            self,
            text="Programar cita",
            style="Titulo.TLabel",
        ).pack(pady=(20, 5))

        ttk.Label(
            self,
            text="Use el formato AAAA-MM-DD HH:MM.",
            style="Subtitulo.TLabel",
        ).pack(pady=(0, 15))

        formulario = ttk.Frame(self)
        formulario.pack(fill=tk.BOTH, expand=True, padx=24)

        ttk.Label(formulario, text="Servicio ID").grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=6,
        )
        self._servicio_id = ttk.Entry(formulario, width=25)
        self._servicio_id.insert(0, "1")
        self._servicio_id.grid(row=0, column=1, sticky=tk.EW, pady=6)

        ttk.Label(formulario, text="Recepcionista ID").grid(
            row=1,
            column=0,
            sticky=tk.W,
            pady=6,
        )
        self._recepcionista_id = ttk.Entry(formulario, width=25)
        self._recepcionista_id.insert(0, "1")
        self._recepcionista_id.grid(row=1, column=1, sticky=tk.EW, pady=6)

        ttk.Label(formulario, text="Fecha y hora de inicio").grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=6,
        )
        self._inicio = ttk.Entry(formulario, width=25)
        self._inicio.grid(row=2, column=1, sticky=tk.EW, pady=6)

        ttk.Label(formulario, text="Fecha y hora de fin").grid(
            row=3,
            column=0,
            sticky=tk.W,
            pady=6,
        )
        self._fin = ttk.Entry(formulario, width=25)
        self._fin.grid(row=3, column=1, sticky=tk.EW, pady=6)

        ttk.Label(formulario, text="Motivo").grid(
            row=4,
            column=0,
            sticky=tk.W,
            pady=6,
        )
        self._motivo = ttk.Entry(formulario, width=25)
        self._motivo.grid(row=4, column=1, sticky=tk.EW, pady=6)

        botones = ttk.Frame(self)
        botones.pack(pady=20)

        ttk.Button(
            botones,
            text="Programar",
            command=self._guardar,
        ).pack(side=tk.LEFT, padx=6)

        ttk.Button(
            botones,
            text="Cancelar",
            style="Secundario.TButton",
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=6)

    def _guardar(self) -> None:
        """Valida y programa la cita."""
        try:
            inicio = datetime.fromisoformat(self._inicio.get().strip()).replace(
                tzinfo=ZONA_LIMA
            )

            fin = datetime.fromisoformat(self._fin.get().strip()).replace(
                tzinfo=ZONA_LIMA
            )

            self._servicio.programar_cita(
                paciente_id=self._paciente_id,
                recepcionista_id=int(self._recepcionista_id.get()),
                servicio_id=int(self._servicio_id.get()),
                fecha_inicio=inicio,
                fecha_fin=fin,
                usuario_creacion="recepcionista",
                motivo=self._motivo.get().strip() or None,
            )

            messagebox.showinfo(
                "Cita programada",
                "La cita fue programada correctamente.",
            )
            self._al_guardar()
            self.destroy()

        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))
        except RuntimeError as error:
            messagebox.showerror("No se pudo programar", str(error))
