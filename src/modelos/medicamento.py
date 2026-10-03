"""
Modelo de dominio para medicamentos.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_entero_no_negativo,
    validar_no_vacio,
)


@dataclass
class Medicamento:
    """Representa un medicamento del catálogo institucional."""

    codigo_medicamento: str
    nombre_generico: str
    nombre_comercial: str
    forma_farmaceutica: str
    concentracion: str
    unidad_medida: str
    id: int | None = None
    requiere_receta: bool = False
    stock_minimo: int = 0
    estado: bool = True
    fecha_registro: datetime | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del medicamento."""
        self.codigo_medicamento = validar_no_vacio(
            self.codigo_medicamento,
            "codigo_medicamento",
        ).upper()
        self.nombre_generico = validar_no_vacio(
            self.nombre_generico,
            "nombre_generico",
        )
        self.nombre_comercial = validar_no_vacio(
            self.nombre_comercial,
            "nombre_comercial",
        )
        self.forma_farmaceutica = validar_no_vacio(
            self.forma_farmaceutica,
            "forma_farmaceutica",
        )
        self.concentracion = validar_no_vacio(
            self.concentracion,
            "concentracion",
        )
        self.unidad_medida = validar_no_vacio(
            self.unidad_medida,
            "unidad_medida",
        )
        self.stock_minimo = validar_entero_no_negativo(
            int(self.stock_minimo),
            "stock_minimo",
        )

    def requiere_receta_medica(self) -> bool:
        """
        Indica si la dispensación requiere receta.

        Returns:
            True cuando requiere receta.
        """
        return self.requiere_receta

    def verificar_stock(self, stock_total: int) -> bool:
        """
        Determina si el stock total cumple el mínimo definido.

        Args:
            stock_total: Stock total calculado a partir de los lotes.

        Returns:
            True cuando el stock es suficiente.
        """
        validar_entero_no_negativo(stock_total, "stock_total")
        return stock_total >= self.stock_minimo

    def generar_alerta_stock(self, stock_total: int) -> bool:
        """
        Indica si el medicamento requiere alerta de stock bajo.

        Args:
            stock_total: Stock total calculado.

        Returns:
            True si el stock está por debajo del mínimo.
        """
        return not self.verificar_stock(stock_total)

    def actualizar(self, datos: dict[str, Any]) -> None:
        """Actualiza atributos permitidos del medicamento."""
        campos_permitidos = {
            "nombre_generico",
            "nombre_comercial",
            "forma_farmaceutica",
            "concentracion",
            "unidad_medida",
            "requiere_receta",
            "stock_minimo",
            "estado",
        }
        campos_invalidos = set(datos) - campos_permitidos

        if campos_invalidos:
            campos = ", ".join(sorted(campos_invalidos))
            raise ValueError(f"Campos no actualizables para medicamento: {campos}.")

        for campo, valor in datos.items():
            setattr(self, campo, valor)

        self.__post_init__()

    def desactivar(self) -> None:
        """Desactiva lógicamente el medicamento."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato de columnas SQLite."""
        return {
            "codigo_medicamento": self.codigo_medicamento,
            "nombre_generico": self.nombre_generico,
            "nombre_comercial": self.nombre_comercial,
            "forma_farmaceutica": self.forma_farmaceutica,
            "concentracion": self.concentracion,
            "unidad_medida": self.unidad_medida,
            "requiere_receta": int(self.requiere_receta),
            "stock_minimo": self.stock_minimo,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Medicamento":
        """Crea un Medicamento desde una fila SQLite."""
        fecha_registro = fila.get("fecha_registro")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            codigo_medicamento=str(fila["codigo_medicamento"]),
            nombre_generico=str(fila["nombre_generico"]),
            nombre_comercial=str(fila["nombre_comercial"]),
            forma_farmaceutica=str(fila["forma_farmaceutica"]),
            concentracion=str(fila["concentracion"]),
            unidad_medida=str(fila["unidad_medida"]),
            requiere_receta=bool(fila.get("requiere_receta", 0)),
            stock_minimo=int(fila.get("stock_minimo", 0)),
            estado=bool(fila.get("estado", 1)),
            fecha_registro=(
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
        )
