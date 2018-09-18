# skip test or selective test, custom markers
# execution command - pytest test_math_selective.py -v
# execution command - py.test test_math_selective.py -v
# execution command - py.test -v -rxs


""" -k "method name "- only run tests which match the given substring expression. An expression is a python evaluatable
                        expression where all names are substring-matched
                        against test names and their parent classes. Example:
                        -k 'test_method or test_other' matches all test
                        functions and classes whose name contains
                        'test_method' or 'test_other', while -k 'not
                        test_method' matches those that don't contain
                        'test_method' in their names. Additionally keywords
                        are matched to classes and functions containing extra
                        names in their 'extra_keyword_matches' set, as well as
                        functions which have names assigned directly to them."""

from pytest import mark
import unittest
import base_code
import sys


class TestMathSample1(unittest.TestCase):
    def test_add(self):
        result = base_code.add(5, 2)
        self.assertEqual(result, 7, "Failed test message")

    @mark.skip(reason='Not implemented method or predicted method')
    def test_add(self):
        self.assertEqual(base_code.add(5, 2), 7)
        self.assertEqual(base_code.add(-5, 2), -3)
        self.assertEqual(base_code.add(-5, -2), -7)

    @mark.skipif(sys.platform == 'win32', reason='OS dependancy')
    def test_subtract(self):
        self.assertEqual(base_code.subtract(5, 1), 4)
        self.assertEqual(base_code.subtract(-1, 2), -3)
        self.assertEqual(base_code.subtract(-1, -10), 9)

    @mark.win
    # py.test -v -rxs -k win
    def test_multiply(self):
        self.assertEqual(base_code.multiply(5, 2), 10)
        self.assertEqual(base_code.multiply(-2, 2), -4)
        self.assertEqual(base_code.multiply(-5, -5), 25)
    @mark.win
    def test_divide(self):
        self.assertEqual(base_code.divide(8, 2), 4)
        self.assertEqual(base_code.divide(-8, 2), -4)
        self.assertEqual(base_code.divide(-8, -1), 8)
        self.assertEqual(base_code.divide(-8, -1), 8.0)  # Check it with // dividing
        self.assertRaises(AssertionError, base_code.divide, 8, 0)  # 1 way to test raised error
        with self.assertRaises(AssertionError):  # 2 way to test raised error
            base_code.divide(8, 0)


if __name__ == "__main__":
    unittest.main()
