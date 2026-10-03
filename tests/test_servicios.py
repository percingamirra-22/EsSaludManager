import unittest
from datetime import date, datetime, timedelta

from src.servicios import AuthServicio, CitaServicio, MedicoServicio, PacienteServicio
from src.utils.seguridad import PermisoDenegado, Rol
from src.utils.validaciones import ErrorValidacion

DATOS_PAC = dict(
    dni="12345678",
    nombres="Ana",
    apellidos="Quispe",
    fecha_nacimiento=date(1990, 5, 1),
    telefono="987654321",
    email="ana@mail.com",
)
DATOS_MED = dict(
    cmp="12345", nombres="Luis", apellidos="Rojas", especialidad="Cardiologia"
)


class Base(unittest.TestCase):
    def setUp(self):
        self.auth = AuthServicio()
        self.admin = self.auth.registrar_usuario(
            None, "admin01", "Clave1234", Rol.ADMIN
        )
        self.adm = self.auth.registrar_usuario(
            self.admin, "admision1", "Clave1234", Rol.ADMISION
        )
        self.doc = self.auth.registrar_usuario(
            self.admin, "doctor01", "Clave1234", Rol.MEDICO
        )
        self.pacs = PacienteServicio()
        self.meds = MedicoServicio()
        self.citas = CitaServicio(self.pacs, self.meds)
        self.p = self.pacs.registrar(self.admin, **DATOS_PAC)
        self.m = self.meds.registrar(self.admin, **DATOS_MED)
        self.fecha = datetime.now() + timedelta(days=2)


class TestAuth(Base):
    def test_primer_usuario_es_admin(self):
        self.assertEqual(self.admin.rol, Rol.ADMIN)

    def test_solo_admin_crea_usuarios(self):
        with self.assertRaises(PermisoDenegado):
            self.auth.registrar_usuario(self.doc, "otro_user", "Clave1234", Rol.MEDICO)
        with self.assertRaises(PermisoDenegado):
            self.auth.registrar_usuario(None, "otro_user", "Clave1234", Rol.MEDICO)

    def test_username_duplicado_y_password_debil(self):
        with self.assertRaises(ErrorValidacion):
            self.auth.registrar_usuario(self.admin, "admin01", "Clave1234", Rol.MEDICO)
        with self.assertRaises(ErrorValidacion):
            self.auth.registrar_usuario(self.admin, "nuevo01", "debil", Rol.MEDICO)

    def test_login_ok_y_fallos(self):
        self.assertEqual(self.auth.login("doctor01", "Clave1234").id, self.doc.id)
        with self.assertRaises(ErrorValidacion):
            self.auth.login("doctor01", "incorrecta1")
        with self.assertRaises(ErrorValidacion):
            self.auth.login("noexiste", "Clave1234")

    def test_password_no_se_guarda_en_claro(self):
        self.assertNotIn("Clave1234", self.admin.password_hash)

    def test_desactivar_usuario_bloquea_login(self):
        self.auth.desactivar_usuario(self.admin, self.doc.id)
        with self.assertRaises(ErrorValidacion):
            self.auth.login("doctor01", "Clave1234")
        with self.assertRaises(ErrorValidacion):
            self.auth.desactivar_usuario(self.admin, 999)


class TestPacienteServicio(Base):
    def test_registrar_y_buscar(self):
        self.assertEqual(self.pacs.buscar_por_dni(self.doc, "12345678").id, self.p.id)
        self.assertIsNone(self.pacs.buscar_por_dni(self.doc, "00000000"))

    def test_dni_duplicado(self):
        with self.assertRaises(ErrorValidacion):
            self.pacs.registrar(self.admin, **DATOS_PAC)

    def test_permisos(self):
        with self.assertRaises(PermisoDenegado):
            self.pacs.registrar(self.doc, **{**DATOS_PAC, "dni": "87654321"})
        with self.assertRaises(PermisoDenegado):
            self.pacs.listar(None)

    def test_actualizar_revalida(self):
        act = self.pacs.actualizar(self.adm, self.p.id, telefono="911111111")
        self.assertEqual(act.telefono, "911111111")
        with self.assertRaises(ErrorValidacion):
            self.pacs.actualizar(self.adm, self.p.id, email="malo")

    def test_eliminar(self):
        self.pacs.eliminar(self.admin, self.p.id)
        with self.assertRaises(ErrorValidacion):
            self.pacs.obtener(self.admin, self.p.id)
        with self.assertRaises(ErrorValidacion):
            self.pacs.eliminar(self.admin, self.p.id)


class TestMedicoServicio(Base):
    def test_cmp_duplicado(self):
        with self.assertRaises(ErrorValidacion):
            self.meds.registrar(self.admin, **DATOS_MED)

    def test_solo_admin_registra(self):
        with self.assertRaises(PermisoDenegado):
            self.meds.registrar(self.adm, **{**DATOS_MED, "cmp": "54321"})

    def test_filtrar_por_especialidad(self):
        self.meds.registrar(
            self.admin, **{**DATOS_MED, "cmp": "54321", "especialidad": "Pediatria"}
        )
        self.assertEqual(len(self.meds.listar(self.doc)), 2)
        self.assertEqual(len(self.meds.listar(self.doc, "cardiologia")), 1)

    def test_obtener_y_eliminar(self):
        self.assertEqual(self.meds.obtener(self.doc, self.m.id).cmp, "12345")
        self.meds.eliminar(self.admin, self.m.id)
        with self.assertRaises(ErrorValidacion):
            self.meds.obtener(self.doc, self.m.id)


class TestCitaServicio(Base):
    def _agendar(self, fecha=None):
        return self.citas.agendar(
            self.adm, self.p.id, self.m.id, fecha or self.fecha, "Control"
        )

    def test_agendar_ok(self):
        c = self._agendar()
        self.assertEqual(c.estado.value, "programada")

    def test_rechaza_datos_invalidos(self):
        with self.assertRaises(ErrorValidacion):
            self.citas.agendar(self.adm, 999, self.m.id, self.fecha, "x")  # paciente
        with self.assertRaises(ErrorValidacion):
            self.citas.agendar(self.adm, self.p.id, 999, self.fecha, "x")  # médico
        with self.assertRaises(ErrorValidacion):
            self.citas.agendar(
                self.adm, self.p.id, self.m.id, datetime.now() - timedelta(days=1), "x"
            )  # pasado
        with self.assertRaises(ErrorValidacion):
            self.citas.agendar(
                self.adm, self.p.id, self.m.id, self.fecha, "  "
            )  # motivo

    def test_medico_no_puede_agendar(self):
        with self.assertRaises(PermisoDenegado):
            self.citas.agendar(self.doc, self.p.id, self.m.id, self.fecha, "x")

    def test_choque_y_liberacion_de_horario(self):
        c = self._agendar()
        with self.assertRaises(ErrorValidacion):
            self._agendar()
        self.citas.cancelar(self.adm, c.id)
        self._agendar()  # tras cancelar, el horario vuelve a estar libre

    def test_flujo_completo_y_permisos(self):
        c = self._agendar()
        with self.assertRaises(PermisoDenegado):
            self.citas.confirmar(self.doc, c.id)
        self.citas.confirmar(self.adm, c.id)
        with self.assertRaises(PermisoDenegado):
            self.citas.atender(self.adm, c.id)
        self.citas.atender(self.doc, c.id)
        with self.assertRaises(ErrorValidacion):
            self.citas.cancelar(self.adm, c.id)

    def test_atender_sin_confirmar_falla(self):
        c = self._agendar()
        with self.assertRaises(ErrorValidacion):
            self.citas.atender(self.doc, c.id)

    def test_cita_inexistente(self):
        with self.assertRaises(ErrorValidacion):
            self.citas.confirmar(self.adm, 999)

    def test_listar_filtrado_y_ordenado(self):
        tarde = self._agendar(self.fecha + timedelta(hours=3))
        temprano = self._agendar()
        todas = self.citas.listar(self.doc)
        self.assertEqual([c.id for c in todas], [temprano.id, tarde.id])
        self.assertEqual(self.citas.listar(self.doc, paciente_id=999), [])


if __name__ == "__main__":
    unittest.main()
