"""
Servicio de negocio para gestión de citas médicas.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.modelos.cita import Cita
from src.repositorios.cita_repository import CitaRepository
from src.utils.validaciones import (
    validar_entero_positivo,
    validar_intervalo_horario,
    validar_no_vacio,
)

ZONA_LIMA = ZoneInfo("America/Lima")


class CitaService:
    """Coordina programación, reprogramación y cancelación de citas."""

    def __init__(self) -> None:
        """Inicializa el repositorio de citas."""
        self._repositorio = CitaRepository()

    def programar_cita(
        self,
        paciente_id: int,
        recepcionista_id: int,
        servicio_id: int,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        usuario_creacion: str,
        motivo: str | None = None,
    ) -> int:
        """
        Programa una cita si no existe colisión de horario.

        Args:
            paciente_id: ID del paciente.
            recepcionista_id: ID del recepcionista.
            servicio_id: ID del servicio.
            fecha_inicio: Inicio de la cita.
            fecha_fin: Fin de la cita.
            usuario_creacion: Usuario que programa.
            motivo: Motivo opcional.

        Returns:
            ID de la cita creada.

        Raises:
            RuntimeError: Si existe colisión de horario.
        """
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        recepcionista_id = validar_entero_positivo(
            recepcionista_id,
            "recepcionista_id",
        )
        servicio_id = validar_entero_positivo(servicio_id, "servicio_id")
        usuario_creacion = validar_no_vacio(
            usuario_creacion,
            "usuario_creacion",
        )
        validar_intervalo_horario(fecha_inicio, fecha_fin)

        if self._repositorio.verificar_colisiones(
            servicio_id,
            fecha_inicio.isoformat(),
            fecha_fin.isoformat(),
        ):
            raise RuntimeError("Ya existe una cita que se superpone con ese horario.")

        cita = Cita(
            paciente_id=paciente_id,
            recepcionista_id=recepcionista_id,
            servicio_id=servicio_id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            usuario_creacion=usuario_creacion,
            motivo=motivo,
        )

        return self._repositorio.create(cita.to_dict())

    def obtener_cita(self, cita_id: int) -> Cita:
        """
        Obtiene una cita por ID.

        Args:
            cita_id: ID de la cita.

        Returns:
            Instancia de Cita.

        Raises:
            LookupError: Si la cita no existe.
        """
        fila = self._repositorio.find_by_id(cita_id)

        if fila is None:
            raise LookupError(f"No existe una cita con ID {cita_id}.")

        return Cita.from_row(fila)

    def listar_citas_de_paciente(
        self,
        paciente_id: int,
        limite: int = 20,
    ) -> list[Cita]:
        """Lista las citas de un paciente."""
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")

        return [
            Cita.from_row(fila)
            for fila in self._repositorio.find_by_paciente(paciente_id, limite)
        ]

    def reprogramar_cita(
        self,
        cita_id: int,
        nueva_fecha_inicio: datetime,
        nueva_fecha_fin: datetime,
        motivo: str,
        usuario_modificacion: str,
    ) -> bool:
        """
        Reprograma una cita si el nuevo horario está disponible.

        Args:
            cita_id: ID de la cita.
            nueva_fecha_inicio: Nuevo inicio.
            nueva_fecha_fin: Nuevo fin.
            motivo: Motivo de reprogramación.
            usuario_modificacion: Usuario responsable.

        Returns:
            True si se reprogramó.

        Raises:
            LookupError: Si la cita no existe.
            RuntimeError: Si hay colisión.
        """
        self.obtener_cita(cita_id)
        validar_intervalo_horario(nueva_fecha_inicio, nueva_fecha_fin)
        motivo = validar_no_vacio(motivo, "motivo")
        usuario_modificacion = validar_no_vacio(
            usuario_modificacion,
            "usuario_modificacion",
        )

        reprogramada = self._repositorio.reprogramar(
            cita_id,
            nueva_fecha_inicio.isoformat(),
            nueva_fecha_fin.isoformat(),
            motivo,
            usuario_modificacion,
        )

        if not reprogramada:
            raise RuntimeError(
                "No se pudo reprogramar la cita por conflicto de horario."
            )

        return True

    def cancelar_cita(
        self,
        cita_id: int,
        motivo: str,
        usuario_modificacion: str,
    ) -> bool:
        """
        Cancela una cita.

        Args:
            cita_id: ID de la cita.
            motivo: Motivo de cancelación.
            usuario_modificacion: Usuario responsable.

        Returns:
            True si se canceló.

        Raises:
            LookupError: Si la cita no existe.
        """
        self.obtener_cita(cita_id)
        motivo = validar_no_vacio(motivo, "motivo")
        usuario_modificacion = validar_no_vacio(
            usuario_modificacion,
            "usuario_modificacion",
        )

        return self._repositorio.cancelar(
            cita_id,
            motivo,
            usuario_modificacion,
        )
