"""
Modelo de dominio para gerentes.
"""

from dataclasses import dataclass
from typing import Any

from src.modelos.empleado import Empleado
from src.utils.validaciones import validar_no_vacio


@dataclass
class Gerente(Empleado):
    """Representa un empleado con responsabilidades gerenciales."""

    area: str = ""
    nivel_gerencial: str = ""

    def __post_init__(self) -> None:
        """Valida atributos comunes y específicos del gerente."""
        super().__post_init__()
        self.area = validar_no_vacio(self.area, "area")
        self.nivel_gerencial = validar_no_vacio(
            self.nivel_gerencial,
            "nivel_gerencial",
        )

    def aprobar_solicitud(self, estado_solicitud: str) -> bool:
        """
        Determina si una solicitud puede aprobarse.

        Args:
            estado_solicitud: Estado actual de la solicitud.

        Returns:
            True si la solicitud estaba pendiente.
        """
        return self.estado and estado_solicitud == "pendiente"

    def to_dict(self) -> dict[str, object]:
        """Convierte los datos específicos a la tabla gerente."""
        if self.id is None:
            raise ValueError("No se puede persistir un gerente sin ID de empleado.")

        return {
            "id": self.id,
            "empleado_id": self.id,
            "area": self.area,
            "nivel_gerencial": self.nivel_gerencial,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Gerente":
        """Crea un Gerente desde un JOIN empleado/gerente."""
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
            area=str(fila["area"]),
            nivel_gerencial=str(fila["nivel_gerencial"]),
        )
