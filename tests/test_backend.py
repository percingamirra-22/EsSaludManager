import unittest
from datetime import date, datetime, timedelta

from src.servicios import AuthServicio, CitaServicio, MedicoServicio, PacienteServicio
from src.utils.seguridad import PermisoDenegado, Rol, hash_password, verificar_password
from src.utils.validaciones import ErrorValidacion, validar_dni


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.auth = AuthServicio()
        self.admin = self.auth.registrar_usuario(
            None, "admin01", "Clave1234", Rol.ADMIN
        )
        self.medico_user = self.auth.registrar_usuario(
            self.admin, "doctor01", "Clave1234", Rol.MEDICO
        )
        self.pacs = PacienteServicio()
        self.meds = MedicoServicio()
        self.citas = CitaServicio(self.pacs, self.meds)
        self.p = self.pacs.registrar(
            self.admin,
            dni="12345678",
            nombres="Ana",
            apellidos="Quispe",
            fecha_nacimiento=date(1990, 5, 1),
            telefono="987654321",
            email="ana@mail.com",
        )
        self.m = self.meds.registrar(
            self.admin,
            cmp="12345",
            nombres="Luis",
            apellidos="Rojas",
            especialidad="Cardiologia",
        )
        self.fecha = datetime.now() + timedelta(days=2)

    def test_hash(self):
        h = hash_password("Clave1234")
        self.assertTrue(verificar_password("Clave1234", h))
        self.assertFalse(verificar_password("otra", h))

    def test_login(self):
        self.assertEqual(self.auth.login("admin01", "Clave1234").id, self.admin.id)
        with self.assertRaises(ErrorValidacion):
            self.auth.login("admin01", "mala")

    def test_dni_invalido(self):
        with self.assertRaises(ErrorValidacion):
            validar_dni("123")

    def test_rbac(self):
        with self.assertRaises(PermisoDenegado):
            self.pacs.registrar(
                self.medico_user,
                dni="87654321",
                nombres="Jo",
                apellidos="Paz",
                fecha_nacimiento=date(2000, 1, 1),
                telefono="911111111",
                email="jo@mail.com",
            )

    def test_dni_duplicado(self):
        with self.assertRaises(ErrorValidacion):
            self.pacs.registrar(
                self.admin,
                dni="12345678",
                nombres="Ana",
                apellidos="Quispe",
                fecha_nacimiento=date(1990, 5, 1),
                telefono="987654321",
                email="ana@mail.com",
            )

    def test_flujo_cita(self):
        c = self.citas.agendar(self.admin, self.p.id, self.m.id, self.fecha, "Control")
        self.citas.confirmar(self.admin, c.id)
        self.citas.atender(self.medico_user, c.id)
        with self.assertRaises(ErrorValidacion):
            self.citas.cancelar(self.admin, c.id)

    def test_cita_choque_horario(self):
        self.citas.agendar(self.admin, self.p.id, self.m.id, self.fecha, "Control")
        with self.assertRaises(ErrorValidacion):
            self.citas.agendar(self.admin, self.p.id, self.m.id, self.fecha, "Otro")


if __name__ == "__main__":
    unittest.main()
