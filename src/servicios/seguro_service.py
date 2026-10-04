"""
Servicio de negocio para seguros médicos.
"""

from datetime import date

from src.modelos.seguro import Seguro
from src.repositorios.paciente_repository import PacienteRepository
from src.repositorios.seguro_repository import SeguroRepository
from src.utils.validaciones import (
    TIPOS_SEGURO,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
    validar_rango_fechas,
)


class SeguroService:
    """Coordina seguros y su asignación a pacientes."""

    def __init__(self) -> None:
        """Inicializa los repositorios de seguros y pacientes."""
        self._seguro_repository = SeguroRepository()
        self._paciente_repository = PacienteRepository()

    def registrar_seguro(
        self,
        tipo_seguro: str,
        nombre_aseguradora: str,
        codigo_plan: str,
        numero_poliza: str,
        fecha_inicio: date,
        fecha_fin: date | None = None,
    ) -> int:
        """
        Registra un seguro médico.

        Args:
            tipo_seguro: EsSalud o Privado.
            nombre_aseguradora: Nombre de la aseguradora.
            codigo_plan: Código del plan.
            numero_poliza: Número único de póliza.
            fecha_inicio: Fecha de inicio.
            fecha_fin: Fecha de fin opcional.

        Returns:
            ID del seguro creado.

        Raises:
            RuntimeError: Si la póliza ya existe.
        """
        tipo_seguro = validar_dominio(
            tipo_seguro.strip(),
            TIPOS_SEGURO,
            "tipo_seguro",
        )
        nombre_aseguradora = validar_no_vacio(
            nombre_aseguradora,
            "nombre_aseguradora",
        )
        codigo_plan = validar_no_vacio(codigo_plan, "codigo_plan")
        numero_poliza = validar_no_vacio(numero_poliza, "numero_poliza")
        validar_rango_fechas(fecha_inicio, fecha_fin)

        if self._seguro_repository.find_by_poliza(numero_poliza):
            raise RuntimeError("Ya existe un seguro con ese número de póliza.")

        seguro = Seguro(
            tipo_seguro=tipo_seguro,
            nombre_aseguradora=nombre_aseguradora,
            codigo_plan=codigo_plan,
            numero_poliza=numero_poliza,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return self._seguro_repository.create(seguro.to_dict())

    def obtener_seguro(self, seguro_id: int) -> Seguro:
        """
        Obtiene un seguro por ID.

        Args:
            seguro_id: ID del seguro.

        Returns:
            Instancia de Seguro.

        Raises:
            LookupError: Si no existe.
        """
        seguro_id = validar_entero_positivo(seguro_id, "seguro_id")
        fila = self._seguro_repository.find_by_id(seguro_id)

        if fila is None:
            raise LookupError(f"No existe un seguro con ID {seguro_id}.")

        return Seguro.from_row(fila)

    def asignar_seguro(
        self,
        paciente_id: int,
        seguro_id: int,
    ) -> int:
        """
        Asigna un seguro activo a un paciente.

        Args:
            paciente_id: ID del paciente.
            seguro_id: ID del seguro.

        Returns:
            ID de la asignación creada.

        Raises:
            LookupError: Si paciente o seguro no existen.
            RuntimeError: Si el paciente ya tiene seguro activo.
        """
        paciente_fila = self._paciente_repository.find_by_id(paciente_id)

        if paciente_fila is None:
            raise LookupError(f"No existe un paciente con ID {paciente_id}.")

        self.obtener_seguro(seguro_id)

        seguro_actual = self._seguro_repository.obtener_seguro_de_paciente(paciente_id)

        if seguro_actual is not None:
            raise RuntimeError("El paciente ya tiene un seguro activo.")

        return self._seguro_repository.asignar_a_paciente(
            paciente_id,
            seguro_id,
        )

    def obtener_seguro_de_paciente(self, paciente_id: int) -> Seguro | None:
        """Obtiene el seguro activo de un paciente."""
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        fila = self._seguro_repository.obtener_seguro_de_paciente(paciente_id)

        return Seguro.from_row(fila) if fila else None

    def desasignar_seguro(
        self,
        paciente_id: int,
        seguro_id: int,
    ) -> bool:
        """Desactiva la asignación de seguro de un paciente."""
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        seguro_id = validar_entero_positivo(seguro_id, "seguro_id")

        return self._seguro_repository.desasignar_de_paciente(
            paciente_id,
            seguro_id,
        )

    def verificar_vigencia(
        self,
        seguro_id: int,
        fecha_consulta: date,
    ) -> bool:
        """Verifica si un seguro está vigente."""
        seguro = self.obtener_seguro(seguro_id)
        return seguro.verificar_vigencia(fecha_consulta)
