"""
Modelo de dominio para especialistas.
"""

from dataclasses import dataclass, field
from datetime import time
from typing import Any, TypedDict

from src.modelos.empleado import Empleado
from src.utils.validaciones import validar_horario, validar_no_vacio


class HorarioDisponible(TypedDict):
    """Horario de atención disponible de un especialista."""

    dia_semana: int
    hora_inicio: time
    hora_fin: time
    estado: bool


def crear_horarios() -> list[HorarioDisponible]:
    """Crea una lista vacía tipada para horarios disponibles."""
    return []


@dataclass
class Especialista(Empleado):
    """Representa un empleado especialista de salud."""

    especialidad: str = ""
    numero_colegiatura: str = ""
    horarios_disponibles: list[HorarioDisponible] = field(
        default_factory=crear_horarios
    )

    def __post_init__(self) -> None:
        """Valida los datos comunes y específicos del especialista."""
        super().__post_init__()
        self.especialidad = validar_no_vacio(self.especialidad, "especialidad")
        self.numero_colegiatura = validar_no_vacio(
            self.numero_colegiatura,
            "numero_colegiatura",
        ).upper()

    def agregar_horario(
        self,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time,
        estado: bool = True,
    ) -> None:
        """
        Agrega un horario disponible en memoria.

        La persistencia se realiza mediante horario_especialista en la capa
        de servicios.

        Args:
            dia_semana: Día de semana entre 0 y 6.
            hora_inicio: Hora de inicio.
            hora_fin: Hora final.
            estado: Indica si el horario está activo.
        """
        if not 0 <= dia_semana <= 6:
            raise ValueError("El día de semana debe estar entre 0 y 6.")

        validar_horario(hora_inicio, hora_fin)

        self.horarios_disponibles.append(
            {
                "dia_semana": dia_semana,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "estado": estado,
            }
        )

    def obtener_horarios(self) -> list[HorarioDisponible]:
        """
        Obtiene una copia de los horarios configurados.

        Returns:
            Lista de horarios disponibles.
        """
        return self.horarios_disponibles.copy()

    def verificar_disponibilidad(
        self,
        dia_semana: int,
        hora_inicio: time,
        hora_fin: time,
    ) -> bool:
        """
        Verifica disponibilidad básica contra los horarios declarados.

        La detección de choques con citas existentes corresponde a CitaService.

        Args:
            dia_semana: Día de la semana.
            hora_inicio: Hora solicitada de inicio.
            hora_fin: Hora solicitada de fin.

        Returns:
            True si el horario solicitado encaja en un horario activo.
        """
        if not 0 <= dia_semana <= 6:
            raise ValueError("El día de semana debe estar entre 0 y 6.")

        validar_horario(hora_inicio, hora_fin)

        for horario in self.horarios_disponibles:
            if not horario["estado"]:
                continue

            if horario["dia_semana"] != dia_semana:
                continue

            if (
                hora_inicio >= horario["hora_inicio"]
                and hora_fin <= horario["hora_fin"]
            ):
                return True

        return False

    def atender_cita(self, estado_cita: str) -> bool:
        """
        Determina si una cita puede ser atendida.

        Args:
            estado_cita: Estado actual de la cita.

        Returns:
            True si el especialista está activo y la cita es atendible.
        """
        return self.estado and estado_cita in {"programada", "reprogramada"}

    def to_dict(self) -> dict[str, object]:
        """
        Convierte los atributos específicos al formato SQLite.

        Raises:
            ValueError: Si el empleado aún no cuenta con ID persistido.
        """
        if self.id is None:
            raise ValueError(
                "No se puede persistir un especialista sin ID de empleado."
            )

        return {
            "id": self.id,
            "empleado_id": self.id,
            "especialidad": self.especialidad,
            "numero_colegiatura": self.numero_colegiatura,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Especialista":
        """Crea un Especialista desde un JOIN empleado/especialista."""
        datos = Empleado.datos_comunes_desde_fila(fila)

        return cls(
            id=datos["id"],
            codigo_empleado=datos["codigo_empleado"],
            nombres=datos["nombres"],
            apellidos=datos["apellidos"],
            tipo_documento=datos["tipo_documento"],
            numero_documento=datos["numero_documento"],
            fecha_contratacion=datos["fecha_contratacion"],
            telefono=datos["telefono"],
            email=datos["email"],
            direccion=datos["direccion"],
            estado=datos["estado"],
            fecha_registro=datos["fecha_registro"],
            fecha_despido=datos["fecha_despido"],
            usuario_registro=datos["usuario_registro"],
            especialidad=str(fila["especialidad"]),
            numero_colegiatura=str(fila["numero_colegiatura"]),
        )
