from src.modelos import Cita, EstadoCita
from src.servicios.repositorio import RepositorioMemoria
from src.utils.seguridad import verificar_permiso
from src.utils.validaciones import ErrorValidacion, validar_fecha_cita


class CitaServicio:
    def __init__(self, paciente_servicio, medico_servicio, repo=None):
        self.pacientes = paciente_servicio
        self.medicos = medico_servicio
        self.repo = repo or RepositorioMemoria()

    def agendar(self, actor, paciente_id, medico_id, fecha_hora, motivo) -> Cita:
        verificar_permiso(actor, "citas:agendar")
        self.pacientes.obtener(actor, paciente_id)   # lanza error si no existe
        self.medicos.obtener(actor, medico_id)
        validar_fecha_cita(fecha_hora)
        if not str(motivo).strip():
            raise ErrorValidacion("El motivo de la cita es obligatorio.")
        if any(c.medico_id == medico_id and c.fecha_hora == fecha_hora
               and c.estado != EstadoCita.CANCELADA for c in self.repo.listar()):
            raise ErrorValidacion("El médico ya tiene una cita en ese horario.")
        return self.repo.guardar(Cita(paciente_id, medico_id, fecha_hora, motivo.strip()))

    def _obtener(self, cita_id) -> Cita:
        cita = self.repo.obtener(cita_id)
        if not cita:
            raise ErrorValidacion("Cita no encontrada.")
        return cita

    def _cambiar(self, actor, permiso, cita_id, estado) -> Cita:
        verificar_permiso(actor, permiso)
        cita = self._obtener(cita_id)
        try:
            cita.cambiar_estado(estado)
        except ValueError as e:
            raise ErrorValidacion(str(e))
        return cita

    def confirmar(self, actor, cita_id):
        return self._cambiar(actor, "citas:gestionar", cita_id, EstadoCita.CONFIRMADA)

    def cancelar(self, actor, cita_id):
        return self._cambiar(actor, "citas:gestionar", cita_id, EstadoCita.CANCELADA)

    def atender(self, actor, cita_id):
        return self._cambiar(actor, "citas:atender", cita_id, EstadoCita.ATENDIDA)

    def listar(self, actor, paciente_id=None, medico_id=None):
        verificar_permiso(actor, "citas:leer")
        citas = self.repo.listar()
        if paciente_id:
            citas = [c for c in citas if c.paciente_id == paciente_id]
        if medico_id:
            citas = [c for c in citas if c.medico_id == medico_id]
        return sorted(citas, key=lambda c: c.fecha_hora)
