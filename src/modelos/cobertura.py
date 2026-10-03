"""
Modelo de dominio para coberturas de seguro por servicio.
"""

from dataclasses import dataclass
from datetime import date
from typing import Any

from src.utils.validaciones import (
    validar_entero_positivo,
    validar_numero_en_rango,
    validar_rango_fechas,
)


@dataclass
class Cobertura:
    """Representa las reglas de cobertura de un seguro para un servicio."""

    seguro_id: int
    servicio_id: int
    porcentaje_cobertura: float
    monto_maximo: float
    copago_fijo: float
    fecha_inicio: date
    id: int | None = None
    fecha_fin: date | None = None
    estado: bool = True

    def __post_init__(self) -> None:
        """Valida los datos de cobertura."""
        self.seguro_id = validar_entero_positivo(self.seguro_id, "seguro_id")
        self.servicio_id = validar_entero_positivo(
            self.servicio_id,
            "servicio_id",
        )
        self.porcentaje_cobertura = validar_numero_en_rango(
            float(self.porcentaje_cobertura),
            0.0,
            100.0,
            "porcentaje_cobertura",
        )
        self.monto_maximo = validar_numero_en_rango(
            float(self.monto_maximo),
            0.0,
            float("inf"),
            "monto_maximo",
        )
        self.copago_fijo = validar_numero_en_rango(
            float(self.copago_fijo),
            0.0,
            float("inf"),
            "copago_fijo",
        )
        validar_rango_fechas(
            self.fecha_inicio,
            self.fecha_fin,
            "fecha_inicio",
            "fecha_fin",
        )

    def verificar_vigencia(self, fecha_consulta: date) -> bool:
        """
        Verifica si la cobertura está vigente.

        Args:
            fecha_consulta: Fecha que se desea validar.

        Returns:
            True si está activa y dentro de vigencia.
        """
        if not self.estado or fecha_consulta < self.fecha_inicio:
            return False

        return self.fecha_fin is None or fecha_consulta <= self.fecha_fin

    def calcular_cobertura(self, monto_total: float) -> dict[str, float]:
        """
        Calcula monto cubierto, copago y monto del paciente.

        Args:
            monto_total: Valor total del servicio facturado.

        Returns:
            Diccionario con monto_cubierto, monto_paciente y copago.

        Raises:
            ValueError: Si el monto es negativo.
        """
        monto_total = validar_numero_en_rango(
            float(monto_total),
            0.0,
            float("inf"),
            "monto_total",
        )

        monto_porcentaje = monto_total * (self.porcentaje_cobertura / 100)
        monto_cubierto = min(monto_porcentaje, self.monto_maximo)
        monto_paciente = max(monto_total - monto_cubierto + self.copago_fijo, 0.0)

        return {
            "monto_cubierto": round(monto_cubierto, 2),
            "copago": round(self.copago_fijo, 2),
            "monto_paciente": round(monto_paciente, 2),
        }

    def desactivar(self) -> None:
        """Desactiva lógicamente la cobertura."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "seguro_id": self.seguro_id,
            "servicio_id": self.servicio_id,
            "porcentaje_cobertura": self.porcentaje_cobertura,
            "monto_maximo": self.monto_maximo,
            "copago_fijo": self.copago_fijo,
            "estado": int(self.estado),
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": (
                self.fecha_fin.isoformat() if self.fecha_fin is not None else None
            ),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Cobertura":
        """Crea una Cobertura desde una fila SQLite."""
        fecha_fin = fila.get("fecha_fin")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            seguro_id=int(fila["seguro_id"]),
            servicio_id=int(fila["servicio_id"]),
            porcentaje_cobertura=float(fila["porcentaje_cobertura"]),
            monto_maximo=float(fila["monto_maximo"]),
            copago_fijo=float(fila["copago_fijo"]),
            estado=bool(fila.get("estado", 1)),
            fecha_inicio=date.fromisoformat(str(fila["fecha_inicio"])),
            fecha_fin=(
                date.fromisoformat(str(fecha_fin)) if fecha_fin is not None else None
            ),
        )
