"""
Gestión centralizada de parámetros de configuración.

Implementa Singleton para acceder a valores de la tabla configuracion.
No reemplaza al Singleton Database: Database administra la conexión,
mientras Configuracion administra valores globales de la aplicación.
"""

from typing import Self

from src.utils.database import Database, db


class Configuracion:
    """Singleton para acceder a configuraciones globales persistidas."""

    _instance: Self | None = None

    def __new__(cls) -> Self:
        """Crea o retorna la única instancia de Configuracion."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Inicializa el acceso a la conexión compartida."""
        self._db: Database = db

    @classmethod
    def get_instance(cls) -> Self:
        """
        Retorna la instancia Singleton.

        Returns:
            Instancia única de Configuracion.
        """
        return cls()

    def obtener(
        self,
        clave: str,
        valor_predeterminado: str | None = None,
    ) -> str | None:
        """
        Obtiene el valor de una configuración.

        Args:
            clave: Clave única almacenada en configuracion.
            valor_predeterminado: Valor retornado si la clave no existe.

        Returns:
            Valor de configuración o el valor predeterminado.
        """
        cursor = self._db.execute_query(
            "SELECT valor FROM configuracion WHERE clave = ?",
            (clave,),
        )
        fila = cursor.fetchone()

        if fila is None:
            return valor_predeterminado

        return str(fila[0])

    def obtener_todas(self) -> dict[str, str]:
        """
        Obtiene todas las configuraciones como diccionario.

        Returns:
            Diccionario clave -> valor.
        """
        cursor = self._db.execute_query(
            "SELECT clave, valor FROM configuracion ORDER BY clave"
        )
        filas = cursor.fetchall()

        return {str(clave): str(valor) for clave, valor in filas}

    def actualizar(
        self,
        clave: str,
        valor: str,
        descripcion: str | None = None,
    ) -> bool:
        """
        Inserta o actualiza una configuración mediante UPSERT.

        Args:
            clave: Clave única.
            valor: Valor que se guardará.
            descripcion: Descripción opcional.

        Returns:
            True si se insertó o actualizó correctamente.
        """
        clave_limpia = clave.strip()
        valor_limpio = valor.strip()

        if not clave_limpia:
            raise ValueError("La clave de configuración no puede estar vacía.")

        if not valor_limpio:
            raise ValueError("El valor de configuración no puede estar vacío.")

        query = """
            INSERT INTO configuracion (
                clave,
                valor,
                descripcion,
                fecha_actualizacion
            )
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(clave) DO UPDATE SET
                valor = excluded.valor,
                descripcion = COALESCE(
                    excluded.descripcion,
                    configuracion.descripcion
                ),
                fecha_actualizacion = CURRENT_TIMESTAMP
        """
        self._db.execute_query(
            query,
            (clave_limpia, valor_limpio, descripcion),
        )
        self._db.commit()

        return True

    def eliminar(self, clave: str) -> bool:
        """
        Elimina una clave de configuración.

        Args:
            clave: Clave a eliminar.

        Returns:
            True si existía y fue eliminada; False en caso contrario.
        """
        cursor = self._db.execute_query(
            "DELETE FROM configuracion WHERE clave = ?",
            (clave,),
        )
        self._db.commit()

        return cursor.rowcount > 0

    def existe(self, clave: str) -> bool:
        """
        Verifica si existe una clave de configuración.

        Args:
            clave: Clave a verificar.

        Returns:
            True si existe; False en caso contrario.
        """
        cursor = self._db.execute_query(
            "SELECT 1 FROM configuracion WHERE clave = ? LIMIT 1",
            (clave,),
        )
        return cursor.fetchone() is not None


configuracion = Configuracion.get_instance()
