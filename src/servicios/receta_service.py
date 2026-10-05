"""
Servicio de negocio para recetas médicas.
"""

from src.modelos.item_receta import ItemReceta
from src.modelos.receta_medica import RecetaMedica
from src.repositorios.medicamento_repository import MedicamentoRepository
from src.repositorios.receta_repository import RecetaRepository
from src.utils.validaciones import (
    validar_entero_positivo,
    validar_no_vacio,
)


class RecetaService:
    """Coordina recetas médicas, ítems y dispensación."""

    def __init__(self) -> None:
        """Inicializa los repositorios de receta y medicamento."""
        self._receta_repository = RecetaRepository()
        self._medicamento_repository = MedicamentoRepository()

    def crear_receta(
        self,
        paciente_id: int,
        especialista_id: int,
        usuario_emisor: str,
        observaciones: str | None = None,
    ) -> int:
        """
        Crea una receta médica activa.

        Args:
            paciente_id: ID del paciente.
            especialista_id: ID del especialista.
            usuario_emisor: Usuario que emite la receta.
            observaciones: Observaciones opcionales.

        Returns:
            ID de la receta creada.
        """
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        especialista_id = validar_entero_positivo(
            especialista_id,
            "especialista_id",
        )
        usuario_emisor = validar_no_vacio(usuario_emisor, "usuario_emisor")

        receta = RecetaMedica(
            paciente_id=paciente_id,
            especialista_id=especialista_id,
            usuario_emisor=usuario_emisor,
            observaciones=observaciones,
        )

        return self._receta_repository.create(receta.to_dict())

    def obtener_receta(self, receta_id: int) -> RecetaMedica:
        """
        Obtiene una receta por ID.

        Args:
            receta_id: ID de la receta.

        Returns:
            Instancia de RecetaMedica.

        Raises:
            LookupError: Si no existe.
        """
        receta_id = validar_entero_positivo(receta_id, "receta_id")
        fila = self._receta_repository.find_by_id(receta_id)

        if fila is None:
            raise LookupError(f"No existe una receta con ID {receta_id}.")

        return RecetaMedica.from_row(fila)

    def agregar_medicamento(
        self,
        receta_id: int,
        medicamento_id: int,
        dosis: str,
        frecuencia: str,
        duracion_dias: int,
    ) -> int:
        """
        Agrega un medicamento a una receta activa.

        Args:
            receta_id: ID de la receta.
            medicamento_id: ID del medicamento.
            dosis: Dosis indicada.
            frecuencia: Frecuencia de consumo.
            duracion_dias: Duración en días.

        Returns:
            ID del ítem creado.

        Raises:
            LookupError: Si receta o medicamento no existen.
            RuntimeError: Si la receta no está activa.
        """
        receta = self.obtener_receta(receta_id)

        if receta.estado != "activa":
            raise RuntimeError(
                "Solo se pueden agregar medicamentos a una receta activa."
            )

        medicamento = self._medicamento_repository.find_by_id(medicamento_id)

        if medicamento is None:
            raise LookupError(f"No existe un medicamento con ID {medicamento_id}.")

        return self._receta_repository.registrar_item(
            receta_id,
            medicamento_id,
            validar_no_vacio(dosis, "dosis"),
            validar_no_vacio(frecuencia, "frecuencia"),
            validar_entero_positivo(duracion_dias, "duracion_dias"),
        )

    def obtener_items(self, receta_id: int) -> list[ItemReceta]:
        """Obtiene los ítems de una receta."""
        self.obtener_receta(receta_id)

        return [
            ItemReceta.from_row(fila)
            for fila in self._receta_repository.obtener_items(receta_id)
        ]

    def verificar_disponibilidad(
        self,
        receta_id: int,
        cantidad_requerida: int,
    ) -> bool:
        """
        Verifica si todos los medicamentos de una receta tienen stock.

        Args:
            receta_id: ID de la receta.
            cantidad_requerida: Cantidad requerida por medicamento.

        Returns:
            True si todos los ítems tienen stock suficiente.
        """
        self.obtener_receta(receta_id)
        cantidad_requerida = validar_entero_positivo(
            cantidad_requerida,
            "cantidad_requerida",
        )
        items = self.obtener_items(receta_id)

        if not items:
            return False

        for item in items:
            stock = self._medicamento_repository.obtener_stock(item.medicamento_id)

            if stock < cantidad_requerida:
                return False

        return True

    def dispensar_receta(self, receta_id: int) -> bool:
        """Marca una receta como dispensada."""
        self.obtener_receta(receta_id)
        items = self.obtener_items(receta_id)

        if not items:
            raise RuntimeError("No se puede dispensar una receta sin ítems.")

        return self._receta_repository.update(
            receta_id,
            {"estado": "dispensada"},
        )

    def cancelar_receta(self, receta_id: int) -> bool:
        """
        Cancela una receta activa.

        Args:
            receta_id: ID de la receta.

        Returns:
            True si se canceló.

        Raises:
            RuntimeError: Si la receta ya fue dispensada.
        """
        receta = self.obtener_receta(receta_id)

        if receta.estado == "dispensada":
            raise RuntimeError("No se puede cancelar una receta dispensada.")

        return self._receta_repository.update(
            receta_id,
            {"estado": "cancelada"},
        )

    def listar_recetas(self) -> list[RecetaMedica]:
        """Lista todas las recetas médicas."""
        filas = self._receta_repository.list_all()
        return [RecetaMedica.from_row(fila) for fila in filas]
