"""
Servicio de negocio para medicamentos, lotes y movimientos.
"""

from datetime import date

from src.modelos.lote_medicamento import LoteMedicamento
from src.modelos.medicamento import Medicamento
from src.modelos.movimiento_medicamento import MovimientoMedicamento
from src.repositorios.lote_medicamento_repository import (
    LoteMedicamentoRepository,
)
from src.repositorios.medicamento_repository import MedicamentoRepository
from src.repositorios.movimiento_medicamento_repository import (
    MovimientoMedicamentoRepository,
)
from src.utils.validaciones import (
    TIPOS_MOVIMIENTO_MEDICAMENTO,
    validar_dominio,
    validar_entero_no_negativo,
    validar_entero_positivo,
    validar_no_vacio,
)


class MedicamentoService:
    """Coordina medicamentos, stock, lotes y movimientos."""

    def __init__(self) -> None:
        """Inicializa los repositorios de medicamentos."""
        self._medicamento_repository = MedicamentoRepository()
        self._lote_repository = LoteMedicamentoRepository()
        self._movimiento_repository = MovimientoMedicamentoRepository()

    def registrar_medicamento(
        self,
        codigo_medicamento: str,
        nombre_generico: str,
        nombre_comercial: str,
        forma_farmaceutica: str,
        concentracion: str,
        unidad_medida: str,
        stock_minimo: int = 0,
        requiere_receta: bool = False,
    ) -> int:
        """
        Registra un medicamento en el catálogo.

        Args:
            codigo_medicamento: Código único.
            nombre_generico: Nombre genérico.
            nombre_comercial: Nombre comercial.
            forma_farmaceutica: Forma farmacéutica.
            concentracion: Concentración.
            unidad_medida: Unidad de medida.
            stock_minimo: Stock mínimo.
            requiere_receta: Indica si requiere receta.

        Returns:
            ID del medicamento creado.

        Raises:
            RuntimeError: Si el código ya existe.
        """
        medicamento = Medicamento(
            codigo_medicamento=codigo_medicamento,
            nombre_generico=nombre_generico,
            nombre_comercial=nombre_comercial,
            forma_farmaceutica=forma_farmaceutica,
            concentracion=concentracion,
            unidad_medida=unidad_medida,
            stock_minimo=stock_minimo,
            requiere_receta=requiere_receta,
        )

        if self._medicamento_repository.find_by_codigo(medicamento.codigo_medicamento):
            raise RuntimeError("Ya existe un medicamento con ese código.")

        return self._medicamento_repository.create(medicamento.to_dict())

    def buscar_medicamento(self, medicamento_id: int) -> Medicamento:
        """
        Obtiene un medicamento por ID.

        Args:
            medicamento_id: ID del medicamento.

        Returns:
            Instancia de Medicamento.

        Raises:
            LookupError: Si no existe.
        """
        medicamento_id = validar_entero_positivo(
            medicamento_id,
            "medicamento_id",
        )
        fila = self._medicamento_repository.find_by_id(medicamento_id)

        if fila is None:
            raise LookupError(f"No existe un medicamento con ID {medicamento_id}.")

        return Medicamento.from_row(fila)

    def buscar_por_codigo(self, codigo_medicamento: str) -> Medicamento | None:
        """Busca un medicamento por código."""
        codigo = validar_no_vacio(codigo_medicamento, "codigo_medicamento")
        fila = self._medicamento_repository.find_by_codigo(codigo.upper())

        return Medicamento.from_row(fila) if fila else None

    def buscar_por_nombre(self, nombre: str, limite: int = 20) -> list[Medicamento]:
        """Busca medicamentos por nombre genérico o comercial."""
        nombre = validar_no_vacio(nombre, "nombre")

        return [
            Medicamento.from_row(fila)
            for fila in self._medicamento_repository.find_by_nombre(
                nombre,
                limite,
            )
        ]

    def obtener_stock_total(self, medicamento_id: int) -> int:
        """Obtiene el stock total activo de un medicamento."""
        self.buscar_medicamento(medicamento_id)
        return self._medicamento_repository.obtener_stock(medicamento_id)

    def registrar_lote(
        self,
        medicamento_id: int,
        proveedor_id: int,
        numero_lote: str,
        fecha_fabricacion: date,
        fecha_vencimiento: date,
        cantidad_inicial: int,
    ) -> int:
        """
        Registra un lote de medicamento.

        Args:
            medicamento_id: ID del medicamento.
            proveedor_id: ID del proveedor.
            numero_lote: Número único de lote.
            fecha_fabricacion: Fecha de fabricación.
            fecha_vencimiento: Fecha de vencimiento.
            cantidad_inicial: Cantidad inicial.

        Returns:
            ID del lote creado.

        Raises:
            RuntimeError: Si el número de lote ya existe.
        """
        self.buscar_medicamento(medicamento_id)

        lote = LoteMedicamento(
            medicamento_id=medicamento_id,
            proveedor_id=proveedor_id,
            numero_lote=numero_lote,
            fecha_fabricacion=fecha_fabricacion,
            fecha_vencimiento=fecha_vencimiento,
            cantidad_inicial=cantidad_inicial,
        )

        if self._lote_repository.find_by_numero_lote(lote.numero_lote):
            raise RuntimeError("Ya existe un lote con ese número.")

        return self._lote_repository.create(lote.to_dict())

    def registrar_movimiento(
        self,
        lote_id: int,
        tipo_movimiento: str,
        cantidad: int,
        usuario_responsable: str,
        motivo: str | None = None,
        documento_referencia: str | None = None,
    ) -> int:
        """
        Registra un movimiento y actualiza el stock del lote.

        Args:
            lote_id: ID del lote.
            tipo_movimiento: entrada, salida o ajuste.
            cantidad: Cantidad del movimiento.
            usuario_responsable: Usuario responsable.
            motivo: Motivo opcional.
            documento_referencia: Documento de referencia opcional.

        Returns:
            ID del movimiento creado.

        Raises:
            LookupError: Si el lote no existe.
            ValueError: Si el movimiento es inválido.
        """
        lote_id = validar_entero_positivo(lote_id, "lote_id")
        tipo_movimiento = validar_dominio(
            tipo_movimiento.strip().lower(),
            TIPOS_MOVIMIENTO_MEDICAMENTO,
            "tipo_movimiento",
        )
        cantidad = validar_entero_positivo(cantidad, "cantidad")
        usuario_responsable = validar_no_vacio(
            usuario_responsable,
            "usuario_responsable",
        )

        fila_lote = self._lote_repository.find_by_id(lote_id)

        if fila_lote is None:
            raise LookupError(f"No existe un lote con ID {lote_id}.")

        lote = LoteMedicamento.from_row(fila_lote)
        lote.actualizar_stock(cantidad, tipo_movimiento)

        movimiento = MovimientoMedicamento(
            lote_id=lote_id,
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad,
            usuario_responsable=usuario_responsable,
            motivo=motivo,
            documento_referencia=documento_referencia,
        )

        movimiento_id = self._movimiento_repository.create(movimiento.to_dict())

        self._lote_repository.actualizar_stock(
            lote_id,
            int(lote.cantidad_actual or 0),
        )

        return movimiento_id

    def listar_lotes_de_medicamento(
        self,
        medicamento_id: int,
        solo_activos: bool = True,
    ) -> list[LoteMedicamento]:
        """Lista los lotes de un medicamento."""
        self.buscar_medicamento(medicamento_id)

        return [
            LoteMedicamento.from_row(fila)
            for fila in self._lote_repository.find_by_medicamento(
                medicamento_id,
                solo_activos,
            )
        ]

    def obtener_movimientos_de_lote(
        self,
        lote_id: int,
        limite: int = 50,
    ) -> list[MovimientoMedicamento]:
        """Obtiene el historial de movimientos de un lote."""
        lote_id = validar_entero_positivo(lote_id, "lote_id")

        return [
            MovimientoMedicamento.from_row(fila)
            for fila in self._movimiento_repository.find_by_lote(
                lote_id,
                limite,
            )
        ]

    def verificar_vencimientos(self, dias_limite: int = 30) -> list[dict[str, object]]:
        """Obtiene lotes próximos a vencer."""
        dias_limite = validar_entero_no_negativo(
            dias_limite,
            "dias_limite",
        )
        return self._medicamento_repository.verificar_vencimientos(dias_limite)
