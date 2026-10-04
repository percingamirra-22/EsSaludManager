"""
Servicio de negocio para órdenes y exámenes médicos.
"""

from src.modelos.examen_medico import ExamenMedico
from src.modelos.orden_examen import OrdenExamen
from src.repositorios.examen_medico_repository import (
    ExamenMedicoRepository,
)
from src.repositorios.orden_examen_repository import (
    OrdenExamenRepository,
)
from src.utils.validaciones import validar_entero_positivo, validar_no_vacio


class ExamenMedicoService:
    """Coordina órdenes de examen y exámenes médicos."""

    def __init__(self) -> None:
        """Inicializa los repositorios de órdenes y exámenes."""
        self._orden_repository = OrdenExamenRepository()
        self._examen_repository = ExamenMedicoRepository()

    def crear_orden(
        self,
        paciente_id: int,
        especialista_id: int,
        observaciones: str | None = None,
    ) -> int:
        """
        Crea una orden de examen pendiente.

        Args:
            paciente_id: ID del paciente.
            especialista_id: ID del especialista.
            observaciones: Observaciones opcionales.

        Returns:
            ID de la orden creada.
        """
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        especialista_id = validar_entero_positivo(
            especialista_id,
            "especialista_id",
        )

        orden = OrdenExamen(
            paciente_id=paciente_id,
            especialista_id=especialista_id,
            observaciones=observaciones,
        )

        return self._orden_repository.create(orden.to_dict())

    def obtener_orden(self, orden_examen_id: int) -> OrdenExamen:
        """
        Obtiene una orden de examen por ID.

        Args:
            orden_examen_id: ID de la orden.

        Returns:
            Instancia de OrdenExamen.

        Raises:
            LookupError: Si no existe.
        """
        orden_examen_id = validar_entero_positivo(
            orden_examen_id,
            "orden_examen_id",
        )
        fila = self._orden_repository.find_by_id(orden_examen_id)

        if fila is None:
            raise LookupError(
                f"No existe una orden de examen con ID {orden_examen_id}."
            )

        return OrdenExamen.from_row(fila)

    def agregar_examen_a_orden(
        self,
        orden_examen_id: int,
        examen_id: int,
    ) -> int:
        """
        Agrega un examen médico a una orden pendiente.

        Args:
            orden_examen_id: ID de la orden.
            examen_id: ID del examen médico.

        Returns:
            ID de la relación examen solicitado.

        Raises:
            LookupError: Si la orden o examen no existen.
            RuntimeError: Si la orden no está pendiente.
        """
        orden = self.obtener_orden(orden_examen_id)

        if orden.estado != "pendiente":
            raise RuntimeError("Solo se pueden agregar exámenes a una orden pendiente.")

        examen = self.obtener_examen(examen_id)

        return self._orden_repository.agregar_examen_solicitado(
            orden_examen_id,
            int(examen.id or 0),
        )

    def crear_examen(
        self,
        servicio_id: int,
        orden_examen_id: int,
        tecnico_id: int,
        tipo_examen: str,
    ) -> int:
        """
        Crea un examen médico programado.

        Args:
            servicio_id: ID del servicio de tipo examen.
            orden_examen_id: ID de la orden.
            tecnico_id: ID del técnico.
            tipo_examen: Tipo de examen.

        Returns:
            ID del examen creado.
        """
        servicio_id = validar_entero_positivo(servicio_id, "servicio_id")
        orden_examen_id = validar_entero_positivo(
            orden_examen_id,
            "orden_examen_id",
        )
        tecnico_id = validar_entero_positivo(tecnico_id, "tecnico_id")
        tipo_examen = validar_no_vacio(tipo_examen, "tipo_examen")

        examen = ExamenMedico(
            id=servicio_id,
            servicio_id=servicio_id,
            orden_examen_id=orden_examen_id,
            tecnico_id=tecnico_id,
            tipo_examen=tipo_examen,
        )

        return self._examen_repository.create(examen.to_dict())

    def obtener_examen(self, examen_id: int) -> ExamenMedico:
        """
        Obtiene un examen médico por ID.

        Args:
            examen_id: ID del examen.

        Returns:
            Instancia de ExamenMedico.

        Raises:
            LookupError: Si no existe.
        """
        examen_id = validar_entero_positivo(examen_id, "examen_id")
        fila = self._examen_repository.find_by_id(examen_id)

        if fila is None:
            raise LookupError(f"No existe un examen con ID {examen_id}.")

        return ExamenMedico.from_row(fila)

    def iniciar_examen(self, examen_id: int) -> bool:
        """
        Inicia un examen programado.

        Args:
            examen_id: ID del examen.

        Returns:
            True si se inició.

        Raises:
            RuntimeError: Si el examen no está programado.
        """
        examen = self.obtener_examen(examen_id)

        if examen.estado != "programado":
            raise RuntimeError("Solo se puede iniciar un examen programado.")

        return self._examen_repository.cambiar_estado(
            examen_id,
            "en proceso",
        )

    def registrar_resultado(
        self,
        examen_id: int,
        resultado: str,
        archivo_resultado: str | None = None,
    ) -> bool:
        """
        Registra el resultado de un examen en proceso.

        Args:
            examen_id: ID del examen.
            resultado: Resultado obtenido.
            archivo_resultado: Ruta opcional del archivo.

        Returns:
            True si se registró.

        Raises:
            RuntimeError: Si el examen no está en proceso.
        """
        examen = self.obtener_examen(examen_id)

        if examen.estado != "en proceso":
            raise RuntimeError(
                "Solo se puede registrar el resultado de un examen en proceso."
            )

        resultado = validar_no_vacio(resultado, "resultado")

        return self._examen_repository.registrar_resultado(
            examen_id,
            resultado,
            archivo_resultado,
        )

    def cancelar_examen(self, examen_id: int) -> bool:
        """
        Cancela un examen programado o en proceso.

        Args:
            examen_id: ID del examen.

        Returns:
            True si se canceló.

        Raises:
            RuntimeError: Si el examen ya está completado.
        """
        examen = self.obtener_examen(examen_id)

        if examen.estado == "completado":
            raise RuntimeError("No se puede cancelar un examen completado.")

        return self._examen_repository.cambiar_estado(
            examen_id,
            "cancelado",
        )
