"""
Módulo de repositorios de EsSaludManager.

Contiene los repositorios para acceso a datos de cada entidad:
- BaseRepository: Clase base abstracta con CRUD genérico.
- PacienteRepository: Repositorio para Paciente.
- HistorialRepository: Repositorio para HistorialClinico.
- CitaRepository: Repositorio para Cita.
- MedicamentoRepository: Repositorio para Medicamento.
- UsuarioRepository: Repositorio para Usuario.
- AuditoriaRepository: Repositorio para Auditoria.
- CoberturaRepository: Repositorio para Cobertura.
- FacturaRepository: Repositorio para Factura.
- LoteMedicamentoRepository: Repositorio para LoteMedicamento.
- MovimientoMedicamentoRepository: Repositorio para MovimientoMedicamento.
- RecetaRepository: Repositorio para Receta.

Uso:
    from src.repositorios import PacienteRepository, db

    repo = PacienteRepository()
    paciente = repo.find_by_id(1)
"""

from .auditoria_repository import AuditoriaRepository
from .base_repository import BaseRepository
from .cita_repository import CitaRepository
from .cobertura_repository import CoberturaRepository
from .examen_medico_repository import ExamenMedicoRepository
from .factura_repository import FacturaRepository
from .historial_repository import HistorialRepository
from .lote_medicamento_repository import LoteMedicamentoRepository
from .medicamento_repository import MedicamentoRepository
from .movimiento_medicamento_repository import MovimientoMedicamentoRepository
from .notificacion_repository import NotificacionRepository
from .orden_examen_repository import OrdenExamenRepository
from .paciente_repository import PacienteRepository
from .receta_repository import RecetaRepository
from .reporte_repository import ReporteRepository
from .seguro_repository import SeguroRepository
from .usuario_repository import UsuarioRepository

__all__ = [
    "AuditoriaRepository",
    "BaseRepository",
    "CitaRepository",
    "CoberturaRepository",
    "ExamenMedicoRepository",
    "FacturaRepository",
    "HistorialRepository",
    "LoteMedicamentoRepository",
    "MedicamentoRepository",
    "MovimientoMedicamentoRepository",
    "NotificacionRepository",
    "OrdenExamenRepository",
    "PacienteRepository",
    "RecetaRepository",
    "ReporteRepository",
    "SeguroRepository",
    "UsuarioRepository",
]
