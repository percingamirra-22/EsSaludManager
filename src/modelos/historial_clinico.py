"""
Modelo de dominio para historiales clínicos.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    ESTADOS_HISTORIAL,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)


def crear_entradas() -> list[int]:
    """Crea una lista tipada para IDs de entradas del historial."""
    return []


@dataclass
class HistorialClinico:
    """Representa el historial clínico de un paciente."""

    paciente_id: int
    numero_historia: str
    id: int | None = None
    fecha_apertura: datetime | None = None
    estado: str = "activo"
    version: int = 1
    fecha_ultima_modificacion: datetime | None = None
    usuario_ultima_modificacion: str | None = None
    entradas_ids: list[int] = field(default_factory=crear_entradas)

    def __post_init__(self) -> None:
        """Valida los datos principales del historial."""
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.numero_historia = validar_no_vacio(
            self.numero_historia,
            "numero_historia",
        ).upper()
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_HISTORIAL,
            "estado",
        )

        if self.version <= 0:
            raise ValueError("La versión del historial debe ser mayor que cero.")

    def registrar_entrada(self, entrada_id: int) -> None:
        """
        Añade el ID de una entrada al historial en memoria.

        Args:
            entrada_id: ID de EntradaHistorial.
        """
        entrada_id = validar_entero_positivo(entrada_id, "entrada_id")

        if entrada_id not in self.entradas_ids:
            self.entradas_ids.append(entrada_id)

    def actualizar_version(
        self,
        usuario: str,
        fecha: datetime,
    ) -> None:
        """
        Incrementa el versionado al registrar un cambio.

        Args:
            usuario: Usuario responsable.
            fecha: Fecha y hora del cambio.
        """
        self.version += 1
        self.fecha_ultima_modificacion = fecha
        self.usuario_ultima_modificacion = validar_no_vacio(
            usuario,
            "usuario_ultima_modificacion",
        )

    def cerrar(self) -> None:
        """Cierra el historial clínico."""
        if self.estado == "desactivado":
            raise ValueError("No se puede cerrar un historial desactivado.")

        if self.estado == "cerrado":
            raise ValueError("El historial clínico ya está cerrado.")

        self.estado = "cerrado"

    def desactivar(self) -> None:
        """Desactiva lógicamente el historial clínico."""
        if self.estado == "desactivado":
            raise ValueError("El historial clínico ya está desactivado.")

        self.estado = "desactivado"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "paciente_id": self.paciente_id,
            "numero_historia": self.numero_historia,
            "estado": self.estado,
            "version": self.version,
            "fecha_ultima_modificacion": (
                self.fecha_ultima_modificacion.isoformat(sep=" ")
                if self.fecha_ultima_modificacion is not None
                else None
            ),
            "usuario_ultima_modificacion": self.usuario_ultima_modificacion,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "HistorialClinico":
        """Crea un HistorialClinico desde una fila SQLite."""
        fecha_apertura = fila.get("fecha_apertura")
        fecha_modificacion = fila.get("fecha_ultima_modificacion")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            paciente_id=int(fila["paciente_id"]),
            numero_historia=str(fila["numero_historia"]),
            fecha_apertura=(
                datetime.fromisoformat(str(fecha_apertura))
                if fecha_apertura is not None
                else None
            ),
            estado=str(fila["estado"]),
            version=int(fila["version"]),
            fecha_ultima_modificacion=(
                datetime.fromisoformat(str(fecha_modificacion))
                if fecha_modificacion is not None
                else None
            ),
            usuario_ultima_modificacion=(
                str(fila["usuario_ultima_modificacion"])
                if fila.get("usuario_ultima_modificacion") is not None
                else None
            ),
        )
