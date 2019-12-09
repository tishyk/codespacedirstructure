import unittest
from check_arithmetic_progression import check_arithmetic_progression


class TestCheckArithmeticProgression(unittest.TestCase):
    def test_check_arithmetic_progression(self):
        self.assertFalse(check_arithmetic_progression(list()))
        self.assertFalse(check_arithmetic_progression([1]))
        self.assertTrue(check_arithmetic_progression([2, 3]))

    def test_check_arithmetic_progression_2(self):
        self.assertFalse(check_arithmetic_progression([2, 3, 1]))
        self.assertTrue(check_arithmetic_progression([2, 3, 4, 5, 6]))

    def test_check_arithmetic_progression_3(self):
        with self.assertRaises(ValueError):
            check_arithmetic_progression({"x": 10})

        with self.assertRaises(ValueError):
            check_arithmetic_progression([0, "x"])


if __name__ == "__main__":
    unittest.main()