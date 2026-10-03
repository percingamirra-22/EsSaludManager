"""
Modelo de dominio para exámenes médicos.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

ESTADOS_EXAMEN_MEDICO = frozenset(
    {"programado", "en proceso", "completado", "cancelado"}
)


@dataclass
class ExamenMedico:
    """
    Representa el detalle de un servicio de examen médico.

    servicio_id debe corresponder a un registro de servicio con
    tipo_servicio='examen'.
    """

    servicio_id: int
    orden_examen_id: int
    tecnico_id: int
    tipo_examen: str
    id: int | None = None
    fecha_realizacion: datetime | None = None
    resultado: str | None = None
    archivo_resultado: str | None = None
    estado: str = "programado"

    def __post_init__(self) -> None:
        """Valida los campos del examen médico."""
        self.servicio_id = validar_entero_positivo(
            self.servicio_id,
            "servicio_id",
        )
        self.orden_examen_id = validar_entero_positivo(
            self.orden_examen_id,
            "orden_examen_id",
        )
        self.tecnico_id = validar_entero_positivo(self.tecnico_id, "tecnico_id")
        self.tipo_examen = validar_no_vacio(self.tipo_examen, "tipo_examen")
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_EXAMEN_MEDICO,
            "estado",
        )

        if self.id is not None and self.id != self.servicio_id:
            raise ValueError(
                "El id de ExamenMedico debe coincidir con servicio_id por la PK compartida."
            )

    def iniciar(self) -> None:
        """Cambia el examen programado a estado en proceso."""
        if self.estado != "programado":
            raise ValueError("Solo un examen programado puede iniciarse.")

        self.estado = "en proceso"

    def registrar_resultado(
        self,
        resultado: str,
        archivo_resultado: str | None,
        fecha_realizacion: datetime,
    ) -> None:
        """
        Registra resultado y completa el examen.

        Args:
            resultado: Resultado clínico del examen.
            archivo_resultado: Ruta opcional a archivo adjunto.
            fecha_realizacion: Fecha de realización.
        """
        if self.estado not in {"programado", "en proceso"}:
            raise ValueError(
                "Solo un examen programado o en proceso puede completarse."
            )

        self.resultado = validar_no_vacio(resultado, "resultado")
        self.archivo_resultado = (
            archivo_resultado.strip()
            if archivo_resultado is not None and archivo_resultado.strip()
            else None
        )
        self.fecha_realizacion = fecha_realizacion
        self.estado = "completado"

    def cancelar(self) -> None:
        """Cancela el examen si todavía no está completado."""
        if self.estado == "completado":
            raise ValueError("No se puede cancelar un examen completado.")

        self.estado = "cancelado"

    def to_dict(self) -> dict[str, object]:
        """
        Convierte el modelo al formato de tabla examen_medico.

        Raises:
            ValueError: Si no tiene ID de servicio persistido.
        """
        if self.id is None:
            raise ValueError(
                "No se puede persistir un examen médico sin ID de servicio."
            )

        return {
            "id": self.id,
            "servicio_id": self.servicio_id,
            "orden_examen_id": self.orden_examen_id,
            "tecnico_id": self.tecnico_id,
            "tipo_examen": self.tipo_examen,
            "fecha_realizacion": (
                self.fecha_realizacion.isoformat(sep=" ")
                if self.fecha_realizacion is not None
                else None
            ),
            "resultado": self.resultado,
            "archivo_resultado": self.archivo_resultado,
            "estado": self.estado,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "ExamenMedico":
        """Crea un ExamenMedico desde una fila SQLite."""
        fecha_realizacion = fila.get("fecha_realizacion")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            servicio_id=int(fila["servicio_id"]),
            orden_examen_id=int(fila["orden_examen_id"]),
            tecnico_id=int(fila["tecnico_id"]),
            tipo_examen=str(fila["tipo_examen"]),
            fecha_realizacion=(
                datetime.fromisoformat(str(fecha_realizacion))
                if fecha_realizacion is not None
                else None
            ),
            resultado=(
                str(fila["resultado"]) if fila.get("resultado") is not None else None
            ),
            archivo_resultado=(
                str(fila["archivo_resultado"])
                if fila.get("archivo_resultado") is not None
                else None
            ),
            estado=str(fila["estado"]),
        )
