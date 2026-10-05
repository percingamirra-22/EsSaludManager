"""
Servicio de negocio para coberturas de seguro.
"""

from datetime import date

from src.modelos.cobertura import Cobertura
from src.repositorios.cobertura_repository import CoberturaRepository
from src.repositorios.seguro_repository import SeguroRepository
from src.utils.validaciones import (
    validar_entero_positivo,
    validar_numero_en_rango,
)


class CoberturaService:
    """Coordina coberturas por seguro y servicio."""

    def __init__(self) -> None:
        """Inicializa los repositorios de cobertura y seguro."""
        self._cobertura_repository = CoberturaRepository()
        self._seguro_repository = SeguroRepository()

    def registrar_cobertura(
        self,
        seguro_id: int,
        servicio_id: int,
        porcentaje_cobertura: float,
        monto_maximo: float,
        copago_fijo: float,
        fecha_inicio: date,
        fecha_fin: date | None = None,
    ) -> int:
        """
        Registra una cobertura para un seguro y servicio.

        Args:
            seguro_id: ID del seguro.
            servicio_id: ID del servicio.
            porcentaje_cobertura: Porcentaje entre 0 y 100.
            monto_maximo: Monto máximo cubierto.
            copago_fijo: Copago fijo.
            fecha_inicio: Fecha de inicio.
            fecha_fin: Fecha de fin opcional.

        Returns:
            ID de la cobertura creada.
        """
        seguro_id = validar_entero_positivo(seguro_id, "seguro_id")
        servicio_id = validar_entero_positivo(servicio_id, "servicio_id")

        fila_seguro = self._seguro_repository.find_by_id(seguro_id)

        if fila_seguro is None:
            raise LookupError(f"No existe un seguro con ID {seguro_id}.")

        cobertura = Cobertura(
            seguro_id=seguro_id,
            servicio_id=servicio_id,
            porcentaje_cobertura=porcentaje_cobertura,
            monto_maximo=monto_maximo,
            copago_fijo=copago_fijo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
        )

        return self._cobertura_repository.create(cobertura.to_dict())

    def obtener_cobertura(self, cobertura_id: int) -> Cobertura:
        """
        Obtiene una cobertura por ID.

        Args:
            cobertura_id: ID de la cobertura.

        Returns:
            Instancia de Cobertura.

        Raises:
            LookupError: Si no existe.
        """
        cobertura_id = validar_entero_positivo(
            cobertura_id,
            "cobertura_id",
        )
        fila = self._cobertura_repository.find_by_id(cobertura_id)

        if fila is None:
            raise LookupError(f"No existe una cobertura con ID {cobertura_id}.")

        return Cobertura.from_row(fila)

    def buscar_cobertura_vigente(
        self,
        seguro_id: int,
        servicio_id: int,
        fecha_consulta: date,
    ) -> Cobertura | None:
        """Busca una cobertura vigente para un seguro y servicio."""
        seguro_id = validar_entero_positivo(seguro_id, "seguro_id")
        servicio_id = validar_entero_positivo(servicio_id, "servicio_id")

        fila = self._cobertura_repository.buscar_vigente(
            seguro_id,
            servicio_id,
            fecha_consulta.isoformat(),
        )

        return Cobertura.from_row(fila) if fila else None

    def calcular_cobertura(
        self,
        cobertura_id: int,
        monto_total: float,
    ) -> dict[str, float]:
        """
        Calcula el monto cubierto, copago y monto del paciente.

        Args:
            cobertura_id: ID de la cobertura.
            monto_total: Monto total del servicio.

        Returns:
            Diccionario con monto_cubierto, copago y monto_paciente.
        """
        cobertura = self.obtener_cobertura(cobertura_id)
        monto_total = validar_numero_en_rango(
            float(monto_total),
            0.0,
            float("inf"),
            "monto_total",
        )

        return cobertura.calcular_cobertura(monto_total)

    def desactivar_cobertura(self, cobertura_id: int) -> bool:
        """Desactiva lógicamente una cobertura."""
        self.obtener_cobertura(cobertura_id)
        return self._cobertura_repository.desactivar(cobertura_id)

    def listar_coberturas(self) -> list[Cobertura]:
        """Lista todas las coberturas registradas."""
        filas = self._cobertura_repository.list_all()
        return [Cobertura.from_row(fila) for fila in filas]
