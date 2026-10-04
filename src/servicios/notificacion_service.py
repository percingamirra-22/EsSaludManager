"""
Servicio de negocio para notificaciones.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.modelos.notificacion import Notificacion
from src.repositorios.notificacion_repository import NotificacionRepository
from src.utils.validaciones import validar_entero_positivo, validar_no_vacio

ZONA_LIMA = ZoneInfo("America/Lima")


class NotificacionService:
    """Coordina recordatorios y notificaciones a pacientes."""

    def __init__(self) -> None:
        """Inicializa el repositorio de notificaciones."""
        self._repositorio = NotificacionRepository()

    def crear_notificacion(
        self,
        paciente_id: int,
        cita_id: int,
        tipo_notificacion: str,
        mensaje: str,
        canal: str,
    ) -> int:
        """
        Crea una notificación pendiente.

        Args:
            paciente_id: ID del paciente.
            cita_id: ID de la cita.
            tipo_notificacion: recordatorio_cita o recordatorio_examen.
            mensaje: Mensaje enviado al paciente.
            canal: sms o email.

        Returns:
            ID de la notificación creada.
        """
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        cita_id = validar_entero_positivo(cita_id, "cita_id")
        mensaje = validar_no_vacio(mensaje, "mensaje")

        notificacion = Notificacion(
            paciente_id=paciente_id,
            cita_id=cita_id,
            tipo_notificacion=tipo_notificacion,
            mensaje=mensaje,
            canal=canal,
        )

        return self._repositorio.create(notificacion.to_dict())

    def obtener_notificacion(self, notificacion_id: int) -> Notificacion:
        """
        Obtiene una notificación por ID.

        Args:
            notificacion_id: ID de la notificación.

        Returns:
            Instancia de Notificacion.

        Raises:
            LookupError: Si no existe.
        """
        notificacion_id = validar_entero_positivo(
            notificacion_id,
            "notificacion_id",
        )
        fila = self._repositorio.find_by_id(notificacion_id)

        if fila is None:
            raise LookupError(f"No existe una notificación con ID {notificacion_id}.")

        return Notificacion.from_row(fila)

    def listar_notificaciones_de_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[Notificacion]:
        """Lista notificaciones de un paciente."""
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")

        return [
            Notificacion.from_row(fila)
            for fila in self._repositorio.find_by_paciente(
                paciente_id,
                limite,
            )
        ]

    def marcar_enviada(self, notificacion_id: int) -> bool:
        """Marca una notificación como enviada."""
        notificacion = self.obtener_notificacion(notificacion_id)
        notificacion.marcar_enviada(datetime.now(ZONA_LIMA))

        return self._repositorio.update(
            notificacion_id,
            {
                "estado": notificacion.estado,
                "fecha_envio": notificacion.fecha_envio.isoformat()
                if notificacion.fecha_envio
                else None,
            },
        )

    def marcar_fallida(self, notificacion_id: int) -> bool:
        """Marca una notificación como fallida."""
        self.obtener_notificacion(notificacion_id)
        return self._repositorio.marcar_fallida(notificacion_id)
