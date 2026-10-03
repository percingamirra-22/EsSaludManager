from src.modelos import Usuario
from src.servicios.repositorio import RepositorioMemoria
from src.utils.seguridad import (
    Rol,
    hash_password,
    verificar_password,
    verificar_permiso,
)
from src.utils.validaciones import ErrorValidacion, validar_password, validar_username


class AuthServicio:
    def __init__(self, repo=None):
        self.repo = repo or RepositorioMemoria()

    def _buscar(self, username):
        return next((u for u in self.repo.listar() if u.username == username), None)

    def registrar_usuario(self, actor, username, password, rol) -> Usuario:
        """Solo un ADMIN puede crear usuarios; el primero (admin inicial) no requiere actor."""
        if self.repo.listar():
            verificar_permiso(actor, "usuarios:administrar")
        else:
            rol = Rol.ADMIN
        username = validar_username(username)
        validar_password(password)
        if self._buscar(username):
            raise ErrorValidacion("El nombre de usuario ya existe.")
        return self.repo.guardar(Usuario(username, hash_password(password), Rol(rol)))

    def login(self, username, password) -> Usuario:
        usuario = self._buscar(username)
        if (
            not usuario
            or not usuario.activo
            or not verificar_password(password, usuario.password_hash)
        ):
            raise ErrorValidacion("Usuario o contraseña incorrectos.")
        return usuario

    def desactivar_usuario(self, actor, usuario_id) -> None:
        verificar_permiso(actor, "usuarios:administrar")
        usuario = self.repo.obtener(usuario_id)
        if not usuario:
            raise ErrorValidacion("Usuario no encontrado.")
        usuario.activo = False
