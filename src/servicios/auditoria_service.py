"""
Servicio de negocio para auditoría y trazabilidad.
"""

from src.repositorios.auditoria_repository import AuditoriaRepository
from src.utils.validaciones import validar_entero_positivo, validar_no_vacio


class AuditoriaService:
    """Coordina el registro y consulta de eventos de auditoría."""

    def __init__(self) -> None:
        """Inicializa el repositorio de auditoría."""
        self._repositorio = AuditoriaRepository()

    def registrar_evento(
        self,
        usuario_id: int,
        empleado_id: int,
        accion: str,
        recurso: str,
        recurso_id: int,
        ip_origen: str,
        detalles: str | None = None,
    ) -> int:
        """
        Registra un evento de auditoría.

        Args:
            usuario_id: ID del usuario que ejecuta la acción.
            empleado_id: ID del empleado asociado.
            accion: Acción realizada.
            recurso: Recurso afectado.
            recurso_id: ID del recurso afectado.
            ip_origen: IP de origen.
            detalles: Detalles adicionales.

        Returns:
            ID del registro de auditoría.
        """
        usuario_id = validar_entero_positivo(usuario_id, "usuario_id")
        empleado_id = validar_entero_positivo(empleado_id, "empleado_id")
        accion = validar_no_vacio(accion, "accion").lower()
        recurso = validar_no_vacio(recurso, "recurso").lower()
        recurso_id = validar_entero_positivo(recurso_id, "recurso_id")
        ip_origen = validar_no_vacio(ip_origen, "ip_origen")

        return self._repositorio.registrar(
            usuario_id=usuario_id,
            empleado_id=empleado_id,
            accion=accion,
            recurso=recurso,
            recurso_id=recurso_id,
            ip_origen=ip_origen,
            detalles=detalles,
        )

    def obtener_historial(
        self,
        filtro: dict[str, object] | None = None,
        limite: int = 100,
    ) -> list[dict[str, object]]:
        """Obtiene eventos de auditoría con filtros opcionales."""
        return self._repositorio.obtener_historial(filtro, limite)

    def obtener_eventos_de_usuario(
        self,
        usuario_id: int,
        limite: int = 50,
    ) -> list[dict[str, object]]:
        """Obtiene eventos de auditoría de un usuario."""
        usuario_id = validar_entero_positivo(usuario_id, "usuario_id")
        return self._repositorio.obtener_por_usuario(usuario_id, limite)

    def obtener_eventos_de_recurso(
        self,
        recurso: str,
        recurso_id: int | None = None,
        limite: int = 50,
    ) -> list[dict[str, object]]:
        """Obtiene eventos de auditoría sobre un recurso."""
        recurso = validar_no_vacio(recurso, "recurso").lower()
        return self._repositorio.obtener_por_recurso(
            recurso,
            recurso_id,
            limite,
        )
