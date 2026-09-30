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

Uso:
    from src.repositorios import PacienteRepository, db

    repo = PacienteRepository()
    paciente = repo.find_by_id(1)
"""

from .auditoria_repository import AuditoriaRepository
from .base_repository import BaseRepository
from .cita_repository import CitaRepository
from .historial_repository import HistorialRepository
from .medicamento_repository import MedicamentoRepository
from .paciente_repository import PacienteRepository
from .usuario_repository import UsuarioRepository

__all__ = [
    "AuditoriaRepository",
    "BaseRepository",
    "CitaRepository",
    "HistorialRepository",
    "MedicamentoRepository",
    "PacienteRepository",
    "UsuarioRepository",
]
