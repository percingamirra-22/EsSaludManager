"""
Módulo de gestión de citas médicas.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from src.gui.componentes import TablaDatos
from src.gui.formularios import FormularioCita
from src.servicios import CitaService, PacienteService


class VentanaCitas(ttk.Frame):
    """Módulo para consultar y programar citas."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo de citas."""
        super().__init__(padre)

        self._cita_service = CitaService()
        self._paciente_service = PacienteService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Citas médicas",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Programar cita",
            command=self._programar_cita,
        ).pack(side=tk.RIGHT)

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("id", "ID", 70),
                ("paciente", "Paciente ID", 120),
                ("servicio", "Servicio ID", 120),
                ("inicio", "Inicio", 190),
                ("fin", "Fin", 190),
                ("estado", "Estado", 130),
            ],
        )
        self._tabla.pack(
            fill=tk.BOTH,
            expand=True,
            padx=24,
            pady=(0, 24),
        )

        acciones = ttk.Frame(self)
        acciones.pack(fill=tk.X, padx=24, pady=(0, 24))

        ttk.Button(
            acciones,
            text="Cancelar cita",
            style="Peligro.TButton",
            command=self._cancelar_cita,
        ).pack(side=tk.RIGHT)

    def _programar_cita(self) -> None:
        """Solicita un paciente y abre el formulario de cita."""
        texto = simpledialog.askstring(
            "Programar cita",
            "Ingrese el ID del paciente:",
            parent=self,
        )

        if not texto:
            return

        try:
            paciente_id = int(texto)
            self._paciente_service.obtener_paciente(paciente_id)
        except ValueError:
            messagebox.showerror(
                "ID inválido",
                "Debe ingresar un número entero.",
            )
            return
        except LookupError as error:
            messagebox.showerror("Paciente no encontrado", str(error))
            return

        FormularioCita(
            self,
            self._cita_service,
            paciente_id,
            self._listar_citas,
        )

    def _listar_citas(self) -> None:
        """Muestra las citas registradas."""
        self._tabla.limpiar()

        for paciente in self._paciente_service.listar_activos():
            citas = self._cita_service.listar_citas_de_paciente(int(paciente.id or 0))

            for cita in citas:
                self._tabla.agregar_fila(
                    identificador=str(cita.id),
                    valores=(
                        cita.id,
                        cita.paciente_id,
                        cita.servicio_id,
                        cita.fecha_inicio.strftime("%Y-%m-%d %H:%M"),
                        cita.fecha_fin.strftime("%Y-%m-%d %H:%M"),
                        cita.estado,
                    ),
                    datos={"id": cita.id},
                )

    def _cancelar_cita(self) -> None:
        """Cancela la cita seleccionada."""
        seleccion = self._tabla.obtener_seleccion()

        if seleccion is None:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione una cita de la tabla.",
            )
            return

        confirmacion = messagebox.askyesno(
            "Confirmar acción",
            "¿Desea cancelar la cita seleccionada?",
        )

        if not confirmacion:
            return

        try:
            self._cita_service.cancelar_cita(
                int(seleccion["id"]),
                "Cancelada desde la interfaz",
                "recepcionista",
            )
            self._listar_citas()
            messagebox.showinfo(
                "Cita cancelada",
                "La cita fue cancelada correctamente.",
            )
        except (LookupError, RuntimeError) as error:
            messagebox.showerror("No se pudo cancelar", str(error))
