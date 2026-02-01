"""
============================================================
TESTS — Ejercicio: Sistema de Registro de Eventos
============================================================
Archivo de autocalificación. NO modifiques este archivo.
Ejecutar: python -m unittest discover tests
============================================================
"""

import contextlib
import io
import time
import unittest
from log import Evento, RegistradorSeguro, TIPOS_VALIDOS


class TestEventoValido(unittest.TestCase):
    def test_crear_evento_login(self):
        e = Evento("LOGIN", "Inicio de sesión")
        self.assertEqual(e.get_tipo(), "LOGIN")
        self.assertEqual(e.get_mensaje(), "Inicio de sesión")

    def test_crear_evento_logout(self):
        e = Evento("LOGOUT", "Cierre de sesión")
        self.assertEqual(e.get_tipo(), "LOGOUT")

    def test_crear_evento_error(self):
        e = Evento("ERROR", "Fallo en autenticación")
        self.assertEqual(e.get_tipo(), "ERROR")

    def test_crear_evento_alerta(self):
        e = Evento("ALERTA", "Actividad sospechosa")
        self.assertEqual(e.get_tipo(), "ALERTA")

    def test_timestamp_es_float(self):
        e = Evento("LOGIN", "test")
        self.assertIsInstance(e.get_timestamp(), float)

    def test_timestamp_es_reciente(self):
        antes = time.time()
        e = Evento("LOGIN", "test")
        despues = time.time()
        self.assertGreaterEqual(e.get_timestamp(), antes)
        self.assertLessEqual(e.get_timestamp(), despues)

    def test_todos_tipos_validos_funcionan(self):
        for tipo in TIPOS_VALIDOS:
            e = Evento(tipo, "mensaje de prueba")
            self.assertEqual(e.get_tipo(), tipo)


class TestEventoValidacion(unittest.TestCase):
    def test_tipo_invalido_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("INVALIDO", "mensaje")

    def test_tipo_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("", "mensaje")

    def test_tipo_minuscula_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("login", "mensaje")

    def test_mensaje_vacio_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("LOGIN", "")

    def test_mensaje_solo_espacios_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("LOGIN", "   ")

    def test_mensaje_tabs_lanza_valueerror(self):
        with self.assertRaises(ValueError):
            Evento("LOGIN", "\t\t")


class TestEventoEncapsulamiento(unittest.TestCase):
    def setUp(self):
        self.e = Evento("LOGIN", "test")

    def test_no_acceso_directo_tipo(self):
        self.assertFalse(hasattr(self.e, "tipo"))

    def test_no_acceso_directo_mensaje(self):
        self.assertFalse(hasattr(self.e, "mensaje"))

    def test_no_acceso_directo_timestamp(self):
        self.assertFalse(hasattr(self.e, "timestamp"))


class TestRegistradorRegistro(unittest.TestCase):
    def setUp(self):
        self.reg = RegistradorSeguro()

    def test_registrar_evento_valido(self):
        e = Evento("LOGIN", "test")
        self.assertTrue(self.reg.registrar(e))

    def test_registrar_no_evento_retorna_false(self):
        self.assertFalse(self.reg.registrar("no soy evento"))

    def test_registrar_none_retorna_false(self):
        self.assertFalse(self.reg.registrar(None))

    def test_registrar_int_retorna_false(self):
        self.assertFalse(self.reg.registrar(42))

    def test_registrar_dict_retorna_false(self):
        self.assertFalse(self.reg.registrar({"tipo": "LOGIN"}))

    def test_cantidad_tras_registrar(self):
        self.reg.registrar(Evento("LOGIN", "e1"))
        self.reg.registrar(Evento("ERROR", "e2"))
        self.reg.registrar(Evento("ALERTA", "e3"))
        self.assertEqual(self.reg.cantidad_eventos(), 3)


class TestRegistradorObtener(unittest.TestCase):
    def setUp(self):
        self.reg = RegistradorSeguro()
        self.reg.registrar(Evento("LOGIN", "evento 1"))
        self.reg.registrar(Evento("ERROR", "evento 2"))

    def test_obtener_retorna_lista(self):
        self.assertIsInstance(self.reg.obtener_eventos(), list)

    def test_obtener_cantidad_correcta(self):
        self.assertEqual(len(self.reg.obtener_eventos()), 2)

    def test_obtener_retorna_copia(self):
        eventos = self.reg.obtener_eventos()
        eventos.clear()
        self.assertEqual(self.reg.cantidad_eventos(), 2)


class TestRegistradorFiltro(unittest.TestCase):
    def setUp(self):
        self.reg = RegistradorSeguro()
        self.reg.registrar(Evento("LOGIN", "login 1"))
        self.reg.registrar(Evento("LOGIN", "login 2"))
        self.reg.registrar(Evento("ERROR", "error 1"))
        self.reg.registrar(Evento("ALERTA", "alerta 1"))
        self.reg.registrar(Evento("LOGOUT", "logout 1"))

    def test_filtrar_login(self):
        resultado = self.reg.filtrar_por_tipo("LOGIN")
        self.assertEqual(len(resultado), 2)

    def test_filtrar_error(self):
        resultado = self.reg.filtrar_por_tipo("ERROR")
        self.assertEqual(len(resultado), 1)

    def test_filtrar_tipo_sin_eventos(self):
        reg2 = RegistradorSeguro()
        reg2.registrar(Evento("LOGIN", "solo login"))
        resultado = reg2.filtrar_por_tipo("ERROR")
        self.assertEqual(len(resultado), 0)

    def test_filtrar_retorna_eventos_correctos(self):
        resultado = self.reg.filtrar_por_tipo("ALERTA")
        self.assertEqual(resultado[0].get_mensaje(), "alerta 1")

    def test_cantidad_por_tipo_login(self):
        self.assertEqual(self.reg.cantidad_por_tipo("LOGIN"), 2)

    def test_cantidad_por_tipo_error(self):
        self.assertEqual(self.reg.cantidad_por_tipo("ERROR"), 1)

    def test_cantidad_por_tipo_inexistente(self):
        self.assertEqual(self.reg.cantidad_por_tipo("LOGOUT"), 1)


class TestRegistradorUltimoYLimpiar(unittest.TestCase):
    def test_ultimo_evento_vacio(self):
        reg = RegistradorSeguro()
        self.assertIsNone(reg.ultimo_evento())

    def test_ultimo_evento_es_el_mas_reciente(self):
        reg = RegistradorSeguro()
        reg.registrar(Evento("LOGIN", "primero"))
        reg.registrar(Evento("ERROR", "segundo"))
        ultimo = reg.ultimo_evento()
        self.assertEqual(ultimo.get_mensaje(), "segundo")
        self.assertEqual(ultimo.get_tipo(), "ERROR")

    def test_limpiar_vacia_el_registro(self):
        reg = RegistradorSeguro()
        reg.registrar(Evento("LOGIN", "test"))
        reg.registrar(Evento("ERROR", "test2"))
        reg.limpiar()
        self.assertEqual(reg.cantidad_eventos(), 0)

    def test_limpiar_y_ultimo_retorna_none(self):
        reg = RegistradorSeguro()
        reg.registrar(Evento("LOGIN", "test"))
        reg.limpiar()
        self.assertIsNone(reg.ultimo_evento())

    def test_cantidad_inicial_es_cero(self):
        reg = RegistradorSeguro()
        self.assertEqual(reg.cantidad_eventos(), 0)


if __name__ == "__main__":
    import __main__

    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    with io.StringIO() as buf:
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
        print(buf.getvalue())
