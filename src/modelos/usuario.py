"""
Modelo de dominio para usuarios del sistema.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.utils.seguridad import verificar_password
from src.utils.validaciones import (
    validar_email,
    validar_entero_positivo,
    validar_no_vacio,
)


def crear_roles_ids() -> list[int]:
    """Crea una lista vacía tipada para IDs de roles asignados."""
    return []


@dataclass
class Usuario:
    """
    Representa credenciales de acceso vinculadas a un empleado.

    Los roles no se almacenan directamente en la tabla usuario; se asocian
    mediante UsuarioRol y se representan temporalmente con roles_ids.
    """

    empleado_id: int
    username: str
    password_hash: str
    email: str
    id: int | None = None
    estado: bool = True
    fecha_creacion: datetime | None = None
    fecha_ultimo_acceso: datetime | None = None
    roles_ids: list[int] = field(default_factory=crear_roles_ids)

    def __post_init__(self) -> None:
        """Valida y normaliza las credenciales del usuario."""
        self.empleado_id = validar_entero_positivo(
            self.empleado_id,
            "empleado_id",
        )
        self.username = validar_no_vacio(self.username, "username").lower()

        if len(self.username) < 3:
            raise ValueError("username debe tener al menos 3 caracteres.")

        self.password_hash = validar_no_vacio(
            self.password_hash,
            "password_hash",
        )
        self.email = validar_email(self.email) or ""

        if not self.email:
            raise ValueError("El correo electrónico del usuario es obligatorio.")

        for rol_id in self.roles_ids:
            validar_entero_positivo(rol_id, "rol_id")

    def autenticar(self, password: str) -> bool:
        """
        Verifica una contraseña contra el hash almacenado.

        Args:
            password: Contraseña en texto plano ingresada.

        Returns:
            True si el usuario está activo y la contraseña coincide.
        """
        return self.estado and verificar_password(password, self.password_hash)

    def cambiar_password_hash(self, nuevo_password_hash: str) -> None:
        """
        Actualiza el hash de la contraseña en memoria.

        Args:
            nuevo_password_hash: Hash generado por seguridad.py.
        """
        self.password_hash = validar_no_vacio(
            nuevo_password_hash,
            "nuevo_password_hash",
        )

    def registrar_acceso(self, fecha_acceso: datetime) -> None:
        """
        Registra la fecha y hora del último acceso.

        Args:
            fecha_acceso: Fecha y hora de autenticación exitosa.
        """
        self.fecha_ultimo_acceso = fecha_acceso

    def asignar_rol(self, rol_id: int) -> bool:
        """
        Agrega un ID de rol temporalmente al usuario.

        La persistencia corresponde a UsuarioRol y UsuarioService.

        Args:
            rol_id: Identificador del rol.

        Returns:
            True si el rol fue agregado; False si ya estaba asignado.
        """
        rol_id = validar_entero_positivo(rol_id, "rol_id")

        if rol_id in self.roles_ids:
            return False

        self.roles_ids.append(rol_id)
        return True

    def revocar_rol(self, rol_id: int) -> bool:
        """
        Retira un ID de rol temporalmente del usuario.

        Args:
            rol_id: Identificador del rol.

        Returns:
            True si fue retirado; False si no estaba asignado.
        """
        rol_id = validar_entero_positivo(rol_id, "rol_id")

        if rol_id not in self.roles_ids:
            return False

        self.roles_ids.remove(rol_id)
        return True

    def desactivar(self) -> None:
        """Desactiva lógicamente al usuario."""
        self.estado = False

    def activar(self) -> None:
        """Activa lógicamente al usuario."""
        self.estado = True

    def to_dict(self) -> dict[str, object]:
        """
        Convierte el modelo al formato de columnas de la tabla usuario.

        Returns:
            Diccionario apto para UsuarioRepository.
        """
        return {
            "empleado_id": self.empleado_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Usuario":
        """
        Crea un Usuario desde una fila SQLite.

        Args:
            fila: Diccionario con columnas de la tabla usuario.

        Returns:
            Instancia de Usuario.
        """
        fecha_creacion = fila.get("fecha_creacion")
        fecha_ultimo_acceso = fila.get("fecha_ultimo_acceso")

        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            empleado_id=int(fila["empleado_id"]),
            username=str(fila["username"]),
            password_hash=str(fila["password_hash"]),
            email=str(fila["email"]),
            estado=bool(fila.get("estado", 1)),
            fecha_creacion=(
                datetime.fromisoformat(str(fecha_creacion))
                if fecha_creacion is not None
                else None
            ),
            fecha_ultimo_acceso=(
                datetime.fromisoformat(str(fecha_ultimo_acceso))
                if fecha_ultimo_acceso is not None
                else None
            ),
        )
