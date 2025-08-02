"""
Test calculator module

"""


from django.test import SimpleTestCase
from app.calculator import (
    add,subtract,multiply,divide,
    power,modulus,square_root,absolute_value,  
    factorial,logarithm 
)


class CalculatorTests(SimpleTestCase):
    """Test cases for calculator functions."""

    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(-1, -1), 0)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(-2, -3), 6)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        with self.assertRaises(ValueError):
            divide(5, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(5, 0), 1)

    def test_modulus(self):
        self.assertEqual(modulus(5, 3), 2)
        with self.assertRaises(ValueError):
            modulus(5, 0)

    def test_square_root(self):
        self.assertEqual(square_root(4), 2)
        with self.assertRaises(ValueError):
            square_root(-4)

    def test_absolute_value(self):
        self.assertEqual(absolute_value(-5), 5)
        self.assertEqual(absolute_value(5), 5)

    def test_factorial(self):
        self.assertEqual(factorial(5), 120)
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_logarithm(self):
        self.assertAlmostEqual(logarithm(100, base=10), 2)
        with self.assertRaises(ValueError):
            logarithm(-10)