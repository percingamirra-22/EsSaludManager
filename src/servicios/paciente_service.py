"""
Servicio de negocio para gestión de pacientes.
"""

from datetime import date

from src.modelos.paciente import Paciente
from src.repositorios.paciente_repository import PacienteRepository
from src.utils.validaciones import (
    validar_documento,
    validar_email,
    validar_no_vacio,
    validar_telefono,
)


class PacienteService:
    """Coordina las operaciones de negocio relacionadas con pacientes."""

    def __init__(self) -> None:
        """Inicializa el repositorio de pacientes."""
        self._repositorio = PacienteRepository()

    def registrar_paciente(
        self,
        codigo_paciente: str,
        nombres: str,
        apellidos: str,
        tipo_documento: str,
        numero_documento: str,
        fecha_nacimiento: date,
        sexo: str,
        telefono: str | None = None,
        email: str | None = None,
        direccion: str | None = None,
        usuario_registro: str | None = None,
    ) -> int:
        """
        Registra un paciente nuevo.

        Args:
            codigo_paciente: Código único del paciente.
            nombres: Nombres del paciente.
            apellidos: Apellidos del paciente.
            tipo_documento: DNI, CE o PAS.
            numero_documento: Número de documento.
            fecha_nacimiento: Fecha de nacimiento.
            sexo: M, F u O.
            telefono: Teléfono opcional.
            email: Correo opcional.
            direccion: Dirección opcional.
            usuario_registro: Usuario responsable del registro.

        Returns:
            ID del paciente creado.

        Raises:
            ValueError: Si los datos son inválidos.
            RuntimeError: Si el documento o código ya existe.
        """
        paciente = Paciente(
            codigo_paciente=codigo_paciente,
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            numero_documento=numero_documento,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            telefono=telefono,
            email=email,
            direccion=direccion,
            usuario_registro=usuario_registro,
        )

        if self._repositorio.find_by_documento(paciente.numero_documento):
            raise RuntimeError("Ya existe un paciente con ese número de documento.")

        if self._repositorio.find_by_codigo(paciente.codigo_paciente):
            raise RuntimeError("Ya existe un paciente con ese código.")

        return self._repositorio.create(paciente.to_dict())

    def obtener_paciente(self, paciente_id: int) -> Paciente:
        """
        Obtiene un paciente por ID.

        Args:
            paciente_id: ID del paciente.

        Returns:
            Instancia de Paciente.

        Raises:
            LookupError: Si el paciente no existe.
        """
        fila = self._repositorio.find_by_id(paciente_id)

        if fila is None:
            raise LookupError(f"No existe un paciente con ID {paciente_id}.")

        return Paciente.from_row(fila)

    def buscar_por_documento(self, numero_documento: str) -> Paciente | None:
        """Busca un paciente por número de documento."""
        fila = self._repositorio.find_by_documento(
            validar_documento("DNI", numero_documento)
            if len(numero_documento) == 8
            else numero_documento
        )

        return Paciente.from_row(fila) if fila else None

    def buscar_por_apellidos(
        self,
        apellidos: str,
        limite: int = 20,
    ) -> list[Paciente]:
        """Busca pacientes por apellidos."""
        apellidos = validar_no_vacio(apellidos, "apellidos")
        filas = self._repositorio.find_by_apellidos(apellidos, limite)

        return [Paciente.from_row(fila) for fila in filas]

    def listar_activos(self) -> list[Paciente]:
        """Lista pacientes activos."""
        return [Paciente.from_row(fila) for fila in self._repositorio.list_activos()]

    def actualizar_paciente(
        self,
        paciente_id: int,
        datos: dict[str, object],
    ) -> bool:
        """
        Actualiza datos permitidos de un paciente.

        Args:
            paciente_id: ID del paciente.
            datos: Campos a actualizar.

        Returns:
            True si se actualizó.

        Raises:
            LookupError: Si el paciente no existe.
            ValueError: Si algún campo es inválido.
        """
        self.obtener_paciente(paciente_id)

        datos_validados: dict[str, object] = {}

        if "telefono" in datos:
            datos_validados["telefono"] = validar_telefono(
                str(datos["telefono"]) if datos["telefono"] else None
            )

        if "email" in datos:
            datos_validados["email"] = validar_email(
                str(datos["email"]) if datos["email"] else None
            )

        if "nombres" in datos:
            datos_validados["nombres"] = validar_no_vacio(
                str(datos["nombres"]),
                "nombres",
            )

        if "apellidos" in datos:
            datos_validados["apellidos"] = validar_no_vacio(
                str(datos["apellidos"]),
                "apellidos",
            )

        if not datos_validados:
            return False

        return self._repositorio.update(paciente_id, datos_validados)

    def desactivar_paciente(self, paciente_id: int) -> bool:
        """Desactiva lógicamente un paciente."""
        self.obtener_paciente(paciente_id)
        return self._repositorio.update(paciente_id, {"estado": 0})
