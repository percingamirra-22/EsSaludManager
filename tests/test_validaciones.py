import unittest
from datetime import date, datetime, timedelta

from src.utils import validaciones as v


class TestValidaciones(unittest.TestCase):
    def test_dni(self):
        self.assertEqual(v.validar_dni(" 12345678 "), "12345678")
        for malo in ["1234567", "123456789", "abcdefgh", "", "1234 678"]:
            with self.subTest(dni=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_dni(malo)

    def test_nombre(self):
        self.assertEqual(v.validar_nombre("José Ñandú"), "José Ñandú")
        for malo in ["A", "", "Ana123", "Ana@"]:
            with self.subTest(nombre=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_nombre(malo)

    def test_email(self):
        self.assertEqual(v.validar_email(" ANA@Mail.COM "), "ana@mail.com")
        for malo in ["ana", "ana@", "@mail.com", "ana@mail", "ana mail@x.com"]:
            with self.subTest(email=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_email(malo)

    def test_telefono(self):
        self.assertEqual(v.validar_telefono("987 654-321"), "987654321")
        for malo in ["887654321", "98765432", "9876543210", "abc"]:
            with self.subTest(tel=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_telefono(malo)

    def test_username(self):
        self.assertEqual(v.validar_username("admin_01"), "admin_01")
        for malo in ["abc", "a" * 21, "con espacio", "raro$"]:
            with self.subTest(user=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_username(malo)

    def test_password(self):
        self.assertEqual(v.validar_password("Clave1234"), "Clave1234")
        for malo in ["corta1", "sololetras", "12345678"]:
            with self.subTest(pw=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_password(malo)

    def test_cmp(self):
        self.assertEqual(v.validar_cmp("12345"), "12345")
        self.assertEqual(v.validar_cmp("123456"), "123456")
        for malo in ["1234", "1234567", "abcde"]:
            with self.subTest(cmp=malo), self.assertRaises(v.ErrorValidacion):
                v.validar_cmp(malo)

    def test_fecha_nacimiento(self):
        self.assertEqual(v.validar_fecha_nacimiento(date(1990, 1, 1)), date(1990, 1, 1))
        with self.assertRaises(v.ErrorValidacion):
            v.validar_fecha_nacimiento(date.today() + timedelta(days=1))
        with self.assertRaises(v.ErrorValidacion):
            v.validar_fecha_nacimiento(date(1800, 1, 1))
        with self.assertRaises(v.ErrorValidacion):
            v.validar_fecha_nacimiento("1990-01-01")

    def test_fecha_cita(self):
        futura = datetime.now() + timedelta(hours=1)
        self.assertEqual(v.validar_fecha_cita(futura), futura)
        with self.assertRaises(v.ErrorValidacion):
            v.validar_fecha_cita(datetime.now() - timedelta(minutes=1))
        with self.assertRaises(v.ErrorValidacion):
            v.validar_fecha_cita(date.today())


if __name__ == "__main__":
    unittest.main()
