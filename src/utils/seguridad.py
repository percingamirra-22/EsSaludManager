"""Seguridad: hash de contraseñas (PBKDF2) y control de acceso por roles (RBAC)."""
import hashlib
import hmac
import secrets
from enum import Enum

_ITERACIONES = 200_000


class PermisoDenegado(PermissionError):
    """El usuario no tiene permiso para realizar la acción."""


# ---------- Hash ----------
def hash_password(password: str) -> str:
    sal = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(sal), _ITERACIONES)
    return f"pbkdf2_sha256${_ITERACIONES}${sal}${h.hex()}"


def verificar_password(password: str, almacenado: str) -> bool:
    try:
        _, iteraciones, sal, h = almacenado.split("$")
        nuevo = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(sal), int(iteraciones))
        return hmac.compare_digest(nuevo.hex(), h)
    except (ValueError, AttributeError):
        return False


# ---------- RBAC ----------
class Rol(str, Enum):
    ADMIN = "admin"
    MEDICO = "medico"
    ADMISION = "admision"


PERMISOS = {
    Rol.ADMIN: {
        "usuarios:administrar", "pacientes:leer", "pacientes:escribir",
        "medicos:leer", "medicos:escribir", "citas:leer", "citas:agendar",
        "citas:gestionar", "citas:atender",
    },
    Rol.ADMISION: {
        "pacientes:leer", "pacientes:escribir", "medicos:leer",
        "citas:leer", "citas:agendar", "citas:gestionar",
    },
    Rol.MEDICO: {
        "pacientes:leer", "medicos:leer", "citas:leer", "citas:atender",
    },
}


def tiene_permiso(rol: Rol, permiso: str) -> bool:
    return permiso in PERMISOS.get(rol, set())


def verificar_permiso(usuario, permiso: str) -> None:
    """Lanza PermisoDenegado si el usuario es None, está inactivo o no tiene el permiso."""
    if usuario is None or not usuario.activo or not tiene_permiso(usuario.rol, permiso):
        raise PermisoDenegado(f"Acceso denegado: se requiere el permiso '{permiso}'.")
