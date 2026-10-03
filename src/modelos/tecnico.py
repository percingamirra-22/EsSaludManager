"""
Modelo de dominio para técnicos de salud.
"""

from dataclasses import dataclass, field
from typing import Any

from src.modelos.empleado import Empleado
from src.utils.validaciones import validar_no_vacio


def crear_certificaciones() -> list[dict[str, object]]:
    """Crea una lista tipada para certificaciones del técnico."""
    return []


@dataclass
class Tecnico(Empleado):
    """Representa un empleado técnico encargado de exámenes médicos."""

    especialidad_tecnica: str = ""
    area_trabajo: str = ""
    certificaciones: list[dict[str, object]] = field(
        default_factory=crear_certificaciones
    )

    def __post_init__(self) -> None:
        """Valida atributos comunes y específicos del técnico."""
        super().__post_init__()
        self.especialidad_tecnica = validar_no_vacio(
            self.especialidad_tecnica,
            "especialidad_tecnica",
        )
        self.area_trabajo = validar_no_vacio(
            self.area_trabajo,
            "area_trabajo",
        )

    def tiene_certificacion_activa(self) -> bool:
        """
        Determina si tiene al menos una certificación activa en memoria.

        Returns:
            True si existe alguna certificación activa.
        """
        return any(
            bool(certificacion.get("estado", True))
            for certificacion in self.certificaciones
        )

    def puede_realizar_examen(self) -> bool:
        """
        Determina si el técnico puede realizar un examen.

        Returns:
            True si está activo.
        """
        return self.estado

    def to_dict(self) -> dict[str, object]:
        """Convierte los datos específicos a la tabla tecnico."""
        if self.id is None:
            raise ValueError("No se puede persistir un técnico sin ID de empleado.")

        return {
            "id": self.id,
            "empleado_id": self.id,
            "especialidad_tecnica": self.especialidad_tecnica,
            "area_trabajo": self.area_trabajo,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Tecnico":
        """Crea un Tecnico desde un JOIN empleado/tecnico."""
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
            especialidad_tecnica=str(fila["especialidad_tecnica"]),
            area_trabajo=str(fila["area_trabajo"]),
        )
