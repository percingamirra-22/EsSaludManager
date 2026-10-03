"""
Modelo de dominio para citas médicas.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.utils.validaciones import (
    ESTADOS_CITA,
    validar_dominio,
    validar_entero_positivo,
    validar_intervalo_horario,
    validar_no_vacio,
)


@dataclass
class Cita:
    """
    Representa una cita para una consulta, examen o procedimiento.

    La detección de conflictos horarios se implementa en CitaService,
    ya que requiere consultar citas existentes en la base de datos.
    """

    paciente_id: int
    recepcionista_id: int
    servicio_id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    usuario_creacion: str
    id: int | None = None
    estado: str = "programada"
    motivo: str | None = None
    observaciones: str | None = None
    fecha_creacion: datetime | None = None
    fecha_ultima_modificacion: datetime | None = None
    usuario_ultima_modificacion: str | None = None

    def __post_init__(self) -> None:
        """Valida los datos básicos de una cita."""
        self.paciente_id = validar_entero_positivo(self.paciente_id, "paciente_id")
        self.recepcionista_id = validar_entero_positivo(
            self.recepcionista_id,
            "recepcionista_id",
        )
        self.servicio_id = validar_entero_positivo(self.servicio_id, "servicio_id")
        validar_intervalo_horario(self.fecha_inicio, self.fecha_fin)
        self.usuario_creacion = validar_no_vacio(
            self.usuario_creacion,
            "usuario_creacion",
        )
        self.estado = validar_dominio(
            self.estado.strip().lower(),
            ESTADOS_CITA,
            "estado",
        )

        if self.motivo is not None:
            self.motivo = self.motivo.strip() or None

        if self.observaciones is not None:
            self.observaciones = self.observaciones.strip() or None

        if self.usuario_ultima_modificacion is not None:
            self.usuario_ultima_modificacion = (
                self.usuario_ultima_modificacion.strip() or None
            )

    def reprogramar(
        self,
        nueva_fecha_inicio: datetime,
        nueva_fecha_fin: datetime,
        motivo: str,
        usuario_modificacion: str,
        fecha_modificacion: datetime,
    ) -> None:
        """
        Cambia el horario de la cita.

        Args:
            nueva_fecha_inicio: Nuevo inicio.
            nueva_fecha_fin: Nuevo fin.
            motivo: Razón de la reprogramación.
            usuario_modificacion: Usuario responsable del cambio.
            fecha_modificacion: Fecha y hora del cambio.

        Raises:
            ValueError: Si la cita está cancelada, completada o el intervalo
                de tiempo no es válido.
        """
        if self.estado in {"cancelada", "completada"}:
            raise ValueError("No se puede reprogramar una cita cancelada o completada.")

        validar_intervalo_horario(nueva_fecha_inicio, nueva_fecha_fin)
        self.fecha_inicio = nueva_fecha_inicio
        self.fecha_fin = nueva_fecha_fin
        self.motivo = validar_no_vacio(motivo, "motivo")
        self.estado = "reprogramada"
        self.fecha_ultima_modificacion = fecha_modificacion
        self.usuario_ultima_modificacion = validar_no_vacio(
            usuario_modificacion,
            "usuario_modificacion",
        )

    def cancelar(
        self,
        motivo: str,
        usuario_modificacion: str,
        fecha_modificacion: datetime,
    ) -> None:
        """
        Cancela la cita.

        Args:
            motivo: Razón de la cancelación.
            usuario_modificacion: Usuario responsable del cambio.
            fecha_modificacion: Fecha y hora del cambio.

        Raises:
            ValueError: Si la cita ya fue completada.
        """
        if self.estado == "completada":
            raise ValueError("No se puede cancelar una cita completada.")

        self.motivo = validar_no_vacio(motivo, "motivo")
        self.estado = "cancelada"
        self.fecha_ultima_modificacion = fecha_modificacion
        self.usuario_ultima_modificacion = validar_no_vacio(
            usuario_modificacion,
            "usuario_modificacion",
        )

    def completar(
        self,
        usuario_modificacion: str,
        fecha_modificacion: datetime,
    ) -> None:
        """
        Marca la cita como completada.

        Args:
            usuario_modificacion: Usuario responsable del cambio.
            fecha_modificacion: Fecha y hora del cambio.

        Raises:
            ValueError: Si la cita fue cancelada.
        """
        if self.estado == "cancelada":
            raise ValueError("No se puede completar una cita cancelada.")

        self.estado = "completada"
        self.fecha_ultima_modificacion = fecha_modificacion
        self.usuario_ultima_modificacion = validar_no_vacio(
            usuario_modificacion,
            "usuario_modificacion",
        )

    def to_dict(self) -> dict[str, object]:
        """Convierte el modelo al formato de columnas SQLite."""
        return {
            "paciente_id": self.paciente_id,
            "recepcionista_id": self.recepcionista_id,
            "servicio_id": self.servicio_id,
            "fecha_inicio": self.fecha_inicio.isoformat(sep=" "),
            "fecha_fin": self.fecha_fin.isoformat(sep=" "),
            "estado": self.estado,
            "motivo": self.motivo,
            "observaciones": self.observaciones,
            "usuario_creacion": self.usuario_creacion,
            "fecha_ultima_modificacion": (
                self.fecha_ultima_modificacion.isoformat(sep=" ")
                if self.fecha_ultima_modificacion is not None
                else None
            ),
            "usuario_ultima_modificacion": self.usuario_ultima_modificacion,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Cita":
        """
        Crea una Cita desde una fila SQLite.

        Args:
            fila: Diccionario con columnas de la tabla cita.

        Returns:
            Instancia de Cita.
        """
        fecha_creacion = fila.get("fecha_creacion")
        fecha_modificacion = fila.get("fecha_ultima_modificacion")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            paciente_id=int(fila["paciente_id"]),
            recepcionista_id=int(fila["recepcionista_id"]),
            servicio_id=int(fila["servicio_id"]),
            fecha_inicio=datetime.fromisoformat(str(fila["fecha_inicio"])),
            fecha_fin=datetime.fromisoformat(str(fila["fecha_fin"])),
            usuario_creacion=str(fila["usuario_creacion"]),
            estado=str(fila["estado"]),
            motivo=(str(fila["motivo"]) if fila.get("motivo") is not None else None),
            observaciones=(
                str(fila["observaciones"])
                if fila.get("observaciones") is not None
                else None
            ),
            fecha_creacion=(
                datetime.fromisoformat(str(fecha_creacion))
                if fecha_creacion is not None
                else None
            ),
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
