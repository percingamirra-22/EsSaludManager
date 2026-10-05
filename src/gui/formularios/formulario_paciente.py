"""
Formulario para registro de pacientes.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import messagebox, ttk

from src.servicios import PacienteService


class FormularioPaciente(tk.Toplevel):
    """Ventana modal para registrar un paciente."""

    def __init__(
        self,
        padre: tk.Misc,
        servicio: PacienteService,
        al_guardar: Callable[[], None],
    ) -> None:
        """
        Inicializa el formulario.

        Args:
            padre: Ventana principal.
            servicio: Servicio de pacientes.
            al_guardar: Acción a ejecutar después de guardar.
        """
        super().__init__(padre)
        self.title("Registrar paciente")
        self.geometry("520x560")
        self.resizable(False, False)
        self.configure(background="#F5F7FA")
        self.grab_set()

        self._servicio = servicio
        self._al_guardar = al_guardar

        ttk.Label(
            self,
            text="Registrar paciente",
            style="Titulo.TLabel",
        ).pack(pady=(20, 5))

        ttk.Label(
            self,
            text="Complete los datos obligatorios del paciente.",
            style="Subtitulo.TLabel",
        ).pack(pady=(0, 15))

        formulario = ttk.Frame(self)
        formulario.pack(fill=tk.BOTH, expand=True, padx=24)

        self._codigo = self._crear_campo(formulario, "Código de paciente", 0)
        self._nombres = self._crear_campo(formulario, "Nombres", 1)
        self._apellidos = self._crear_campo(formulario, "Apellidos", 2)
        self._documento = self._crear_campo(formulario, "Número de DNI", 3)

        ttk.Label(formulario, text="Sexo").grid(
            row=4,
            column=0,
            sticky=tk.W,
            pady=6,
        )

        self._sexo = tk.StringVar(value="F")
        ttk.Combobox(
            formulario,
            textvariable=self._sexo,
            values=["F", "M", "O"],
            state="readonly",
            width=25,
        ).grid(row=4, column=1, sticky=tk.EW, pady=6)

        ttk.Label(formulario, text="Fecha de nacimiento (AAAA-MM-DD)").grid(
            row=5,
            column=0,
            sticky=tk.W,
            pady=6,
        )

        self._fecha_nacimiento = ttk.Entry(formulario, width=28)
        self._fecha_nacimiento.grid(row=5, column=1, sticky=tk.EW, pady=6)

        self._telefono = self._crear_campo(formulario, "Teléfono", 6)
        self._email = self._crear_campo(formulario, "Correo electrónico", 7)

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
        """Valida y registra el paciente."""
        try:
            from datetime import date

            fecha_nacimiento = date.fromisoformat(self._fecha_nacimiento.get().strip())

            self._servicio.registrar_paciente(
                codigo_paciente=self._codigo.get().strip(),
                nombres=self._nombres.get().strip(),
                apellidos=self._apellidos.get().strip(),
                tipo_documento="DNI",
                numero_documento=self._documento.get().strip(),
                fecha_nacimiento=fecha_nacimiento,
                sexo=self._sexo.get(),
                telefono=self._telefono.get().strip() or None,
                email=self._email.get().strip() or None,
                usuario_registro="admin",
            )

            messagebox.showinfo(
                "Paciente registrado",
                "El paciente fue registrado correctamente.",
            )
            self._al_guardar()
            self.destroy()

        except ValueError as error:
            messagebox.showerror("Datos inválidos", str(error))
        except RuntimeError as error:
            messagebox.showerror("No se pudo registrar", str(error))
