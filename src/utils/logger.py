"""
Logger técnico centralizado para EsSaludManager.

Registra mensajes INFO, WARNING y ERROR en la tabla log_sistema.
No sustituye AuditoriaRepository: auditoría registra acciones de usuarios
sobre datos sensibles; este módulo registra eventos técnicos.
"""

from typing import Self

from src.utils.database import Database, db

NIVELES_LOG_VALIDOS = frozenset({"INFO", "WARNING", "ERROR"})


class LogSistema:
    """Singleton para el registro técnico de eventos del sistema."""

    _instance: Self | None = None

    def __new__(cls) -> Self:
        """Crea o retorna la única instancia de LogSistema."""
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
            Instancia única de LogSistema.
        """
        return cls()

    def registrar(
        self,
        mensaje: str,
        nivel: str = "INFO",
        modulo: str | None = None,
    ) -> int:
        """
        Inserta un evento técnico en log_sistema.

        Args:
            mensaje: Mensaje técnico a registrar.
            nivel: INFO, WARNING o ERROR.
            modulo: Módulo que generó el evento.

        Returns:
            ID del registro creado.

        Raises:
            ValueError: Si el nivel no está permitido o el mensaje está vacío.
        """
        mensaje_limpio = mensaje.strip()
        nivel_limpio = nivel.strip().upper()

        if not mensaje_limpio:
            raise ValueError("El mensaje de log no puede estar vacío.")

        if nivel_limpio not in NIVELES_LOG_VALIDOS:
            niveles = ", ".join(sorted(NIVELES_LOG_VALIDOS))
            raise ValueError(
                f"Nivel de log inválido: '{nivel}'. Niveles permitidos: {niveles}."
            )

        cursor = self._db.execute_query(
            """
            INSERT INTO log_sistema (nivel, mensaje, modulo)
            VALUES (?, ?, ?)
            """,
            (nivel_limpio, mensaje_limpio, modulo),
        )
        self._db.commit()

        if cursor.lastrowid is None:
            raise RuntimeError("No se pudo obtener el ID del log registrado.")

        return cursor.lastrowid

    def obtener_logs(
        self,
        filtro: dict[str, str] | None = None,
        limite: int = 100,
    ) -> list[dict[str, object]]:
        """
        Obtiene logs técnicos con filtros opcionales.

        Filtros admitidos:
        - nivel
        - modulo
        - fecha_desde
        - fecha_hasta

        Args:
            filtro: Diccionario con filtros opcionales.
            limite: Máximo de registros retornados.

        Returns:
            Lista de logs ordenada del más reciente al más antiguo.

        Raises:
            ValueError: Si limite no es positivo.
        """
        if limite <= 0:
            raise ValueError("El límite de logs debe ser mayor que cero.")

        query = "SELECT * FROM log_sistema WHERE 1 = 1"
        parametros: list[object] = []

        if filtro is not None:
            if "nivel" in filtro:
                nivel = filtro["nivel"].strip().upper()
                if nivel not in NIVELES_LOG_VALIDOS:
                    raise ValueError(f"Nivel de log inválido: '{nivel}'.")

                query += " AND nivel = ?"
                parametros.append(nivel)

            if "modulo" in filtro:
                query += " AND modulo = ?"
                parametros.append(filtro["modulo"])

            if "fecha_desde" in filtro:
                query += " AND fecha_registro >= ?"
                parametros.append(filtro["fecha_desde"])

            if "fecha_hasta" in filtro:
                query += " AND fecha_registro <= ?"
                parametros.append(filtro["fecha_hasta"])

        query += " ORDER BY fecha_registro DESC LIMIT ?"
        parametros.append(limite)

        cursor = self._db.execute_query(query, tuple(parametros))
        filas = cursor.fetchall()
        columnas = [descripcion[0] for descripcion in cursor.description]

        return [dict(zip(columnas, fila, strict=True)) for fila in filas]


logger = LogSistema.get_instance()
