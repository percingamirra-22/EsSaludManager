"""
Servicio de negocio para usuarios, autenticación y roles.
"""

from typing import Any

from src.modelos.usuario import Usuario
from src.repositorios.usuario_repository import UsuarioRepository
from src.utils.seguridad import generar_hash_password, verificar_password
from src.utils.validaciones import validar_email, validar_no_vacio


class UsuarioService:
    """Coordina usuarios, autenticación, roles y permisos."""

    def __init__(self) -> None:
        """Inicializa el repositorio de usuarios."""
        self._repositorio = UsuarioRepository()

    def registrar_usuario(
        self,
        empleado_id: int,
        username: str,
        password: str,
        email: str,
    ) -> int:
        """
        Registra un usuario con contraseña cifrada.

        Args:
            empleado_id: ID del empleado asociado.
            username: Nombre de usuario único.
            password: Contraseña en texto plano.
            email: Correo único del usuario.

        Returns:
            ID del usuario creado.

        Raises:
            RuntimeError: Si username o email ya existen.
            ValueError: Si los datos son inválidos.
        """
        username = validar_no_vacio(username, "username").lower()
        email_validado = validar_email(email)

        if email_validado is None:
            raise ValueError("El campo 'email' es obligatorio.")

        if self._repositorio.find_by_username(username):
            raise RuntimeError("El nombre de usuario ya está registrado.")

        if self._repositorio.find_by_email(email_validado):
            raise RuntimeError("El correo electrónico ya está registrado.")

        usuario = Usuario(
            empleado_id=empleado_id,
            username=username,
            password_hash=generar_hash_password(password),
            email=email_validado,
        )

        return self._repositorio.create(usuario.to_dict())

    def autenticar(
        self,
        username: str,
        password: str,
    ) -> dict[str, object] | None:
        """
        Autentica un usuario.

        Args:
            username: Nombre de usuario.
            password: Contraseña en texto plano.

        Returns:
            Datos del usuario si las credenciales son válidas.
        """
        username = validar_no_vacio(username, "username").lower()

        usuario_fila = self._repositorio.find_by_username(username)

        if usuario_fila is None:
            return None

        if not verificar_password(
            password,
            str(usuario_fila["password_hash"]),
        ):
            return None

        self._repositorio.update_last_access(int(usuario_fila["id"]))
        return usuario_fila

    def obtener_usuario(self, usuario_id: int) -> Usuario:
        """
        Obtiene un usuario por ID.

        Args:
            usuario_id: ID del usuario.

        Returns:
            Instancia de Usuario.

        Raises:
            LookupError: Si el usuario no existe.
        """
        fila = self._repositorio.find_by_id(usuario_id)

        if fila is None:
            raise LookupError(f"No existe un usuario con ID {usuario_id}.")

        return Usuario.from_row(fila)

    def obtener_roles(self, usuario_id: int) -> list[dict[str, object]]:
        """Obtiene los roles activos de un usuario."""
        self.obtener_usuario(usuario_id)
        return self._repositorio.find_roles(usuario_id)

    def obtener_permisos(self, usuario_id: int) -> list[dict[str, object]]:
        """Obtiene los permisos efectivos de un usuario."""
        self.obtener_usuario(usuario_id)
        return self._repositorio.find_permissions(usuario_id)

    def tiene_permiso(
        self,
        usuario_id: int,
        recurso: str,
        accion: str,
    ) -> bool:
        """
        Verifica si un usuario tiene un permiso específico.

        Args:
            usuario_id: ID del usuario.
            recurso: Recurso solicitado.
            accion: Acción solicitada.

        Returns:
            True si tiene el permiso.
        """
        permisos = self.obtener_permisos(usuario_id)

        return any(
            permiso["recurso"] == recurso and permiso["accion"] == accion
            for permiso in permisos
        )

    def listar_usuarios(self) -> list[dict[str, Any]]:
        """Lista todos los usuarios registrados."""
        return self._repositorio.list_all()
