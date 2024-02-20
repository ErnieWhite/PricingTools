import unittest


from utility import (
    valid_formula,
)


class UtilityTest(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(valid_formula(''))

    def test_basis_formula(self):
        self.assertTrue(valid_formula('*0.5'))

    def test_formula_leading_decimal(self):
        self.assertTrue(valid_formula('*.5'))

    def test_formula_trailing_decimal(self):
        self.assertTrue(valid_formula('*1.'))

    def test_formula_no_decimal(self):
        self.assertTrue(valid_formula('*1'))

    def test_formula_just_asterisk(self):
        self.assertFalse(valid_formula('*'))

    def test_formula_two_decimals(self):
        self.assertFalse(valid_formula('*..'))
        self.assertFalse(valid_formula('*0.1.5'))

    def test_test_double_signs(self):
        self.assertFalse(valid_formula('x--0.5'))

    def test_none_formula(self):
        formula = None
        self.assertFalse(valid_formula(formula))
