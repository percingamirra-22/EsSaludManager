"""
Modelo base abstracto para empleados.
"""

from abc import ABC
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, TypedDict

from src.utils.validaciones import (
    TIPOS_DOCUMENTO,
    validar_documento,
    validar_dominio,
    validar_email,
    validar_fecha_no_futura,
    validar_no_vacio,
    validar_telefono,
)


class DatosEmpleado(TypedDict):
    """Datos comunes de un empleado obtenidos desde SQLite."""

    id: int | None
    codigo_empleado: str
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    telefono: str | None
    email: str | None
    direccion: str | None
    fecha_contratacion: date
    estado: bool
    fecha_registro: datetime | None
    fecha_despido: date | None
    usuario_registro: str | None


@dataclass
class Empleado(ABC):
    """
    Clase base para empleados del establecimiento.

    Las subclases Especialista, Gerente, Recepcionista y Tecnico heredan
    los atributos de identidad y contacto de esta entidad.
    """

    codigo_empleado: str
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    fecha_contratacion: date
    id: int | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    estado: bool = True
    fecha_registro: datetime | None = None
    fecha_despido: date | None = None
    usuario_registro: str | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los atributos comunes de un empleado."""
        self.codigo_empleado = validar_no_vacio(
            self.codigo_empleado,
            "codigo_empleado",
        ).upper()
        self.nombres = validar_no_vacio(self.nombres, "nombres")
        self.apellidos = validar_no_vacio(self.apellidos, "apellidos")
        self.tipo_documento = validar_dominio(
            self.tipo_documento.strip().upper(),
            TIPOS_DOCUMENTO,
            "tipo_documento",
        )
        self.numero_documento = validar_documento(
            self.tipo_documento,
            self.numero_documento,
        )
        self.fecha_contratacion = validar_fecha_no_futura(
            self.fecha_contratacion,
            "fecha_contratacion",
        )
        self.telefono = validar_telefono(self.telefono)
        self.email = validar_email(self.email)

        if self.direccion is not None:
            self.direccion = self.direccion.strip() or None

        if self.usuario_registro is not None:
            self.usuario_registro = self.usuario_registro.strip() or None

        if (
            self.fecha_despido is not None
            and self.fecha_despido < self.fecha_contratacion
        ):
            raise ValueError(
                "La fecha de despido no puede ser anterior a la contratación."
            )

    @property
    def empleado_id(self) -> int | None:
        """
        Retorna el ID compartido con la tabla de subtipo.

        Returns:
            Identificador del empleado.
        """
        return self.id

    def actualizar(self, datos: dict[str, Any]) -> None:
        """
        Actualiza atributos permitidos del empleado.

        Args:
            datos: Campos y valores que se modificarán.
        """
        campos_permitidos = {
            "nombres",
            "apellidos",
            "telefono",
            "email",
            "direccion",
            "fecha_despido",
            "estado",
        }
        campos_invalidos = set(datos) - campos_permitidos

        if campos_invalidos:
            campos = ", ".join(sorted(campos_invalidos))
            raise ValueError(f"Campos no actualizables para empleado: {campos}.")

        for campo, valor in datos.items():
            setattr(self, campo, valor)

        self.__post_init__()

    def desactivar(self) -> None:
        """Desactiva lógicamente al empleado."""
        self.estado = False

    def despedir(self, fecha_despido: date) -> None:
        """
        Registra el despido e inactiva al empleado.

        Args:
            fecha_despido: Fecha efectiva del despido.
        """
        if fecha_despido < self.fecha_contratacion:
            raise ValueError(
                "La fecha de despido no puede ser anterior a la contratación."
            )

        self.fecha_despido = fecha_despido
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte los atributos comunes al formato SQLite."""
        return {
            "codigo_empleado": self.codigo_empleado,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "fecha_contratacion": self.fecha_contratacion.isoformat(),
            "estado": int(self.estado),
            "fecha_despido": (
                self.fecha_despido.isoformat()
                if self.fecha_despido is not None
                else None
            ),
            "usuario_registro": self.usuario_registro,
        }

    @classmethod
    def datos_comunes_desde_fila(cls, fila: dict[str, Any]) -> DatosEmpleado:
        """
        Extrae datos comunes de empleado desde una fila SQLite.

        Args:
            fila: Fila con columnas de empleado o JOIN de empleado/subtipo.

        Returns:
            Diccionario tipado reutilizable por las subclases.
        """
        fecha_registro = fila.get("fecha_registro")
        fecha_despido = fila.get("fecha_despido")

        return {
            "id": int(fila["id"]) if fila.get("id") is not None else None,
            "codigo_empleado": str(fila["codigo_empleado"]),
            "nombres": str(fila["nombres"]),
            "apellidos": str(fila["apellidos"]),
            "tipo_documento": str(fila["tipo_documento"]),
            "numero_documento": str(fila["numero_documento"]),
            "telefono": (
                str(fila["telefono"]) if fila.get("telefono") is not None else None
            ),
            "email": str(fila["email"]) if fila.get("email") is not None else None,
            "direccion": (
                str(fila["direccion"]) if fila.get("direccion") is not None else None
            ),
            "fecha_contratacion": date.fromisoformat(str(fila["fecha_contratacion"])),
            "estado": bool(fila.get("estado", 1)),
            "fecha_registro": (
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
            "fecha_despido": (
                date.fromisoformat(str(fecha_despido))
                if fecha_despido is not None
                else None
            ),
            "usuario_registro": (
                str(fila["usuario_registro"])
                if fila.get("usuario_registro") is not None
                else None
            ),
        }
