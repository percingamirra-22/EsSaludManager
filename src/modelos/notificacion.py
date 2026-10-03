"""
Modelo de dominio para notificaciones de pacientes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

TIPOS_NOTIFICACION = frozenset({"recordatorio_cita", "recordatorio_examen"})
ESTADOS_NOTIFICACION = frozenset({"pendiente", "enviada", "fallida"})
CANALES_NOTIFICACION = frozenset({"sms", "email"})


@dataclass
class Notificacion:
    """Representa un recordatorio de cita o examen."""

    paciente_id: int
    cita_id: int
    tipo_notificacion: str
    mensaje: str
    canal: str
    id: int | None = None
    fecha_envio: datetime | None = None
    estado: str = "pendiente"

    def __post_init__(self) -> None:
        """Valida atributos de la notificación."""
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.cita_id = validar_entero_positivo(self.cita_id, "cita_id")
        self.tipo_notificacion = validar_dominio(
            self.tipo_notificacion.strip().lower(),
            TIPOS_NOTIFICACION,
            "tipo_notificacion",
        )
        self.mensaje = validar_no_vacio(self.mensaje, "mensaje")
        self.canal = validar_dominio(
            self.canal.strip().lower(),
            CANALES_NOTIFICACION,
            "canal",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_NOTIFICACION,
            "estado",
        )

    def marcar_enviada(self, fecha_envio: datetime) -> None:
        """Marca la notificación como enviada."""
        if self.estado == "enviada":
            raise ValueError("La notificación ya fue enviada.")

        self.fecha_envio = fecha_envio
        self.estado = "enviada"

    def marcar_fallida(self) -> None:
        """Marca la notificación como fallida."""
        if self.estado == "enviada":
            raise ValueError(
                "No se puede marcar como fallida una notificación enviada."
            )

        if self.estado == "fallida":
            raise ValueError("La notificación ya está marcada como fallida.")

        self.estado = "fallida"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "paciente_id": self.paciente_id,
            "cita_id": self.cita_id,
            "tipo_notificacion": self.tipo_notificacion,
            "mensaje": self.mensaje,
            "fecha_envio": (
                self.fecha_envio.isoformat(sep=" ")
                if self.fecha_envio is not None
                else None
            ),
            "estado": self.estado,
            "canal": self.canal,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Notificacion":
        """Crea una Notificacion desde una fila SQLite."""
        fecha_envio = fila.get("fecha_envio")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            paciente_id=int(fila["paciente_id"]),
            cita_id=int(fila["cita_id"]),
            tipo_notificacion=str(fila["tipo_notificacion"]),
            mensaje=str(fila["mensaje"]),
            fecha_envio=(
                datetime.fromisoformat(str(fecha_envio))
                if fecha_envio is not None
                else None
            ),
            estado=str(fila["estado"]),
            canal=str(fila["canal"]),
        )
