"""
Modelo de dominio para permisos RBAC.
"""

from dataclasses import dataclass
from typing import Any

from src.utils.validaciones import validar_dominio, validar_no_vacio

ACCIONES_PERMITIDAS = frozenset({"crear", "leer", "actualizar", "eliminar", "aprobar"})


@dataclass
class Permiso:
    """Representa un permiso sobre un recurso del sistema."""

    codigo_permiso: str
    recurso: str
    accion: str
    id: int | None = None
    descripcion: str | None = None
    estado: bool = True

    def __post_init__(self) -> None:
        """Valida y normaliza los datos del permiso."""
        self.codigo_permiso = validar_no_vacio(
            self.codigo_permiso,
            "codigo_permiso",
        ).upper()
        self.recurso = validar_no_vacio(self.recurso, "recurso").lower()
        self.accion = validar_dominio(
            self.accion.strip().lower(),
            ACCIONES_PERMITIDAS,
            "accion",
        )

        if self.descripcion is not None:
            self.descripcion = self.descripcion.strip() or None

    def coincide_con(self, recurso: str, accion: str) -> bool:
        """
        Determina si el permiso permite operar sobre recurso y acción.

        Args:
            recurso: Recurso solicitado.
            accion: Acción solicitada.

        Returns:
            True si coincide con el permiso activo.
        """
        if not self.estado:
            return False

        recurso_solicitado = recurso.strip().lower()
        accion_solicitada = accion.strip().lower()

        recurso_valido = self.recurso in {"*", recurso_solicitado}
        accion_valida = self.accion in {"*", accion_solicitada}

        return recurso_valido and accion_valida

    def desactivar(self) -> None:
        """Desactiva lógicamente el permiso."""
        self.estado = False

    def to_dict(self) -> dict[str, object]:
        """Convierte atributos persistibles al formato SQLite."""
        return {
            "codigo_permiso": self.codigo_permiso,
            "descripcion": self.descripcion,
            "recurso": self.recurso,
            "accion": self.accion,
            "estado": int(self.estado),
        }

    @classmethod
    def from_row(cls, fila: dict[str, Any]) -> "Permiso":
        """Crea un Permiso desde una fila SQLite."""
        return cls(
            id=int(fila["id"]) if fila.get("id") is not None else None,
            codigo_permiso=str(fila["codigo_permiso"]),
            descripcion=(
                str(fila["descripcion"])
                if fila.get("descripcion") is not None
                else None
            ),
            recurso=str(fila["recurso"]),
            accion=str(fila["accion"]),
            estado=bool(fila.get("estado", 1)),
        )
