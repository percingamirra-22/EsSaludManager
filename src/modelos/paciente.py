from dataclasses import dataclass
from datetime import date

from src.utils import validaciones as v


@dataclass
class Paciente:
    dni: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    telefono: str
    email: str
    id: int = 0

    def __post_init__(self):
        self.dni = v.validar_dni(self.dni)
        self.nombres = v.validar_nombre(self.nombres, "Nombres")
        self.apellidos = v.validar_nombre(self.apellidos, "Apellidos")
        self.fecha_nacimiento = v.validar_fecha_nacimiento(self.fecha_nacimiento)
        self.telefono = v.validar_telefono(self.telefono)
        self.email = v.validar_email(self.email)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombres} {self.apellidos}"

    @property
    def edad(self) -> int:
        hoy = date.today()
        n = self.fecha_nacimiento
        return hoy.year - n.year - ((hoy.month, hoy.day) < (n.month, n.day))
