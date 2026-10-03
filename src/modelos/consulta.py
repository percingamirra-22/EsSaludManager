"""
Modelo de dominio para detalles de servicios de consulta.
"""

from dataclasses import dataclass
from typing import Any

from src.utils.validaciones import (
    validar_entero_positivo,
)


@dataclass
class Consulta:
    """
    Representa el detalle de una consulta médica.

    servicio_id debe corresponder a un registro de la tabla servicio
    con tipo_servicio='consulta'.
    """

    servicio_id: int
    especialista_id: int
    duracion: int
    id: int | None = None
    requiere_preparacion: bool = False

    def __post_init__(self) -> None:
        """Valida las referencias y duración de la consulta."""
        self.servicio_id = validar_entero_positivo(
            self.servicio_id,
            "servicio_id",
        )
        self.especialista_id = validar_entero_positivo(
            self.especialista_id,
            "especialista_id",
        )
        self.duracion = validar_entero_positivo(self.duracion, "duracion")

        if self.id is not None and self.id != self.servicio_id:
            raise ValueError(
                "El id de Consulta debe coincidir con servicio_id por la PK compartida."
            )

    def programar_cita(self) -> bool:
        """
        Indica que una consulta puede ser asociada a una cita.

        La disponibilidad y persistencia se validan en CitaService.

        Returns:
            True si tiene referencias válidas.
        """
        return self.servicio_id > 0 and self.especialista_id > 0

    def completar_consulta(self) -> bool:
        """
        Indica que la consulta puede completarse.

        Returns:
            True si tiene duración válida.
        """
        return self.duracion > 0

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato de tabla consulta."""
        if self.id is None:
            raise ValueError("No se puede persistir una consulta sin ID de servicio.")

        return {
            "id": self.id,
            "servicio_id": self.servicio_id,
            "especialista_id": self.especialista_id,
            "duracion": self.duracion,
            "requiere_preparacion": int(self.requiere_preparacion),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Consulta":
        """Crea una Consulta desde una fila SQLite."""
        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            servicio_id=int(fila["servicio_id"]),
            especialista_id=int(fila["especialista_id"]),
            duracion=int(fila["duracion"]),
            requiere_preparacion=bool(fila.get("requiere_preparacion", 0)),
        )
