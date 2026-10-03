"""
Modelo de dominio para roles RBAC.
"""

from dataclasses import dataclass, field
from typing import Any

from src.utils.validaciones import validar_no_vacio


def crear_lista_permisos() -> list[str]:
    """Crea una lista vacía tipada para permisos del rol."""
    return []


@dataclass
class Rol:
    """Representa un rol de control de acceso basado en roles."""

    nombre_rol: str
    id: int | None = None
    descripcion: str | None = None
    estado: bool = True
    permisos: list[str] = field(default_factory=crear_lista_permisos)

    def __post_init__(self) -> None:
        """Valida y normaliza el nombre y descripción del rol."""
        self.nombre_rol = validar_no_vacio(
            self.nombre_rol,
            "nombre_rol",
        )

        if self.descripcion is not None:
            self.descripcion = self.descripcion.strip() or None

    def asignar_permiso(self, codigo_permiso: str) -> bool:
        """
        Agrega un código de permiso al rol en memoria.

        La persistencia se realiza mediante RolPermiso en la capa de servicio.

        Args:
            codigo_permiso: Código del permiso.

        Returns:
            True si se agregó; False si ya estaba presente.
        """
        permiso = validar_no_vacio(codigo_permiso, "codigo_permiso").upper()

        if permiso in self.permisos:
            return False

        self.permisos.append(permiso)
        return True

    def revocar_permiso(self, codigo_permiso: str) -> bool:
        """
        Elimina un código de permiso del rol en memoria.

        Args:
            codigo_permiso: Código del permiso.

        Returns:
            True si se removió; False si no estaba asignado.
        """
        permiso = codigo_permiso.strip().upper()

        if permiso not in self.permisos:
            return False

        self.permisos.remove(permiso)
        return True

    def desactivar(self) -> None:
        """Desactiva lógicamente el rol."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte atributos persistibles al formato SQLite."""
        return {
            "nombre_rol": self.nombre_rol,
            "descripcion": self.descripcion,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Rol":
        """Crea un Rol desde una fila SQLite."""
        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            nombre_rol=str(fila["nombre_rol"]),
            descripcion=(
                str(fila["descripcion"])
                if fila.get("descripcion") is not None
                else None
            ),
            estado=bool(fila.get("estado", 1)),
        )
