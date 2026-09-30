"""
Repositorio para gestión de usuarios y autenticación.
"""

from typing import Any

from .base_repository import BaseRepository


class UsuarioRepository(BaseRepository[dict[str, Any]]):
    """
    Repositorio para la entidad Usuario.

    Métodos específicos:
    - authenticate(username, password): Valida credenciales.
    - find_by_username(username): Busca usuario por nombre.
    - find_by_email(email): Busca usuario por email.
    - find_roles(usuario_id): Obtiene roles del usuario.
    - find_permissions(usuario_id): Obtiene permisos del usuario.
    """

    def __init__(self) -> None:
        super().__init__("usuario")

    def authenticate(self, username: str, password_hash: str) -> dict[str, Any] | None:
        """
        Autentica un usuario por username y password hash.

        Args:
            username: Nombre de usuario.
            password_hash: Hash de la contraseña.

        Returns:
            dict | None: Datos del usuario si autentica, None si no.
        """
        query = """
            SELECT * FROM usuario 
            WHERE username = ? AND password_hash = ? AND estado = 1
        """
        cursor = self._db.execute_query(query, (username, password_hash))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        """Busca usuario por username."""
        query = "SELECT * FROM usuario WHERE username = ?"
        cursor = self._db.execute_query(query, (username,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        """Busca usuario por email."""
        query = "SELECT * FROM usuario WHERE email = ?"
        cursor = self._db.execute_query(query, (email,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))  # type: ignore[return-value]

    def find_roles(self, usuario_id: int) -> list[dict[str, Any]]:
        """
        Obtiene los roles asignados a un usuario.

        Returns:
            list[dict]: Lista de roles con id, nombre_rol, descripcion.
        """
        query = """
            SELECT r.id, r.nombre_rol, r.descripcion
            FROM rol r
            INNER JOIN usuario_rol ur ON r.id = ur.rol_id
            WHERE ur.usuario_id = ? AND ur.estado = 1 AND r.estado = 1
        """
        cursor = self._db.execute_query(query, (usuario_id,))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def find_permissions(self, usuario_id: int) -> list[dict[str, Any]]:
        """
        Obtiene los permisos asignados a un usuario (vía roles).

        Returns:
            list[dict]: Lista de permisos con codigo_permiso, recurso, accion.
        """
        query = """
            SELECT DISTINCT p.codigo_permiso, p.recurso, p.accion, p.descripcion
            FROM permiso p
            INNER JOIN rol_permiso rp ON p.id = rp.permiso_id
            INNER JOIN usuario_rol ur ON rp.rol_id = ur.rol_id
            WHERE ur.usuario_id = ? AND ur.estado = 1 
                  AND p.estado = 1 AND rp.fecha_asignacion IS NOT NULL
        """
        cursor = self._db.execute_query(query, (usuario_id,))
        rows = cursor.fetchall()

        if not rows:
            return []

        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]  # type: ignore[return-value]

    def update_last_access(self, usuario_id: int) -> bool:
        """
        Actualiza la fecha de último acceso del usuario.

        Args:
            usuario_id: ID del usuario.

        Returns:
            bool: True si se actualizó, False si no existe.
        """
        query = """
            UPDATE usuario 
            SET fecha_ultimo_acceso = CURRENT_TIMESTAMP 
            WHERE id = ?
        """
        cursor = self._db.execute_query(query, (usuario_id,))
        self._db.commit()
        return cursor.rowcount > 0
