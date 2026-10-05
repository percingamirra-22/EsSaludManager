"""
Formulario base reutilizable para la GUI.
"""

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from src.gui.componentes.campo_formulario import CampoFormulario
from src.gui.componentes.panel_estado import PanelEstado


class FormularioBase(tk.Toplevel):
    """Ventana modal base para formularios de registro."""

    def __init__(
        self,
        padre: tk.Misc,
        titulo: str,
        al_guardar: Callable[[], None],
    ) -> None:
        """Inicializa el formulario."""
        super().__init__(padre)

        self.title(titulo)
        self.geometry("460x520")
        self.resizable(False, False)
        self.grab_set()

        self._al_guardar = al_guardar
        self._campos: dict[str, CampoFormulario] = {}

        ttk.Label(
            self,
            text=titulo,
            style="Titulo.TLabel",
        ).pack(pady=(20, 12))

        self._cuerpo = ttk.Frame(self)
        self._cuerpo.pack(fill=tk.BOTH, expand=True, padx=24)

        self._estado = PanelEstado(self)
        self._estado.pack(pady=10)

        botones = ttk.Frame(self)
        botones.pack(pady=(0, 20))

        ttk.Button(
            botones,
            text="Guardar",
            command=self._guardar,
        ).pack(side=tk.LEFT, padx=8)

        ttk.Button(
            botones,
            text="Cancelar",
            command=self.destroy,
        ).pack(side=tk.LEFT, padx=8)

    def agregar_campo(
        self,
        nombre: str,
        etiqueta: str,
        es_password: bool = False,
    ) -> CampoFormulario:
        """Agrega un campo al formulario."""
        campo = CampoFormulario(
            self._cuerpo,
            etiqueta,
            es_password=es_password,
        )
        campo.pack(fill=tk.X, pady=6)
        self._campos[nombre] = campo
        return campo

    def obtener_valor(self, nombre: str) -> str:
        """Obtiene el valor de un campo."""
        return self._campos[nombre].obtener_valor()

    def marcar_error(self, nombre: str, mensaje: str) -> None:
        """Muestra un error en un campo."""
        self._campos[nombre].mostrar_error(mensaje)

    def _guardar(self) -> None:
        """Valida y guarda el formulario."""
        for campo in self._campos.values():
            campo.limpiar_error()

        try:
            self.guardar()
        except (ValueError, RuntimeError, LookupError) as error:
            self._estado.mostrar_error(str(error))

    def guardar(self) -> None:
        """Debe implementarse en cada formulario concreto."""
        raise NotImplementedError

    def _notificar_guardado(self) -> None:
        """Notifica el guardado y cierra el formulario."""
        self._al_guardar()
        self.destroy()
