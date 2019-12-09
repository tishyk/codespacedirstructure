import unittest
from check_power_of_three import check_power_of_three


class TestCheckPowerOfThree(unittest.TestCase):
    def test_check_power_of_three_1(self):
        self.assertEqual(check_power_of_three(1), True)
        self.assertEqual(check_power_of_three(2), False)
        self.assertEqual(check_power_of_three(3), True)

    def test_check_power_of_three_2(self):
        with self.assertRaises(ValueError):
            check_power_of_three(3.8)


if __name__ == "__main__":
    unittest.main()