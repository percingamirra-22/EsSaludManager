"""
Funciones de seguridad para EsSaludManager.

Incluye hash de contraseñas, verificación de credenciales y evaluación
de permisos RBAC. No accede directamente a la interfaz gráfica.
"""

import hashlib
import hmac
import os
from base64 import b64decode, b64encode
from typing import Any, Final

_ALGORITMO_HASH: Final[str] = "sha256"
_ITERACIONES_PBKDF2: Final[int] = 310_000
_TAMANIO_SAL: Final[int] = 16


def validar_password(password: str) -> str:
    """
    Valida una contraseña para el prototipo.

    Args:
        password: Contraseña en texto plano.

    Returns:
        La contraseña validada.

    Raises:
        ValueError: Si no cumple la longitud mínima.
    """
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")

    return password


def generar_hash_password(password: str) -> str:
    """
    Genera un hash PBKDF2-HMAC-SHA256 con sal aleatoria.

    El formato almacenado es:
    algoritmo$iteraciones$sal_base64$hash_base64

    Args:
        password: Contraseña en texto plano.

    Returns:
        Hash serializado listo para persistir en usuario.password_hash.
    """
    validar_password(password)

    sal = os.urandom(_TAMANIO_SAL)
    hash_password = hashlib.pbkdf2_hmac(
        _ALGORITMO_HASH,
        password.encode("utf-8"),
        sal,
        _ITERACIONES_PBKDF2,
    )

    return "$".join(
        (
            _ALGORITMO_HASH,
            str(_ITERACIONES_PBKDF2),
            b64encode(sal).decode("ascii"),
            b64encode(hash_password).decode("ascii"),
        )
    )


def verificar_password(password: str, password_hash: str) -> bool:
    """
    Verifica una contraseña contra un hash PBKDF2 almacenado.

    Args:
        password: Contraseña en texto plano ingresada por el usuario.
        password_hash: Hash almacenado en la tabla usuario.

    Returns:
        True si la contraseña coincide; False en caso contrario.
    """
    try:
        algoritmo, iteraciones, sal_codificada, hash_almacenado = password_hash.split(
            "$", maxsplit=3
        )
        sal = b64decode(sal_codificada.encode("ascii"))
        hash_esperado = b64decode(hash_almacenado.encode("ascii"))
        hash_ingresado = hashlib.pbkdf2_hmac(
            algoritmo,
            password.encode("utf-8"),
            sal,
            int(iteraciones),
        )
    except (TypeError, ValueError, UnicodeError):
        return False

    return hmac.compare_digest(hash_ingresado, hash_esperado)


def tiene_permiso(
    permisos: list[dict[str, Any]],
    recurso: str,
    accion: str,
) -> bool:
    """
    Determina si una colección de permisos habilita una acción.

    Cada permiso debe incluir, como mínimo, las claves 'recurso' y 'accion'.
    Se admite '*' como comodín para recurso o acción.

    Args:
        permisos: Permisos obtenidos a través de UsuarioRepository.
        recurso: Recurso a consultar, por ejemplo: 'paciente'.
        accion: Acción solicitada, por ejemplo: 'actualizar'.

    Returns:
        True cuando el usuario tiene el permiso requerido.
    """
    for permiso in permisos:
        recurso_permiso = str(permiso.get("recurso", "")).strip().lower()
        accion_permiso = str(permiso.get("accion", "")).strip().lower()

        recurso_valido = recurso_permiso in {"*", recurso.strip().lower()}
        accion_valida = accion_permiso in {"*", accion.strip().lower()}

        if recurso_valido and accion_valida:
            return True

    return False


def exigir_permiso(
    permisos: list[dict[str, Any]],
    recurso: str,
    accion: str,
) -> None:
    """
    Exige un permiso RBAC.

    Args:
        permisos: Lista de permisos del usuario.
        recurso: Recurso solicitado.
        accion: Acción solicitada.

    Raises:
        PermissionError: Si el permiso no está asignado.
    """
    if not tiene_permiso(permisos, recurso, accion):
        raise PermissionError(
            f"No tiene permiso para ejecutar '{accion}' sobre '{recurso}'."
        )
