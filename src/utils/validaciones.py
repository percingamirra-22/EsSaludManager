"""Validaciones de datos de entrada (DNI, correo, teléfono, fechas, etc.)."""
import re
from datetime import date, datetime


class ErrorValidacion(ValueError):
    """Se lanza cuando un dato no cumple las reglas de negocio."""


def validar_dni(dni: str) -> str:
    dni = str(dni).strip()
    if not re.fullmatch(r"\d{8}", dni):
        raise ErrorValidacion("El DNI debe tener exactamente 8 dígitos.")
    return dni


def validar_nombre(valor: str, campo: str = "Nombre") -> str:
    valor = str(valor).strip()
    if len(valor) < 2 or not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñÜü' ]+", valor):
        raise ErrorValidacion(f"{campo} inválido: solo letras, mínimo 2 caracteres.")
    return valor


def validar_email(email: str) -> str:
    email = str(email).strip().lower()
    if not re.fullmatch(r"[\w.+-]+@[\w-]+(\.[\w-]+)+", email):
        raise ErrorValidacion("Correo electrónico inválido.")
    return email


def validar_telefono(telefono: str) -> str:
    telefono = re.sub(r"[\s-]", "", str(telefono))
    if not re.fullmatch(r"9\d{8}", telefono):
        raise ErrorValidacion("El teléfono debe tener 9 dígitos y empezar con 9.")
    return telefono


def validar_username(username: str) -> str:
    username = str(username).strip()
    if not re.fullmatch(r"[A-Za-z0-9_.]{4,20}", username):
        raise ErrorValidacion("Usuario: 4 a 20 caracteres (letras, números, _ o .).")
    return username


def validar_password(password: str) -> str:
    if (len(password) < 8 or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)):
        raise ErrorValidacion("La contraseña debe tener mínimo 8 caracteres, letras y números.")
    return password


def validar_cmp(cmp_: str) -> str:
    cmp_ = str(cmp_).strip()
    if not re.fullmatch(r"\d{5,6}", cmp_):
        raise ErrorValidacion("El CMP debe tener 5 o 6 dígitos.")
    return cmp_


def validar_fecha_nacimiento(fecha: date) -> date:
    if not isinstance(fecha, date) or fecha > date.today():
        raise ErrorValidacion("La fecha de nacimiento no puede ser futura.")
    if (date.today() - fecha).days > 120 * 365:
        raise ErrorValidacion("La fecha de nacimiento no es realista.")
    return fecha


def validar_fecha_cita(fecha_hora: datetime) -> datetime:
    if not isinstance(fecha_hora, datetime) or fecha_hora <= datetime.now():
        raise ErrorValidacion("La cita debe programarse en una fecha y hora futura.")
    return fecha_hora
