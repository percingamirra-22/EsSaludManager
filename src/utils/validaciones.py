"""
Validaciones reutilizables para EsSaludManager.

Este módulo no accede a la base de datos ni a la interfaz gráfica.
Sus funciones validan datos de entrada y lanzan ValueError cuando
una regla de negocio o formato no se cumple.
"""

import re
from datetime import date, datetime, time
from typing import Final
from zoneinfo import ZoneInfo

TIPOS_DOCUMENTO: Final[frozenset[str]] = frozenset({"DNI", "CE", "PAS"})
SEXOS: Final[frozenset[str]] = frozenset({"M", "F", "O"})
TIPOS_SEGURO: frozenset[str] = frozenset({"EsSalud", "Privado"})
ESTADOS_CITA: Final[frozenset[str]] = frozenset(
    {"programada", "completada", "cancelada", "reprogramada"}
)
ESTADOS_HISTORIAL: Final[frozenset[str]] = frozenset(
    {"activo", "cerrado", "desactivado"}
)
TIPOS_ENTRADA_HISTORIAL: Final[frozenset[str]] = frozenset(
    {"nota", "diagnóstico", "tratamiento", "examen", "receta"}
)
TIPOS_MOVIMIENTO_MEDICAMENTO: Final[frozenset[str]] = frozenset(
    {"entrada", "salida", "ajuste"}
)
METODOS_PAGO: Final[frozenset[str]] = frozenset(
    {"efectivo", "tarjeta", "transferencia"}
)

_PATRON_DNI: Final[re.Pattern[str]] = re.compile(r"^\d{8}$")
_PATRON_CE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9]{9,12}$")
_PATRON_PASAPORTE: Final[re.Pattern[str]] = re.compile(r"^[A-Za-z0-9]{6,12}$")
_PATRON_RUC: Final[re.Pattern[str]] = re.compile(r"^\d{11}$")
_PATRON_EMAIL: Final[re.Pattern[str]] = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)
_PATRON_TELEFONO: Final[re.Pattern[str]] = re.compile(
    r"^(?:\+51\s?)?(?:9\d{8}|[1-9]\d{5,8})$"
)


def validar_no_vacio(valor: str, nombre_campo: str) -> str:
    """
    Valida que un texto contenga información no vacía.

    Args:
        valor: Texto a validar.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        El valor limpio, sin espacios al inicio ni al final.

    Raises:
        ValueError: Si el valor está vacío o solo contiene espacios.
    """
    valor_limpio = valor.strip()

    if not valor_limpio:
        raise ValueError(f"El campo '{nombre_campo}' es obligatorio.")

    return valor_limpio


def validar_dominio(
    valor: str,
    valores_permitidos: frozenset[str],
    nombre_campo: str,
) -> str:
    """
    Valida que un valor pertenezca a un dominio permitido.

    Args:
        valor: Valor a validar.
        valores_permitidos: Conjunto de valores admitidos.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        El valor validado.

    Raises:
        ValueError: Si el valor no pertenece al dominio permitido.
    """
    if valor not in valores_permitidos:
        permitidos = ", ".join(sorted(valores_permitidos))
        raise ValueError(
            f"Valor inválido para '{nombre_campo}': '{valor}'. "
            f"Valores permitidos: {permitidos}."
        )

    return valor


def validar_documento(tipo_documento: str, numero_documento: str) -> str:
    """
    Valida un documento según su tipo: DNI, CE o PAS.

    Args:
        tipo_documento: Tipo de documento.
        numero_documento: Número o código del documento.

    Returns:
        El documento limpio y en mayúsculas cuando corresponde.

    Raises:
        ValueError: Si el tipo o el formato del documento no es válido.
    """
    tipo_limpio = validar_dominio(
        tipo_documento.strip().upper(),
        TIPOS_DOCUMENTO,
        "tipo_documento",
    )
    documento = validar_no_vacio(numero_documento, "numero_documento").upper()

    patrones = {
        "DNI": _PATRON_DNI,
        "CE": _PATRON_CE,
        "PAS": _PATRON_PASAPORTE,
    }

    if not patrones[tipo_limpio].fullmatch(documento):
        mensajes = {
            "DNI": "El DNI debe contener exactamente 8 dígitos.",
            "CE": "El CE debe contener entre 9 y 12 caracteres alfanuméricos.",
            "PAS": (
                "El pasaporte debe contener entre 6 y 12 caracteres alfanuméricos."
            ),
        }
        raise ValueError(mensajes[tipo_limpio])

    return documento


def validar_ruc(ruc: str) -> str:
    """
    Valida el formato básico de un RUC peruano.

    Nota:
        Verifica que tenga 11 dígitos. No realiza consulta a SUNAT.

    Args:
        ruc: Número de RUC.

    Returns:
        El RUC validado.

    Raises:
        ValueError: Si el RUC no tiene 11 dígitos.
    """
    ruc_limpio = validar_no_vacio(ruc, "ruc")

    if not _PATRON_RUC.fullmatch(ruc_limpio):
        raise ValueError("El RUC debe contener exactamente 11 dígitos.")

    return ruc_limpio


def validar_email(email: str | None) -> str | None:
    """
    Valida un correo electrónico opcional.

    Args:
        email: Correo a validar o None.

    Returns:
        El correo limpio en minúsculas o None si no se proporcionó.

    Raises:
        ValueError: Si el formato del correo es inválido.
    """
    if email is None or not email.strip():
        return None

    email_limpio = email.strip().lower()

    if not _PATRON_EMAIL.fullmatch(email_limpio):
        raise ValueError("El correo electrónico no tiene un formato válido.")

    return email_limpio


def validar_telefono(telefono: str | None) -> str | None:
    """
    Valida un teléfono peruano opcional.

    Admite celular de nueve dígitos, teléfono fijo y prefijo +51.

    Args:
        telefono: Teléfono a validar o None.

    Returns:
        Teléfono normalizado o None si no se proporcionó.

    Raises:
        ValueError: Si el formato no es válido.
    """
    if telefono is None or not telefono.strip():
        return None

    telefono_limpio = re.sub(r"[\s()-]", "", telefono)

    if not _PATRON_TELEFONO.fullmatch(telefono_limpio):
        raise ValueError("El teléfono no tiene un formato peruano válido.")

    return telefono_limpio


def validar_fecha_no_futura(fecha: date, nombre_campo: str) -> date:
    """
    Valida que una fecha no sea posterior a la fecha actual.

    Args:
        fecha: Fecha a validar.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        La fecha validada.

    Raises:
        ValueError: Si la fecha es futura.
    """
    fecha_actual = datetime.now(ZoneInfo("America/Lima")).date()

    if fecha > fecha_actual:
        raise ValueError(f"El campo '{nombre_campo}' no puede ser una fecha futura.")

    return fecha


def validar_rango_fechas(
    fecha_inicio: date | datetime,
    fecha_fin: date | datetime | None,
    nombre_inicio: str = "fecha_inicio",
    nombre_fin: str = "fecha_fin",
) -> None:
    """
    Valida que una fecha final no sea anterior a la fecha inicial.

    Args:
        fecha_inicio: Inicio del período.
        fecha_fin: Fin del período; puede ser None para períodos vigentes.
        nombre_inicio: Etiqueta del inicio.
        nombre_fin: Etiqueta del fin.

    Raises:
        ValueError: Si la fecha final es anterior a la inicial.
    """
    if fecha_fin is not None and fecha_fin < fecha_inicio:
        raise ValueError(f"'{nombre_fin}' no puede ser anterior a '{nombre_inicio}'.")


def validar_intervalo_horario(
    fecha_inicio: datetime,
    fecha_fin: datetime,
) -> None:
    """
    Valida que un intervalo de cita o examen sea coherente.

    Args:
        fecha_inicio: Fecha y hora de inicio.
        fecha_fin: Fecha y hora de fin.

    Raises:
        ValueError: Si el fin no es posterior al inicio.
    """
    if fecha_fin <= fecha_inicio:
        raise ValueError(
            "La fecha y hora de fin debe ser posterior a la fecha y hora de inicio."
        )


def validar_horario(
    hora_inicio: time,
    hora_fin: time,
) -> None:
    """
    Valida que una hora final sea posterior a una hora inicial.

    Args:
        hora_inicio: Hora de inicio.
        hora_fin: Hora de fin.

    Raises:
        ValueError: Si el horario no es válido.
    """
    if hora_fin <= hora_inicio:
        raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")


def validar_entero_no_negativo(
    valor: int,
    nombre_campo: str,
) -> int:
    """
    Valida que un entero sea mayor o igual a cero.

    Args:
        valor: Entero a validar.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        El entero validado.

    Raises:
        ValueError: Si es negativo.
    """
    if valor < 0:
        raise ValueError(f"El campo '{nombre_campo}' no puede ser negativo.")

    return valor


def validar_entero_positivo(
    valor: int,
    nombre_campo: str,
) -> int:
    """
    Valida que un entero sea mayor que cero.

    Args:
        valor: Entero a validar.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        El entero validado.

    Raises:
        ValueError: Si es cero o negativo.
    """
    if valor <= 0:
        raise ValueError(f"El campo '{nombre_campo}' debe ser mayor que cero.")

    return valor


def validar_numero_en_rango(
    valor: float,
    minimo: float,
    maximo: float,
    nombre_campo: str,
) -> float:
    """
    Valida que un número esté dentro de un rango inclusivo.

    Args:
        valor: Número a validar.
        minimo: Límite mínimo.
        maximo: Límite máximo.
        nombre_campo: Nombre descriptivo del campo.

    Returns:
        El número validado.

    Raises:
        ValueError: Si está fuera del rango.
    """
    if not minimo <= valor <= maximo:
        raise ValueError(
            f"El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}."
        )

    return valor
