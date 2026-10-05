"""
Módulo de gestión de pacientes.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.gui.componentes import BusquedaFiltro, TablaDatos
from src.gui.formularios import FormularioPaciente
from src.servicios import PacienteService


class VentanaPacientes(ttk.Frame):
    """Módulo para buscar, registrar y administrar pacientes."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo de pacientes."""
        super().__init__(padre)

        self._servicio = PacienteService()

        encabezado = ttk.Frame(self)
        encabezado.pack(fill=tk.X, padx=24, pady=(24, 12))

        ttk.Label(
            encabezado,
            text="Pacientes",
            style="Titulo.TLabel",
        ).pack(side=tk.LEFT)

        ttk.Button(
            encabezado,
            text="Nuevo paciente",
            command=self._abrir_formulario,
        ).pack(side=tk.RIGHT)

        busqueda = BusquedaFiltro(
            self,
            "Buscar por apellidos...",
            self._buscar,
        )
        busqueda.pack(fill=tk.X, padx=24, pady=(0, 12))

        self._tabla = TablaDatos(
            self,
            columnas=[
                ("codigo", "Código", 130),
                ("nombres", "Nombres", 180),
                ("apellidos", "Apellidos", 180),
                ("documento", "Documento", 130),
                ("telefono", "Teléfono", 130),
                ("estado", "Estado", 90),
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
            text="Desactivar paciente",
            style="Peligro.TButton",
            command=self._desactivar,
        ).pack(side=tk.RIGHT)

        self._listar_pacientes()

    def _listar_pacientes(self) -> None:
        """Carga los pacientes activos en la tabla."""
        self._tabla.limpiar()

        for paciente in self._servicio.listar_activos():
            self._tabla.agregar_fila(
                identificador=str(paciente.id),
                valores=(
                    paciente.codigo_paciente,
                    paciente.nombres,
                    paciente.apellidos,
                    paciente.numero_documento,
                    paciente.telefono or "",
                    "Activo" if paciente.estado else "Inactivo",
                ),
                datos={"id": paciente.id},
            )

    def _buscar(self, texto: str) -> None:
        """Busca pacientes por apellidos."""
        self._tabla.limpiar()

        if not texto:
            self._listar_pacientes()
            return

        pacientes = self._servicio.buscar_por_apellidos(texto)

        for paciente in pacientes:
            self._tabla.agregar_fila(
                identificador=str(paciente.id),
                valores=(
                    paciente.codigo_paciente,
                    paciente.nombres,
                    paciente.apellidos,
                    paciente.numero_documento,
                    paciente.telefono or "",
                    "Activo" if paciente.estado else "Inactivo",
                ),
                datos={"id": paciente.id},
            )

    def _abrir_formulario(self) -> None:
        """Abre el formulario de registro de paciente."""
        FormularioPaciente(
            self,
            self._servicio,
            self._listar_pacientes,
        )

    def _desactivar(self) -> None:
        """Desactiva el paciente seleccionado."""
        seleccion = self._tabla.obtener_seleccion()

        if seleccion is None:
            messagebox.showwarning(
                "Selección requerida",
                "Seleccione un paciente de la tabla.",
            )
            return

        confirmacion = messagebox.askyesno(
            "Confirmar acción",
            "¿Desea desactivar el paciente seleccionado?",
        )

        if not confirmacion:
            return

        try:
            self._servicio.desactivar_paciente(
                int(seleccion["id"]),
            )
            self._listar_pacientes()
            messagebox.showinfo(
                "Paciente desactivado",
                "El paciente fue desactivado correctamente.",
            )
        except (LookupError, RuntimeError) as error:
            messagebox.showerror("No se pudo desactivar", str(error))
