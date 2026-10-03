"""
Modelo de dominio para entradas de historial clínico.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    TIPOS_ENTRADA_HISTORIAL,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

ESTADOS_ENTRADA_HISTORIAL = frozenset({"activa", "desactivada"})


@dataclass
class EntradaHistorial:
    """Representa una entrada versionada de historial clínico."""

    historial_id: int
    tipo_entrada: str
    contenido: str
    usuario_registro: str
    id: int | None = None
    fecha_registro: datetime | None = None
    version: int = 1
    estado: str = "activa"

    def __post_init__(self) -> None:
        """Valida los datos de la entrada."""
        self.historial_id = validar_entero_positivo(
            self.historial_id,
            "historial_id",
        )
        self.tipo_entrada = validar_dominio(
            self.tipo_entrada.strip().lower(),
            TIPOS_ENTRADA_HISTORIAL,
            "tipo_entrada",
        )
        self.contenido = validar_no_vacio(self.contenido, "contenido")
        self.usuario_registro = validar_no_vacio(
            self.usuario_registro,
            "usuario_registro",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_ENTRADA_HISTORIAL,
            "estado",
        )

        if self.version <= 0:
            raise ValueError("La versión de la entrada debe ser mayor que cero.")

    def nueva_version(
        self,
        nuevo_contenido: str,
        usuario_registro: str,
    ) -> "EntradaHistorial":
        """
        Genera una nueva versión de la entrada.

        La entrada actual debe ser desactivada por HistorialService.

        Args:
            nuevo_contenido: Contenido actualizado.
            usuario_registro: Usuario que registra la nueva versión.

        Returns:
            Nueva entrada con versión incrementada.

        Raises:
            ValueError: Si la entrada ya está desactivada.
        """
        if self.estado != "activa":
            raise ValueError(
                "Solo se puede generar una nueva versión desde una entrada activa."
            )

        return EntradaHistorial(
            historial_id=self.historial_id,
            tipo_entrada=self.tipo_entrada,
            contenido=nuevo_contenido,
            usuario_registro=usuario_registro,
            version=self.version + 1,
        )

    def desactivar(self) -> None:
        """Desactiva lógicamente la entrada actual."""
        self.estado = "desactivada"

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato SQLite."""
        return {
            "historial_id": self.historial_id,
            "tipo_entrada": self.tipo_entrada,
            "contenido": self.contenido,
            "usuario_registro": self.usuario_registro,
            "version": self.version,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "EntradaHistorial":
        """Crea una EntradaHistorial desde una fila SQLite."""
        fecha_registro = fila.get("fecha_registro")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            historial_id=int(fila["historial_id"]),
            tipo_entrada=str(fila["tipo_entrada"]),
            contenido=str(fila["contenido"]),
            fecha_registro=(
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
            usuario_registro=str(fila["usuario_registro"]),
            version=int(fila["version"]),
            estado=str(fila["estado"]),
        )
