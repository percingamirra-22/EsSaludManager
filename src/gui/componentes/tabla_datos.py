"""
Componente reutilizable para tablas de datos.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any


class TablaDatos(ttk.Frame):
    """Tabla basada en Treeview para mostrar registros."""

    def __init__(
        self,
        padre: tk.Misc,
        columnas: list[tuple[str, str, int]],
        alto: int = 12,
    ) -> None:
        """
        Inicializa la tabla.

        Args:
            padre: Widget contenedor.
            columnas: Lista con (id_columna, titulo, ancho).
            alto: Cantidad visible de filas.
        """
        super().__init__(padre)

        self._columnas = columnas
        self._filas: dict[str, dict[str, Any]] = {}

        contenedor = ttk.Frame(self, style="Superficie.TFrame")
        contenedor.pack(fill=tk.BOTH, expand=True)

        identificadores = [columna[0] for columna in columnas]

        self._tabla = ttk.Treeview(
            contenedor,
            columns=identificadores,
            show="headings",
            height=alto,
        )

        for identificador, titulo, ancho in columnas:
            self._tabla.heading(identificador, text=titulo)
            self._tabla.column(
                identificador,
                width=ancho,
                anchor=tk.W,
            )

        barra = ttk.Scrollbar(
            contenedor,
            orient=tk.VERTICAL,
            command=self._desplazar_vertical,
        )
        self._tabla.configure(yscrollcommand=barra.set)

        self._tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        barra.pack(side=tk.RIGHT, fill=tk.Y)

    def _desplazar_vertical(self, inicio: float, fin: float) -> None:
        """
        Desplaza verticalmente la tabla.

        Args:
            inicio: Posición inicial visible.
            fin: Posición final visible.
        """
        self._tabla.yview_moveto(inicio)

    def limpiar(self) -> None:
        """Elimina todas las filas mostradas."""
        self._tabla.delete(*self._tabla.get_children())
        self._filas.clear()

    def agregar_fila(
        self,
        identificador: str,
        valores: tuple[object, ...],
        datos: dict[str, Any],
    ) -> None:
        """
        Agrega una fila a la tabla.

        Args:
            identificador: ID único interno de la fila.
            valores: Valores visibles en las columnas.
            datos: Datos asociados a la fila.
        """
        self._tabla.insert("", tk.END, iid=identificador, values=valores)
        self._filas[identificador] = datos

    def obtener_seleccion(self) -> dict[str, Any] | None:
        """
        Obtiene los datos de la fila seleccionada.

        Returns:
            Datos asociados o None si no hay selección.
        """
        seleccion = self._tabla.selection()

        if not seleccion:
            return None

        return self._filas.get(seleccion[0])
