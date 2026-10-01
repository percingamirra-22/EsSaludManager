from dataclasses import dataclass

from src.utils.seguridad import Rol
from src.utils.validaciones import validar_username


@dataclass
class Usuario:
    username: str
    password_hash: str
    rol: Rol
    activo: bool = True
    id: int = 0

    def __post_init__(self):
        self.username = validar_username(self.username)
        self.rol = Rol(self.rol)
