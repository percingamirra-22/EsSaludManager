from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EstadoCita(str, Enum):
    PROGRAMADA = "programada"
    CONFIRMADA = "confirmada"
    ATENDIDA = "atendida"
    CANCELADA = "cancelada"


# Transiciones de estado permitidas
_TRANSICIONES = {
    EstadoCita.PROGRAMADA: {EstadoCita.CONFIRMADA, EstadoCita.CANCELADA},
    EstadoCita.CONFIRMADA: {EstadoCita.ATENDIDA, EstadoCita.CANCELADA},
    EstadoCita.ATENDIDA: set(),
    EstadoCita.CANCELADA: set(),
}


@dataclass
class Cita:
    paciente_id: int
    medico_id: int
    fecha_hora: datetime
    motivo: str
    estado: EstadoCita = EstadoCita.PROGRAMADA
    id: int = 0

    def cambiar_estado(self, nuevo: EstadoCita) -> None:
        if nuevo not in _TRANSICIONES[self.estado]:
            raise ValueError(f"No se puede pasar de '{self.estado.value}' a '{nuevo.value}'.")
        self.estado = nuevo
