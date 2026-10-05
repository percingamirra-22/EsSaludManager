"""
Módulo de generación de reportes.
"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.servicios import PacienteService, ReporteService


class VentanaReportes(ttk.Frame):
    """Módulo para generar reportes de pacientes en CSV o PDF."""

    def __init__(self, padre: tk.Misc) -> None:
        """Inicializa el módulo de reportes."""
        super().__init__(padre)

        self._reporte_service = ReporteService()
        self._paciente_service = PacienteService()
        self._formato = tk.StringVar(value="CSV")
        self._separador = tk.StringVar(value=",")

        ttk.Label(
            self,
            text="Reportes",
            style="Titulo.TLabel",
        ).pack(pady=(24, 5))

        ttk.Label(
            self,
            text="Genera un reporte de pacientes activos.",
            style="Subtitulo.TLabel",
        ).pack(pady=(0, 20))

        opciones = ttk.Frame(self)
        opciones.pack(pady=10)

        ttk.Label(
            opciones,
            text="Formato:",
            style="Subtitulo.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Combobox(
            opciones,
            textvariable=self._formato,
            values=["CSV", "PDF"],
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT, padx=(0, 20))

        ttk.Label(
            opciones,
            text="Separador CSV:",
            style="Subtitulo.TLabel",
        ).pack(side=tk.LEFT, padx=(0, 6))

        ttk.Combobox(
            opciones,
            textvariable=self._separador,
            values=[",", ";"],
            state="readonly",
            width=5,
        ).pack(side=tk.LEFT)

        ttk.Button(
            self,
            text="Generar reporte de pacientes",
            command=self._generar_reporte,
        ).pack(pady=20)

    def _crear_reporte_base(self, ruta_archivo: str) -> int:
        """Crea el registro base del reporte."""
        return self._reporte_service.crear_reporte(
            tipo_reporte="pacientes_activos",
            formato=self._formato.get(),
            usuario_solicitante_id=1,
            ruta_archivo=ruta_archivo,
        )

    def _generar_reporte(self) -> None:
        """Genera un reporte de pacientes activos."""
        formato = self._formato.get()
        separador = self._separador.get()

        try:
            pacientes = self._paciente_service.listar_activos()

            filas: list[list[object]] = [
                [
                    paciente.codigo_paciente,
                    paciente.nombres,
                    paciente.apellidos,
                    paciente.numero_documento,
                ]
                for paciente in pacientes
            ]

            encabezados = [
                "Código",
                "Nombres",
                "Apellidos",
                "Documento",
            ]

            if formato == "PDF":
                ruta_archivo = "reportes/pacientes_activos.pdf"
                reporte_id = self._crear_reporte_base(ruta_archivo)

                ruta = self._reporte_service.exportar_pdf(
                    reporte_id=reporte_id,
                    titulo="Reporte de pacientes activos",
                    encabezados=encabezados,
                    filas=filas,
                    ruta_archivo=ruta_archivo,
                )
            else:
                ruta_archivo = "reportes/pacientes_activos.csv"
                reporte_id = self._crear_reporte_base(ruta_archivo)

                ruta = self._reporte_service.exportar_csv(
                    reporte_id=reporte_id,
                    encabezados=encabezados,
                    filas=filas,
                    ruta_archivo=ruta_archivo,
                    separador=separador,
                )

            messagebox.showinfo(
                "Reporte generado",
                f"El reporte fue generado en:\n{ruta}",
            )

        except (ValueError, RuntimeError, LookupError) as error:
            messagebox.showerror(
                "No se pudo generar",
                str(error),
            )
