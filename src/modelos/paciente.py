"""
Modelo de dominio para pacientes.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from src.utils.validaciones import (
    SEXOS,
    TIPOS_DOCUMENTO,
    validar_documento,
    validar_dominio,
    validar_email,
    validar_fecha_no_futura,
    validar_no_vacio,
    validar_telefono,
)


@dataclass
class Paciente:
    """
    Representa la identidad y datos de contacto de un paciente.

    La persistencia se realiza mediante PacienteRepository y PacienteService.
    """

    codigo_paciente: str
    nombres: str
    apellidos: str
    tipo_documento: str
    numero_documento: str
    fecha_nacimiento: date
    sexo: str
    id: int | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None
    estado: bool = True
    fecha_registro: datetime | None = None
    usuario_registro: str | None = None

    def __post_init__(self) -> None:
        """Valida y normaliza los datos principales del paciente."""
        self.codigo_paciente = validar_no_vacio(
            self.codigo_paciente,
            "codigo_paciente",
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
        self.fecha_nacimiento = validar_fecha_no_futura(
            self.fecha_nacimiento,
            "fecha_nacimiento",
        )
        self.sexo = validar_dominio(
            self.sexo.strip().upper(),
            SEXOS,
            "sexo",
        )
        self.telefono = validar_telefono(self.telefono)
        self.email = validar_email(self.email)

        if self.direccion is not None:
            self.direccion = self.direccion.strip() or None

        if self.usuario_registro is not None:
            self.usuario_registro = self.usuario_registro.strip() or None

    def actualizar(self, datos: dict[str, Any]) -> None:
        """
        Actualiza atributos permitidos y vuelve a validar el modelo.

        Args:
            datos: Campos y valores que se modificarán.

        Raises:
            ValueError: Si se intenta modificar un atributo no permitido.
        """
        campos_permitidos = {
            "nombres",
            "apellidos",
            "telefono",
            "email",
            "direccion",
            "fecha_nacimiento",
            "sexo",
        }
        campos_invalidos = set(datos) - campos_permitidos

        if campos_invalidos:
            campos = ", ".join(sorted(campos_invalidos))
            raise ValueError(f"Campos no actualizables para paciente: {campos}.")

        for campo, valor in datos.items():
            setattr(self, campo, valor)

        self.__post_init__()

    def desactivar(self) -> None:
        """Desactiva lógicamente al paciente."""
        self.estado = False

    def activar(self) -> None:
        """Activa lógicamente al paciente."""
        self.estado = True

    def validar_documento(self) -> bool:
        """
        Verifica nuevamente que el documento sea válido.

        Returns:
            True si el documento cumple su formato.
        """
        validar_documento(self.tipo_documento, self.numero_documento)
        return True

    def to_dict(self) -> dict[str, object]:
        """
        Convierte el modelo al formato de columnas SQLite.

        Returns:
            Diccionario listo para PacienteRepository.
        """
        return {
            "codigo_paciente": self.codigo_paciente,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "tipo_documento": self.tipo_documento,
            "numero_documento": self.numero_documento,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat(),
            "sexo": self.sexo,
            "telefono": self.telefono,
            "email": self.email,
            "direccion": self.direccion,
            "estado": int(self.estado),
            "usuario_registro": self.usuario_registro,
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Paciente":
        """
        Crea un Paciente desde una fila devuelta por SQLite.

        Args:
            fila: Diccionario con columnas de la tabla paciente.

        Returns:
            Instancia de Paciente.
        """
        fecha_registro = fila.get("fecha_registro")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            codigo_paciente=str(fila["codigo_paciente"]),
            nombres=str(fila["nombres"]),
            apellidos=str(fila["apellidos"]),
            tipo_documento=str(fila["tipo_documento"]),
            numero_documento=str(fila["numero_documento"]),
            fecha_nacimiento=date.fromisoformat(str(fila["fecha_nacimiento"])),
            sexo=str(fila["sexo"]),
            telefono=(
                str(fila["telefono"]) if fila.get("telefono") is not None else None
            ),
            email=str(fila["email"]) if fila.get("email") is not None else None,
            direccion=(
                str(fila["direccion"]) if fila.get("direccion") is not None else None
            ),
            estado=bool(fila.get("estado", 1)),
            fecha_registro=(
                datetime.fromisoformat(str(fecha_registro))
                if fecha_registro is not None
                else None
            ),
            usuario_registro=(
                str(fila["usuario_registro"])
                if fila.get("usuario_registro") is not None
                else None
            ),
        )
