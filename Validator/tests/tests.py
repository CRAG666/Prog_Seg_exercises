"""
============================================================
TESTS — Ejercicio: Validador Modular de Formularios
============================================================
Archivo de autocalificación. NO modifiques este archivo.
Ejecutar: python -m unittest discover tests
============================================================
"""

import contextlib
import io
import unittest
from validador import (
    Regla,
    ReglaNoPalabrasProhibidas,
    ReglaLongitud,
    ReglaFormatoEmail,
    ReglaNoEspacios,
    Validador,
)


class TestReglaPalabrasProhibidas(unittest.TestCase):
    def setUp(self):
        self.regla = ReglaNoPalabrasProhibidas()

    def test_texto_limpio_es_valido(self):
        self.assertTrue(self.regla.validar("hola mundo"))

    def test_contiene_admin(self):
        self.assertFalse(self.regla.validar("soy admin del sistema"))

    def test_contiene_root(self):
        self.assertFalse(self.regla.validar("acceso root"))

    def test_contiene_hack(self):
        self.assertFalse(self.regla.validar("voy a hackearte"))

    def test_contiene_drop(self):
        self.assertFalse(self.regla.validar("drop table usuarios"))

    def test_contiene_select(self):
        self.assertFalse(self.regla.validar("select * from tabla"))

    def test_contiene_delete(self):
        self.assertFalse(self.regla.validar("delete all"))

    def test_case_insensitive_mayusculas(self):
        self.assertFalse(self.regla.validar("soy ADMIN"))

    def test_case_insensitive_mixto(self):
        self.assertFalse(self.regla.validar("soy AdMiN"))

    def test_palabra_prohibida_sola(self):
        self.assertFalse(self.regla.validar("admin"))

    def test_texto_sin_palabras_prohibidas(self):
        self.assertTrue(self.regla.validar("usuario normal de prueba"))

    def test_mensaje_error(self):
        self.assertEqual(
            self.regla.mensaje_error(), "El valor contiene palabras prohibidas"
        )


class TestReglaLongitud(unittest.TestCase):
    def test_minimo_negativo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            ReglaLongitud(-1, 10)

    def test_maximo_menor_minimo_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            ReglaLongitud(10, 5)

    def test_longitud_dentro_rango(self):
        regla = ReglaLongitud(3, 10)
        self.assertTrue(regla.validar("hola"))

    def test_longitud_exactamente_minimo(self):
        regla = ReglaLongitud(3, 10)
        self.assertTrue(regla.validar("abc"))

    def test_longitud_exactamente_maximo(self):
        regla = ReglaLongitud(3, 10)
        self.assertTrue(regla.validar("abcdefghij"))

    def test_longitud_menor_que_minimo(self):
        regla = ReglaLongitud(3, 10)
        self.assertFalse(regla.validar("ab"))

    def test_longitud_mayor_que_maximo(self):
        regla = ReglaLongitud(3, 10)
        self.assertFalse(regla.validar("abcdefghijk"))

    def test_longitud_vacia(self):
        regla = ReglaLongitud(1, 10)
        self.assertFalse(regla.validar(""))

    def test_minimo_igual_maximo(self):
        regla = ReglaLongitud(5, 5)
        self.assertTrue(regla.validar("abcde"))
        self.assertFalse(regla.validar("abcd"))
        self.assertFalse(regla.validar("abcdef"))

    def test_mensaje_error(self):
        regla = ReglaLongitud(3, 50)
        self.assertEqual(regla.mensaje_error(), "La longitud debe estar entre 3 y 50")

    def test_mensaje_error_otros_valores(self):
        regla = ReglaLongitud(1, 100)
        self.assertEqual(regla.mensaje_error(), "La longitud debe estar entre 1 y 100")


class TestReglaFormatoEmail(unittest.TestCase):
    def setUp(self):
        self.regla = ReglaFormatoEmail()

    def test_email_valido_basico(self):
        self.assertTrue(self.regla.validar("user@example.com"))

    def test_email_valido_minimo(self):
        self.assertTrue(self.regla.validar("a@b.c"))

    def test_email_valido_con_subdomain(self):
        self.assertTrue(self.regla.validar("user@sub.example.com"))

    def test_email_sin_at(self):
        self.assertFalse(self.regla.validar("userexample.com"))

    def test_email_dos_at(self):
        self.assertFalse(self.regla.validar("user@@example.com"))

    def test_email_sin_usuario(self):
        self.assertFalse(self.regla.validar("@example.com"))

    def test_email_sin_dominio(self):
        self.assertFalse(self.regla.validar("user@"))

    def test_email_sin_punto_en_dominio(self):
        self.assertFalse(self.regla.validar("user@example"))

    def test_email_extension_vacia(self):
        self.assertFalse(self.regla.validar("user@example."))

    def test_email_solo_at(self):
        self.assertFalse(self.regla.validar("@"))

    def test_email_vacio(self):
        self.assertFalse(self.regla.validar(""))

    def test_mensaje_error(self):
        self.assertEqual(self.regla.mensaje_error(), "El formato de email no es válido")


class TestReglaNoEspacios(unittest.TestCase):
    def setUp(self):
        self.regla = ReglaNoEspacios()

    def test_sin_espacios_es_valido(self):
        self.assertTrue(self.regla.validar("sinespacio"))

    def test_con_espacio_en_medio(self):
        self.assertFalse(self.regla.validar("con espacio"))

    def test_con_espacio_al_inicio(self):
        self.assertFalse(self.regla.validar(" inicio"))

    def test_con_espacio_al_final(self):
        self.assertFalse(self.regla.validar("final "))

    def test_solo_espacios(self):
        self.assertFalse(self.regla.validar("   "))

    def test_cadena_vacia_es_valida(self):
        self.assertTrue(self.regla.validar(""))

    def test_mensaje_error(self):
        self.assertEqual(
            self.regla.mensaje_error(), "El valor no puede contener espacios"
        )


class TestHerenciaRegla(unittest.TestCase):
    def test_palabras_prohibidas_es_regla(self):
        self.assertIsInstance(ReglaNoPalabrasProhibidas(), Regla)

    def test_longitud_es_regla(self):
        self.assertIsInstance(ReglaLongitud(1, 10), Regla)

    def test_formato_email_es_regla(self):
        self.assertIsInstance(ReglaFormatoEmail(), Regla)

    def test_no_espacios_es_regla(self):
        self.assertIsInstance(ReglaNoEspacios(), Regla)

    def test_regla_es_abstracta(self):
        with self.assertRaises(TypeError):
            Regla()


class TestValidadorAgregar(unittest.TestCase):
    def setUp(self):
        self.v = Validador()

    def test_agregar_regla_valida(self):
        self.v.agregar_regla(ReglaNoEspacios())
        self.assertEqual(self.v.cantidad_reglas(), 1)

    def test_agregar_no_regla_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            self.v.agregar_regla("no soy regla")

    def test_agregar_none_lanza_typeerror(self):
        with self.assertRaises(TypeError):
            self.v.agregar_regla(None)

    def test_agregar_multiples_reglas(self):
        self.v.agregar_regla(ReglaNoEspacios())
        self.v.agregar_regla(ReglaLongitud(3, 50))
        self.v.agregar_regla(ReglaNoPalabrasProhibidas())
        self.assertEqual(self.v.cantidad_reglas(), 3)

    def test_cantidad_inicial_cero(self):
        self.assertEqual(self.v.cantidad_reglas(), 0)


class TestValidadorUnaRegla(unittest.TestCase):
    def test_una_regla_pasa(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("sinespacio")
        self.assertTrue(resultado["es_valido"])
        self.assertEqual(resultado["errores"], [])

    def test_una_regla_falla(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("con espacio")
        self.assertFalse(resultado["es_valido"])
        self.assertEqual(len(resultado["errores"]), 1)
        self.assertIn("espacios", resultado["errores"][0])


class TestValidadorMultiplesReglas(unittest.TestCase):
    def setUp(self):
        self.v = Validador()
        self.v.agregar_regla(ReglaLongitud(3, 50))
        self.v.agregar_regla(ReglaNoPalabrasProhibidas())
        self.v.agregar_regla(ReglaNoEspacios())

    def test_todas_pasan(self):
        resultado = self.v.validar("holaamigo")
        self.assertTrue(resultado["es_valido"])
        self.assertEqual(resultado["errores"], [])

    def test_una_falla(self):
        # "ab" falla por longitud, pero no tiene palabras prohibidas ni espacios
        resultado = self.v.validar("ab")
        self.assertFalse(resultado["es_valido"])
        self.assertEqual(len(resultado["errores"]), 1)

    def test_dos_fallan(self):
        # "a " tiene longitud 2 (falla longitud) y tiene espacio (falla espacios)
        resultado = self.v.validar("a ")
        self.assertFalse(resultado["es_valido"])
        self.assertEqual(len(resultado["errores"]), 2)

    def test_todas_fallan(self):
        # "root " tiene palabra prohibida (falla), tiene espacio (falla),
        # y con longitud mínimo=7 también falla por longitud
        v = Validador()
        v.agregar_regla(ReglaLongitud(7, 50))
        v.agregar_regla(ReglaNoPalabrasProhibidas())
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("root ")
        self.assertFalse(resultado["es_valido"])
        self.assertEqual(len(resultado["errores"]), 3)

    def test_palabra_prohibida_falla(self):
        resultado = self.v.validar("eseadmin")
        self.assertFalse(resultado["es_valido"])
        self.assertIn("palabras prohibidas", resultado["errores"][0])


class TestValidadorSinReglas(unittest.TestCase):
    def test_sin_reglas_todo_es_valido(self):
        v = Validador()
        resultado = v.validar("cualquier cosa")
        self.assertTrue(resultado["es_valido"])
        self.assertEqual(resultado["errores"], [])


class TestValidadorEstructura(unittest.TestCase):
    def test_retorna_diccionario(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("test")
        self.assertIsInstance(resultado, dict)

    def test_tiene_clave_es_valido(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("test")
        self.assertIn("es_valido", resultado)

    def test_tiene_clave_errores(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("test")
        self.assertIn("errores", resultado)

    def test_errores_es_lista(self):
        v = Validador()
        v.agregar_regla(ReglaNoEspacios())
        resultado = v.validar("test")
        self.assertIsInstance(resultado["errores"], list)


if __name__ == "__main__":
    import __main__

    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
        print(buf.getvalue())
