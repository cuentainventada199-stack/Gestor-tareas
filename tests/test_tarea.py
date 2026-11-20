import unittest
from tarea import Tarea

class PruebasTarea(unittest.TestCase):
    def test_crear_y_editar(self):
        tarea = Tarea(1, 'Estudiar')
        self.assertEqual(tarea.get_titulo(), 'Estudiar')
        tarea.set_titulo('Practicar Flask')
        self.assertEqual(tarea.get_titulo(), 'Practicar Flask')

    def test_titulo_vacio(self):
        with self.assertRaises(ValueError):
            Tarea(1, '   ')

    def test_completar(self):
        tarea = Tarea(1, 'Ejercicio')
        tarea.set_completada(True)
        self.assertTrue(tarea.get_completada())

if __name__ == '__main__':
    unittest.main()
