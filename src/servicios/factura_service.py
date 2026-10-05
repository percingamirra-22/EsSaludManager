"""
Servicio de negocio para facturación.
"""

from src.modelos.cobertura import Cobertura
from src.modelos.factura import Factura
from src.repositorios.cobertura_repository import CoberturaRepository
from src.repositorios.factura_repository import FacturaRepository
from src.utils.validaciones import (
    validar_entero_positivo,
    validar_no_vacio,
    validar_numero_en_rango,
)


class FacturaService:
    """Coordina facturas, ítems facturables y coberturas."""

    def __init__(self) -> None:
        """Inicializa los repositorios de factura y cobertura."""
        self._factura_repository = FacturaRepository()
        self._cobertura_repository = CoberturaRepository()

    def crear_factura(
        self,
        numero_factura: str,
        paciente_id: int,
        usuario_emisor: str,
    ) -> int:
        """
        Crea una factura pendiente.

        Args:
            numero_factura: Número único de factura.
            paciente_id: ID del paciente.
            usuario_emisor: Usuario que emite la factura.

        Returns:
            ID de la factura creada.

        Raises:
            RuntimeError: Si el número de factura ya existe.
        """
        numero_factura = validar_no_vacio(
            numero_factura,
            "numero_factura",
        ).upper()
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        usuario_emisor = validar_no_vacio(usuario_emisor, "usuario_emisor")

        if self._factura_repository.find_by_numero(numero_factura):
            raise RuntimeError("Ya existe una factura con ese número.")

        factura = Factura(
            numero_factura=numero_factura,
            paciente_id=paciente_id,
            usuario_emisor=usuario_emisor,
        )

        return self._factura_repository.create(factura.to_dict())

    def obtener_factura(self, factura_id: int) -> Factura:
        """
        Obtiene una factura por ID.

        Args:
            factura_id: ID de la factura.

        Returns:
            Instancia de Factura.

        Raises:
            LookupError: Si no existe.
        """
        factura_id = validar_entero_positivo(factura_id, "factura_id")
        fila = self._factura_repository.find_by_id(factura_id)

        if fila is None:
            raise LookupError(f"No existe una factura con ID {factura_id}.")

        return Factura.from_row(fila)

    def agregar_item(
        self,
        factura_id: int,
        servicio_id: int,
        descripcion: str,
        costo: float,
    ) -> int:
        """
        Agrega un ítem a una factura pendiente.

        Args:
            factura_id: ID de la factura.
            servicio_id: ID del servicio.
            descripcion: Descripción del servicio.
            costo: Costo del ítem.

        Returns:
            ID del ítem creado.

        Raises:
            RuntimeError: Si la factura no está pendiente.
        """
        factura = self.obtener_factura(factura_id)

        if factura.estado != "pendiente":
            raise RuntimeError("Solo se pueden agregar ítems a una factura pendiente.")

        servicio_id = validar_entero_positivo(servicio_id, "servicio_id")
        descripcion = validar_no_vacio(descripcion, "descripcion")
        costo = validar_numero_en_rango(
            float(costo),
            0.0,
            float("inf"),
            "costo",
        )

        return self._factura_repository.registrar_item(
            factura_id,
            servicio_id,
            descripcion,
            costo,
        )

    def recalcular_montos(self, factura_id: int) -> float:
        """
        Recalcula el monto total desde los ítems activos.

        Args:
            factura_id: ID de la factura.

        Returns:
            Monto total recalculado.
        """
        self.obtener_factura(factura_id)
        items = self._factura_repository.obtener_items(factura_id)

        costos_activos = [
            float(item["costo"]) for item in items if item["estado"] == "activo"
        ]

        factura = self.obtener_factura(factura_id)
        factura.recalcular_montos(costos_activos)

        self._factura_repository.update(
            factura_id,
            {
                "monto_total": factura.monto_total,
                "monto_cubierto": factura.monto_cubierto,
                "monto_paciente": factura.monto_paciente,
            },
        )

        return factura.monto_total

    def aplicar_cobertura(
        self,
        factura_id: int,
        cobertura_id: int,
    ) -> dict[str, float]:
        """
        Aplica una cobertura vigente a una factura.

        Args:
            factura_id: ID de la factura.
            cobertura_id: ID de la cobertura.

        Returns:
            Diccionario con monto_cubierto, copago y monto_paciente.

        Raises:
            RuntimeError: Si la factura no está pendiente.
        """
        factura = self.obtener_factura(factura_id)

        if factura.estado != "pendiente":
            raise RuntimeError(
                "Solo se puede aplicar cobertura a una factura pendiente."
            )

        cobertura_fila = self._cobertura_repository.find_by_id(cobertura_id)

        if cobertura_fila is None:
            raise LookupError(f"No existe una cobertura con ID {cobertura_id}.")

        cobertura = Cobertura.from_row(cobertura_fila)
        calculo = cobertura.calcular_cobertura(factura.monto_total)

        factura.aplicar_cobertura(
            calculo["monto_cubierto"],
            calculo["copago"],
        )

        self._factura_repository.update(
            factura_id,
            {
                "monto_cubierto": factura.monto_cubierto,
                "monto_paciente": factura.monto_paciente,
            },
        )

        return calculo

    def anular_factura(self, factura_id: int) -> bool:
        """
        Anula una factura pendiente.

        Args:
            factura_id: ID de la factura.

        Returns:
            True si se anuló.

        Raises:
            RuntimeError: Si la factura ya fue pagada.
        """
        factura = self.obtener_factura(factura_id)

        if factura.estado == "pagada":
            raise RuntimeError("No se puede anular una factura pagada.")

        return self._factura_repository.update(
            factura_id,
            {"estado": "anulada"},
        )

    def generar_estado_cuenta(self, factura_id: int) -> dict[str, float | str]:
        """
        Genera el estado de cuenta de una factura.

        Args:
            factura_id: ID de la factura.

        Returns:
            Resumen de montos y saldo pendiente.
        """
        factura = self.obtener_factura(factura_id)
        total_pagado = self._factura_repository.calcular_total_pagado(factura_id)

        return factura.generar_estado_cuenta(total_pagado)

    def listar_facturas(self) -> list[Factura]:
        """Lista todas las facturas registradas."""
        filas = self._factura_repository.list_all()
        return [Factura.from_row(fila) for fila in filas]
