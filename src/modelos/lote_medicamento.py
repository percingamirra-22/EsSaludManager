"""
Modelo de dominio para lotes de medicamentos.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_no_negativo,
    validar_entero_positivo,
    validar_no_vacio,
    validar_rango_fechas,
)

ESTADOS_LOTE = frozenset({"activo", "agotado", "vencido"})


@dataclass
class LoteMedicamento:
    """Representa un lote trazable de un medicamento."""

    medicamento_id: int
    proveedor_id: int
    numero_lote: str
    fecha_fabricacion: date
    fecha_vencimiento: date
    cantidad_inicial: int
    id: int | None = None
    cantidad_actual: int | None = None
    estado: str = "activo"
    fecha_registro: datetime | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del lote."""
        self.medicamento_id = validar_entero_positivo(
            self.medicamento_id,
            "medicamento_id",
        )
        self.proveedor_id = validar_entero_positivo(
            self.proveedor_id,
            "proveedor_id",
        )
        self.numero_lote = validar_no_vacio(
            self.numero_lote,
            "numero_lote",
        ).upper()
        validar_rango_fechas(
            self.fecha_fabricacion,
            self.fecha_vencimiento,
            "fecha_fabricacion",
            "fecha_vencimiento",
        )
        self.cantidad_inicial = validar_entero_no_negativo(
            self.cantidad_inicial,
            "cantidad_inicial",
        )

        if self.cantidad_actual is None:
            self.cantidad_actual = self.cantidad_inicial

        self.cantidad_actual = validar_entero_no_negativo(
            self.cantidad_actual,
            "cantidad_actual",
        )

        if self.cantidad_actual > self.cantidad_inicial:
            raise ValueError(
                "cantidad_actual no puede superar cantidad_inicial al crear un lote."
            )

        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_LOTE,
            "estado",
        )
        self._actualizar_estado_por_stock()

    def _actualizar_estado_por_stock(self) -> None:
        """Actualiza el estado cuando el stock llega a cero."""
        stock_actual = self._obtener_stock_actual()

        if stock_actual == 0 and self.estado == "activo":
            self.estado = "agotado"

    def verificar_vencimiento(self, fecha_consulta: date) -> bool:
        """
        Verifica si el lote se encuentra vencido.

        Args:
            fecha_consulta: Fecha sobre la cual se evalúa el vencimiento.

        Returns:
            True si el lote está vencido.
        """
        if fecha_consulta > self.fecha_vencimiento:
            self.estado = "vencido"
            return True

        return False

    def _obtener_stock_actual(self) -> int:
        """
        Retorna el stock actual garantizando un valor entero.

        Returns:
            Stock actual del lote.

        Raises:
            ValueError: Si el stock actual no fue inicializado.
        """
        if self.cantidad_actual is None:
            raise ValueError("El stock actual del lote no fue inicializado.")

        return self.cantidad_actual

    def actualizar_stock(
        self,
        cantidad: int,
        tipo_movimiento: str,
    ) -> None:
        """
        Actualiza el stock en memoria a partir de un movimiento.

        Args:
            cantidad: Cantidad a aplicar.
            tipo_movimiento: entrada, salida o ajuste.

        Raises:
            ValueError: Si el movimiento es inválido o genera stock negativo.

        Note:
            La persistencia y la transacción corresponden a MedicamentoService.
        """
        cantidad = validar_entero_positivo(cantidad, "cantidad")
        tipo_movimiento = validar_dominio(
            tipo_movimiento.strip().lower(),
            frozenset({"entrada", "salida", "ajuste"}),
            "tipo_movimiento",
        )

        if self.estado == "vencido":
            raise ValueError("No se puede modificar stock de un lote vencido.")

        stock_actual = self._obtener_stock_actual()

        if tipo_movimiento == "entrada":
            stock_actual += cantidad
        elif tipo_movimiento == "salida":
            if cantidad > stock_actual:
                raise ValueError("La salida no puede superar el stock disponible.")

            stock_actual -= cantidad
        else:
            stock_actual = cantidad

        self.cantidad_actual = stock_actual
        self._actualizar_estado_por_stock()

    def generar_alerta_stock(self, stock_minimo: int) -> bool:
        """
        Indica si el lote está por debajo del stock mínimo.

        Args:
            stock_minimo: Umbral mínimo definido para el medicamento.

        Returns:
            True si el stock actual es menor al mínimo.
        """
        stock_minimo = validar_entero_no_negativo(
            stock_minimo,
            "stock_minimo",
        )
        return self._obtener_stock_actual() < stock_minimo

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "medicamento_id": self.medicamento_id,
            "proveedor_id": self.proveedor_id,
            "numero_lote": self.numero_lote,
            "fecha_fabricacion": self.fecha_fabricacion.isoformat(),
            "fecha_vencimiento": self.fecha_vencimiento.isoformat(),
            "cantidad_inicial": self.cantidad_inicial,
            "cantidad_actual": self.cantidad_actual,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "LoteMedicamento":
        """Crea un LoteMedicamento desde una fila SQLite."""
        fecha_registro = fila.get("fecha_registro")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            medicamento_id=int(fila["medicamento_id"]),
            proveedor_id=int(fila["proveedor_id"]),
            numero_lote=str(fila["numero_lote"]),
            fecha_fabricacion=date.fromisoformat(str(fila["fecha_fabricacion"])),
            fecha_vencimiento=date.fromisoformat(str(fila["fecha_vencimiento"])),
            cantidad_inicial=int(fila["cantidad_inicial"]),
            cantidad_actual=int(fila["cantidad_actual"]),
            estado=str(fila["estado"]),
            fecha_registro=(
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
        )
