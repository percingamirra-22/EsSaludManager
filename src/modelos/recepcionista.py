"""
Modelo de dominio para recepcionistas.
"""

from dataclasses import dataclass
from typing import Any

from src.modelos.empleado import Empleado
from src.utils.validaciones import validar_dominio, validar_no_vacio

TURNOS_RECEPCIONISTA = frozenset({"Mañana", "Tarde", "Noche"})


@dataclass
class Recepcionista(Empleado):
    """Representa un empleado responsable de atención y citas."""

    turno: str = ""
    modulo_atencion: str = ""

    def __post_init__(self) -> None:
        """Valida atributos comunes y específicos de la recepcionista."""
        super().__post_init__()
        self.turno = validar_dominio(
            self.turno.strip().capitalize(),
            TURNOS_RECEPCIONISTA,
            "turno",
        )
        self.modulo_atencion = validar_no_vacio(
            self.modulo_atencion,
            "modulo_atencion",
        )

    def puede_gestionar_citas(self) -> bool:
        """
        Determina si la recepcionista está activa.

        Returns:
            True si puede gestionar citas.
        """
        return self.estado

    def to_dict(self) -> dict[str, object]:
        """Convierte los datos específicos a la tabla recepcionista."""
        if self.id is None:
            raise ValueError(
                "No se puede persistir una recepcionista sin ID de empleado."
            )

        return {
            "id": self.id,
            "empleado_id": self.id,
            "turno": self.turno,
            "modulo_atencion": self.modulo_atencion,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Recepcionista":
        """Crea una Recepcionista desde un JOIN empleado/recepcionista."""
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
            turno=str(fila["turno"]),
            modulo_atencion=str(fila["modulo_atencion"]),
        )
