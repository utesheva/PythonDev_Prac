import unittest
import square

class TestSquare(unittest.TestCase):
    def test_0(self):
        self.assertEqual(square.sqroots('1 -2 -24'), "6.0, -4.0")

    def test_1(self):
        self.assertEqual(square.sqroots('1 2 1'), "-1.0")

    def test_exception(self):
        with self.assertRaises(Exception):
            square.sqroots('0 0 0')

