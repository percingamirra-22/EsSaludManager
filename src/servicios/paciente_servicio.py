from src.modelos import Paciente
from src.servicios.repositorio import RepositorioMemoria
from src.utils.seguridad import verificar_permiso
from src.utils.validaciones import ErrorValidacion


class PacienteServicio:
    def __init__(self, repo=None):
        self.repo = repo or RepositorioMemoria()

    def registrar(self, actor, **datos) -> Paciente:
        verificar_permiso(actor, "pacientes:escribir")
        paciente = Paciente(**datos)
        if self.buscar_por_dni(actor, paciente.dni):
            raise ErrorValidacion("Ya existe un paciente con ese DNI.")
        return self.repo.guardar(paciente)

    def buscar_por_dni(self, actor, dni):
        verificar_permiso(actor, "pacientes:leer")
        return next((p for p in self.repo.listar() if p.dni == dni), None)

    def obtener(self, actor, paciente_id) -> Paciente:
        verificar_permiso(actor, "pacientes:leer")
        paciente = self.repo.obtener(paciente_id)
        if not paciente:
            raise ErrorValidacion("Paciente no encontrado.")
        return paciente

    def listar(self, actor):
        verificar_permiso(actor, "pacientes:leer")
        return self.repo.listar()

    def actualizar(self, actor, paciente_id, **cambios) -> Paciente:
        verificar_permiso(actor, "pacientes:escribir")
        actual = self.obtener(actor, paciente_id)
        datos = {**vars(actual), **cambios}
        nuevo = Paciente(**datos)  # revalida todo
        return self.repo.guardar(nuevo)

    def eliminar(self, actor, paciente_id) -> None:
        verificar_permiso(actor, "pacientes:escribir")
        if not self.repo.eliminar(paciente_id):
            raise ErrorValidacion("Paciente no encontrado.")
