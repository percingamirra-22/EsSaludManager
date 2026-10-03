import unittest

from src.modelos import Usuario
from src.utils.seguridad import (
    PERMISOS,
    PermisoDenegado,
    Rol,
    hash_password,
    tiene_permiso,
    verificar_password,
    verificar_permiso,
)


class TestHash(unittest.TestCase):
    def test_hash_correcto_e_incorrecto(self):
        h = hash_password("Clave1234")
        self.assertTrue(verificar_password("Clave1234", h))
        self.assertFalse(verificar_password("clave1234", h))

    def test_hash_no_guarda_texto_plano(self):
        self.assertNotIn("Clave1234", hash_password("Clave1234"))

    def test_sal_distinta_en_cada_hash(self):
        self.assertNotEqual(hash_password("Clave1234"), hash_password("Clave1234"))

    def test_hash_malformado(self):
        for raro in ["", "abc", "a$b$c$d", None]:
            with self.subTest(h=raro):
                self.assertFalse(verificar_password("x", raro))


class TestRBAC(unittest.TestCase):
    def _u(self, rol, activo=True):
        return Usuario("usuario01", "hash", rol, activo)

    def test_admin_tiene_todos_los_permisos(self):
        todos = set().union(*PERMISOS.values())
        for p in todos:
            self.assertTrue(tiene_permiso(Rol.ADMIN, p), p)

    def test_medico_solo_atiende(self):
        self.assertTrue(tiene_permiso(Rol.MEDICO, "citas:atender"))
        self.assertFalse(tiene_permiso(Rol.MEDICO, "citas:agendar"))
        self.assertFalse(tiene_permiso(Rol.MEDICO, "pacientes:escribir"))

    def test_admision_no_administra_usuarios(self):
        self.assertFalse(tiene_permiso(Rol.ADMISION, "usuarios:administrar"))
        self.assertTrue(tiene_permiso(Rol.ADMISION, "citas:agendar"))

    def test_verificar_permiso(self):
        verificar_permiso(self._u(Rol.ADMIN), "usuarios:administrar")
        with self.assertRaises(PermisoDenegado):
            verificar_permiso(self._u(Rol.MEDICO), "usuarios:administrar")

    def test_usuario_inactivo_o_none(self):
        with self.assertRaises(PermisoDenegado):
            verificar_permiso(self._u(Rol.ADMIN, activo=False), "pacientes:leer")
        with self.assertRaises(PermisoDenegado):
            verificar_permiso(None, "pacientes:leer")


if __name__ == "__main__":
    unittest.main()
