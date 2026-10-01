from src.modelos import Medico
from src.servicios.repositorio import RepositorioMemoria
from src.utils.seguridad import verificar_permiso
from src.utils.validaciones import ErrorValidacion


class MedicoServicio:
    def __init__(self, repo=None):
        self.repo = repo or RepositorioMemoria()

    def registrar(self, actor, **datos) -> Medico:
        verificar_permiso(actor, "medicos:escribir")
        medico = Medico(**datos)
        if any(m.cmp == medico.cmp for m in self.repo.listar()):
            raise ErrorValidacion("Ya existe un médico con ese CMP.")
        return self.repo.guardar(medico)

    def obtener(self, actor, medico_id) -> Medico:
        verificar_permiso(actor, "medicos:leer")
        medico = self.repo.obtener(medico_id)
        if not medico:
            raise ErrorValidacion("Médico no encontrado.")
        return medico

    def listar(self, actor, especialidad=None):
        verificar_permiso(actor, "medicos:leer")
        medicos = self.repo.listar()
        if especialidad:
            medicos = [m for m in medicos
                       if m.especialidad.lower() == especialidad.strip().lower()]
        return medicos

    def eliminar(self, actor, medico_id) -> None:
        verificar_permiso(actor, "medicos:escribir")
        if not self.repo.eliminar(medico_id):
            raise ErrorValidacion("Médico no encontrado.")
