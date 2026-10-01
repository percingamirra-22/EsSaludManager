import unittest
from datetime import date, datetime, timedelta

from src.modelos import Cita, EstadoCita, Medico, Paciente, Usuario
from src.utils.seguridad import Rol
from src.utils.validaciones import ErrorValidacion


def paciente(**kw):
    datos = dict(
        dni="12345678",
        nombres="Ana",
        apellidos="Quispe",
        fecha_nacimiento=date(1990, 5, 1),
        telefono="987654321",
        email="ana@mail.com",
    )
    datos.update(kw)
    return Paciente(**datos)


class TestPaciente(unittest.TestCase):
    def test_creacion_valida(self):
        p = paciente()
        self.assertEqual(p.nombre_completo, "Ana Quispe")

    def test_edad(self):
        nac = date.today().replace(year=date.today().year - 30)
        self.assertEqual(paciente(fecha_nacimiento=nac).edad, 30)

    def test_datos_invalidos(self):
        for campo, valor in [
            ("dni", "123"),
            ("telefono", "123"),
            ("email", "x"),
            ("nombres", "1"),
        ]:
            with self.subTest(campo=campo), self.assertRaises(ErrorValidacion):
                paciente(**{campo: valor})


class TestMedico(unittest.TestCase):
    def test_creacion_y_nombre(self):
        m = Medico("12345", "Luis", "Rojas", "Cardiologia")
        self.assertEqual(m.nombre_completo, "Dr(a). Luis Rojas")

    def test_cmp_invalido(self):
        with self.assertRaises(ErrorValidacion):
            Medico("12", "Luis", "Rojas", "Cardiologia")


class TestUsuario(unittest.TestCase):
    def test_rol_se_convierte_a_enum(self):
        self.assertIs(Usuario("admin01", "h", "admin").rol, Rol.ADMIN)

    def test_rol_invalido(self):
        with self.assertRaises(ValueError):
            Usuario("admin01", "h", "superman")


class TestCita(unittest.TestCase):
    def _cita(self):
        return Cita(1, 1, datetime.now() + timedelta(days=1), "Control")

    def test_estado_inicial(self):
        self.assertEqual(self._cita().estado, EstadoCita.PROGRAMADA)

    def test_flujo_valido(self):
        c = self._cita()
        c.cambiar_estado(EstadoCita.CONFIRMADA)
        c.cambiar_estado(EstadoCita.ATENDIDA)
        self.assertEqual(c.estado, EstadoCita.ATENDIDA)

    def test_transiciones_invalidas(self):
        c = self._cita()
        with self.assertRaises(ValueError):
            c.cambiar_estado(EstadoCita.ATENDIDA)  # sin confirmar
        c.cambiar_estado(EstadoCita.CANCELADA)
        with self.assertRaises(ValueError):
            c.cambiar_estado(EstadoCita.CONFIRMADA)  # ya cancelada


if __name__ == "__main__":
    unittest.main()
