"""
Servicio de negocio para historial clínico.
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.modelos.entrada_historial import EntradaHistorial
from src.modelos.historial_clinico import HistorialClinico
from src.repositorios.historial_repository import HistorialRepository
from src.utils.validaciones import (
    TIPOS_ENTRADA_HISTORIAL,
    validar_dominio,
    validar_entero_positivo,
    validar_no_vacio,
)

ZONA_LIMA = ZoneInfo("America/Lima")


class HistorialService:
    """Coordina historiales clínicos y sus entradas versionadas."""

    def __init__(self) -> None:
        """Inicializa el repositorio de historial clínico."""
        self._repositorio = HistorialRepository()

    def crear_historial(
        self,
        paciente_id: int,
        numero_historia: str,
    ) -> int:
        """
        Crea un historial clínico para un paciente.

        Args:
            paciente_id: ID del paciente.
            numero_historia: Número único de historia clínica.

        Returns:
            ID del historial creado.

        Raises:
            RuntimeError: Si el paciente ya tiene historial.
        """
        paciente_id = validar_entero_positivo(paciente_id, "paciente_id")
        numero_historia = validar_no_vacio(numero_historia, "numero_historia")

        if self._repositorio.find_by_paciente(paciente_id):
            raise RuntimeError("El paciente ya tiene un historial clínico.")

        historial = HistorialClinico(
            paciente_id=paciente_id,
            numero_historia=numero_historia,
        )

        return self._repositorio.create(historial.to_dict())

    def obtener_historial(self, paciente_id: int) -> HistorialClinico:
        """
        Obtiene el historial clínico de un paciente.

        Args:
            paciente_id: ID del paciente.

        Returns:
            Historial clínico encontrado.

        Raises:
            LookupError: Si no existe historial.
        """
        fila = self._repositorio.find_by_paciente(paciente_id)

        if fila is None:
            raise LookupError("El paciente no tiene historial clínico.")

        return HistorialClinico.from_row(fila)

    def registrar_entrada(
        self,
        paciente_id: int,
        tipo_entrada: str,
        contenido: str,
        usuario_registro: str,
    ) -> int:
        """
        Registra una entrada clínica y actualiza la versión del historial.

        Args:
            paciente_id: ID del paciente.
            tipo_entrada: Tipo permitido de entrada.
            contenido: Contenido clínico.
            usuario_registro: Usuario responsable.

        Returns:
            ID de la entrada creada.
        """
        historial = self.obtener_historial(paciente_id)
        tipo_entrada = validar_dominio(
            tipo_entrada.strip().lower(),
            TIPOS_ENTRADA_HISTORIAL,
            "tipo_entrada",
        )
        contenido = validar_no_vacio(contenido, "contenido")
        usuario_registro = validar_no_vacio(
            usuario_registro,
            "usuario_registro",
        )

        entrada_id = self._repositorio.registrar_entrada(
            historial_id=int(historial.id or 0),
            tipo_entrada=tipo_entrada,
            contenido=contenido,
            usuario_registro=usuario_registro,
        )

        self._repositorio.update(
            int(historial.id or 0),
            {
                "version": historial.version + 1,
                "fecha_ultima_modificacion": datetime.now(ZONA_LIMA).isoformat(),
                "usuario_ultima_modificacion": usuario_registro,
            },
        )

        return entrada_id

    def obtener_entradas(
        self,
        paciente_id: int,
        filtro: dict[str, str] | None = None,
    ) -> list[EntradaHistorial]:
        """Obtiene las entradas del historial de un paciente."""
        historial = self.obtener_historial(paciente_id)
        filas = self._repositorio.obtener_entradas(
            int(historial.id or 0),
            filtro,
        )

        return [EntradaHistorial.from_row(fila) for fila in filas]

    def actualizar_entrada(
        self,
        entrada_id: int,
        contenido: str,
        usuario_registro: str,
    ) -> bool:
        """
        Crea una nueva versión de una entrada clínica.

        Args:
            entrada_id: ID de la entrada original.
            contenido: Nuevo contenido.
            usuario_registro: Usuario responsable.

        Returns:
            True si se creó la nueva versión.
        """
        contenido = validar_no_vacio(contenido, "contenido")
        usuario_registro = validar_no_vacio(
            usuario_registro,
            "usuario_registro",
        )

        return self._repositorio.actualizar_entrada(
            entrada_id,
            contenido,
            usuario_registro,
        )

    def listar_historiales(self) -> list[HistorialClinico]:
        """Lista todos los historiales clínicos."""
        return [
            HistorialClinico.from_row(fila) for fila in self._repositorio.list_all()
        ]
