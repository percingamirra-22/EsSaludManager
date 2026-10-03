"""
Modelo de dominio para órdenes de examen.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
)

ESTADOS_ORDEN_EXAMEN = frozenset({"pendiente", "completada", "cancelada"})


def crear_examenes_solicitados() -> list[int]:
    """Crea una lista tipada para exámenes solicitados."""
    return []


@dataclass
class OrdenExamen:
    """Representa una orden emitida por un especialista."""

    paciente_id: int
    especialista_id: int
    id: int | None = None
    fecha_orden: datetime | None = None
    estado: str = "pendiente"
    observaciones: str | None = None
    examenes_solicitados_ids: list[int] = field(
        default_factory=crear_examenes_solicitados
    )

    def __post_init__(self) -> None:
        """Valida las referencias y estado de la orden."""
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.especialista_id = validar_entero_positivo(
            self.especialista_id,
            "especialista_id",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_ORDEN_EXAMEN,
            "estado",
        )

        if self.observaciones is not None:
            self.observaciones = self.observaciones.strip() or None

    def agregar_examen(self, examen_id: int) -> bool:
        """
        Agrega un examen solicitado en memoria.

        Args:
            examen_id: ID de ExamenMedico.

        Returns:
            True si se agregó; False si ya estaba presente.

        Raises:
            ValueError: Si la orden no está pendiente.
        """
        if self.estado != "pendiente":
            raise ValueError("Solo se pueden agregar exámenes a una orden pendiente.")

        examen_id = validar_entero_positivo(examen_id, "examen_id")

        if examen_id in self.examenes_solicitados_ids:
            return False

        self.examenes_solicitados_ids.append(examen_id)
        return True

    def completar(self) -> None:
        """Marca la orden como completada."""
        if self.estado == "cancelada":
            raise ValueError("No se puede completar una orden cancelada.")

        self.estado = "completada"

    def cancelar(self) -> None:
        """Cancela una orden pendiente."""
        if self.estado == "completada":
            raise ValueError("No se puede cancelar una orden completada.")

        self.estado = "cancelada"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "paciente_id": self.paciente_id,
            "especialista_id": self.especialista_id,
            "estado": self.estado,
            "observaciones": self.observaciones,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "OrdenExamen":
        """Crea una OrdenExamen desde una fila SQLite."""
        fecha_orden = fila.get("fecha_orden")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            paciente_id=int(fila["paciente_id"]),
            especialista_id=int(fila["especialista_id"]),
            fecha_orden=(
                datetime.fromisoformat(str(fecha_orden))
                if fecha_orden is not None
                else None
            ),
            estado=str(fila["estado"]),
            observaciones=(
                str(fila["observaciones"])
                if fila.get("observaciones") is not None
                else None
            ),
        )
