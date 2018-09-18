# https://docs.python.org/3/library/unittest.html
# help is here https://www.youtube.com/watch?v=6tNS--WetLI&t=1177s

import unittest
import base_code


class TestMathSample1(unittest.TestCase):
    # def test_add(self):
    #     result = base_code.add(5,2)
    #     self.assertEqual(result,7,"Failed test message")

    def test_add(self):
        self.assertEqual(base_code.add(5, 2), 7)
        self.assertEqual(base_code.add(-5, 2), -3)
        self.assertEqual(base_code.add(-5, -2), -7)

    def test_subtract(self):
        self.assertEqual(base_code.subtract(5, 1), 4)
        self.assertEqual(base_code.subtract(-1, 2), -3)
        self.assertEqual(base_code.subtract(-1, -10), 9)

    def test_multiply(self):
        self.assertEqual(base_code.multiply(5, 2), 10)
        self.assertEqual(base_code.multiply(-2, 2), -4)
        self.assertEqual(base_code.multiply(-5, -5), 25)

    def test_divide(self):
        self.assertEqual(base_code.divide(8, 2), 4)
        self.assertEqual(base_code.divide(-8, 2), -4)
        self.assertEqual(base_code.divide(-8, -1), 8)
        # self.assertEqual(base_code.divide(-8, -1), 8.0)
        # Check it with // dividing
        self.assertRaises(AssertionError, base_code.divide, 8, 0)   # 1 way to test raised error
        with self.assertRaises(AssertionError):                     # 2 way to test raised error
            base_code.divide(8,0)
#
#
if __name__ == "__main__":
    unittest.main()
