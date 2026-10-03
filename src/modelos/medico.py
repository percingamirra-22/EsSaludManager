from dataclasses import dataclass

from src.utils import validaciones as v


@dataclass
class Medico:
    cmp: str
    nombres: str
    apellidos: str
    especialidad: str
    id: int = 0

    def __post_init__(self):
        self.cmp = v.validar_cmp(self.cmp)
        self.nombres = v.validar_nombre(self.nombres, "Nombres")
        self.apellidos = v.validar_nombre(self.apellidos, "Apellidos")
        self.especialidad = v.validar_nombre(self.especialidad, "Especialidad")

    @property
    def nombre_completo(self) -> str:
        return f"Dr(a). {self.nombres} {self.apellidos}"
